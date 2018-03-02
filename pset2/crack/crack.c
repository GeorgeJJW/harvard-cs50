#define _XOPEN_SOURCE
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        // obtain target hash as string
        string pass = argv[1];
        
        // generate single digit possibilities (A-Z and a-z)
        char c[123] = {};
        string single[] = {};
        for (int i = 'A'; i <= 'z'; i++)
        {
            c[i] = i;
            // convert single digit characters to strings
            sprintf(single[i], "%c%c", c[i], '\0');
            
            // crypt hash comparison module
            // convert single digit string to hash
            string hash = crypt(single[i], "50");
            // compare hash with target hash
            if (strcmp(hash, pass) == 0)
            {
                // print actual password
                printf("%s\n", single[i]);
                return 0;
            }
        }
        
        // generate two-digits possibilities
        string d[] = {};
        for (int i = 65; i <= 122; i++)
        {
            for (int j = 65; j <= 122; j++)
            {
                sprintf(d[i], "%c%c", c[i], c[j]);
                
                // crypt hash comparison module
                // convert double digit string to hash
                string hash = crypt(d[i], "50");
                // compare hash with target hash
                if (strcmp(hash, pass) == 0)
                {
                    // print actual password
                    printf("%s\n", d[i]);
                    return 0;
                }
            }
        }
        
        // gemerate three-digits possibilities
        string t[] = {};
        for (int i = 65; i <= 122; i++)
        {
            for (int j = 65; j <= 122; j++)
            {
                for (int k = 65; k <= 122; k++)
                {
                    sprintf(t[i], "%c%c%c", c[i], c[j], c[k]);
                    
                    // crypt hash comparison module
                    // convert three-digits string to hash
                    string hash = crypt(t[i], "50");
                    //eprintf("%s\n", hash);
                    // compare hash with target hash
                    if (strcmp(hash, pass) == 0)
                    {
                        // print actual password
                        printf("%s\n", t[i]);
                        return 0;
                    }
                }
            }
        }
        
        // generate four-digits possibilities
        string q[] = {};
        for (int i = 65; i <= 122; i++)
        {
            for (int j = 65; j <= 122; j++)
            {
                for (int k = 65; k <= 122; k++)
                {
                    for (int l = 65; l <= 122; l++)
                    {
                        sprintf(q[i], "%c%c%c%c", c[i], c[j], c[k], c[l]);
                        
                        // crypt hash comparison module
                        // convert four-digits string to hash
                        string hash = crypt(q[i], "50");
                        // compare hash with target hash
                        if (strcmp(hash, pass) == 0)
                        {
                            // print actual password
                            printf("%s\n", q[i]);
                            return 0;
                        }
                    }
                }
            }
        }
    }
    else
    {
        // print error message if argc is not equal to 2
        printf("Usage: ./crack hash");
        return 1;
    }
}