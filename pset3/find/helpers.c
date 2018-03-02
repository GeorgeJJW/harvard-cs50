/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
   if (n < 0)
   {
       return false;
   }
   
   for (int i = 0; i < n; i ++)
   {
       if (values[i] == value)
       {
           return true;
       }
   }
   
   return false;
}

/**
 * Sorts array of n values.
 */
// using counting sort

void sort(int values[], int n)
{
    // count the frequency of each value
    int count[65537] = {};
    
    for (int i = 0; i < n; i++)
    {
        count[values[i]] += 1;
    }
    
    // transform count[] by determining the starting index of each unique value
    int sum = 0;
    
    for (int j = 0; j <= 65536; j++)
    {
        int previous_count = count[j];
        count[j] += sum;
        sum += previous_count;
    }
    
    // compile the sorted array
    int sorted[65537] = {};
    
    for (int i = 0; i < n; i++)
    {
        sorted[count[values[i]] - 1] = values[i];
        count[values[i]] -= 1;
    }
    
    // copy the sorted array back to the original array
    for (int i = 0; i < n; i++)
    {
        values[i] = sorted[i];
    }
}
