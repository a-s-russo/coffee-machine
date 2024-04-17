"""A script to simulate a coffee vending machine."""

import sys
from time import sleep
from tabulate import tabulate

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "milk": 0,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": {
        "amount": 300,
        "unit": "ml",
        "max": 1000,
    },
    "milk": {
        "amount": 200,
        "unit": "ml",
        "max": 1000,
    },
    "coffee": {
        "amount": 100,
        "unit": "g",
        "max": 1000,
    }
}

profit = 0


def print_menu():
    """Prints the items in the menu and their costs."""
    print("\n")
    items = [item.title() for item in MENU]
    costs = [f"${item['cost']:,.2f}" for item in MENU.values()]
    print(tabulate({"Item": items,
                    "Cost": costs},
                   headers="keys",
                   colalign=("left", "right"),
                   tablefmt="pretty"))


def get_order():
    """Asks for and returns a menu item."""
    print_menu()
    order = input("\nWhat would you like to order?\n").lower()
    valid_options = list(
        MENU.keys()) + ['report', 'off', 'restock', 'resupply', 'refill', 'replenish', 'money']
    while order not in valid_options:
        order = input(
            "\nSorry, I didn't understand that. What would you like?\n")
    return order


def print_report():
    """Prints the ingredients in the machine and their quantities, and the current profit."""
    print("\n")
    for ingredient, info in resources.items():
        amount = info['amount']
        unit = info['unit']
        print(f"{ingredient.title()}: {amount:,.0f}{unit}")
    print(f"Money: ${profit:,.2f}")
    input("\nPress Enter to continue...")


def turn_off():
    "Turns off the machine and exits the program."
    print("\nTurning machine off...")
    print_processing_indicator()
    sys.exit()


def is_enough_resources(order):
    """Checks if there are enough ingredients to make the order."""
    for ingredient, info in resources.items():
        if info['amount'] < MENU[order]['ingredients'][ingredient]:
            return False
    return True


def get_coins(coin_type):
    """Gets the number of coins inserted for a given coin type."""
    while True:
        try:
            coins = int(input("\nHow many " + coin_type + "? "))
            if 0 <= coins <= 100:
                break
            if coins < 0:
                print("Invalid input.")
            else:
                print("Too many coins inserted.")
        except ValueError:
            print("Invalid input.")
    return coins


def get_money():
    """Returns the total value calculated from the coins inserted."""
    print("\nPlease insert coins.")
    quarters = get_coins("quarters")
    dimes = get_coins("dimes")
    nickles = get_coins("nickles")
    pennies = get_coins("pennies")
    return quarters * 0.25 + dimes * 0.1 + nickles * 0.05 + pennies * 0.01


def give_change(order, amount):
    """Returns the change in the event of overpayment."""
    cost = MENU[order]['cost']
    change = amount - cost
    if change > 0:
        print(f"\nHere is ${change:,.2f} in change.")
    else:
        print("\nExact money inserted.")
    global profit
    profit = profit + cost


def is_enough_money(order, amount):
    """Checks if the coins inserted are enough to pay for the order."""
    cost = MENU[order]['cost']
    if amount >= cost:
        return True
    else:
        return False


def use_ingredients(order):
    """Deducts the required ingredient quantities from the resources."""
    for ingredient, info in resources.items():
        info['amount'] -= MENU[order]['ingredients'][ingredient]


def get_ingredient():
    """Asks for and returns an ingredient to restock."""
    print_report()
    ingredient = input("\nWhich ingredient?\n").lower()
    valid_options = list(resources.keys())
    while ingredient not in valid_options:
        ingredient = input(
            "\nSorry, I didn't understand that. Which ingredient?\n")
    return ingredient


def get_amount(ingredient):
    """Asks for and returns the amount of an ingredient to be restocked."""
    while True:
        try:
            unit = resources[ingredient]['unit']
            current_amount = resources[ingredient]['amount']
            max_amount = resources[ingredient]['max']
            remaining_amount = max_amount - current_amount
            msg_how_much = "\nHow much " + ingredient + " (in " + unit + ")?\n"
            msg_max_amount = f"(Maximum capacity: {max_amount:,.0f}{unit})\n"
            msg_remaining_amount = f"(Remaining capacity: {
                remaining_amount:,.0f}{unit})\n"
            desired_amount = int(
                input(msg_how_much + msg_max_amount + msg_remaining_amount))
            if desired_amount > 0 and desired_amount + current_amount <= max_amount:
                break
            if desired_amount == 0:
                print("Current amount will remain unchanged.")
                break
            elif desired_amount < 0:
                print("Invalid input.")
            else:
                print("Machine capacity will be exceeded.")
        except ValueError:
            print("Invalid input.")
    return desired_amount


def refill_ingredients():
    """Restocks an ingredient."""
    while True:
        ingredient = get_ingredient()
        amount = get_amount(ingredient)
        resources[ingredient]['amount'] += amount
        if amount > 0:
            print("\nRefilling machine...")
            print_processing_indicator()
        action = input("\nRefill again, or exit?\n").lower()
        if action in ['restock', 'resupply', 'refill', 'replenish']:
            continue
        elif action in ['exit', 'quit']:
            return
        else:
            print('Unknown command. Exiting...')
            break


def print_processing_indicator(repetitions=3):
    """Prints a processing indicator."""
    for _ in range(repetitions):
        sleep(1)
        print('...')


def dispense_order(order):
    """Dispenses an order from the machine."""
    use_ingredients(order)
    print("\nPreparing drink...")
    print_processing_indicator()
    print("\nHere is your", order, "\b:")
    print("\n☕")
    print("\nCAUTION! *Drink may be hot.*")
    input("Please press Enter to take your drink...")


def process_order(order):
    """Processes an order."""
    if is_enough_resources(order):
        money_inserted = get_money()
        if is_enough_money(order, money_inserted):
            give_change(order, money_inserted)
            dispense_order(order)
        else:
            if money_inserted > 0:
                print("\nInsufficient money. Refunding coins...")
            else:
                print("\nNo money inserted. Cancelling order...")
            print_processing_indicator()
    else:
        print("\nInsufficient ingredients. Cancelling order...")
        print_processing_indicator()


def withdraw_money():
    """Retrieves any coins from the machine."""
    global profit
    if profit > 0:
        print(f"\nDispensing ${profit:,.2f}...")
    else:
        print("\nThere is no money to dispense. Exiting...")
    print_processing_indicator()
    profit = 0


def get_action(order):
    """Gets the corresponding action of an order or command."""
    if order.lower() == 'report':
        return print_report()
    elif order.lower() in ['restock', 'resupply', 'refill', 'replenish']:
        return refill_ingredients()
    elif order.lower() == 'money':
        return withdraw_money()
    elif order == 'off':
        return turn_off()
    else:
        return process_order(order)


if __name__ == "__main__":
    while True:
        choice = get_order()
        get_action(choice)
