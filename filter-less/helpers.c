#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float rgbAvg;
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            // never forget to round!!!
            rgbAvg = round((image[j][i].rgbtBlue + image[j][i].rgbtGreen + image[j][i].rgbtRed) / 3.000);

            image[j][i].rgbtBlue = rgbAvg;
            image[j][i].rgbtGreen = rgbAvg;
            image[j][i].rgbtRed = rgbAvg;
        }
    }
}

int rgbMax(int RGB) // prevents the weirdness from overflow
{
    if (RGB > 255)
    {
        RGB = 255;
    }
    return RGB;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaB, sepiaG, sepiaR;
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            sepiaB = rgbMax(round(0.272 * image [j][i].rgbtRed + 0.534 * image[j][i].rgbtGreen + 0.131 * image[j][i].rgbtBlue));
            sepiaG = rgbMax(round(0.349 * image [j][i].rgbtRed + 0.686 * image[j][i].rgbtGreen + 0.168 * image[j][i].rgbtBlue));
            sepiaR = rgbMax(round(0.393 * image [j][i].rgbtRed + 0.769 * image[j][i].rgbtGreen + 0.189 * image[j][i].rgbtBlue));

            image[j][i].rgbtBlue = sepiaB;
            image[j][i].rgbtGreen = sepiaG;
            image[j][i].rgbtRed = sepiaR;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp;
    for (int j = 0; j < width / 2; j++)
    {
        for (int i = 0; i < height; i++) // coud probably be better
        {
            tmp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int plusB, plusG, plusR;
    float count;

    RGBTRIPLE tmp[height][width]; // important not to alter actual values
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            plusB = 0, plusG = 0, plusR = 0, count = 0.00;
            for (int k = -1; k < 2; k++) // hard to wrap my head around that
            {
                if (j + k < 0 || j + k > height - 1)
                {
                    continue;
                }

                for (int h = -1; h < 2; h++)
                {
                    if (i + h < 0 || i + h > width - 1)
                    {
                        continue;
                    }

                    plusB += image[j + k][i + h].rgbtBlue;
                    plusG += image[j + k][i + h].rgbtGreen;
                    plusR += image[j + k][i + h].rgbtRed;
                    count++;
                }
            } // feel like giving up now :(

            tmp[j][i].rgbtBlue = round(plusB / count);
            tmp[j][i].rgbtGreen = round(plusG / count);
            tmp[j][i].rgbtRed = round(plusR / count);
            // finally i'm gonna sleep
        }
    }

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            image[j][i].rgbtBlue = tmp[j][i].rgbtBlue;
            image[j][i].rgbtGreen = tmp[j][i].rgbtGreen;
            image[j][i].rgbtRed = tmp[j][i].rgbtRed;
        }
    }
}
