from datetime import datetime


class Transaction:
    def __init__(self,
                 event_time,
                 symbol,
                 trade_id,
                 price,
                 quantity,
                 buyer_order_id,
                 seller_order_id,
                 transaction_time,
                 is_the_buyer_market_maker
                 ):
        self.event_time = event_time
        self.symbol = symbol
        self.trade_id = trade_id
        self.price = price
        self.quantity = quantity
        self.buyer_order_id = buyer_order_id
        self.seller_order_id = seller_order_id
        self.transaction_time = transaction_time
        self.is_the_buyer_market_maker = is_the_buyer_market_maker
        
        self.formatted_event_time = datetime.fromtimestamp(event_time / 1000).strftime("%Y:%m:%dT%H:%M:%S:%f")[:-3]
        self.formatted_transaction_time = datetime.fromtimestamp(transaction_time / 1000).strftime("%Y:%m:%dT%H:%M:%S:%f")[:-3]
        self.market_order_side = 'B' if not is_the_buyer_market_maker else 'S'

    def __repr__(self):
        return f"{self.formatted_event_time} {self.event_time} {self.symbol} {self.trade_id} {self.price} {self.quantity} {self.buyer_order_id} {self.seller_order_id} {self.formatted_transaction_time} {self.transaction_time} {self.market_order_side} {self.is_the_buyer_market_maker}"
