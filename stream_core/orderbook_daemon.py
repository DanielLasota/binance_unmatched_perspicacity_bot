import threading
from binance import ThreadedWebsocketManager
import os

from .stream_orderbook import StreamOrderbook


class OrderbookDaemon:
    def __init__(self):
        self.observers = []
        self.lock = threading.Lock()
        self.orderbook_message = None
        self.formatted_target_orderbook = None

    def subscribe(self, observer):
        self.observers.append(observer)
        
    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, information):
        for observer in self.observers:
            observer.update('orderbookBestBidsQueue', information.best_bids_repr)
            observer.update('orderbookBestAsksQueue', information.best_asks_repr)

    def orderbook_listener(self, instrument):

        def handle_orderbook(message):
            with self.lock:
                self.orderbook_message = message
                self.formatted_target_orderbook = StreamOrderbook(message)
                print(self.formatted_target_orderbook)
                self.notify_observers(self.formatted_target_orderbook)

        api_key, api_secret = os.environ.get('DEV_MODE_API_KEY'), os.environ.get('DEV_MODE_API_SECRET')
            
        twm = ThreadedWebsocketManager(api_key, api_secret)
        twm.start()

        twm.start_depth_socket(callback=handle_orderbook, symbol=instrument, depth='20', interval=100)
        
        twm.join()
        
    def run(self, instrument):
        thread = threading.Thread(target=self.orderbook_listener, args=(instrument,))
        thread.daemon = True
        thread.start()
        