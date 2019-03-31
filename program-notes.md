## Programming notes

Assignment specifications can be found in the [README](README.md).

### Program decomposition. 
In other words, breaking down the tasks to a level at which each one is either very small and can be accomplished with a 1-3 lines of code on its own (call this unit task), or is more complex, but is just an assembly of unit tasks that are already done (call this composite task).

1. Toggling/switching between two screens with a long press (aka hold) of the **B** button.
   1. Define a variable indicating which screen you are in. Can be 0 and 1, so you can just increment it _modulo 2_ when you detect the toggle-screen signal. Example:
      ```python
      screen = 0  # initial value

      # then, when you identify the toggle-screen signal
      screen = (screen + 1) % 2  # thus, it will toggle 0, 1, 0, 1, ...
      ```
   2. Distinguish a long press (aka hold) of a button from simple press. You will need to count the milliseconds between press and release of the button. Consider the [`is_pressed`](https://microbit-micropython.readthedocs.io/en/latest/button.html) function and the functions in [`utime`](https://microbit-micropython.readthedocs.io/en/latest/utime.html). the following code snippet:
      ```python
      import utime

      hold_ms = 2000  # set a hold threshold (2000 ms = 2 s), you can tune later
      if button_b.is_pressed():
          start_ms = utime.ticks_ms()
          while True:
              if not button_b.is_pressed():
                  break
          if utime.ticks_diff(utime.ticks_ms(), start_ms) < hold_ms:
              # simple press
              pass
          else:
              # hold: toggle the screen
              pass
      ```
2. Defining the bit pattern to interpret. This is the first "screen" (`screen = 0`). 
   1. Toggle LEDs on/off in the proper order (from top-left, row-by-row, to bottom-right) on one page (so, just the first 25).
      1. Toggle a single LED on and off with the correct function from the [`display`](https://microbit-micropython.readthedocs.io/en/latest/display.html) object of the micro:bit. Use the **A** button, and keep track of whether the LED is on or off:
         ```python
         current_led_value = 0  # off
         if button_a.was_pressed():
             led_value = (current_led_value + 1) % 2  # alternating: if 1, then 0; if 0, then 1
         ```
      2. OFF is 0. Define a constant for ON (1-9), which you can fine-tune at the end. _See the section on the cursor further below._ Example:
         ```python
         bit_on_intensity = 5
         ```
      3. Advance one position each time the **B** button is pressed. _See the next section on keeping track._
   2. Manage the bit pattern that will need to be interpreted.
      1. Hold the bit pattern in a list. Start with an empty list. Example:
         ```python
         bit_pattern = []
         ```
      2. Append a bit character (`'1'` or `'0'`) to the list each time the **B** button is pressed.
         ```python
         # then, in the code that is getting user selections
         bit_pattern.append('1')  # append the 1 or 0 you just got
         # see above for keeping thrack of the value while A is toggled
         ```
      3. Finally, to get the bit pattern as a string, use the `join()` method of a string object, as in 
         ```python
         bit_pattern_as_string = ''.join(['1', '0', '1', '1'])
         # or
         bit_pattern_as_string = ''.join(bit_pattern)
         ```
         which results in `'1011'`. Note the empty string `''`, on which `join()` is called. The idea is that the string on which `join()` is called will be the delimiter of the joined strings. If instead it were `' '` (a single space), the result would be `'1 0 1 1'`.
   3. Put (1) and (2) together, by switching to a blank screen when the 25th (i = 24) bit is selected with the press of the **B** button. Note that you have to use index `j = i - 24` for the second page, because you are starting anew, or `len(bit_pattern) - 25`. _See next section._
   4. Calculating which LED _(x: 0-4, y: 0-4)_ position corresponds to a bit at a specific index in a 32-bit pattern _(i: 0-31)_.
      1. Check the coordinate system by lighting one LED at a time with the proper function of the [`display`](https://microbit-micropython.readthedocs.io/en/latest/display.html) object. Find where the origin _(0, 0)_ is.
      2. The basic equations for finding the x-coordinate and y-coordinate from the index i (the 5 comes because we have a 5-by-5 matrix of LEDs):
         - `x = i % 5` (modulo operator, which leaves only the remainder of the integer division)
         - `y = i // 5` (integer division, which leaves only the whole part of the division as an integer)
      3. Since the index starts at _0_, you can actually use `len(bit_pattern)` for the current index. Think about it!
      4. Depending on where _(0, 0)_ happens to be, one of the equations or both equations might need to be adjusted. _Note that we are assuming that x is “across”/”horizontal” and y is “up-down”/”vertical”. If they are not (that is, they are reversed) the equations have to be reversed._
         - They work in their original form if _(0, 0)_ is at the _top-left_.
         - If _x=0_ is on the right, instead of left, the equation becomes `x = 4 - (i % 5)`. This corresponds to _mirroring along the vertical axis_. Check it!
         - If _y=0_ is at the bottom, instead of at the top, the equation becomes `y = 4 - (i // 5)`. This corresponds to _mirroring along the horizontal axis_. Check it!
   5. Adding a blinking cursor.
      1. Get a single LED to blink, which means turning on and off indefinitely until something happens (e.g. button **B** is pressed for selection and advancement). It’s probably easiest to have equal intervals of on and off, but you might want to play with the interval pattern (e.g. **11-00-11-00-11-00** vs **000-1-000-1-000-1**, like the light patterns on different harbor lights so they can be told apart in the dark during navigation).
      2. The cursor is the current _(x, y)_ position which is being defined. This is where the fact that the LEDs have a range of intensity _(0-9)_ comes in handy. We have two things we want to accomplish with the cursor:
         - indicate which is the current LED to be defined, and
         - show its current value (OFF for 0 and ON for 1). 
      3. If we choose the intensity of the LED at 5 for ON (see the section on LED toggling above), we can have the cursor blink **55-99-55-99-55** for ON and **00-99-00-99-00** for OFF. This will be perfectly distinguishable for the human eye. Here's an example putting it all together:
         ```python
         import utime

         blink_half_period = 500  # half a second
         blink_value = 0
         blink_ms = utime.ticks_ms()

         current_led_value = 1
         x = 3
         y = 2

         while True:
             check_ms = utime.ticks_ms()
             if utime.tick_diff(check_ms, blink_ms) >= blink_half_period:
                 blink_ms = check_ms
                 blink_value = (blink_value + 1) % 2
                 if blink_value:
                     display.set_pixel(x, y, 9)
                 elif current_led_value:
                     display.set_pixel(x, y, bit_on_intensity)
                 else:
                     display.set_pixel(x, y, 0)
             
         # other code...
         ```
3. Interpreting the bit pattern. This is the second screen.
   1. You already know how to toggle screens, so now you can toggle pages. The distinction between _screens_ and _pages_ is artificial, so it doesn’t matter to the micro:bit, but it helps us in the program decomposition. This screen has two pages: the data type selection and the scrolling display of the of the bit pattern interpreted as the selected data type. The user should be able to toggle between the two, so they can select different data types to see the same bit pattern interpreted as.
      1. Design 4 `microbit.Image()` constants for the 4 data types:
         - **U** for unsigned integer.
         - **I** for signed integer.
         - **F** for floating point real.
         - **C** for characters (since each character is 1 byte, the 32-bit pattern can be interpreted as a 4-character string.  
      2. Define a variable for which data-type you are on. This way you can display the right data type every type you are showing this page. Consider a list `[‘U’, ‘I’, ‘F’, ‘C’]` and the variable being the index `i`. This preserves the order and you can “scroll” by using modulo-4 increments like 
         ```python
         i = (i + 1) % 4  # this causes i to change as follows: 0, 1, 2, 3, 0, 1, 2, 3, 0, … 
         ```
      3. Scroll through the 4 data-type images with the button **A**.
   2. Interpreting.
      1. We have learned about different data types. Even though Python does not require you to explicitly define the types of your variables, it definitely keeps track of their types (aka classes, since everything in Python is an object) behind the scenes. For example, if you try to do something with a variable that is doesn’t work for its type, Python will respond with a **`TypeError`**. But Python also allows you to convert values from one type to another.
         - Verify at the console that `int(bit_pattern_str, 2)` converts the bit pattern string to an integer in decimal. The second argument `2` indicates the base.
         - Because Python presumes to work with _"infinitely"_ large integers, interpreting the bit pattern string as a fixed-width 32-bit _signed_ integer has to follow the 2's complement rules. For now, leave unimplemented by just returning `'Unimplemented'` to the caller of the function so you can scroll this text when the format choice is `'I'`. 
         - Because floating-point numbers in Python are implicitly `binary64`, interpreting the bit pattern string as an IEEE 754 floating-point number has to follow the standard. For now, leave unimplemented by just returning `'Unimplemented'` to the caller of the function so you can scroll this text when the format choice is `'F'`.
         - Because strings in Python are assumed to be `UTF-8` encoded, interpreting the 32-bit pattern as a string of 4 ASCII characters has to follow the general decoding process. For now, leave unimplemented by just returning `'Unimplemented'` to the caller of the function so you can scroll this text when the format choice is `'C'`.
         - I will provide the functions after the break, explain them, and we'll finish Part 2 of this assignment. 
      2. You will have to associate two different things with the index:
         - the corresponding `microbit.Image()` constant you have to display, and 
         - the function you will use to get the corresponding interpretation of the bit pattern to scroll on the next page
      3. For the associations, consider using dictionaries, using the index as key, and the images and function as values. Alternatively, and the more _"pythonic"_ way, would be to use the characters of the list themselves, as keys. This will be a lot more readable. For example,
         ```python
         # define "conversion" functions like 
         def convert_to_float(bit_pattern):
             pass   # this is a placeholder for the body of a yet unimplemented function
        
         def convert_to_chars(bit_pattern):
             pass 
         
         # define a dictionary that looks like 
         interpret_dict = {'F': convert_to_float, 'C': convert_to_chars}
 
         # in the code for the interpretation selection you have something like
         choice = choices_list[2]  # which is 'F'
    
         # once you have a selection for the data type, you can call the correct function like 
         to_scroll = interpret_dict[choice](bit_pattern_as_string)
         ```
      4. For the curious, in the above code snippet, you are not storing the _names_ of the functions, but _references to the functions themselves_. Also, you can call them like this, because they are *first-class entities* in Python.
 
### (TODO) Program composition
In other words, putting the different components together in a way that makes sense from the perspective of the user, anticipating what the user might try to do, and gently guiding them toward the intended behavior.
