# CPE 1040 - Comprehensive Review & Enrichment - Week 9 - Part I

Part I of the CRE in week 9 consists of a programming assignment for the micro:bit in MicroPython.

## Requirements

### Overview

Write an application which interprets binary strings as unsigned and signed integers, floating point reals, and character strings.

### Detailed requirements

#### Screens

"Screens" is used in the sense of sub-programs, which are mutually exclusive (that is, only one can be active at a time), and each of which has a distinct function. The application should have two pages:
1. Definition of a 32-bit binary pattern (that is, a sequence of 32 1s and 0s).
2. Interpretation of the 32-bit pattern as different formats and presentation of the interpretation in decimal.

#### Bit pattern definition screen

1. The bit pattern should be represented on the LEDs of the micro:bit, from top-left to bottom-right, row-by-row.
2. Use two pages, one for the first 25 bits, and a second for the remaining 7 bits.
3. Use a blinking cursor to indicate which bit is being selected. Start from the top-left-most bit and go across and down, line-by-line.
4. Button B advances the cursor.
5. Button A toggles the value of the current bit.
6. The LEDs mean the following:
   1. LED on:  1
   2. LED off: 0 

#### Interpretation screen

1. The 32-bit pattern from the other screen should be interpreted in 4 different ways:
   1. U - unsigned integer
   2. I - signed integer
   3. F - floating-point real (single-precision IEEE 754 floating point)
   4. C - a string of 4 ASCII characters *(Note: Some ASCII values might not have character representations on the micro:bit.)*
2. The screen has two different pages:
   1. Format menu, which cycles through `U`, `I`, `F`, and `C` images (that is, user-defined `Image()` constants)
   2. Value page, which scrolls the interpreted number or string, and then returns to the format menu.
3. Button A cycles through the format menu.
4. Button B switches to the value menu with the currently selected format.
5. _Hint: There are datatype conversion functions in Python/MicroPython. You don't have to write them from scratch._

#### Toggling between screens

1. Use a *long press* of button B to toggle between bit pattern definition and interpretation screens.

## Submission

1. Fork this repository on Github.
2. Clone to PyCharm (or an alternative Git interface).
3. Add a Python file to the repository. _Don't forget to `git add` it, too._
4. Code in PyCharm and mu, and test until you are satisfied with the functionality.
5. Commit your code in PyCharm (or an alternative Git interface).
6. Push to remote on Github.
