from .stream_orderbook_price_level import OrderbookPriceLevel


def _generate_short_representation(order_list):
    representation = []
    for order in order_list:
        representation.append(f"{float(order.price_level):.2f}      {float(order.cumulated_quantity):.5f}")
    return "\n".join(representation)


def _generate_representation(order_list):
    representation = []
    for order in order_list:
        representation.append(f'{order}')
    return "\n".join(representation)


class StreamOrderbook:
    def __init__(self, message: dict) -> None:
        self.message = message
        self.asks = [OrderbookPriceLevel(price, quantity, 'S') for price, quantity in message['asks']]
        self.bids = [OrderbookPriceLevel(price, quantity, 'B') for price, quantity in message['bids']]

    @property
    def best_bid(self):
        return self.bids[0] if self.bids else None

    @property
    def best_ask(self):
        return self.asks[0] if self.asks else None

    @property
    def best_asks_repr(self):
        return _generate_short_representation(self.asks[::-1])

    @property
    def best_bids_repr(self):
        return _generate_short_representation(self.bids)

    def best_n_asks_repr(self, n: int):
        return _generate_short_representation(self.asks[:n][::-1])

    def best_n_bids_repr(self, n: int):
        return _generate_short_representation(self.bids[:n])

    def __repr__(self):
        asks_repr = _generate_representation(self.asks[::-1])
        bids_repr = _generate_representation(self.bids)
        return f"{asks_repr}\n{bids_repr}"

    # '\033[0m'
    # '\033[31m'
    # '\033[92m'
