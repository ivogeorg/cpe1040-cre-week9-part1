from microbit import *

bit_list = [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
bit_on = 5
current_bit = 1


def bit_image():
    global bit_list
    
    num_bits = len(bit_list)                                # how many bits are already defined
    show_bits = []                                          # list for constructing the Image

    # which page are we on?
    if num_bits <= 25:
        show_bits = [b for b in bit_list]
    else:
        show_bits = [b for b in bit_list[25:]]

    # add the current bit (0 or 1)
    show_bits.append(current_bit)

    # right-pad with 0s
    show_bits.extend([0 for _ in range(25 - len(show_bits))])
    
    # convert list values to characters and join into a string
    bit_string = ''.join([str(bit_on) if b == 1 else '0' for b in show_bits])

    # construct image string
    img_string = ':'.join([bit_string[0:5], bit_string[5:10], bit_string[10:15], bit_string[15:20], bit_string[20:]])

    return Image(img_string)


while True:
    # display.show(Image('01234:56789:87654:32101:23456'))
    # display.show(Image('55555:55555:55000:00000:00000'))
    display.show(bit_image())