# test_reviewer.py
from graph.state import create_initial_state
from agents.planner import run_planner
from agents.writer import run_writer
from agents.test_runner import run_tests
from agents.reviewer import fix_failing_tests

# Run planner and writer first
state = create_initial_state(
    "Add input validation to the user registration form"
)
state = run_planner(state)
if state.get("error"):
    print("Planner error:", state["error"])
    exit()

state = run_writer(state)
if state.get("error"):
    print("Writer error:", state["error"])
    exit()

# Run tests
state = run_tests(state)
print(f"\nTests passed: {state['test_passed']}")
print(f"Test output preview: {state['test_output'][:200]}")

# If tests failed run the reviewer
if not state["test_passed"]:
    print("\nRunning reviewer to fix failures...")
    state = fix_failing_tests(state)
    print(f"Retry count: {state['retry_count']}")
    print(f"Files fixed: {state['written_files']}")
else:
    print("\nTests passed on first run. Reviewer not needed.")