#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

#define ERR_WRITE 1
#define OUTFILE "out.txt"

/*
Warning: There is minimal error handling in this program
*/

int main() {
    char* buf = "Hello world\n";
    int size = strlen(buf);
    int f = open(OUTFILE, O_CREAT|O_RDWR);
    write(f, buf, size);
    close(f);
}