import logging
import os
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def setup_logging():
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

def log_token_usage(component, usage):
    console.print(f"[bold yellow]Token usage for {component}:[/bold yellow]")
    console.print(f"  Prompt tokens: {usage.prompt_tokens}")
    console.print(f"  Completion tokens: {usage.completion_tokens}")
    console.print(f"  Total tokens: {usage.total_tokens}")

def print_colored(text, color):
    console.print(f"[{color}]{text}[/{color}]")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')