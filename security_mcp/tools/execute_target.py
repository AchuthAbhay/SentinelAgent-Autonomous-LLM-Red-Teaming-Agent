import re

from langchain.chat_models import init_chat_model

from security_mcp.mcp_instance import mcp
from shared.config import settings


def _visible_response(content: str) -> str:
    """Remove provider reasoning blocks before exposing target output."""
    content = re.sub(
        r"<think>.*?</think>",
        "",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return content.strip()


@mcp.tool()
def execute_target(
    model: str,
    prompt: str,
) -> str:
    """
    Execute an attack prompt against the target model.
    """

    if model not in settings.ALLOWED_TARGETS:
        raise ValueError(f"{model} is not allowed.")

    if not settings.TARGET_SYSTEM_PROMPT.strip():
        raise ValueError("TARGET_SYSTEM_PROMPT must not be empty.")

    llm = init_chat_model(
        model=model,
        api_key=settings.GROQ_API_KEY,
        reasoning_format="hidden",
    )

    response = llm.invoke(
        [
            ("system", settings.TARGET_SYSTEM_PROMPT),
            ("human", prompt),
        ]
    )

    return _visible_response(response.content)