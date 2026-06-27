# agents/planner.py
import os
import json
import re
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from mcp.github import read_file, list_directory, create_feature_branch
from graph.state import AgentState

load_dotenv()
client = OpenAI()

# Pydantic models — define the exact shape of the planner output
class Subtask(BaseModel):
    id: str
    description: str
    file_path: str
    status: str = "pending"

class PlannerOutput(BaseModel):
    subtasks: List[Subtask]

def run_planner(state: AgentState) -> AgentState:
    task = state["original_task"]
    feature_branch = state["feature_branch"]

    print(f"\nPlanner: analysing task...")
    print(f"Task: {task}")

    # Step 1 — read repo structure
    try:
        repo_structure = list_directory("")
        structure_context = "\n".join(repo_structure)
    except Exception:
        structure_context = "Could not read repo structure"

    # Step 2 — read guidelines.md if it exists
    try:
        guidelines = read_file("guidelines.md")
        guidelines_context = f"Project guidelines:\n{guidelines}"
    except Exception:
        guidelines_context = "No guidelines.md found. Infer conventions from the repo structure."

    # Step 3 — create the feature branch
    try:
        create_feature_branch(feature_branch)
        print(f"Planner: created branch {feature_branch}")
    except Exception as e:
        print(f"Planner: branch may already exist — {e}")

    # Step 4 — call the model with structured output enforcement
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        max_tokens=1500,
        messages=[
            {
                "role": "system",
                "content": """You are a senior software engineer planning a code change.

Your job is to break a plain English task into concrete subtasks.
Each subtask must have a specific file path and a clear description of exactly what to change.

Rules:
- Only include files that need to change
- Be specific about what each file change involves
- Include a test file subtask if the change has testable behaviour
- Follow the project conventions shown in the repo structure and guidelines
- Keep each subtask description concise and action-oriented
- Format: verb + what + where
- Example: 'Add loading spinner to submit button in LoginForm.js'
- Not: 'Locate the login form component file within the server module...'"""
            },
            {
                "role": "user",
                "content": f"""Task: {task}

Repo structure:
{structure_context}

{guidelines_context}

Break this into subtasks."""
            }
        ],
        response_format=PlannerOutput,  # enforced at the API level
    )

    # Step 5 — get the parsed result — already typed, no JSON parsing needed
    result = response.choices[0].message.parsed

    if result is None:
        return {
            **state,
            "error": "Planner returned no output. Check your OpenAI API key and model access."
        }

    # Convert Pydantic models to dicts for LangGraph state
    subtasks = [subtask.model_dump() for subtask in result.subtasks]

    print(f"Planner: created {len(subtasks)} subtasks")
    for s in subtasks:
        print(f"  {s['id']}. {s['file_path']} — {s['description']}")

    return {
        **state,
        "subtasks": subtasks,
        "current_subtask_index": 0,
    }