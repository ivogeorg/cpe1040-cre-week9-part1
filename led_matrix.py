# How to determine the coordinate system of the led matrix

from microbit import *

bit_on = 5

while True:
    display.set_pixel(0, 0, bit_on)  # origin
    display.set_pixel(1, 1, bit_on)  # diagonal growth direction
    display.set_pixel(2, 3, bit_on)  # orientation of of x and y

# So:
# 1. origin (0, 0) is top-left
# 2. x is across, which is standard for matrices
# 3. y is up-down, which is standard for matrices

# Note:
# The construction of a micorbit Image object for the function show()
# is a dead giveaway of what the coordinate system is, as it is
# constructed by concatenating line after line from top to bottom!
