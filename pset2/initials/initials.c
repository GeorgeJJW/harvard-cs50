#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    // obtain user's name as a string
    string name = get_string();
    
    // first letter
    if (name[0] != ' ')
    {
        printf("%c", toupper(name[0]));
    }
    
    // letters following spaces
    // name[i + 1] should not be indexing the \0 null terminator, hence n - 1 in the for loop
    for (int i = 0, n = strlen(name); i < n - 1; i++)
    {
        if (name[i] == ' ' && name[i + 1] != ' ' )
        {
            printf("%c", toupper(name[i + 1]));
        }
    }
    
    // append line break
    printf("\n");
}