import argparse
import sys
from utils.logger import (
    log_error,
    log_info,
    log_success,
    log_warning,
    print_banner,
    print_database_table,
    console
)
from core.client import HTTPClient
from core.detector import VulnerabilityDetector
from core.mapper import DatabaseMapper

def main():
    #config cli (menerima input dari terminal)
    parser = argparse.ArgumentParser(
        description=(
            "Mini SQL Mapping & Vulnerabillity Scanner - Edukasi"
        )
    )
    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="URL target yang ingin di uji (contoh: http://localhost:8000/api?id=1)"
    )
    args = parser.parse_args()

    print_banner()

    target_url = args.url
    console.print(f"[cyan][*] Mengonfigurasi target: {target_url}[/cyan]")

    #init http client
    client = HTTPClient()
    if not client.check_connection(target_url):
        console.print(
            "[red][!] Gagal terhubung ke target. Pastikan URL aktif.[/red]"
        )
        sys.exit(1)

    #deteksi celah 
    console.print(
        "[cyan][*] Menjalankan pemindaian kerentanan SQL Injection...[/cyan]"
    )
    detector = VulnerabilityDetector(client)
    is_vulnerable = detector.scan_parameter(target_url)

    if not is_vulnerable:
        console.print(
            "[yellow][-] Pemindaian selesai. Parameter target aman (Tidak"
            " rentan).[/yellow]"
        )
        sys.exit(0)

    console.print(
        "[green][+] KONFIRMASI: Target rentan terhadap SQL Injection![/green]"
    )

    #tahan mapping dan ekstaksi data (memanggil mapper)
    console.print("[cyan][*] Memulai ekstraksi informasi database...[/cyan]")
    mapper = DatabaseMapper(client)
    mapper.dump_database(target_url)


if __name__ == "__main__":
  main()
