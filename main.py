import tkinter as tk

from preview import *
from gameScreen import *


def terminate(e: tk.Event):
    global flag
    flag = False


def toggleGame(game: GameScreen, e: tk.Event) -> None:
    global running
    if (e.char != ' '):
        return
    deletePreview(game)
    running = not running
    game.showInfo(running)


def startGame(t: float, dt: float, game: GameScreen, root: tk.Tk) -> None:
    global flag, running
    while (flag):
        while (running and flag):
            t += dt
            game.draw_objects(dt)
            game.render_objects(dt)
            game.update()
        root.update()


def showHelpWindow() -> None:
    helpWin = tk.Tk()

    tk.Label(helpWin, text= "Press Space bar to start / pause simulation\n" + 
             "Press left mouse button to select or create new object object\n" +
             "Press right mouse button to delete selected object\n" + 
             "Press Enter to apply changes made in pop up menu with properties\n" + 
             "Press left Alt to save object into simulation screen\n" + 
             "Press c to copy selected object\n").pack()
    
    tk.Button(helpWin, text= "Understood", command= lambda : helpWin.destroy()).pack()



if (__name__ == "__main__"):
    global flag
    global running
    flag: bool = True
    running: bool = False

    root = tk.Tk()

    setUpGlobals(root)

    sHeight = root.winfo_screenheight()
    sWidth = root.winfo_screenwidth()

    gameWidth = sWidth
    gameHeight = sHeight - 200

    game = GameScreen(root, width= gameWidth, height= gameHeight, bg= "black", scale= 1e5)

    helpButton = tk.Button(game.getCanvas(), text= "Help", command= showHelpWindow)

    winId = game.getWindowId()
    game.getCanvas().itemconfigure(winId, window= helpButton)

    game.getCanvas().bind("<Button-1>", lambda e: previewObject(e, game))
    game.getCanvas().bind("<Button-3>", lambda e: deletePreview(game))

    root.bind("<Key>", lambda e: toggleGame(game, e))
    root.bind("<Escape>", terminate)

    t: float = 0
    dt: float = 0.1

    o1 = game.create_object(1e20, 3, "yellow", [2e7, 4.8e7])
    o2 = game.create_object(1e22, 40, "blue", [7e7, 2e7])
    o3 = game.create_object(6e24, 64, "green", [6e7, 5e7])
    o4 = game.create_object(1.9e24, 20, "purple", [2e7, 5e7])

    o1.velocity[0] = 1.3e4

    game.changeObject(o1)


    objects = [o1, o2, o3, o4]

    # Main game loop
    startGame(t, dt, game, root)

    root.destroy()

    root.mainloop()