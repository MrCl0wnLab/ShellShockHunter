import shodan

SHODAN_API_KEY = "wOz4TpERqzEbYvj7JjWxskh3F5DBUnIf"


class ShodanShock:
    def __init__(self, shoddan_api_key_str: str):
        self._api = shodan.Shodan(shoddan_api_key_str)

    def search_str(self, word: str):
        try:
            # Search Shodan
            results = self._api.search(word)
            if results:
                return results
            return None
        except shodan.APIError as err:
            print('Error: {}'.format(err))

    def search_ip_str(self, word: str) -> list:
        try:
            if word:
                ip_list = []
                results = self.search_str(word)
                if results:
                    for result in results['matches']:
                        ip_list.append(format(result['ip_str']))
                    return ip_list
                return None
            return None
        except shodan.APIError as err:
            print('Error: {}'.format(err))
