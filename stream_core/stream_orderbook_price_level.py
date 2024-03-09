class OrderbookPriceLevel:
    def __init__(self,
                 price_level: str,
                 cumulated_quantity: str,
                 side: str
                 ) -> None:
        self.price_level = price_level
        self.cumulated_quantity = cumulated_quantity
        self.side = side
        
    def __repr__(self):
        return f"{self.side} {self.price_level} {self.cumulated_quantity}"
    