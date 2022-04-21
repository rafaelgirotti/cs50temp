from cs50 import get_string  # import from cs50 library

name = get_string("What is your name?")  # uses cs50 get_string instead of input
print(f"Hello, {name}")  # prints {name}