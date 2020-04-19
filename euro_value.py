import requests
import json
import time


class BitcoinExchange(object):
    def __init__(self):
        self.total_wait = 0
        self.accumulative_value = 0
        self.limit = 20
        self.link = "https://blockchain.info/ticker"

    def do_get_request(self):
        try:
            request = requests.get(self.link)
        except requests.exceptions.Timeout:
            # Wait then retry
            time.sleep(0.1)
            request = requests.get(self.link)

        return json.loads(request.text).get("EUR", {}).get("last", 0)

    def get_euro_rate(self):
        try:
            # Request Euro rate
            result = self.do_get_request()
        except requests.exceptions.RequestException as e:
            # Bad request, default to 0
            result = 0

        self.accumulative_value += result
        self.total_wait += 2

        time.sleep(2)
        return result

    def get_average_rate(self):
        if self.total_wait >= self.limit:
            avg = self.accumulative_value / (self.limit / 2)
            self.total_wait = 0
            self.accumulative_value = 0
            return avg
        return None


if __name__ == "__main__":
    bitcoin_rate = BitcoinExchange()
    while True:
        current_euro_rate = bitcoin_rate.get_euro_rate()
        print(f"Current exchange rate => `{current_euro_rate}`")
        current_avg = bitcoin_rate.get_average_rate()
        if current_avg:
            print(f"Average exchange rate => `{current_avg}`")
