from sys import exit
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
    valid_options = list(
        MENU.keys()) + ['report', 'off', 'restock', 'resupply', 'refill', 'replenish', 'money']
    while order not in valid_options:
        order = input(
            "\nSorry, I didn't understand that. What would you like?\n")
    return order


def print_report():
    print("\n")
    for item in resources:
        amount = resources[item]['amount']
        unit = resources[item]['unit']
        print(item.title(), ": ", '{:,.0f}'.format(amount), unit, sep="")
    print("Money:", '${:,.2f}'.format(profit))
    input("\nPress Enter to continue...")


def turn_off():
    print("\nTurning machine off...")
    print_processing_indicator()
    exit()


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
        print("\nExact money inserted.")
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


def get_ingredient():
    print_report()
    ingredient = input("\nWhich ingredient?\n").lower()
    valid_options = list(resources.keys())
    while ingredient not in valid_options:
        ingredient = input(
            "\nSorry, I didn't understand that. Which ingredient?\n")
    return ingredient


def get_amount(ingredient):
    while True:
        try:
            unit = resources[ingredient]['unit']
            current_amount = resources[ingredient]['amount']
            max_amount = resources[ingredient]['max']
            remaining_amount = max_amount - current_amount
            msg_how_much = "\nHow much " + ingredient + " (in " + unit + ")?\n"
            msg_max_amount = "(Maximum capacity: " + \
                '{:,.0f}'.format(max_amount) + unit + ")\n"
            msg_remaining_amount = "(Remaining capacity: " + \
                '{:,.0f}'.format(remaining_amount) + unit + ")\n"
            desired_amount = int(
                input(msg_how_much + msg_max_amount + msg_remaining_amount))
            if desired_amount > 0 and desired_amount + current_amount <= max_amount:
                break
            elif desired_amount == 0:
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
    for i in range(repetitions):
        sleep(1)
        print('...')


def dispense_order(order):
    use_ingredients(order)
    print("\nPreparing drink...")
    print_processing_indicator()
    print("\nHere is your", order, "\b:")
    print("\n☕")
    print("\nCAUTION! *Drink may be hot.*")
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


def withdraw_money():
    global profit
    print("\nDispensing", '${:,.2f}'.format(profit), "\b...")
    print_processing_indicator()
    profit = 0


def get_action(order):
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
        order = get_order()
        get_action(order)
