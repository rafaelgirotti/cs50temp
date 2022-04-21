from cs50 import get_int

# get height and also check if more than 1 or less than 8
h = 0
while h > 8 or h < 1:
    h = get_int("Height: ")

# prints with height value
for i in range(1, h+1):
    print(" " * (h-i), end="")
    print("#" * (i))