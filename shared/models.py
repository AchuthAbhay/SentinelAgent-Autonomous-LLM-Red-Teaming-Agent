from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ==========================================================
# ENUMS
# ==========================================================

class AttackCategory(str, Enum):
    PROMPT_INJECTION = "prompt_injection"
    SENSITIVE_INFORMATION_DISCLOSURE = "sensitive_information_disclosure"


class JudgeVerdict(str, Enum):
    SAFE = "safe"
    UNSAFE = "unsafe"
    BORDERLINE = "borderline"


class VerificationOutcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    INCONCLUSIVE = "inconclusive"


# ==========================================================
# STRATEGY
# ==========================================================

class AttackStrategy(BaseModel):
    """
    Strategy selected by the Strategist node.
    """

    category: AttackCategory

    tactic: str

    objective: str

    template_name: str

    variables: dict[str, str] = Field(
        default_factory=dict
    )


# ==========================================================
# MCP REQUEST / RESPONSE
# ==========================================================

class AttackRequest(BaseModel):
    model: str
    prompt: str


class AttackResponse(BaseModel):
    response: str


class JudgeRequest(BaseModel):
    prompt: str
    response: str


# ==========================================================
# SAFETY JUDGE
# ==========================================================

class JudgeResult(BaseModel):
    """
    Result produced by a safety judge.
    """

    verdict: JudgeVerdict

    score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score",
    )

    reason: str


# ==========================================================
# OBJECTIVE VERIFICATION
# ==========================================================

class VerificationOutcome(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    INCONCLUSIVE = "inconclusive"


class ObjectiveVerification(BaseModel):

    outcome: VerificationOutcome

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    evidence: list[str] = Field(
        default_factory=list
    )

    ground_truth_match: float = Field(
        ge=0.0,
        le=1.0,
    )

    failure_mode: str | None = None

    disclosed_content: str = ""

    missing_elements: list[str] = Field(
        default_factory=list
    )

    fabrication_detected: bool = False

# ==========================================================
# ATTACK ATTEMPT
# ==========================================================

class AttackAttempt(BaseModel):
    """
    Complete record of one red-team attack attempt.
    """

    turn: int

    strategy: AttackStrategy

    prompt: str

    response: str

    # Safety evaluation
    safeguard: JudgeResult

    heuristic_guard: JudgeResult

    # Objective evaluation
    objective_verification: ObjectiveVerification


# ==========================================================
# ANALYSIS
# ==========================================================

class AnalysisResult(BaseModel):
    """
    Evidence-grounded analysis produced after an attack.
    """

    outcome: VerificationOutcome

    objective_evidence: list[str] = Field(
        default_factory=list
    )

    disagreement_notes: list[str] = Field(
        default_factory=list
    )

    target_behavior_hypothesis: str

    next_hypothesis: str


# ==========================================================
# FINAL REPORT
# ==========================================================

class Report(BaseModel):

    target_model: str

    total_attempts: int

    successful_attacks: int

    attack_success_rate: float

    attempts: list[AttackAttempt] = Field(
        default_factory=list
    )

    summary: Optional[str] = None