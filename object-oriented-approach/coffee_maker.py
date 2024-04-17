"""Module providing a class for modelling a coffee maker."""

import sys

from tabulate import tabulate


class Ingredient:
    """Models the ingredients of a coffee machine."""

    def __init__(self, name, amount, unit, max_amount):
        self.name = name
        self.info = {
            "amount": amount,
            "unit": unit,
            "max": max_amount,
        }


class CoffeeMaker:
    """Models the machine that makes the coffee."""

    def __init__(self):
        self.resources = [
            Ingredient(name="water", amount=300, unit="ml", max_amount=1000),
            Ingredient(name="milk", amount=200, unit="ml", max_amount=1000),
            Ingredient(name="coffee", amount=100, unit="g", max_amount=1000)
        ]

    def __str__(self):
        """Prints the ingredients in the machine and their quantities."""
        ingredients = [ingredient.name.title()
                       for ingredient in self.resources]
        quantities = [f"{ingredient.info["amount"]:,.0f}{
            ingredient.info["unit"]:}" for ingredient in self.resources]
        return "\n" + tabulate({"Ingredient": ingredients,
                                "Quantity": quantities},
                               headers="keys",
                               colalign=("left", "right"),
                               tablefmt="pretty")

    def is_enough_resources(self, order):
        """Checks if there are enough ingredients to make the order."""
        for ingredient, index in zip(order.ingredients, range(0, len(self.resources))):
            if order.ingredients[ingredient] > self.resources[index].info['amount']:
                print("\nInsufficient ingredients. Cancelling order...")
                # print_processing_indicator()
                return False
        return True

    def use_ingredients(self, order):
        """Deducts the required ingredient quantities from the resources."""
        for ingredient, index in zip(order.ingredients, range(0, len(self.resources))):
            self.resources[index].info['amount'] -= order.ingredients[ingredient]

    def dispense_order(self, order):
        """Dispenses an order from the machine."""
        self.use_ingredients(order)
        print("\nPreparing drink...")
        # print_processing_indicator()
        print("\nHere is your " + order.name + ":")
        print("\n☕")
        print("\nCAUTION! *Drink may be hot.*")
        input("Please press Enter to take your drink...")

    def turn_off(self):
        "Turns off the machine and exits the program."
        print("\nTurning machine off...")
        # print_processing_indicator()
        sys.exit()
