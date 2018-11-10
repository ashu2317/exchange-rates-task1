import threading


class ExchangeDictionary:
    exchange_rate_map = {}
    interval = 5

    @staticmethod
    def clear_exchange_rate_map_in_every_hour():
        threading.Timer(ExchangeDictionary.interval, ExchangeDictionary.clear_exchange_rate_map_in_every_hour).start()
        ExchangeDictionary.exchange_rate_map.clear()

