# graph/state.py
from typing import TypedDict, List, Optional
import time

class Subtask(TypedDict):
    id: str
    description: str
    file_path: str
    status: str  # pending, in_progress, done, failed

class AgentState(TypedDict):
    # Input -> planner agent input
    original_task: str

    # Planner output
    subtasks: List[Subtask] # writer agent input
    current_subtask_index: int # writer agent 
    feature_branch: str # created by planner agent and used by reviewer agent

    # Writer output
    written_files: List[str] # reviewer agent input

    # Test runner output
    test_output: Optional[str]
    test_passed: bool
    retry_count: int

    # PR opener output
    pr_url: Optional[str] # final output

    # Error handling
    error: Optional[str]

def create_initial_state(task: str) -> AgentState:
    timestamp = int(time.time())
    branch_name = f"feat/agent-task-{timestamp}"

    return AgentState(
        original_task=task,
        subtasks=[],
        current_subtask_index=0,
        feature_branch=branch_name,
        written_files=[],
        test_output=None,
        test_passed=False,
        retry_count=0,
        pr_url=None,
        error=None,
    )