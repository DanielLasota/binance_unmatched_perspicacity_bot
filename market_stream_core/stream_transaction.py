from datetime import datetime


class StreamTransaction:
    def __init__(
            self, 
            message
            ):
        self.event_time = message['E']
        self.symbol = message['s']
        self.trade_id = message['t']
        self.price = float(message['p'])
        self.quantity = float(message['q'])
        self.buyer_order_id = message['b']
        self.seller_order_id = message['a']
        self.transaction_time = message['T']
        self.is_the_buyer_market_maker = message['m']
        
        self.formatted_event_time = datetime.fromtimestamp(self.event_time / 1000).strftime("%Y:%m:%dT%H:%M:%S:%f")[:-3]
        self.formatted_transaction_time = datetime.fromtimestamp(self.transaction_time / 1000).strftime("%Y:%m:%dT%H:%M:%S:%f")[:-3]
        self.market_order_side = 'B' if not self.is_the_buyer_market_maker else 'S'
        rounded_price_value = round(float(self.price), 2)
        self.price = f"{rounded_price_value:.2f}"
        
    def __repr__(self):
        return f"{self.formatted_event_time} {self.event_time} {self.symbol} {self.trade_id} {self.price} {self.quantity} {self.buyer_order_id} {self.seller_order_id} {self.formatted_transaction_time} {self.transaction_time} {self.market_order_side} {self.is_the_buyer_market_maker}"