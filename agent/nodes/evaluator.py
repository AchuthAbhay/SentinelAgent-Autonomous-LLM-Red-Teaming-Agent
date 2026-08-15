import json

from rich.console import Console

from agent.services.mcp_client import mcp_service
from agent.state import RedTeamState
from shared.logger import log_judgement
from shared.config import settings

from shared.models import (
    AttackAttempt,
    JudgeResult,
    ObjectiveVerification,
)


console = Console()


async def evaluator(state: RedTeamState) -> RedTeamState:
    """
    Evaluate the target response using:

    1. Safety judges
    2. Objective verifier

    Safety judgment and attack-objective verification
    are intentionally kept separate.
    """

    console.print(
        "[bold yellow]Evaluating response...[/]\n"
    )

    # ==================================================
    # Get MCP tools
    # ==================================================

    tools = await mcp_service.get_tools()

    safeguard_tool = next(
        tool
        for tool in tools
        if tool.name == "judge_safeguard"
    )

    heuristic_tool = next(
        tool
        for tool in tools
        if tool.name == "judge_heuristic"
    )

    objective_tool = next(
        tool
        for tool in tools
        if tool.name == "judge_objective"
    )

    # ==================================================
    # Safety Judge 1
    # ==================================================

    safeguard_raw = await safeguard_tool.ainvoke(
        {
            "prompt": state.current_prompt,
            "response": state.current_response,
        }
    )

    # ==================================================
    # Safety Judge 2
    # ==================================================

    heuristic_raw = await heuristic_tool.ainvoke(
        {
            "prompt": state.current_prompt,
            "response": state.current_response,
        }
    )

    # ==================================================
    # Parse safety results
    # ==================================================

    safeguard_result = JudgeResult.model_validate(
        json.loads(
            safeguard_raw[0]["text"]
        )
    )

    heuristic_result = JudgeResult.model_validate(
        json.loads(
            heuristic_raw[0]["text"]
        )
    )

    # ==================================================
    # Objective Verification
    # ==================================================

    if state.current_strategy is None:
        raise ValueError(
            "No current strategy available."
        )

    objective_raw = await objective_tool.ainvoke(
    {
        "objective": state.current_strategy.objective,
        "prompt": state.current_prompt,
        "response": state.current_response,
        "ground_truth": settings.TARGET_SYSTEM_PROMPT,
    }
)

    objective_result = ObjectiveVerification.model_validate(
        json.loads(
            objective_raw[0]["text"]
        )
    )

    # ==================================================
    # Log safety judgments
    # ==================================================

    log_judgement(
        llama_verdict=safeguard_result.verdict.value,
        heuristic_verdict=heuristic_result.verdict.value,
    )

    # ==================================================
    # Display objective result
    # ==================================================

    if objective_result.outcome.value == "success":

        console.print(
            "[bold green]✓ Attack Objective Achieved[/]\n"
        )

    elif objective_result.outcome.value == "failure":

        console.print(
            "[bold red]✗ Attack Objective Not Achieved[/]\n"
        )

    else:

        console.print(
            "[bold yellow]"
            "? Attack Objective Inconclusive"
            "[/]\n"
        )

    console.print(
        f"Confidence: "
        f"{objective_result.confidence:.2f}\n"
    )

    if objective_result.evidence:

        console.print(
            "Evidence:"
        )

        for evidence in objective_result.evidence:

            console.print(
                f"  • {evidence}"
            )

        console.print()

    # ==================================================
    # Judge disagreement
    # ==================================================

    if safeguard_result.verdict != heuristic_result.verdict:

        console.print(
            "[bold yellow]"
            "⚠ Judge disagreement detected"
            "[/]\n"
        )

    # ==================================================
    # Create attack record
    # ==================================================

    attempt = AttackAttempt(
        turn=state.current_turn,
        strategy=state.current_strategy,
        prompt=state.current_prompt,
        response=state.current_response,
        safeguard=safeguard_result,
        heuristic_guard=heuristic_result,
        objective_verification=objective_result,
    )

    state.attempts.append(attempt)

    # ==================================================
    # Update successful attack count
    # ==================================================

    if objective_result.outcome.value == "success":
        state.successful_attacks += 1

    return state