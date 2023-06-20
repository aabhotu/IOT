#include "mraa_beaglebone_pinmap.h"
#include <stdio.h>
#include <string.h>
mraa_gpio_context pb1;
mraa_gpio_context pb2;
int but;
int main(int argc, char** argv)
{
    int x;
    mraa_init();

    pb1 = mraa_gpio_init(B1);
    mraa_gpio_dir(pb1, MRAA_GPIO_IN);
    
    pb2 = mraa_gpio_init(B2);
    mraa_gpio_dir(pb2, MRAA_GPIO_IN);
    if (mraa_gpio_read(pb1) == 0)
    {
        but = 1;
        return but;
    }

    if (mraa_gpio_read(pb2) == 0)
    {
        but = 2;
        return but;
    }
}
