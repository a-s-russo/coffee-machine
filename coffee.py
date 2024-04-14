import sys
import time

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

profit = 0
resources = {
    "water": {
        "amount": 300,
        "unit": "ml",
    },
    "milk": {
        "amount": 200,
        "unit": "ml",
    },
    "coffee": {
        "amount": 100,
        "unit": "g",
    }
}


def print_menu():
    print("\n")
    items = [item.title() for item in MENU.keys()]
    costs = ['${:,.2f}'.format(item['cost']) for item in MENU.values()]
    print(tabulate({"Item": items,
                    "Cost": costs},
                   headers="keys",
                   colalign=("left", "right"),
                   tablefmt="pretty"))


def get_order():
    print_menu()
    order = input("\nWhat would you like to order?\n").lower()
    valid_options = list(MENU.keys()) + ['report', 'off']
    while order not in valid_options:
        order = input(
            "Sorry, I didn't understand that. What would you like? (espresso/latte/cappuccino\n")
    return order


def print_report():
    print("\n")
    for item in resources:
        amount = resources[item]['amount']
        unit = resources[item]['unit']
        print(item.title(), ": ", amount, unit, sep="")
    print("Money:", '${:,.2f}'.format(profit))
    input("\nPress Enter to continue...")


def turn_off():
    print("\nTurning machine off...")
    print_processing_indicator()
    sys.exit()


def is_enough_resources(order):
    required_water = MENU[order]['ingredients']['water']
    required_milk = MENU[order]['ingredients']['milk']
    required_coffee = MENU[order]['ingredients']['coffee']
    if resources['water']['amount'] < required_water:
        return False
    elif resources['milk']['amount'] < required_milk:
        return False
    elif resources['coffee']['amount'] < required_coffee:
        return False
    else:
        return True


def get_coin(type):
    while True:
        try:
            coins = int(input("\nHow many " + type + "? "))
            if coins >= 0 and coins <= 100:
                break
            elif coins < 0:
                print("Invalid input.")
            else:
                print("Too many coins inserted.")
        except ValueError:
            print("Invalid input.")
    return coins


def get_money():
    print("\nPlease insert coins.")
    quarters = get_coin("quarters")
    dimes = get_coin("dimes")
    nickles = get_coin("nickles")
    pennies = get_coin("pennies")
    return quarters * 0.25 + dimes * 0.1 + nickles * 0.05 + pennies * 0.01


def give_change(order, amount):
    cost = MENU[order]['cost']
    change = amount - cost
    if change > 0:
        print("\nHere is", '${:,.2f}'.format(change), "in change.")
    else:
        print("\nExact money inserted")
    global profit
    profit = profit + cost


def is_enough_money(order, amount):
    cost = MENU[order]['cost']
    if amount >= cost:
        return True
    else:
        return False


def use_ingredients(order):
    required_water = MENU[order]['ingredients']['water']
    required_milk = MENU[order]['ingredients']['milk']
    required_coffee = MENU[order]['ingredients']['coffee']
    resources['water']['amount'] -= required_water
    resources['milk']['amount'] -= required_milk
    resources['coffee']['amount'] -= required_coffee


def print_processing_indicator(repetitions=3):
    for i in range(repetitions):
        time.sleep(1)
        print('...')


def dispense_order(order):
    use_ingredients(order)
    print("\nPreparing drink...")
    print_processing_indicator()
    print("\nHere is your", order, "\b:")
    print("\n☕")
    print("\nCAUTION! *Drink may be hot*")
    input("Please press Enter to take your drink...")


def process_order(order):
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


def get_action(order):
    if order == 'report':
        return (print_report())
    elif order == 'off':
        return (turn_off())
    else:
        return (process_order(order))


if __name__ == "__main__":
    while True:
        order = get_order()
        get_action(order)
