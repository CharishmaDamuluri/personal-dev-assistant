# test_planner.py
# Run this file to test the planner agent in isolation
# before connecting it to the rest of the pipeline
#
# Usage: python test_planner.py

import sys
import json
from graph.state import create_initial_state
from agents.planner import run_planner

def print_divider():
    print("\n" + "=" * 60 + "\n")

def test_planner(task: str):
    print_divider()
    print(f"TEST: {task}")
    print_divider()

    # Create initial state
    state = create_initial_state(task)
    print(f"Initial state created")
    print(f"Branch: {state['feature_branch']}")

    # Run the planner
    result = run_planner(state)

    # Check for errors
    if result.get("error"):
        print(f"\nERROR: {result['error']}")
        return False

    # Check subtasks exist
    subtasks = result.get("subtasks", [])
    if not subtasks:
        print("\nFAIL: Planner returned no subtasks")
        return False

    # Print results
    print(f"\nSUCCESS: {len(subtasks)} subtasks generated\n")

    for i, subtask in enumerate(subtasks):
        print(f"Subtask {subtask['id']}:")
        print(f"  File:        {subtask['file_path']}")
        print(f"  Description: {subtask['description']}")
        print(f"  Status:      {subtask['status']}")
        print()

    # Validate each subtask has required fields
    required_fields = ["id", "description", "file_path", "status"]
    for subtask in subtasks:
        for field in required_fields:
            if field not in subtask:
                print(f"FAIL: Subtask missing field '{field}'")
                return False

    print("Validation: all subtasks have required fields")
    print(f"Current index: {result['current_subtask_index']}")
    print(f"Feature branch: {result['feature_branch']}")

    return True

def run_all_tests():
    results = []

    # Test 1 — simple single file change
    results.append(test_planner(
        "Add a loading spinner to the submit button on the login form"
    ))

    # Test 2 — multi file change with validation
    results.append(test_planner(
        "Add input validation to the user registration form. "
        "Email must be valid format. Password minimum 8 characters."
    ))

    # Test 3 — new feature
    results.append(test_planner(
        "Add a logout button to the navigation bar that clears the session and redirects to the login page"
    ))

    # Summary
    print_divider()
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed. Planner agent is working correctly.")
    else:
        print("Some tests failed. Check the output above.")

    print_divider()

if __name__ == "__main__":
    # Run a single task if passed as argument
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        test_planner(task)
    else:
        # Run all tests
        run_all_tests()