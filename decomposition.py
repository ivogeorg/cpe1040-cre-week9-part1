from microbit import *
import utime

#######################################
#         GLOBAL VARIABLES            #
#######################################

# screens and pages
screen_id = 0  # for toggling screens
screens = {0: 'bits', 1: 'value'}  # screen (sub-function) dictionary
page_id = 0  # for toggling pages in screen 'value'
pages = {0: 'type', 1: 'scroll'}  # for screen 'value'
type_id = 0  # for cycling through data types in page 'type' in screen 'value'
types = {0: 'U', 1: 'I', 2: 'F', 3: 'C'}  # for page 'type'
scroll_value = 2.134  # placeholder, will be set properly before being shown
value_funs = {}  # value function dictionary (see VALUE FUNCTIONS)
scrolled = False
hold_b = False

# intervals
hold_ms = 2000  # hold delay threshold (2000 ms = 2 s), you can tune later
blink_ms = 500  # cursor blink half period
scroll_ms = 1000  # scroll delay

# bits
bit_list = []  # the bit list is filled with 1 and 0 as integers
current_bit = 0  # value of bit currently being set
bit_on = 5  # led intensity
cursor_on = 9  # led intensity
led_array_side = 5  # width/height of the square led array
max_array_bits = led_array_side * led_array_side  # maximum leds in the led array/matrix
max_bits = 32  # the maximum number of bits in the bit list


#######################################
#          DISPLAY FUNCTIONS          #
#######################################

# identify where you are (screen and page) and display
# use the variables above

def bit_image():
    pass

# show display (note: cannot use display as a function name because it would shadow the eponymous microbit object)
def show():
    global screen_id
    global screens
    global page_id
    global pages
    global type_id
    global types
    global scroll_ms
    global scrolled

    if screens[screen_id] == 'bits':
        display.show(bit_image())
        # TODO: blinking cursor on top of current bit
    elif screens[screen_id] == 'value':
        if pages[page_id] == 'type':
            display.show(types[type_id])
        elif pages[page_id] == 'scroll':
            if not scrolled:
                scrolled = True
                display.scroll(scroll_value, wait=False)  # scroll in the background, allow holding buttons


#######################################
#           VALUE FUNCTIONS           #
#######################################
def bit_pattern_value_unsigned(bit_string):
    global scroll_value

    scroll_value = int(bit_string, 2)


def bit_pattern_value_signed(bit_string):
    global scroll_value

    scroll_value = 'Unimplemented'


def bit_pattern_value_floating(bit_string):
    global scroll_value

    scroll_value = 'Unimplemented'


def bit_pattern_value_ascii(bit_string):
    global scroll_value

    scroll_value = 'Unimplemented'


value_funs[types[0]] = bit_pattern_value_unsigned
value_funs[types[1]] = bit_pattern_value_signed
value_funs[types[2]] = bit_pattern_value_floating
value_funs[types[3]] = bit_pattern_value_ascii


#######################################
#          CONTROL FUNCTIONS          #
#######################################

# controls:
# screen "bits":
#   A press: toggle value of current bit
#   B press: write bit and advance cursor, advancing pass, if necessary
#   B hold:  toggle to "value" screen, right-padding bit list with 0s
# screen "value":
#   A press: cycle through data type selections
#   B press: toggle "type" and "scroll" pages


# toggle screen

# TODO: SUBTLE BUG
# after toggling back 'value' to 'bits', but ONLY from 'scroll' and not from 'type',
# it takes TWO simple presses of button B to transition to 'value' at the last bit

def toggle_screen():
    pass

# action B press
def action_b_press():
    global bit_list
    global current_bit
    global pages
    global page_id
    global max_bits
    global types
    global type_id
    global value_funs
    global scroll_value
    global scrolled

    pass

# action A press
def action_a_press():
    global bit_list
    global current_bit
    global type_id
    global types
    global scrolled
    global pages
    global page_id

    if screens[screen_id] == 'bits':
        if len(bit_list) < max_bits:
            current_bit = (current_bit + 1) % 2
    elif screens[screen_id] == 'value':
        if pages[page_id] == 'type':
            type_id = (type_id + 1) % len(types)
            scrolled = False


#######################################
#              MAIN LOOP              #
#######################################

while True:
    # show current display state according to screen, page, etc.
    show()

    # poll for control actions and dispatch corresponding functions
    hold_b = False
    if button_b.is_pressed():
        start_ms = utime.ticks_ms()
        while True:
            if not button_b.is_pressed():
                break
        if utime.ticks_diff(utime.ticks_ms(), start_ms) >= hold_ms:
            # hold
            hold_b = True  # set hold-B to prevent a simple press to be registered
            toggle_screen()

    if button_b.was_pressed():  # note: was_pressed is better for toggling and cycling
        if hold_b:
            hold_b = False  # reset hold-B
        else:
            action_b_press()

    elif button_a.was_pressed():  # note: was_pressed is better for toggling and cycling
        action_a_press()
