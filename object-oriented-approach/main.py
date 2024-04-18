"""A script to simulate a coffee vending machine."""

from coffee_maker import CoffeeMaker
from menu import Menu
from money_machine import MoneyMachine

coffee_maker = CoffeeMaker()
menu = Menu()
money_machine = MoneyMachine()


if __name__ == "__main__":
    while True:
        order = menu.get_order()
        if order == 'report':
            print(coffee_maker)
            print(money_machine)
            input("\nPress Enter to continue...")
        elif order in coffee_maker.REFILL_COMMANDS:
            coffee_maker.refill_ingredients()
        elif order == 'money':
            money_machine.withdraw_money()
        elif order == 'off':
            coffee_maker.turn_off()
        else:
            if coffee_maker.is_enough_resources(order):
                if money_machine.process_payment(order.cost):
                    coffee_maker.dispense_order(order)
