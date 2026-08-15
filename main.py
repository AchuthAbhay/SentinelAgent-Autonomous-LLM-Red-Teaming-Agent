import asyncio
from pprint import pprint

from agent.graph import build_graph
from agent.state import RedTeamState
from attack_library.loader import load_attack_library
from shared.config import settings


async def main():

    # ---------------------------------------------
    # Load Attack Library
    # ---------------------------------------------

    attack_queue = load_attack_library()

    # ---------------------------------------------
    # Create Initial State
    # ---------------------------------------------

    initial_state = RedTeamState(
        target_model=settings.TARGET_MODEL,
        max_turns=settings.MAX_TURNS,
        attack_queue=attack_queue,
    )

    # ---------------------------------------------
    # Build Graph
    # ---------------------------------------------

    graph = build_graph()

    print("\nStarting Sentinel Agent...\n")

    # ---------------------------------------------
    # Execute Graph
    # ---------------------------------------------

    final_state = await graph.ainvoke(
        initial_state,
        config={
            "configurable": {
                "thread_id": "run-001"
            }
        },
    )

    # ---------------------------------------------
    # Print Final Report
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)

    pprint(final_state["final_summary"].model_dump())


if __name__ == "__main__":
    asyncio.run(main())