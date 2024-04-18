"""Module providing a class for modelling a coffee maker."""

import sys

from tabulate import tabulate
from utilities import print_processing_indicator


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

    REFILL_COMMANDS = ['restock', 'resupply', 'refill', 'replenish']

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
                print_processing_indicator()
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
        print_processing_indicator()
        print("\nHere is your " + order.name + ":")
        print("\n☕")
        print("\nCAUTION! *Drink may be hot.*")
        input("Please press Enter to take your drink...")

    def get_ingredient(self):
        """Asks for and returns an ingredient to restock."""
        print(self)
        ingredient_name = input("\nWhich ingredient?\n").lower()
        valid_options = [ingredient.name.lower()
                         for ingredient in self.resources]
        while ingredient_name not in valid_options:
            ingredient_name = input(
                "\nSorry, I didn't understand that. Which ingredient?\n")
        for ingredient in self.resources:
            if ingredient.name == ingredient_name:
                return ingredient

    def get_amount(self, ingredient):
        """Asks for and returns the amount of an ingredient to be restocked."""
        while True:
            try:
                remaining_amount = ingredient.info['max'] - \
                    ingredient.info['amount']
                if remaining_amount == 0:
                    print("Machine capacity already reached.")
                    return 0
                msg_how_much = f"\nHow much {
                    ingredient.name} (in {ingredient.info['unit']})?\n"
                msg_max_amount = f"(Maximum capacity: {ingredient.info['max']:,.0f}{
                    ingredient.info['unit']})\n"
                msg_remaining_amount = f"(Remaining capacity: {
                    remaining_amount:,.0f}{ingredient.info['unit']})\n"
                desired_amount = int(
                    input(msg_how_much + msg_max_amount + msg_remaining_amount))
                if desired_amount > 0 and \
                        desired_amount + ingredient.info['amount'] <= ingredient.info['max']:
                    break
                if desired_amount == 0:
                    print("Current amount will remain unchanged.")
                    break
                if desired_amount < 0:
                    print("Invalid input.")
                else:
                    print("Machine capacity will be exceeded.")
            except ValueError:
                print("Invalid input.")
        return desired_amount

    def refill_ingredients(self):
        """Restocks an ingredient."""
        while True:
            ingredient_to_refill = self.get_ingredient()
            amount_to_refill = self.get_amount(ingredient_to_refill)
            for ingredient in self.resources:
                if ingredient_to_refill.name == ingredient.name:
                    ingredient.info['amount'] += amount_to_refill
            if amount_to_refill > 0:
                print("\nRefilling machine...")
                print_processing_indicator()
            action = input("\nRefill again, or exit?\n").lower()
            if action in self.REFILL_COMMANDS:
                continue
            elif action in ['exit', 'quit']:
                return
            else:
                print('Unknown command. Exiting...')
                print_processing_indicator()
                break

    def turn_off(self):
        "Turns off the machine and exits the program."
        print("\nTurning machine off...")
        print_processing_indicator()
        sys.exit()
