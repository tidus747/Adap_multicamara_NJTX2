#!/bin/bash

# Script para la configuracion de los GPIO del conector Auvidea J20

sudo i2cset -f -y 0 0x77 3 0xfb  # enable 1.8V power to the J20
sudo i2cset -f -y 2 0x20 6 0x3e  # no data collisionrt expander (low byte) - clock lines remain input, so there is is no data collision
sudo i2cset -f -y 2 0x20 7 0x33  # configure the out puts of the I2C port expander (high byte) 
sudo i2cset -f -y 2 0x20 2 0xfe  # write ones to all GPIO outputs and turn on LED (low byte)
sudo i2cset -f -y 2 0x20 3 0xff  # write ones to all GPIO outputs (high byte)
