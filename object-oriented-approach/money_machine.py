"""Module providing a class for modelling a payment machine."""

from utilities import print_processing_indicator


class MoneyMachine:
    """Models the machine that processes the payment."""

    COIN_VALUES = {
        "quarters": 0.25,
        "dimes": 0.10,
        "nickles": 0.05,
        "pennies": 0.01,
    }

    def __init__(self):
        self.profit = 0
        self.money_received = 0

    def __str__(self):
        """Prints the current profit."""
        return "Money: " + f"${self.profit:,.2f}"

    def get_coins(self, coin_type):
        """Gets the number of coins inserted for a given coin type."""
        while True:
            try:
                coins = int(input("\nHow many " + coin_type + "? "))
                if coins >= 0 and coins <= 100:
                    break
                elif coins < 0:
                    print("Invalid input.")
                else:
                    print("Too many coins inserted.")
            except ValueError:
                print("Invalid input.")
        return coins

    def get_money(self):
        """Returns the total value calculated from the coins inserted."""
        print("\nPlease insert coins.")
        for coin_type, coin_value in self.COIN_VALUES.items():
            self.money_received += self.get_coins(coin_type) * \
                coin_value
        return self.money_received

    def is_enough_money(self, cost):
        """Checks if the coins inserted are enough to pay for the order."""
        if self.money_received >= cost:
            return True
        return False

    def give_change(self, cost):
        """Returns the change in the event of overpayment."""
        change = self.money_received - cost
        if change > 0:
            print(f"\nHere is ${change:,.2f} in change.")
        else:
            print("\nExact money inserted.")

    def process_payment(self, cost):
        """Process the payment."""
        self.get_money()
        if self.is_enough_money(cost):
            self.give_change(cost)
            self.profit += cost
            self.money_received = 0
            return True
        else:
            if self.money_received > 0:
                print("\nInsufficient money. Refunding coins...")
            else:
                print("\nNo money inserted. Cancelling order...")
            self.money_received = 0
            print_processing_indicator()
            return False

    def withdraw_money(self):
        """Retrieves any coins from the machine."""
        if self.profit > 0:
            print("\nDispensing", f"${self.profit:,.2f}...")
        else:
            print("\nThere is no money to dispense. Exiting...")
        print_processing_indicator()
        self.profit = 0
