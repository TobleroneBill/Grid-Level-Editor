# Grid-Level-Editor
mario maker style editor which generates levels for my c++ game
Itch link is here:
https://billiams.itch.io/grid-based-level-editor

This is pretty early in development so far, but I am also working on a c++ project that will become a 2d platformer using SFML.

This is my level editor, which exports into a 256x16 grid of 0-6. This will then be used by my c++ game to generate the levels when they are loaded.

Got a few things I still need to work out, but functions currently and will hopefully be adding some cool stuff in the future to make it more accessable, and less awful lol

Controls:
- WASD - Movement
- Left Alt - Fast Movement
- Shift + Movement - Skip 5 units
- = - Increase Unit Skip
- (minus) - Decrease Unit Skip (I have a wierd keyboard)
- Home - go to x:0
- End - goto x:256
- Tab - Jump forward 1 screen
- Shift+Tab - Jump back 1 screen
- F1 - Export current layout to file
- F2 - Load current layout to file
- ESC - Quit (faster than using the window quit)
- Period - Cycle forward blocktype
- Comma - change to previous blocktype


As you can see thats alot of things currently, but hoping to add:

- Mouse Controls
- Actual Block & entity Types
- Area Select
- Brush Size & shape
- Better Export Window
- Sound effects
