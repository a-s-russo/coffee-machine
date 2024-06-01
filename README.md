# Coffee vending machine

A script to simulate interaction with a coffee vending machine via the command line interface as a customer or as an owner (via secret commands).

Inspired by the project for day 15 of the course: [100 Days of Python](https://100daysofpython.dev/).

## Running

To run the simulation:
1. Ensure [Python](https://www.python.org/) is installed on your computer.
2. Ensure the Python package [tabulate](https://pypi.org/project/tabulate/) is installed using `pip install tabulate`.
3. Download the relevant files from this repository:
    - For the functional programming approach, downloand `coffee.py` from the `📁functional-programming-approach` folder.
    - For the object-oriented approach, download the Python scripts from the `📁object-oriented-approach` folder (that is, the five `*.py` files) into the same folder.
4. Run `coffee.py` or `main.py`, respectively.

(The functionality between the functional programming and object-oriented approaches should be mostly the same.)

## Modifying

Change the relevant values in the relevant scripts as desired, such as the menu items and the machine's starting stock levels.

## Ordering a beverage

```
+------------+-------+
| Item       |  Cost |
+------------+-------+
| Espresso   | $1.50 |
| Latte      | $2.50 |
| Cappuccino | $3.00 |
+------------+-------+

What would you like to order?
latte
```

## Inserting coins

```
Please insert coins.

How many quarters? 9

How many dimes? 3

How many nickles? 0

How many pennies? 0

Here is $0.05 in change.

Preparing drink...
...
...
...

Here is your latte:

☕

CAUTION! *Drink may be hot.*
Please press Enter to take your drink...
```

## Checking supplies

```
What would you like to order?
report


Water: 100ml
Milk: 50ml
Coffee: 76g
Money: $2.50

Press Enter to continue...
```

## Restocking ingredients

```
What would you like to order?
refill


Water: 100ml
Milk: 50ml
Coffee: 76g
Money: $2.50

Press Enter to continue...

Which ingredient?
milk

How much milk (in ml)?
(Maximum capacity: 1,000ml)
(Remaining capacity: 950ml)
500

Refilling machine...
...
...
...

Refill again, or exit?
exit
```

## Withdrawing profit

```
What would you like to order?
money

Dispensing $2.50...
...
...
...
```

## Turning off

```
What would you like to order?
off

Turning machine off...
...
...
...
```
