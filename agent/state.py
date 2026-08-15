from pydantic import BaseModel, Field

from shared.models import (
    AnalysisResult,
    AttackAttempt,
    AttackStrategy,
    Report,
)


class RedTeamState(BaseModel):
    """
    Shared state that flows through every LangGraph node.

    Each node reads from the state, performs its work,
    updates the relevant fields, and passes the state onward.
    """

    # ======================================================
    # Run Information
    # ======================================================

    target_model: str

    max_turns: int

    current_turn: int = 1

    budget_used: float = 0.0

    # ======================================================
    # Strategy
    # ======================================================

    attack_queue: list[AttackStrategy] = Field(
        default_factory=list
    )

    current_strategy: AttackStrategy | None = None

    # ======================================================
    # Current Attack
    # ======================================================

    current_prompt: str = ""

    current_response: str = ""

    # ======================================================
    # Current Analysis
    # ======================================================

    current_analysis: AnalysisResult | None = None

    # ======================================================
    # History
    # ======================================================

    attempts: list[AttackAttempt] = Field(
        default_factory=list
    )

    # ======================================================
    # Execution Control
    # ======================================================

    successful_attacks: int = 0

    should_continue: bool = True

    # ======================================================
    # Final Output
    # ======================================================

    final_summary: Report | None = None