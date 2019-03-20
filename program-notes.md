### Program decomposition. 
In other words, breaking down the tasks to where each one is either very small and can be accomplished with a 1-3 lines of code on its own (call this unit task), or is more complex, but is just an assembly of unit tasks that are already done (call this composite task).

1. Toggling/switching between two screens with a long press of the B button.
   1. Define a variable indicating which screen you are in. Can be zero and 1, so you can just increment it modulo 2 when you detect the toggle-to-other screen signal.
   2. Distinguish a long press (aka hold) of a button from simple press. You might need to use a timed delay.
2. Defining the bit pattern to interpret. This is the first screen. 
   1. Toggling LEDs on/off in the proper order (from top-left, row-by-row, to bottom-right) on one page (so, just the first 25).
      1. Toggling a single LED on and off.
      2. OFF is 0, define a constant for ON (1-9), which you can fine-tune it at the end.
      3. Advancing one position each time the B button is pressed.
   2. Managing the bit pattern that will need to be interpreted.
      1. Hold the bit pattern in a list. Start with an empty list.
      2. Append a bit character (‘1’ or ‘0’) to the list each time the B button is pressed.
      3. Finally, to get the bit pattern as a string, use the join method of the string object, as in bit_pattern_as_string = ''.join(['1', '0', '1', '1']), which results in ‘1011’. Note the empty string ‘’, on which join is called. The idea is that the string on which join is called will be the delimiter of the joined strings. If instead it were ‘ ‘ (a single space), the result would be ‘1 0 1 1’.
   3. Put (1) and (2) together, by switching to a blank screen when the 25th (i = 24) bit is selected with the press of the B button. Note that you have to use index j = i - 24 for the second page, because you are starting anew!
   4. Calculating which LED (x: 0-4, y: 0-4) position corresponds to a bit at a specific index in a 32-bit pattern (i: 0-31).
      1. Check the coordinate system by lighting one LED at a time with the proper function of the display object. Find where (0, 0) is.
      2. Remember the basic equations for finding the x-coordinate and y-coordinate from the index i (the 5 comes because we have a 5-by-5 matrix of LEDs):
         - x = i % 5 (modulo operator, which leaves only the remainder of the division)
         - y = i // 5 (integer division, which leaves only the whole part of the division as an integer)
      3. Depending on where (0, 0) is, one of the equations or both equations might need to be modified. Note that we are assuming that x is “across”/”horizontal” and y is “up-down”/”vertical”. If they are not (that is, they are reversed) the equations have to be reversed.
         - They work in their original form if (0, 0) is top-left.
         - If x=0 is on the right, instead of left, the equation becomes x = 4 - (i % 5). This corresponds to mirroring along the vertical axis. Check it!
         - If y=0 is at the bottom, instead of at the top, the equation becomes y = 4 - (i // 5). This corresponds to mirroring along the horizontal axis. Check it!
   5. Adding a blinking cursor.
      1. Get a single LED to blink, which means turning on and off indefinitely until something happens (e.g. button B is pressed). It’s probably easiest to have equal intervals of on and off, but you might want to play with the interval pattern (e.g. 11-00-11-00-11-00 vs 000-1-000-1-000-1, like the light patterns on different harbor lights so they can be told apart in the dark during navigation).
      2. The cursor is the current (x, y) position which is being defined. This is where the fact that the LEDs have a range of intensity (0-9) comes in handy. We have two things we want to accomplish with the cursor, (i) indicate which is the current LED to be defined, and (ii) show its current value (OFF for 0 and ON for 1). If we choose the intensity of the LED at 5 for ON, we can have the cursor blink 55-99-55-99-55 for ON and 00-99-00-99-00 for OFF. Done! 
3. (TODO) Interpreting the bit pattern. This is the second screen.
   1. You already know how to toggle screens, so now you can toggle pages. The distinction between screens and pages is artificial, so it doesn’t matter to the micro:bit, but it helps us in the program decomposition. This screen has two pages: the data type selection and the scrolling display of the of the bit pattern interpreted as the selected data type. The user should be able to toggle between the two, so they can select different data types to see the same bit pattern interpreted as.
      1. Design 4 microbit.Image() constants for the 4 data types:
         - U for unsigned integer.
         - I for signed integer.
         - F for floating point real.
         - C for characters (since each character is 1 byte, the 32-bit pattern can be interpreted as a 4-character string.  
      2. Define a variable for which data-type you are on. This way you can display the right data type every type you are showing this page. Consider a list [‘U’, ‘I’, ‘F’, ‘C’] and the variable being the index. This preserves the order and you can “scroll” by using modulo-4 increments like i = (i + 1) % 4. This causes i to change as follows: 0, 1, 2, 3, 0, 1, 2, 3, 0, … 
      3. Scroll through the 4 data-type images with the button A.
   2. (TODO) Interpreting.
      1. We have learned about different data types. Even though Python does not require you to explicitly define the types of your variables, it definitely keeps track of their types (aka classes, since everything in Python is an object) behind the scenes. For example, if you try to do something with a variable that is doesn’t work for its type, Python will respond with a TypeError. But Python also allows you to convert values from one type to another.
         - (TODO) *Guidance for each of the 4 conversions*
      2. You will have to associate two different things with the index: the corresponding microbit.Image() you have to display, and the function you will use to get the corresponding interpretation of the bit pattern to scroll on the next page. Consider using dictionaries, using the index as key, and the images and function as values. Alternatively, and the more pythonic way, would be to use the characters of the list themselves, as keys. This will be a lot more readable. For example, assume you have defined functions like convert_to_float, convert_to_chars, etc. Then you can have a dictionary that looks like interpret_dict = {‘F’: convert_to_float, ‘C’: convert_to_chars} and, once you have a selection for the data type, you can call the correct function like to_scroll = interpret_dict[‘F’](bit_pattern_as_string). (Incidentally, for the curious, you are not storing the names of the functions, but references to the functions themselves, and you can call them like this, because they are first-class citizens in Python.)
 
### (TODO) Program composition
In other words, putting the different components together in a way that makes sense from the perspective of the user, anticipating what the user might try to do, and gently guiding them toward the intended behavior.
