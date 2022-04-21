from cs50 import get_float

# get input that's bigger than 0
dol = 0
while dol <= 0:
    dol = get_float("Cents: ")

coins = 0
cents = round(dol * 100, 0)

# calculate change
while cents > 0:
    if cents >= 25:
        cents -= 25
        coins += 1
    elif cents >= 10:
        cents -= 10
        coins += 1
    elif cents >= 5:
        cents -= 5
        coins += 1
    else:
        cents -= 1
        coins += 1

# prints calculation results
print(f"{coins}")