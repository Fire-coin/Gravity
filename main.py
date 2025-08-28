import tkinter as tk
from math import sqrt
from copy import deepcopy

G: float = 6.6743e-11

class ObjectForm:
    def __init__(self, master: tk.Tk) -> None:
        self.frame1 = tk.Frame(master, height= 300)
        self.frame2 = tk.Frame(self.frame1)
        self.mass = tk.DoubleVar(self.frame1, name= "mass", value= 1e4)
        self.color = tk.StringVar(self.frame1, name= "color", value= "blue")
        self.radius = tk.DoubleVar(self.frame1, name= "radius", value= 50)
        self.velX = tk.DoubleVar(self.frame1, name= "velX", value= 0)
        self.velY = tk.DoubleVar(self.frame1, name= "velY", value= 0)



        self.l1 = tk.Label(self.frame2, text= "Mass: ")
        self.e1 = tk.Entry(self.frame1, textvariable= self.mass)

        self.l2 = tk.Label(self.frame2, text= "Color: ")
        self.e2 = tk.Entry(self.frame1, textvariable= self.color)

        self.l3 = tk.Label(self.frame2, text= "Radius: ")
        self.e3 = tk.Entry(self.frame1, textvariable= self.radius)

        self.l4 = tk.Label(self.frame2, text= "velocity X: ")
        self.e4 = tk.Entry(self.frame1, textvariable= self.velX)
        
        self.l5 = tk.Label(self.frame2, text= "velocity Y: ")
        self.e5 = tk.Entry(self.frame1, textvariable= self.velY)
        

    
    def pack(self, side: str) -> None:
        self.frame1.pack(side= side) # type: ignore
        self.frame2.pack(side= "left")
        self.l1.pack()
        self.e1.pack(pady= 1)
        
        self.l2.pack()
        self.e2.pack(pady= 1)

        self.l3.pack()
        self.e3.pack(pady= 1)

        self.l4.pack()
        self.e4.pack(pady= 1)

        self.l5.pack()
        self.e5.pack(pady= 1)
        
    def get(self) -> list[str]:
        output: list[str] = []
        output.append(self.e1.get())
        output.append(self.e2.get())
        output.append(self.e3.get())
        output.append(self.e4.get())
        output.append(self.e5.get())
    
        return output
    
    def destroy(self) -> None:
        self.frame1.destroy()
        self.frame2.destroy()

    def hide(self) -> None:
        self.frame1.pack_forget()
        self.frame2.pack_forget()



class Object:
    """This is suposed to be struct aka. everything public"""
    def __init__(self, mass: float, radius: float, color: str, center: list[float], id: int) -> None:
        self.mass = mass
        self.radius = radius
        self.color = color
        self.center = center
        self.ID = id
        self.velocity: list[float] = [0, 0]
    
    def __str__(self) -> str:
        return f"Object: {self.ID}, {self.mass=}, {self.radius=}, {self.velocity=}"



