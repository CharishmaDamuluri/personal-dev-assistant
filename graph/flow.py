# graph/flow.py
from langgraph.graph import StateGraph, END
from agents.planner import run_planner
from agents.writer import run_writer
from agents.test_runner import run_tests
from agents.reviewer import fix_failing_tests
from agents.pr_opener import open_pr
from graph.state import AgentState

# Decision functions — these tell LangGraph which node to go to next

def should_write_more(state: AgentState) -> str:
    # If there are more subtasks send back to writer
    # If all subtasks are done move to test runner
    index = state["current_subtask_index"]
    total = len(state["subtasks"])

    if state.get("error"):
        return "end"

    if index < total:
        return "write"

    return "test"

def should_retry_or_pass(state: AgentState) -> str:
    # If tests passed open the PR
    # If tests failed and retry limit not hit send to reviewer
    # If retry limit hit end with error
    if state["test_passed"]:
        return "open_pr"

    if state["retry_count"] >= 3:
        print("\nMax retries reached. Tests still failing.")
        return "end"

    return "fix"

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Add all nodes
    graph.add_node("planner", run_planner)
    graph.add_node("writer", run_writer)
    graph.add_node("test_runner", run_tests)
    graph.add_node("reviewer", fix_failing_tests)
    graph.add_node("pr_opener", open_pr)

    # Entry point
    graph.set_entry_point("planner")

    # Planner always goes to writer
    graph.add_edge("planner", "writer")

    # Writer loops back to itself or moves to test runner
    graph.add_conditional_edges(
        "writer",
        should_write_more,
        {
            "write": "writer",
            "test": "test_runner",
            "end": END,
        }
    )

    # Test runner either opens PR, sends to reviewer, or ends
    graph.add_conditional_edges(
        "test_runner",
        should_retry_or_pass,
        {
            "open_pr": "pr_opener",
            "fix": "reviewer",
            "end": END,
        }
    )

    # Reviewer always goes back to test runner
    graph.add_edge("reviewer", "test_runner")

    # PR opener ends the flow
    graph.add_edge("pr_opener", END)

    return graph.compile()

# Compiled graph — imported by the FastAPI server
agent_graph = build_graph()