
import time
import requests
from urllib.parse import urlparse
from requests.exceptions import ConnectionError

class RequestShock:
    def __init__(self):
        self.protocol = 'https'
        self.timeout = 4
        self.header = {}

    def send_request(self, _target: str, _value_header: str):
        try:
            if _target:

                target_url = self.protocol + '://'+_target
                url_parser = urlparse(target_url)

                header = {
                    "Content-type": "application/x-www-form-urlencoded",
                    "Referer": _value_header,
                    "Cookie": _value_header,
                    "User-Agent": _value_header,
                    "host": url_parser.netloc
                }
                start = time.time()
                result = requests.get(
                    url=target_url, headers=header, verify=False, timeout=self.timeout
                )
                time_final = (f'in {time.time() - start:.2f}s')
                result.raise_for_status()
                
                if result:
                    return target_url, result.text.replace("\n", ""), result.status_code, time_final
                return target_url, 'ERROR!', result.status_code, time_final
        except:
            return target_url, str(), str(), str()
