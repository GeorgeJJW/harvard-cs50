#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string s = get_string();
    
    int n = 0;
    
    // computer uses eight 0 bits to designate that a string ends
    while (s[n] != '\0')
    {
        n++;
    }
    
    printf("%i\n", n);
}