from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def divider(title: str):
    console.rule(f"[bold cyan]{title}")


def log_strategy(category: str, tactic: str, objective: str):
    table = Table(title="Selected Strategy")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Category", category)
    table.add_row("Tactic", tactic)
    table.add_row("Objective", objective)

    console.print(table)


def log_prompt(prompt: str):
    console.print(
        Panel(
            prompt,
            title="Generated Prompt",
            border_style="yellow",
        )
    )


def log_response(response: str):
    console.print(
        Panel(
            response,
            title="Target Response",
            border_style="green",
        )
    )


def log_judgement(
    llama_verdict: str,
    heuristic_verdict: str,
):
    table = Table(title="Evaluation")

    table.add_column("Judge")
    table.add_column("Verdict")

    table.add_row("LLM Judge", llama_verdict)
    table.add_row("Heuristic", heuristic_verdict)

    console.print(table)


def log_decision(continue_running: bool):
    if continue_running:
        console.print("[bold yellow]Decision:[/] Continue\n")
    else:
        console.print("[bold green]Decision:[/] Finish\n")