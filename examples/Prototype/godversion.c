#include <stdio.h>
int g(int n);
int main()
{
    g(1<<(1<<1^1)^1);
    return 0;
}

int g(int n)
{
    n = (!n)? n+1: g(n+(~1 + 1));
    printf("%d\n",n);
    return n+1;
}
