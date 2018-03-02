#include <stdio.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
    // obtain file name
    char *filename = argv[1];
    
    // open card file
    FILE *cardfile = fopen(filename, "r");
    
    if (cardfile == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", filename);
        return 2;
    }
    
    // initialize variables
    bool jpegfound = false;
    FILE *jpegfile = NULL;
    int jpegcounter = 0;
    int eof = 1;
    
    // read card file
    while (eof == 1)
    {
        // temporary block storage
        unsigned char block[512];
        
        // read 512 bytes from cardfile
        eof = fread(&block, sizeof(block), 1, cardfile);
        
        // exit program if reaches the end of file where the last block is not 512 bytes in size
        if (eof != 1)
        {
            fclose(jpegfile);
            fclose(cardfile);            
            return 0;
        }
        
        // determine if it is start of a new JPEG, if yes
        if (block[0] == 0xff &&
            block[1] == 0xd8 &&
            block[2] == 0xff &&
            (block[3] & 0xf0) == 0xe0)
        {
            // determine if we have already found a JPEG
            // if yes
            if (jpegfound == true)
            {
                // close previous JPEG file and then start a new JPEG
                fclose(jpegfile);
            }
            // if not, start new JPEG
            else
            {
                jpegfound = true;
            }
            
            // determine new JPEG name
            char jpegname[8];
            sprintf(jpegname, "%03i.jpg", jpegcounter);
            jpegcounter += 1;
                
            // open new JPEG file
            jpegfile = fopen(jpegname, "w");
                
            // write signature block to the new JPEG file
            fwrite(&block, sizeof(block), 1, jpegfile);   
        }
        // if it is not the start of a new JPEG
        else
        {
            // determine if we have already found a JPEG
            // if yes
            if (jpegfound == true)
            {
                // write current block to the current JPEG file
                fwrite(&block, sizeof(block), 1, jpegfile);   
            }
            // if not
            //discard block and return to top of loop
        }
    }
    
    // close card file
    fclose(cardfile);

    // success
    return 0;
}