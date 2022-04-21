// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    node *w = table[hash(word)];

    if (strcasecmp(w->word, word) == 0)
    {
        return true;
    }

    while (w->next != NULL)
    {
        w = w->next;
        if (strcasecmp(w->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int n = (int) tolower(word[0]) - 97;
    return n;
}

int total = 0;
// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    char *dw = malloc(LENGTH + 1);
    if (dw != NULL)
    {
        while (fscanf(file, "%s", dw) != EOF)
        {
            node *n = malloc(sizeof(node));
            if (n != NULL)
            {
                strcpy(n->word, dw);
                total++;
                n->next = table[hash(dw)];
                table[hash(dw)] = n;
            }
        }
    }

    fclose(file);
    free(dw);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return total;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *tmp, *w;
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            w = table[i];
            tmp = w;
            while (w->next != NULL)
            {
                w = w->next;
                free(tmp);
                tmp = w;
            }
            free(w);
        }
        else
        {
            continue;
        }
    }
    return true;
}
