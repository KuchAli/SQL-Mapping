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

    # print_banner()

    target_url = args.url
    console.print(f"[cyan][*] Mengonfigurasi target: {target_url}[/cyan]")

    #init http client