class GameScreen(tk.Canvas):
    def __init__(self, master: tk.Tk, width: int= 100, height: int = 100, bg: str = "grey", scale: float=  1e10) -> None:
        self.__scale = scale
        self.__w = tk.Canvas(master, width= width, height= height, bg= bg)
        self.__w.pack()
        self.__objects: dict[str, Object] = {}
        self.__idCounter = 0
        self.__w.bind("<Button-1>", lambda e: previewObject(e, self))
        self.__w.bind("<Button-3>", lambda e: deletePreview())
    

    def getCanvas(self) -> tk.Canvas:
        return self.__w

    
    def create_object(self, mass: float, radius: float, color: str, center: list[float]) -> Object:
        o = Object(mass, radius, color, center, self.__idCounter)
        self.__objects[f"object{o.ID}"] = o
        self.__idCounter += 1

        self.__w.create_oval((o.center[0]) / self.__scale - o.radius,
                             (o.center[1]) / self.__scale - o.radius,
                             (o.center[0]) / self.__scale + o.radius,
                             (o.center[1]) / self.__scale + o.radius,
                             fill= o.color,
                             tags= [f"object{o.ID}"])
        return deepcopy(o)

    def draw_object(self, objectOrId: Object | int, dt: float) -> None:
        if (isinstance(objectOrId, Object)):
            o = self.__objects[f"object{objectOrId.ID}"]
        else:
            o = self.__objects[f"object{objectOrId}"]
        
        o.center[0] += o.velocity[0] * dt
        o.center[1] += o.velocity[1] * dt
        self.__w.moveto(f"object{o.ID}", (o.center[0]) / self.__scale - o.radius,
                         (o.center[1]) / self.__scale - o.radius)
    

    def draw_objects(self, dt: float) -> None:
        for o in self.__objects.values():
            self.draw_object(o, dt)
    

    def render_objects(self, dt: float) -> None:
        for o in self.__objects.values():
            self.render_object(o, dt)

    
    def delete_object(self, objectOrId: Object | int) -> None:
        if (isinstance(objectOrId, Object)):
            self.__w.delete(f"object{objectOrId.ID}")
            del self.__objects[f"object{objectOrId.ID}"]
            self.__w.update()
        else:
            self.__w.delete(f"object{objectOrId}")
            del self.__objects[f"object{objectOrId}"]
            self.__w.update()


    def render_object(self, objectOrId: Object | int, dt: float) -> None:
        if (isinstance(objectOrId, Object)):
            o = objectOrId
        else:
            o = self.__objects[f"object{objectOrId}"]
        
        id = f"object{o.ID}"
        acceleration: list[float] = [0, 0]
        # TODO test to only search through values, because it has 0 distance from itself
        for key, value in self.__objects.items():
            if (key == id):
                continue
            
            deltaX = value.center[0] - o.center[0]
            deltaY = o.center[1] - value.center[1]

            distance: float = sqrt((deltaX * deltaX) + (deltaY * deltaY))

            aScalar: float = (value.mass * G) / (distance * distance)

            acceleration[0] += deltaX * (aScalar / distance)
            acceleration[1] += deltaY * (aScalar / distance)

        o.velocity[0] += acceleration[0] * dt
        o.velocity[1] += acceleration[1] * dt


    def changeObject(self, object: Object) -> None:
        self.__objects[f"object{object.ID}"] = deepcopy(object)


    def update(self) -> None:
        self.__w.update()
    
    def getScale(self) -> float:
        return self.__scale



def deletePreviewForm() -> None:
    global last_form
    if (last_form):
        last_form.destroy()


def deletePreviewObject() -> None:
    global last_object 
    if (last_object.ID != -1):
        game.delete_object(last_object)
        last_object.ID = -1


def deletePreview() -> None:
    global last_form
    deletePreviewObject()
    deletePreviewForm()


def createForm() -> None:
    global last_form

    deletePreviewForm()

    last_form = ObjectForm(root)
    last_form.pack("left")


def showPreviewObject(e: tk.Event | None, game: GameScreen) -> None:
    global last_object
    deletePreviewObject()

    values: list[str] = last_form.get()

    mass = float(values[0])
    color = values[1]
    radius = float(values[2])
    velX = float(values[3])
    velY = float(values[4])

    scale: float = game.getScale()

    if (e is not None):
        last_object = game.create_object(mass, radius, color, [e.x * scale, e.y * scale])
    else:
        last_object = game.create_object(mass, radius, color, last_object.center)


    last_object.velocity = [velX, velY]

    game.changeObject(last_object)


def previewObject(e: tk.Event, game: GameScreen) -> None:
    global root
    global last_object
    global last_form
    # Make Alt place the object and rebind this function to other key
    root.bind("<Return>", lambda ee: showPreviewObject(None, game))
    game.getCanvas().unbind("<Button-1>")
    game.getCanvas().bind("<Button-1>", lambda ee: showPreviewObject(ee, game))
    root.bind("<Alt_L>", lambda ee: createObject(game))

    createForm()
    showPreviewObject(e, game)


def createObject(game: GameScreen) -> None:
    global last_object

    last_object.ID = -1

    deletePreviewForm()

    game.getCanvas().bind("<Button-1>", lambda e: previewObject(e, game))


def terminate(e: tk.Event):
    global flag
    flag = False


def toggleGame() -> None:
    global running
    deletePreview()
    running = not running


def startGame(t: float, dt: float) -> None:
    global flag, running
    while (flag):
        while (running and flag):
            t += dt
            game.draw_objects(dt)
            game.render_objects(dt)
            game.update()
        root.update()


if (__name__ == "__main__"):
    global flag
    global running
    global root
    global last_object
    global last_form
    flag: bool = True
    running: bool = False


    last_object: Object = Object(0, 0, "", [0, 0], -1)
    
    root = tk.Tk()

    last_form: ObjectForm = ObjectForm(root)

    gameWidth = 1000
    gameHeight = 700

    game = GameScreen(root, width= gameWidth, height= gameHeight, bg= "black", scale= 1e5)


    startStopButton = tk.Button(root, text= "Start / Stop", command= toggleGame)
    startStopButton.pack(side= "left")

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
    startGame(t, dt)

    root.destroy()

    root.mainloop()