import threading
from binance import ThreadedWebsocketManager
import os

from .stream_transaction import StreamTransaction


class TransactionDaemon:
    def __init__(self):
        self.lock = threading.Lock()
        self.observers = []
        self.transaction = None

    def subscribe(self, observer):
        self.observers.append(observer)
        
    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, information):
        for observer in self.observers:
            observer.update(
                'transaction',
                f'{information.price}  '
                f'{information.quantity:.5f}  '
                f'{information.market_order_side}'
            )

    def transaction_listener(self, instrument):
        
        def handle_transaction(message):
            with self.lock:
                self.transaction = StreamTransaction(message)
                print(self.transaction)
                self.notify_observers(self.transaction)

        api_key, api_secret = os.environ.get('DEV_MODE_API_KEY'), os.environ.get('DEV_MODE_API_SECRET')
            
        twm = ThreadedWebsocketManager(api_key, api_secret)
        twm.start()

        twm.start_trade_socket(callback=handle_transaction, symbol=instrument)
        
        twm.join()
        
    def run(self, instrument):
        thread = threading.Thread(target=self.transaction_listener, args=(instrument,))
        thread.daemon = True
        thread.start()
