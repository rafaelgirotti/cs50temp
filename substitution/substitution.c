#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2) // if command line argument is not equal to 2
    {
        printf("Usage: ./substitution key\n"); // prints message of usage
        return 1;
    }

    int argvlen = strlen(argv[1]);
    if (argvlen != 26)
    {
        printf("Key must be up to 26\n"); // if key is not 26 characters
        return 1;
    }
    for (int i = 0; i < argvlen; i++)
    {
        if (!isalpha(argv[1][i])) // if key is not alphabet
        {
            printf("All Key must be an Alphabet\n");
            return 1;
        }
        for (int j = i + 1; j < argvlen; j++)
        {
            if (argv[1][i] == argv[1][j])
            {
                printf("Key must not contain repeated alphabet");
                return 1;
            }
        }
    }

    string txt = get_string("plaintext: "); // get input for text
    printf("ciphertext: "); // print ciphertext
    int txtlen = strlen(txt);
    for (int i = 0; i < txtlen; i++)
    {
        if (isupper(txt[i])) // check uppercase
        {
            printf("%c", toupper(argv[1][txt[i] - 65])); // stay uppercase
        }
        else if (islower(txt[i]))  //check if lowercase
        {
            printf("%c", tolower(argv[1][txt[i] - 97])); // stay lowercase
        }
        else
        {
            printf("%c", txt[i]);
        }

    }
    printf("\n");
}
