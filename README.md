This is simple gravity simulation of bodies in flat space

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