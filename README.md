
<img width="1913" height="912" alt="img1" src="https://github.com/Fire-coin/Gravity/tree/main/img/img1.png" />

# Gravity Simulator
This is simple gravity simulation of bodies in flat space
There is no colision detection

# Usage
## Starting and pausing simulation
By pressing Space bar you will start / pause simulation, the current state of simulation is shown in top left corner in info menu.

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

## Creating an object
Press the left mouse button to create an object in space, with that there will be a menu in the bottom of screen, where you can change its properties.

## Modifing an object
By pressing left mouse button on already existing object, the same menu as when creating object will be at the bottom of screen where you can change it's properties.

## Selected object
When you create an object it is automatically set as selected object.
When you modify object, it is also set as selected object.
You can change properties of only selected obtject.
Selected object will move each time to the new mouse position when left mouse button is clicked.
### Apply changes to the selected object
By pressing Enter key, the changes you made to the object properties will be applied.
### Placing selected object in simulation
To place the selected object in simulation you need to press left Alt, by this the properties menu will hide and object will not be deleted when simulation will start.
If selected object is not placed in the simulation using left Alt, it will be deleted from simulation when simulation is started.
### Deleting selected object
By pressing right mouse button you can delete selected object.
### Copying selected object
By pressing c key, you will selected object, this mean that current selected object will be placed in the simulation and there will be new selected object with same properties as original object.

# Creating executable localy
Maybe you want to change some things in the code, and make an executable from it, this is step by step to do it.
## Installing pyinstaller
This package allows to compile python code into executable
Type the following into python terminal: <code>pip install pyinstaller</code>

Here are also alternative ways to install it: https://pyinstaller.org/en/stable/installation.html

## Getting the code files
Next clone the repository in your local machine, or unpack the zip file from release version
Then run this script in terminal: <code>python -m PyInstaller main.py -F -w -n Gravity_Simulation</code>
You can change the Gravity_Simulation to whatever you want

## flag definitions:
    -F tells pyinstaller to make the executable 1 file, so it can be run not only in this repository
    -w makes the exe windowed, hence the terminal will not pop up when it is ran
    -n renames the executable Gravity_Simulation

For additional flags go on this page: https://pyinstaller.org/en/stable/usage.html

Finally, when compiled, 2 folders will appear: build and dist, the executable will be in deit folder. 
