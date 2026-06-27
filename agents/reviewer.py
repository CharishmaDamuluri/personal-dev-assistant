# agents/reviewer.py
import os
from openai import OpenAI
from typing import Annotated, List
from pydantic import BaseModel, field_validator, StringConstraints
from dotenv import load_dotenv
from mcp.github import read_file, write_file
from graph.state import AgentState

load_dotenv()
client = OpenAI()

# Pydantic models
class FileFix(BaseModel):
    file_path: str
    updated_code: str
    explanation: Annotated[str, StringConstraints(max_length=72)]

    @field_validator("file_path")
    @classmethod
    def must_be_a_file(cls, v):
        if "." not in v.split("/")[-1]:
            raise ValueError(f"file_path must point to a file not a directory: {v}")
        return v

class ReviewerOutput(BaseModel):
    fixes: List[FileFix]
    root_cause: str  # one sentence explaining why the tests failed

def fix_failing_tests(state: AgentState) -> AgentState:
    test_output = state["test_output"]
    written_files = state["written_files"]
    feature_branch = state["feature_branch"]
    retry_count = state["retry_count"]

    print(f"\nReviewer: analysing test failures (attempt {retry_count + 1} of 3)")
    print(f"Reviewer: reading {len(written_files)} changed files")

    # Step 1 — read all the files the writer touched
    file_contents = {}
    for path in written_files:
        try:
            file_contents[path] = read_file(path)
        except Exception as e:
            file_contents[path] = f"Could not read file: {e}"

    # Format file contents for the prompt
    files_context = "\n\n".join([
        f"File: {path}\n{content}"
        for path, content in file_contents.items()
    ])

    # Step 2 — call the model with structured output
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": """You are a senior software engineer fixing failing tests.

You will be given:
- The test failure output
- The files that were changed

Your job is to identify exactly what is wrong and fix it.

Rules:
- Only fix what is causing the test failures
- Do not change anything unrelated to the failures
- Return the complete file content for every file you fix
- Never return partial file content
- Never use markdown formatting in code
- Keep explanations to one sentence in imperative mood"""
            },
            {
                "role": "user",
                "content": f"""Test failures:
{test_output}

Changed files:
{files_context}

Identify the root cause and fix the failing tests."""
            }
        ],
        response_format=ReviewerOutput,
    )

    result = response.choices[0].message.parsed

    if result is None:
        return {
            **state,
            "retry_count": retry_count + 1,
            "error": "Reviewer returned no output"
        }

    print(f"Reviewer: root cause — {result.root_cause}")
    print(f"Reviewer: fixing {len(result.fixes)} files")

    # Step 3 — commit each fix
    fixed_files = []
    for fix in result.fixes:
        try:
            write_file(
                path=fix.file_path,
                content=fix.updated_code,
                message=f"fix: {fix.explanation}",
                branch=feature_branch,
            )
            print(f"Reviewer: committed fix to {fix.file_path}")
            fixed_files.append(fix.file_path)
        except Exception as e:
            print(f"Reviewer: failed to commit {fix.file_path} — {e}")

    return {
        **state,
        "retry_count": retry_count + 1,
        "written_files": list(set(state["written_files"] + fixed_files)),
    }