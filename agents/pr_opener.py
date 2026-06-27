# agents/pr_opener.py
import os
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from mcp.github import open_pull_request
from graph.state import AgentState

load_dotenv()
client = OpenAI()

class PRDescription(BaseModel):
    title: str
    body: str

def open_pr(state: AgentState) -> AgentState:
    print(f"\nPR Opener: generating pull request description")

    # Generate a clean PR title and body using the model
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        max_tokens=500,
        messages=[
            {
                "role": "system",
                "content": """You are a senior engineer writing a pull request description.

Rules:
- Title must be concise, under 72 characters, imperative mood
- Body must summarise what changed and why in 2 to 3 sentences
- Never use markdown headers in the body
- Never use bullet points"""
            },
            {
                "role": "user",
                "content": f"""Original task: {state['original_task']}

Files changed: {state['written_files']}

Write a pull request title and description."""
            }
        ],
        response_format=PRDescription,
    )

    result = response.choices[0].message.parsed

    if result is None:
        title = f"feat: {state['original_task'][:60]}"
        body = f"Automated PR for task: {state['original_task']}"
    else:
        title = result.title
        body = result.body

    # Open the PR
    try:
        pr_url = open_pull_request(
            title=title,
            body=body,
            head_branch=state["feature_branch"],
        )
        print(f"PR Opener: pull request opened")
        print(f"PR Opener: {pr_url}")

        return {
            **state,
            "pr_url": pr_url,
        }

    except Exception as e:
        return {
            **state,
            "error": f"Failed to open PR: {e}"
        }