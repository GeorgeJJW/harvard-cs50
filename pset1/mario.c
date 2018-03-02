#include <cs50.h>
#include <stdio.h>

void draw(int h);
void padding(int n);
void hash(int n);
void space(void);

int main(void){
    
    printf("Height: ");
    int h = get_int();
    
    while (h < 0 || h > 23)
    {
        printf("Height: ");
        h = get_int();
    }
    
    draw(h);
}

void draw(int h)
{
    for (int i = 1; i <= h; i++)
    {
        padding(h - i);
        hash(i);
        space();
        hash(i);
        printf("\n");
    }
}

void padding(int n) {
    for (int i = n; i > 0; i--)
    {
        printf(" ");
    }
}

void hash(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
}

void space(void)
{
    printf("  ");
}