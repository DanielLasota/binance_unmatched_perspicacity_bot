import threading
from binance import ThreadedWebsocketManager
import os

from abstract_base_classes.observer import Observer
from .stream_orderbook import StreamOrderbook


class OrderbookDaemon(Observer):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.orderbook_message = None
        self.formatted_target_orderbook = None

    def orderbook_listener(self, instrument):

        def handle_orderbook(message):
            with self.lock:
                self.orderbook_message = message
                self.formatted_target_orderbook = StreamOrderbook(message)

                # print(self.formatted_target_orderbook)
                
                self.notify_observers({'orderbookBestBidsQueue': self.formatted_target_orderbook.best_n_bids_repr(17)})
                self.notify_observers({'orderbookBestAsksQueue': self.formatted_target_orderbook.best_n_asks_repr(17)})

        api_key, api_secret = os.environ.get('DEV_MODE_API_KEY'), os.environ.get('DEV_MODE_API_SECRET')
            
        twm = ThreadedWebsocketManager(api_key, api_secret)
        twm.start()

        twm.start_depth_socket(callback=handle_orderbook, symbol=instrument, depth='20', interval=100)
        
        twm.join()
        
    def run(self, instrument):
        thread = threading.Thread(target=self.orderbook_listener, args=(instrument,))
        thread.daemon = True
        thread.start()
        