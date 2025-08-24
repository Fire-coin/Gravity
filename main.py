import tkinter as tk
from math import sqrt

G: float = 6.6743e-11

class Object:
    """This is suposed to be struct aka. everything public"""
    def __init__(self, mass: float, radius: float, color: str, center: list[float], id: int) -> None:
        self.mass = mass
        self.radius = radius
        self.color = color
        self.center = center
        self.id = id
        self.velocity: list[float] = [0, 0]



class GameScreen(tk.Canvas):
    def __init__(self, master: tk.Tk, width: int= 100, height: int = 100, bg: str = "grey", scale: float=  1e10) -> None:
        self.__scale = scale
        self.__w = tk.Canvas(master, width= width, height= height, bg= bg)
        self.__w.pack()
        self.__objects: dict[str, Object] = {}
        self.__idCounter = 0
        self.__w.bind("<Button-1>", lambda e: print(f"Mouse at: {e.x}, {e.y}"))
    
    def create_object(self, mass: float, radius: float, color: str, center: list[float]) -> Object:
        o = Object(mass, radius, color, center, self.__idCounter)
        self.__objects[f"object{o.id}"] = o
        self.__idCounter += 1

        self.__w.create_oval((o.center[0] - o.radius) / self.__scale,
                             (o.center[1] - o.radius) / self.__scale,
                             (o.center[0] + o.radius) / self.__scale,
                             (o.center[1] + o.radius) / self.__scale,
                             fill= o.color,
                             tags= [f"object{o.id}"])
        return o

    def draw_object(self, objectOrId: Object | int, dt: float) -> None:
        if (isinstance(objectOrId, Object)):
            o = self.__objects[f"object{objectOrId.id}"]
        else:
            o = self.__objects[f"object{objectOrId}"]
        
        o.center[0] += o.velocity[0] * dt
        o.center[1] += o.velocity[1] * dt
        self.__w.moveto(f"object{o.id}", (o.center[0] - o.radius) / self.__scale,
                         (o.center[1] - o.radius) / self.__scale)
        


    def render_object(self, objectOrId: Object | int, dt: float) -> None:
        if (isinstance(objectOrId, Object)):
            o = objectOrId
        else:
            o = self.__objects[f"object{objectOrId}"]
        
        id = f"object{o.id}"
        acceleration: list[float] = [0, 0]
        # TODO test to only search through values, because it has 0 distance from itself
        for key, value in self.__objects.items():
            if (key == id):
                continue
            
            deltaX = value.center[0] - o.center[0]
            deltaY = value.center[1] - o.center[1]

            distance: float = sqrt((deltaX * deltaX) + (deltaY * deltaY))

            aScalar: float = (value.mass * G) / (distance * distance)

            acceleration[0] += deltaX * (aScalar / distance)
            acceleration[1] += deltaY * (aScalar / distance)

        o.velocity[0] += acceleration[0] * dt
        o.velocity[1] += acceleration[1] * dt


    def update(self) -> None:
        self.__w.update()
    


def terminate(e: tk.Event):
    global flag
    flag = False


def toggleGame() -> None:
    global running
    running = not running


def startGame(t: float, dt: float) -> None:
    global flag, running
    while (flag):
        while (running and flag):
            t += dt
            for i in objects:
                game.draw_object(i, dt)
            for i in objects:
                game.render_object(i, dt)
            game.update()
        root.update()


if (__name__ == "__main__"):
    global flag
    global running
    flag: bool = True
    running: bool = True
    
    root = tk.Tk()

    gameWidth = 1000
    gameHeight = 700

    game = GameScreen(root, width= gameWidth, height= gameHeight, bg= "black", scale= 1e10)


    startStopButton = tk.Button(root, text= "Start / Stop", command= toggleGame)
    startStopButton.pack()

    root.bind("<Escape>", terminate)
    t: float = 0
    dt: float = 0.1

    o1 = game.create_object(1e42, 3e11, "yellow", [3e12, 4e12])
    o2 = game.create_object(1e40, 4e11, "blue", [7e12, 2e12])
    o3 = game.create_object(4.3e41, 4e11, "green", [6e12, 5e12])
    o4 = game.create_object(1e39, 4e11, "purple", [2e12, 5e12])

    o1.velocity[0] = 5e9


    objects = [o1, o2, o3, o4]

    # Main game loop
    startGame(t, dt)

    root.destroy()

    root.mainloop()