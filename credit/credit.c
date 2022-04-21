#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int AE1 = 34, AE2 = 37, MC1 = 51, MC2 = 52, MC3 = 53, MC4 = 54, MC5 = 55, Visa = 4;
    int count;
    long card = 0;
    int brand = 0;

    card = get_long("CC Number: "); // get input number
    long temp = card;
    count = 0;

    while (temp > 0) // digits counter
    {
        count++;
        temp /= 10;
    }

    if (count == 13) // visa if count is 13
    {
        int temp13 = card / 1000000000000;
        if (temp13 == Visa)
        {
            brand = 1;
        }
    }
    else if (count == 15) // american express if count is 15
    {
        int temp15 = card / 10000000000000;
        if (temp15 == AE1 || temp15 == AE2)
        {
            brand = 2;
        }
    }
    else if (count == 16) // mastercard or visa if count is 16
    {
        int temp16MC = card / 100000000000000;
        int temp16V = card / 1000000000000000;
        if (temp16MC == MC1 || temp16MC == MC2 || temp16MC == MC3 || temp16MC == MC4 || temp16MC == MC5)
        {
            brand = 3;
        }
        else if (temp16V == Visa)
        {
            brand = 1;
        }
    }

    if (brand != 0)
    {
        int tempx;
        int last = 0;
        int secToLast = 0;

        while (card > 0) // get odd and even numbers from the end and sums them
        {
            last += card % 10;
            card /= 10;
            tempx = (card % 10) * 2;

            if (tempx > 9)
            {
                secToLast += tempx % 10 + tempx / 10;
            }
            else
            {
                secToLast += tempx;
            }
            card /= 10;
        }

        if ((last + secToLast) % 10 == 0) // if algorithm checks up, get brand
        {
            if (brand == 1)
            {
                printf("VISA\n"); // visa
            }
            else if (brand == 2)
            {
                printf("AMEX\n"); // american express
            }
            else if (brand == 3)
            {
                printf("MASTERCARD\n"); // mastercard
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}