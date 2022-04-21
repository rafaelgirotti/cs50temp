#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h; // height
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8); // not less than 1 nor greater than 8

    for (int row = 0; row < h; row++) // prints new line as row
    {
        for (int spc = h - row - 1; spc > 0; spc--) // prints space
        {
            printf(" ");
        }

        for (int hash = 0; hash < row + 1; hash++) // prints hashes
        {
            printf("#");
        }

        printf("  ");
        for (int rhash = 0; rhash < row + 1; rhash++) // prints right blocks
        {
            printf("#");
        }
        printf("\n");
    }
}