#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // obtain unsorted array
    int values[7] = {10, 7, 12, 4, 9, 13};
    int n = 6;
    
    // count the frequency of each unique value and store them to count[]
    int count[14] = {};
    
    for (int i = 0; i < n; i++)
    {
        count[values[i]] += 1;
    }

    // transform count[] by determining the starting index of each unique value
    int sum = 0;
    
    for (int j = 0; j <= 13; j++)
    {
        int previous_count = count[j];
        count[j] += sum;
        sum += previous_count;
    }
    
    // compile the sorted array
    int sorted[7] = {};
    
    for (int i = 0; i < n; i++)
    {
        sorted[count[values[i]] - 1] = values[i];
        count[values[i]] -= 1;
    }
        for (int i = 0; i < n; i++)
    {
        values[i] = sorted[i];
    }
    
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", values[i]);
    }
}