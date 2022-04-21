#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    int l = 0, w = 1, s = 0; // letter, word and sentence count
    string txt = get_string("Text: ");
    int txtlen = strlen(txt);

    for (int i = 0; i < txtlen; i++) // loop to count letters
    {
        if (isalpha(txt[i])) // is alphabet
        {
            l++;
        }
    }
    for (int i = 0; i < txtlen; i++) // loop to count words
    {
        if (isspace(txt[i]))
        {
            w++;
        }
    }
    for (int i = 0; i < txtlen; i++) // loop to count sentences
    {
        if (txt[i] == '.' || txt[i] == '?' || txt[i] == '!') // check for end sentence characters
        {
            s++;
        }
    }

    float calc = (0.0588 * l / w * 100) - (0.296 * s / w * 100) - 15.8; // readability formula calculation
    int idx = round(calc);

    if (idx < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (idx > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", idx);
    }
}