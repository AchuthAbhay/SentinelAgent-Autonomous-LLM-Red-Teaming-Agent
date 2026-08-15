from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """Application configuration."""

    # ========= API Keys =========

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        "",
    )

    # ========= Models =========

    TARGET_MODEL: str = os.getenv(
        "TARGET_MODEL",
        "groq:llama-3.3-70b-versatile",
    )

    SAFEGUARD_MODEL: str = os.getenv(
        "SAFEGUARD_MODEL",
        "openai/gpt-oss-safeguard-20b",
    )

    STRATEGIST_MODEL: str = "openai/gpt-oss-120b"

    # ========= Target Ground Truth =========

    TARGET_SYSTEM_PROMPT: str = os.getenv(
        "TARGET_SYSTEM_PROMPT",
        "",
    )

    # ========= Limits =========

    MAX_TURNS: int = int(
        os.getenv(
            "MAX_TURNS",
            5,
        )
    )

    MAX_SPEND_USD: float = float(
        os.getenv(
            "MAX_SPEND_USD",
            1.0,
        )
    )

    # ========= Security =========

    ALLOWED_TARGETS: list[str] = [
        model.strip()
        for model in os.getenv(
            "ALLOWED_TARGETS",
            "",
        ).split(",")
        if model.strip()
    ]


settings = Settings()