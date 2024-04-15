# Coffee vending machine

A script to simulate interaction with a coffee vending machine via the command line interface as a customer or as an owner (via secret commands).

Inspired by the project for day 15 of the course: [100 Days of Python](https://100daysofpython.dev/).

## Order beverage

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

## Insert coins

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

## Check supplies

```
What would you like to order?
report


Water: 100ml
Milk: 50ml
Coffee: 76g
Money: $2.50

Press Enter to continue...
```

## Restock ingredients

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
350

Refilling machine...
...
...
...

Refill again, or exit?
exit
```

## Withdraw profit

```
What would you like to order?
money

Dispensing $2.50...
...
...
...
```

## Turn off

```
What would you like to order?
off

Turning machine off...
...
...
...
```