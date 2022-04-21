from cs50 import get_string

text = get_string("Text: ")

# letters, words, sentences, counter
l = w = s = i = 0
length = len(text)

while i < length:
    # check if it's alphabet to add letters
    if text[i].isalpha():
        l += 1
    # check for spaces to add words
    if i == 0 and text[i] != " " or i != length and text[i] == " " and text[i+1] != " ":
        w += 1
    # check for periods, question or exclamation marks to add sentences
    if text[i] == "." or text[i] == "?" or text[i] == "!":
        s += 1
    i += 1

L = l * 100 / w
S = s * 100 / w
idx = round(0.0588 * L - 0.296 * S - 15.8)

if idx < 1:
    print("Before Grade 1")
elif idx >= 16:
    print("Grade 16+")
else:
    print(f"Grade {idx}")