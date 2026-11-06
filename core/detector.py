import re
from core.client import HTTPClient
from utils.logger import(
    log_error,
    log_info,
    log_success,
)

class VulnerabilityDetector:
    def __init__(self, client=HTTPClient):
        self.client = client

        self.error_patterns = [
            r"you have an error in your sql syntax;",
            r"warning: mysql_",
            r"unquoted string gpointer",
            r"pg_query\(\): supplied argument is not a valid MySQL result",
            r"syntax error at or near",  # Khas PostgreSQL
            r"unterminated quoted string",
            r"SQLite/JDBCDriver",
        ]

    def scan_parameter(self, base_url: str)-> bool:
        log_info("Menguji payload Error-Based (Karakter Petik Tunggal)...")

        payload_error = "'"
        res = self.client.send_payload(base_url, payload_error)

        if res["success"]:
            #cek apakah respon mengandung pola error database
            for pattern in self.error_patterns:
                if re.search(pattern, res["text"], re.IGNORECASE):
                    log_success(
                        f"Ditemukan Error-Based SQLi dengan pola: '{pattern}'"
                    )
                    return True
        log_info(
            "Mencoba teknik Time-Based Blind SQLi (Delay 3 detik untuk"
            " PostgreSQL)..."
        )

        #uji coba time-based (contoh payload delay PostgreSQL: )
        payload_time= ";SELECT pg_sleep(3)--"
        res_time = self.client.send_payload(base_url, payload_time)

        #waktu respon melambat lebih dari 3 detik
        if res_time["timeout"] or res_time["elapsed"] >= 3.0:
            log_success(
                f"ditemukan Time-based SQLi! Server merespons dalam"
                f"{res_time['elapsed']:.2f} detik"
            )
            return True
        return False