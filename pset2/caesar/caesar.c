#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        // plaintext prompt
        printf("plaintext: ");
        string plain = get_string();
        
        // generate key 
        int k = atoi(argv[1]);
        
        // encrypt letters with key k, excluding punctuations
        printf("ciphertext: ");
        
        for (int i = 0, n = strlen(plain); i < n; i++)
        {
            if (isalpha(plain[i]) && isupper(plain[i]))
            {
                // convert uppercase letters from ASCII index to alphabetical index and back
                printf("%c", (((plain[i] - 65 ) + k ) % 26) + 65);
            }
            else if (isalpha(plain[i]) && islower(plain[i]))
            {
                // convert lowercase letters from ASCII index to alphabetical index and back
                printf("%c", (((plain[i] - 97 ) + k ) % 26) + 97);
            }
            else
            {
                // leaving non-letter characters as they were 
                printf("%c", plain[i]);
            }
        }
        
        // append newline
        printf("\n");
        
        // exit
        return 0;
    }
        
    else
    {
        // error message if argc is not 2
        printf("Usage: ./caesar k\n");
        return 1;
    }
}