#include<cs50.h>
#include<stdio.h>

void validate(long long n);
void company(long long n);

int main(void)
{
    printf("Number: ");
    long long n = get_long_long();
    
    validate(n);
    
    company(n);
}

void validate(long long n)
{
    long long sum = 0;
    
    for (long long  i = 10; i <= n; i *= 100)
    {
        long long one = (((n / i) % 10) * 2);
        
        for (long long j = 1; j <= one + 1; j *= 10)
        {
            long long two = (one / j) % 10;
            sum = sum + two;
        }
    }
    
    for (long long k = 1; k <= n; k *=100)
    {
        long long three = ((n / k) % 10);
        sum = sum + three;
    }
    
    if ((sum % 10) != 0)
    {
        printf("INVALID\n");
    }
}

void company(long long n)
{
    // AMEX
    if (n >= 340000000000000 & n < 1000000000000000)
    {
        printf("AMEX\n");
    }
    // MasterCard
    else if (n >= 5100000000000000)
    {
        printf("MASTERCARD\n");
    }
    // VISA
    else if (n >= 4000000000000 || n >= 4000000000000000)
    {
        printf("VISA\n");
    } 
}