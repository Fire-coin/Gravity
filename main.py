import tkinter as tk

class GameScreen(tk.Canvas):
    def __init__(self, master: tk.Tk, width: int= 100, height: int = 100, bg: str = "grey"):
        self.w = tk.Canvas(master, width= width, height= height, bg= bg)
        self.w.pack()
    
    def update(self) -> None:
        self.w.update()



def terminate(e: tk.Event):
    global flag
    flag = False


if (__name__ == "__main__"):
    global flag
    flag = True
    
    root = tk.Tk()
    game = GameScreen(root, 500, 500, "grey")

    root.bind("<Escape>", terminate)
    t: float = 0
    dt: float = 0.1

    # Main game loop
    while (flag):
        t += dt
        game.update()
    
    root.destroy()

    root.mainloop()
