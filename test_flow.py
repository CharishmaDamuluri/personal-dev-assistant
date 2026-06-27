# test_flow.py
from graph.flow import agent_graph
from graph.state import create_initial_state

def run(task: str):
    print(f"\nStarting task: {task}")
    print("=" * 60)

    initial_state = create_initial_state(task)

    result = agent_graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("RESULT:")

    if result.get("error"):
        print(f"Error: {result['error']}")
        return

    if result.get("pr_url"):
        print(f"PR opened: {result['pr_url']}")

    print(f"Files written: {result['written_files']}")
    print(f"Subtasks completed: {result['current_subtask_index']} of {len(result['subtasks'])}")
    print(f"Test retries: {result['retry_count']}")

if __name__ == "__main__":
    run("Add a loading spinner to the submit button on the login form")