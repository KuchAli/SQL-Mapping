import time
import requests 

class HTTPClient:
    def __init__(self, timeout: int=10):
        self.timeout = timeout

        #menggunakan user agent browser agar terlihat seperti trafik normal
        self.headers={
            "User-Agent": {
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            },
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def check_connection(self, url: str)->bool:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            return response.status_code < 500
        except:
            return False