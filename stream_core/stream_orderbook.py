from .orderbook_price_level import OrderbookPriceLevel


class StreamOrderbook:
    def __init__(self, msg):
        self.msg = msg
        self.asks = [OrderbookPriceLevel(price, quantity, 'S') for price, quantity in self.msg['asks']]
        self.bids = [OrderbookPriceLevel(price, quantity, 'B') for price, quantity in self.msg['bids']]
        
    @property
    def best_bid(self):
        return self.bids[0] if self.bids else None

    @property
    def best_ask(self):
        return self.asks[0] if self.asks else None
        
    def __repr__(self):
        orderbook_representation = []
        orderbook_representation.append('\033[31m')
        for ask in self.asks[::-1]:
            orderbook_representation.append(f"{ask.side} {ask.price_level} {ask.cumulated_quantity}")
            
        orderbook_representation.append('\033[92m')
        for bid in self.bids:
            orderbook_representation.append(f"{bid.side} {bid.price_level} {bid.cumulated_quantity}")
        
        return "\n".join(orderbook_representation)