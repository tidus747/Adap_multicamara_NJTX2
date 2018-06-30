#!/bin/bash

sudo i2cset -f -y 2 0x20 2 0  # write ones to all GPIO outputs and turn on LED (low byte)
sudo i2cset -f -y 2 0x20 3 0  # write ones to all GPIO outputs (high byte)

sudo i2cset -f -y 2 0x20 2 0xfe  # write ones to all GPIO outputs and turn on LED (low byte)
sudo i2cset -f -y 2 0x20 3 0xff  # write ones to all GPIO outputs (high byte)