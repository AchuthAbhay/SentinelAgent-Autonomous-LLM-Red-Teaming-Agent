from rich.console import Console

from agent.state import RedTeamState
from shared.config import settings
from shared.logger import log_decision

console = Console()


async def adapter(state: RedTeamState) -> RedTeamState:
    """
    Decide whether the agent should continue attacking
    or finish the run.
    """

    state.current_turn += 1

    console.print("[bold cyan]Adapter[/]")
    console.print(f"Current Turn      : {state.current_turn}")
    console.print(f"Successful Attacks: {state.successful_attacks}")
    console.print(f"Maximum Turns     : {state.max_turns}")
    console.print()

    # --------------------------------------------------
    # Stop if maximum turns reached
    # --------------------------------------------------

    if state.current_turn >= state.max_turns:
        state.should_continue = False

        console.print(
            "[bold red]Maximum number of turns reached.[/]"
        )

        log_decision(False)

        return state

    # --------------------------------------------------
    # Stop if budget exceeded
    # --------------------------------------------------

    if state.budget_used >= settings.MAX_SPEND_USD:
        state.should_continue = False

        console.print(
            "[bold red]Budget limit exceeded.[/]"
        )

        log_decision(False)

        return state

    # --------------------------------------------------
    # Continue
    # --------------------------------------------------

    state.should_continue = True

    log_decision(True)

    return state