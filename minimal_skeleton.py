# a minimal skeleton for the program

from microbit import *
import utime

# screens and pages
screen_id = 0  # for toggling screens
screens = {0: 'bits', 1: 'value'}
page_id = 0  # for toggling pages in screen 'value'
pages = {0: 'type', 1: 'scroll'}  # for screen 'value'
type_id = 0  # for cycling through data types in page 'type' in screen 'value'
types = {0: 'U', 1: 'I', 2: 'F', 3: 'C'}  # for page 'type'

# intervals
hold_ms = 2000  # hold delay threshold (2000 ms = 2 s), you can tune later
blink_ms = 500  # cursor blink half period

# bits
bit_list = []  # the bit list
current_bit = 0  # value of current bit
bit_on = 5  # led intensity
cursor_on = 9  # led intensity


# toggle screen
def toggle_screen():
    global screen_id
    screen_id = (screen_id + 1) % 2  # toggle screen
    display.show(screen_id)


# identify where you are (screen and page) and display
# use the variables above

# show display (note: cannot use display because it would shadow the eponymous microbit object)
def show():
    pass


# controls:
# screen "bits":
#   A press: toggle value of current bit
#   B press: write bit and advance cursor, advancing pass, if necessary
#   B hold:  toggle to "value" screen, right-padding bit list with 0s
# screen "value":
#   A press: cycle through data type selections
#   B press: toggle "type" and "scroll" pages
#   B hold:  toggle to "bits" screen, clearing the bits


# action B press
def action_b_press():
    pass


# action A press
def action_a_press():
    pass


while True:
    # show current display state according to current screen, page, etc.
    show()

    # call control functions according to button presses to change state
    if button_b.is_pressed():
        start_ms = utime.ticks_ms()
        while True:
            if not button_b.is_pressed():
                break
        if utime.ticks_diff(utime.ticks_ms(), start_ms) < hold_ms:
            # simple press
            action_b_press()
        else:
            # hold
            toggle_screen()
    elif button_a.is_pressed():
        action_a_press()
