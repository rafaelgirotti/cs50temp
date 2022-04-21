#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2) // if no argument present
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "rb");
    if (!file) // if no file present
    {
        return 1;
    }

    FILE *img = NULL;

    BYTE buffer[512];
    char filename[8];
    int counter = 0;
    while (fread(buffer, sizeof(BYTE), 512, file) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (counter == 0) // writes image if counter = 0
            {
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "wb");
                fwrite(&buffer, sizeof(BYTE), 512, img);
                counter += 1;
            }
            else if (counter > 0) // ** using rb and wb instead of r and w for non-text files
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "wb");
                fwrite(&buffer, sizeof(BYTE), 512, img);
                counter += 1;
            }
        }
        else if (counter > 0) // if not new image, keeps writing
        {
            fwrite(&buffer, sizeof(BYTE), 512, img);
        }
    }

    fclose(file);
    fclose(img);
}