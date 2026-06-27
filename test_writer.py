# test_writer.py
from graph.state import create_initial_state
from agents.planner import run_planner
from agents.writer import run_writer

# Step 1 — run the planner to get subtasks
state = create_initial_state(
    "Add a loading spinner to the submit button on the login form"
)
state = run_planner(state)

if state.get("error"):
    print("Planner error:", state["error"])
    exit()

print(f"\nPlanner produced {len(state['subtasks'])} subtasks")

# Step 2 — run the writer on the first subtask only
state = run_writer(state)

if state.get("error"):
    print("Writer error:", state["error"])
    exit()

print(f"\nWriter results:")
print(f"Files written: {state['written_files']}")
print(f"Current index: {state['current_subtask_index']}")
print(f"Subtask status: {state['subtasks'][0]['status']}")
print("\nCheck your GitHub repo — the file should be committed to the feature branch.")