#include <unistd.h>
#include <stdlib.h>

#include "attr.h"

int main(int argc, unused char **argv)
{
    if (argc != 1)
        return EXIT_FAILURE;
    write(1, "Hello World!\n", 13);
    return EXIT_SUCCESS;
}
