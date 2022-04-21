#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2) // argument has to exist
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int arg_length = strlen(argv[1]); // argument's length
    for (int i = 0; i < arg_length; i++)
    {
        if (!isdigit(argv[1][i])) // check if argument's not a digit
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    string ptxt = get_string("Plaintext: "); // get input
    printf("Ciphertext: "); // enciphered output

    int key = atoi(argv[1]), ptxtlen = strlen(ptxt); // atoi means ascii to integer, length of plaintext

    for (int i = 0; i < ptxtlen; i++)
    {
        if (isupper(ptxt[i])) // if character is uppercase
        {
            printf("%c", (((ptxt[i] - 65) + key) % 26) + 65); // ensure enciphered char is also upper
        }
        else if (islower(ptxt[i])) // if character is lower case
        {
            printf("%c", (((ptxt[i] - 97) + key) % 26) + 97); // ensure enciphered char is also lower
        }
        else // anything else besides alphabet
        {
            printf("%c", ptxt[i]);
        }
    }
    printf("\n");
}