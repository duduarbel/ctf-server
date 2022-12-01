#include <stdio.h>  /* printf */
#include <stdlib.h> /* malloc */
#include <time.h>   /* time */
#include <string.h> /* strncpy */

#define PASS_SIZE (12)


void print_flag(void)
{
    FILE *fd;

    fd = fopen("flag.txt", "r");
    if (fd)
    {
        while (1)
        {
            int ch = getc(fd);
            if (ch == -1)
                break;
            putchar(ch);
        }
        putchar('\n');
        fclose(fd);
    }
}


int main()
{
    setvbuf(stdout, NULL, _IONBF, 0); // cancel stdout buffering

    char *password = (char *)malloc(PASS_SIZE);
    char user_buf[PASS_SIZE + 2];
    int i;

    srand(time(0));

	
    for (i = 0; i < PASS_SIZE; i++)
    {
        password[i] = 'A' + rand() % ('z' - 'A' + 1);
    }

    while (1)
    {
      	read(0, user_buf, PASS_SIZE+2);

        if (strncmp(user_buf, password, PASS_SIZE) == 0)
        {
            print_flag();
        }
        else
        {
            puts("nop");
        }
    }

    return 0;
}
