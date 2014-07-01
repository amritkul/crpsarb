class Orders:
        def __init__(self, 'marketid', [orderid], [created], [ordertype], [price], [quantity], [total], [orig_quantity])
                self.marketid = marketid
                self.orderid = orderid
                self.created = created
                self.ordertype = ordertype
                self.price = price
                self.quantity = quantity
                self.total = total
                self.orig_quantity = orig_quantity
                
        def __repr__(self):
                return repr((self.marketid, self.orderid, self.created, self.ordertype, self.price, self.quantity, self.total, self.orig_quantity))

