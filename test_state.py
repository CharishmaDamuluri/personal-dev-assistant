# test_state.py
from graph.state import create_initial_state

state = create_initial_state("Add input validation to the registration form")

print("Task:", state["original_task"])
print("Branch:", state["feature_branch"])
print("Subtasks:", state["subtasks"])
print("Index:", state["current_subtask_index"])
print("Tests passed:", state["test_passed"])
print("Retry count:", state["retry_count"])