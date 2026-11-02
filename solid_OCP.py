class Payment:
    def pay(self, amount):
        pass


class UPI(Payment):
    def pay(self, amount):
        print("UPI payment:", amount)


class Card(Payment):
    def pay(self, amount):
        print("Card payment:", amount)


class Wallet(Payment):
    def pay(self, amount):
        print("Wallet payment:", amount)


def process_payment(payment_method, amount):
    payment_method.pay(amount)


process_payment(UPI(), 500)
process_payment(Card(), 1000)
process_payment(Wallet(), 200)