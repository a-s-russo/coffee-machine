"""Module providing classes for modelling a menu and menu items."""

from operator import attrgetter
from tabulate import tabulate


class MenuItem:
    """Models a menu item."""

    def __init__(self, name, cost, water, milk, coffee):
        self.name = name
        self.cost = cost
        self.ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee,
        }


class Menu:
    """Models a menu of items."""

    SECRET_COMMANDS = ['report', 'off', 'money']
    REFILL_COMMANDS = ['restock', 'resupply', 'refill', 'replenish']

    def __init__(self):
        self.menu = sorted([
            MenuItem(name="espresso", water=50, milk=0, coffee=18, cost=1.5),
            MenuItem(name="latte", water=200, milk=150, coffee=24, cost=2.5),
            MenuItem(name="cappuccino", water=250, milk=50, coffee=24, cost=3),
        ], key=attrgetter('cost', 'name'))

    def __str__(self):
        """Prints the items in the menu and their costs."""
        items = [item.name.title() for item in self.menu]
        costs = [f"${item.cost:,.2f}" for item in self.menu]
        return "\n" + tabulate({"Item": items,
                                "Cost": costs},
                               headers="keys",
                               colalign=("left", "right"),
                               tablefmt="pretty")

    def get_order(self):
        """Asks for and returns a menu item."""
        print(self)
        order_name = input("\nWhat would you like to order?\n").lower()
        items = [item.name for item in self.menu]
        valid_options = items + self.REFILL_COMMANDS + self.SECRET_COMMANDS
        while order_name not in valid_options:
            order_name = input(
                "\nSorry, I didn't understand that. What would you like?\n")
        if order_name in items:
            for item in self.menu:
                if item.name == order_name:
                    return item
        return order_name
