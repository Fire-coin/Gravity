# Gravity Simulator
This is simple gravity simulation of bodies in flat space
There is no colision detection

# Usage
Press the left mouse button to create an object in space, with that there will be a menu in the bottom of screen, where you can change its properties, such as mass, radius, velocity, .etc
## Object properties
### Mass
You can enter any numerical value you want, and in any way, however it is recomended to enter in standart form, to keep it managable
Default value is 5.972e24, which is same as mass of Earth
### Radius
The radius is given in pixels on the screen, because of lack of collision detection, it serves only decorative purpose
Default value is 50
### Color
You can enter any valid color name supported by tkinter canvas, and also rgb values in this format #RRGGBB
Default value is blue
### Velocity X
This is x component of velocity vector of object, measured in m/s
Default is set to 0
### Velocity Y
This is y component of velocity vector of object, measured in m/s
Default is set to 0
### X coord
X coordinate of center of an object
Default is set to the mouse position during click
### Y coord
Y coordinate of center of an object
Default is set to the mouse position during click

To create exe file you need to install pyinstaller first:
type the following into python terminal: pip install pyinstaller

here are alternative ways to install it: https://pyinstaller.org/en/stable/installation.html

Next clone the repository in your local machine, then run this script in terminal: python -m PyInstaller main.py -F -w -n Gravity_Simulation

flag definitions:
    -F tells pyinstaller to make the executable 1 file, so it can be run not only in this repository
    -w makes the exe windowed, hence the terminal will not pop up when it is ran
    -n renames the executable Gravity_Simulation

For additional flags go on this page: https://pyinstaller.org/en/stable/usage.html

Finally, when compiled, 2 folders will appear: build and dest, the executable will be in dest folder. 
