import threading
from binance import ThreadedWebsocketManager
import os

from abstract_base_classes.observer import Observer
from .stream_transaction import StreamTransaction


class TransactionDaemon(Observer):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.transaction = None

    def transaction_listener(self, instrument):

        def handle_transaction(message):
            with self.lock:
                # print(message)
                self.transaction = StreamTransaction(message)
                # print(self.transaction)
                information_to_send = (
                    f'{self.transaction.price} '
                    f'{self.transaction.quantity:.5f} '
                    f'{self.transaction.market_order_side}'
                )

                self.notify_observers(
                    {'transaction': information_to_send}
                )

        api_key, api_secret = os.environ.get('DEV_MODE_API_KEY'), os.environ.get('DEV_MODE_API_SECRET')

        twm = ThreadedWebsocketManager(api_key, api_secret)
        twm.start()

        twm.start_trade_socket(callback=handle_transaction, symbol=instrument)

        twm.join()

    def run(self, instrument):
        thread = threading.Thread(target=self.transaction_listener, args=(instrument,))
        thread.daemon = True
        thread.start()
