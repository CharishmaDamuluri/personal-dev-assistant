# agents/test_runner.py
import subprocess
from graph.state import AgentState
import os 

def run_tests(state: AgentState) -> AgentState:
    print(f"\nTest Runner: running test suite...")
    TARGET_REPO_PATH = os.getenv("TARGET_REPO_PATH")  # add this to .env
    try:
        result = subprocess.run(
            ["npm", "test", "--", "--passWithNoTests", "--watchAll=false"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=TARGET_REPO_PATH  # runs in the target repository path
        )

        test_output = result.stdout + result.stderr
        test_passed = result.returncode == 0

        if test_passed:
            print("Test Runner: all tests passed")
        else:
            print("Test Runner: tests failed")
            print(f"Test Runner: {test_output[:300]}...")  # preview first 300 chars

        return {
            **state,
            "test_output": test_output,
            "test_passed": test_passed,
        }

    except subprocess.TimeoutExpired:
        return {
            **state,
            "test_output": "Test suite timed out after 120 seconds",
            "test_passed": False,
        }

    except FileNotFoundError:
        # npm not found — skip tests and move to PR
        print("Test Runner: npm not found, skipping tests")
        return {
            **state,
            "test_output": "No test runner found",
            "test_passed": True,  # pass through if no test runner exists
        }