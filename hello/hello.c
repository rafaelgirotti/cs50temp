#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("What's your name? "); // asks for name
    printf("hello, %s\n", name); // prints name
}