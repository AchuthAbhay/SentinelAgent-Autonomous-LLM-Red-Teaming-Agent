from langgraph.graph import END, START, StateGraph

from agent.nodes.adapter import adapter
from agent.nodes.analyzer import analyzer
from agent.nodes.evaluator import evaluator
from agent.nodes.executor import executor
from agent.nodes.generator import generator
from agent.nodes.reporter import reporter
from agent.nodes.strategist import strategist
from agent.state import RedTeamState


def should_continue(state: RedTeamState) -> str:
    """
    Decide whether to continue the attack loop
    or finish and generate the report.
    """

    if state.should_continue:
        return "continue"

    return "finish"


def build_graph():

    builder = StateGraph(RedTeamState)

    # -------------------------------------------------
    # Nodes
    # -------------------------------------------------

    builder.add_node("strategist", strategist)
    builder.add_node("generator", generator)
    builder.add_node("executor", executor)
    builder.add_node("evaluator", evaluator)
    builder.add_node("analyzer", analyzer)
    builder.add_node("adapter", adapter)
    builder.add_node("reporter", reporter)

    # -------------------------------------------------
    # Entry
    # -------------------------------------------------

    builder.add_edge(START, "strategist")

    # -------------------------------------------------
    # Main Flow
    # -------------------------------------------------

    builder.add_edge("strategist", "generator")

    builder.add_edge("generator", "executor")

    builder.add_edge("executor", "evaluator")

    # Evaluator → Analyzer
    builder.add_edge("evaluator", "analyzer")

    # Analyzer → Adapter
    builder.add_edge("analyzer", "adapter")

    # -------------------------------------------------
    # Loop
    # -------------------------------------------------

    builder.add_conditional_edges(
        "adapter",
        should_continue,
        {
            "continue": "strategist",
            "finish": "reporter",
        },
    )

    # -------------------------------------------------
    # Exit
    # -------------------------------------------------

    builder.add_edge("reporter", END)

    return builder.compile()