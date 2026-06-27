# agents/writer.py
import os
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from mcp.github import read_file, write_file
from graph.state import AgentState

load_dotenv()
client = OpenAI()

# Pydantic model for the writer output
class WriterOutput(BaseModel):
    updated_code: str
    explanation: Annotated[str, StringConstraints(max_length=72)]

def run_writer(state: AgentState) -> AgentState:
    subtasks = state["subtasks"]
    index = state["current_subtask_index"]
    feature_branch = state["feature_branch"]

    # Guard — no more subtasks to process
    if index >= len(subtasks):
        return state

    subtask = subtasks[index]

    print(f"\nWriter: working on subtask {subtask['id']} of {len(subtasks)}")
    print(f"File: {subtask['file_path']}")
    print(f"Task: {subtask['description']}")

    # Step 1 — read the existing file
    try:
        existing_code = read_file(subtask["file_path"])
        file_context = f"Existing file content:\n{existing_code}"
    except Exception:
        existing_code = ""
        file_context = "This is a new file. It does not exist yet."

    # Step 2 — call the model with structured output
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        max_tokens=3000,
        messages=[
            {
                "role": "system",
                "content": """You are a senior software engineer writing production code.

Rules:
- Follow the existing code patterns and conventions exactly
- Do not change anything outside the scope of the task
- Write complete file content not just the changed section
- Do not include markdown formatting in the code
- Do not add unnecessary comments
- Match the existing import style, naming conventions, and file structure
- Write the explanation as a git commit message body
- Use imperative mood: 'Add spinner' not 'Added spinner'
- Keep it under 72 characters
- Be specific: 'Add loading spinner to LoginForm submit button' not 'Update login form'"""
            },
            {
                "role": "user",
                "content": f"""Task: {subtask["description"]}
File: {subtask["file_path"]}

{file_context}

Write the complete updated file content.
"""
            }
        ],
        response_format=WriterOutput,
    )

    result = response.choices[0].message.parsed

    if result is None:
        updated_subtasks = subtasks.copy()
        updated_subtasks[index]["status"] = "failed"
        return {
            **state,
            "subtasks": updated_subtasks,
            "error": f"Writer returned no output for subtask {subtask['id']}"
        }

    print(f"Writer: {result.explanation}")

    # Step 3 — write and commit the file
    commit_message = result.explanation[:72].strip()
    try:
        write_file(
            path=subtask["file_path"],
            content=result.updated_code,
            message=f"feat: {commit_message}",
            branch=feature_branch,
        )
        print(f"Writer: committed {subtask['file_path']}")
    except Exception as e:
        updated_subtasks = subtasks.copy()
        updated_subtasks[index]["status"] = "failed"
        return {
            **state,
            "subtasks": updated_subtasks,
            "error": f"Writer failed to commit {subtask['file_path']}: {e}"
        }

    # Step 4 — mark subtask done and advance the index
    updated_subtasks = [s.copy() for s in subtasks]
    updated_subtasks[index]["status"] = "done"

    return {
        **state,
        "subtasks": updated_subtasks,
        "current_subtask_index": index + 1,
        "written_files": state["written_files"] + [subtask["file_path"]],
    }