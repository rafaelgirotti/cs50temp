#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int y;  // integer for height
    do
    {
        y = get_int("Height: ");  // ask for y value
    }
    while (y < 1 || y > 8); // y can't be less than 1 or more than 8

    for (int z = 0; z < y; z++) // loops spaces and hashes
    {
        for (int w = y; w - 1 > z; w--)
        {
            printf(" ");  // if w is bigger than z, less space
        }
        for (int x = 0; x <= z; x++)
        {
            printf("#");  // if x is less than or equal to z, more hashes
        }
        printf("\n");  // added new line after instead of before, so no weird space
    }
}