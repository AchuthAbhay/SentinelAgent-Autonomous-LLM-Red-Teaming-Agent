from rich.console import Console

from agent.services.mcp_client import mcp_service
from agent.state import RedTeamState
from shared.logger import log_response

console = Console()


async def executor(state: RedTeamState) -> RedTeamState:
    """
    Execute the generated attack prompt against the target model.
    """

    console.print("[bold yellow]Executing attack...[/]\n")

    tools = await mcp_service.get_tools()

    execute_tool = next(
        tool
        for tool in tools
        if tool.name == "execute_target"
    )

    result = await execute_tool.ainvoke(
        {
            "model": state.target_model,
            "prompt": state.current_prompt,
        }
    )

    # MCP returns a list of content blocks
    state.current_response = result[0]["text"]

    console.print("[bold green]✓ Response received[/]\n")

    log_response(state.current_response)

    return state