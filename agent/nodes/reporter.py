import json
from datetime import datetime
from pathlib import Path

from rich.console import Console

from agent.state import RedTeamState
from shared.models import Report

console = Console()

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


async def reporter(state: RedTeamState) -> RedTeamState:
    """
    Generate the final report and save it as JSON.
    """

    total_attempts = len(state.attempts)

    attack_success_rate = (
        (state.successful_attacks / total_attempts) * 100
        if total_attempts > 0
        else 0.0
    )

    report = Report(
        target_model=state.target_model,
        total_attempts=total_attempts,
        successful_attacks=state.successful_attacks,
        attack_success_rate=attack_success_rate,
        attempts=state.attempts,
        summary=(
            f"Completed {total_attempts} attack(s). "
            f"{state.successful_attacks} successful "
            f"({attack_success_rate:.2f}% success rate)."
        ),
    )

    state.final_summary = report

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = REPORT_DIR / f"run_{timestamp}.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(
            report.model_dump(mode="json"),
            f,
            indent=4,
            ensure_ascii=False,
        )

    console.print(
        f"\n[bold green]✓ Report saved:[/] {report_path}"
    )

    return state