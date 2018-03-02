#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <math.h>
#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // obtain scale factor
    float f = ceil(atof(argv[1]));
    
    // ensure scaling factor within range
    if (f > 100 || f <= 0)
    {
        fprintf(stderr, "n out of range, must be 0 < n <= 100\n");
        return 1;
    }
    
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 1;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 1;
    }
    
    // determine original padding before scaling
    float old_width = bi.biWidth;
    int old_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // change height and width according to scale factor
    bi.biWidth *= f;
    bi.biHeight *= f;

    // determine new padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // change to image size according to scale factor
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    int linecount = 0;
    
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < old_width; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write RGB triple to outfile
            for (int k = 0; k < f; k++)
            {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);                
            }
        }

        // skip over padding, if any
        fseek(inptr, old_padding, SEEK_CUR);

        // then add it back (to demonstrate how)
        for (int l = 0; l < padding; l++)
        {
            fputc(0x00, outptr);
        }
        
        linecount += 1;
        
        // vertical scaling
        // reset file pointer to start of scanline according to scale factor
        if (linecount < f)
        {
            fseek(inptr, -((old_width * sizeof(RGBTRIPLE)) + old_padding), SEEK_CUR);
            //eprintf("Going back one line!\n");
        }
        // otherwise proceed to scanning the next line
        else
        {
            linecount = 0;    
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
