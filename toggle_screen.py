from microbit import *
import utime

# screen id
screen_id = 0

# hold delay threshold (2000 ms = 2 s), you can tune later
hold_ms = 2000


# placeholder function to id the screen
def show_screen(id):
    display.show(id)


while True:
    if button_b.is_pressed():
        start_ms = utime.ticks_ms()
        while True:
            if not button_b.is_pressed():
                break
        if utime.ticks_diff(utime.ticks_ms(), start_ms) < hold_ms:
            # simple press
            continue
        else:
            # hold
            screen_id = (screen_id + 1) % 2  # toggle screen
            show_screen(screen_id)
