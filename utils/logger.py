from rich.console import Console
from rich.table import Table

#init console global
console = Console()

def print_banner():
    banner = """
    [bold cyan]╔══════════════════════════════════════════╗[/bold cyan]
    [bold cyan]║          MINI SQL MAPPER & SCANNER       ║[/bold cyan]
    [bold cyan]║      Educational Security Testing Tool   ║[/bold cyan]
    [bold cyan]╚══════════════════════════════════════════╝[/bold cyan]
        """
    console.print(banner)

def log_info(message: str):
    console.print(f"[cyan][*][/cyan] {message}")

def log_success(message: str):
    console.print(f"[green][*][/green] {message}")

def log_warning(message: str):
    console.print(f"[yellow][*][/yellow] {message}")

def log_error(message: str):
    console.print(f"[red][*][/red] {message}")

def print_database_table(title: str, columns: str, rows: str):
    #cetak hasil mapping database 
    table =Table(title=title, style="bold magenta")

    for col in columns:
        table.add_column(col, style="cyan", no_wrap=True)

    for row in rows:
        table.add_row(*[str(item) for item in row])

    console.print(table)