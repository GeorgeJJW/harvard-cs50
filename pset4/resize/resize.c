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
    float f = atof(argv[1]);
    
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

    // read infile's BITMAPFILEHEADER and BITMAPINFOHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    
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
    
    // obtain original width, height, and padding before scaling
    int old_width = bi.biWidth;
    int old_height = bi.biHeight;
    int old_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // calculate new width, height, padding, and image size after scaling
    bi.biWidth *= f;
    bi.biHeight *= f;
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    // write outfile's new header
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // declare an array called source to store triple information from infile
    RGBTRIPLE source[old_width][abs(old_height)];
 
    // store triple informaiton into the source array   
    for (int h = 0, biHeight = abs(old_height); h < biHeight; h++)
    {
        for (int w = 0; w < old_width; w++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // store current triple to source
            source[w][h] = triple;
        }
        
        // skip over padding, if any
        fseek(inptr, old_padding, SEEK_CUR);
    }
    
    // write triple to output file after scaling
    for (int h = 0, biHeight = abs(bi.biHeight); h < biHeight; h++)
    {
        for (int w = 0; w < bi.biWidth; w++)
        {
            // temporary storage
            RGBTRIPLE triple;
            
            // scale indexes according to f
            // repeat appropriate pixels f > 1
            // skip appropriate pixels if 0 < f < 1
            int index_w = w / f;
            int index_h = h / f;
            triple = source[index_w][index_h];
            
            // write RGB triple to outfile
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr); 
        }
        
        // write new padding
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
