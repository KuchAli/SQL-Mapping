import warnings
import time
import requests 
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)

class HTTPClient:
    def __init__(self, timeout: int=10):
        self.timeout = timeout

        #menggunakan user agent browser agar terlihat seperti trafik normal
        self.headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def check_connection(self, url: str)->bool:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        try:
            response = requests.get(
                url, headers=self.headers, timeout=self.timeout, verify=False
            )
            return response.status_code < 500
        except requests.exceptions.RequestException as e:
            print(f"\n[DEBUG ERROR] {e}\n")
            return False

    def send_payload(self, base_url:str, payload:str)->dict:
        target_url = f"{base_url}{payload}"

        start_time= time.time()
        try :
            response = requests.get(
                target_url, headers=self.headers, timeout=self.timeout, verify=False
            )
            elapsed_time= time.time() - start_time
            return{
                "success": True,
                "status_code": response.status_code,
                "text": response.text,
                "elapsed": elapsed_time,
                "timeout": False
            }
        except requests.exceptions.Timeout:
            #jika terjadi timeout
            elapsed_time = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "text": "",
                "elapsed": elapsed_time,
                "timeout": True
            }
        except requests.exceptions.RequestException:
            #menangani eror jaringan lainnya
            return {
                "success": False,
                "status_code": 0,
                "text":"",
                "elapsed": 0.0,
                "timeout": False
            }