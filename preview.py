import tkinter as tk

from gameScreen import GameScreen, Object

last_object: Object
last_form: "ObjectForm"

class ObjectForm:
    def __init__(self, master: tk.Tk) -> None:
        self.frame1 = tk.Frame(master, height= 300)
        self.frame2 = tk.Frame(self.frame1)
        self.mass = tk.DoubleVar(self.frame1, name= "mass", value= 1e4)
        self.color = tk.StringVar(self.frame1, name= "color", value= "blue")
        self.radius = tk.DoubleVar(self.frame1, name= "radius", value= 50)
        self.velX = tk.DoubleVar(self.frame1, name= "velX", value= 0)
        self.velY = tk.DoubleVar(self.frame1, name= "velY", value= 0)
        self.coordX = tk.DoubleVar(self.frame1, name= "coordX", value= 0)
        self.coordY = tk.DoubleVar(self.frame1, name= "coordY", value= 0)



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

        self.l6 = tk.Label(self.frame2, text= "X coord: ")
        self.e6 = tk.Entry(self.frame1, textvariable= self.coordX)
        
        self.l7 = tk.Label(self.frame2, text= "Y coord: ")
        self.e7 = tk.Entry(self.frame1, textvariable= self.coordY)

    
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

        self.l6.pack()
        self.e6.pack(pady= 1)

        self.l7.pack()
        self.e7.pack(pady= 1)
        
    def get(self) -> list[str]:
        output: list[str] = []
        output.append(self.e1.get())
        output.append(self.e2.get())
        output.append(self.e3.get())
        output.append(self.e4.get())
        output.append(self.e5.get())
        output.append(self.e6.get())
        output.append(self.e7.get())
    
        return output
    
    def destroy(self) -> None:
        self.frame1.destroy()
        self.frame2.destroy()

    def hide(self) -> None:
        self.frame1.pack_forget()
        self.frame2.pack_forget()



def setUpGlobals(root: tk.Tk) -> None:
    global last_object
    global last_form

    last_object = Object(0, 0, "", [0, 0], -1)
    last_form = ObjectForm(root)


def resetBinding(game: GameScreen) -> None:
    game.getCanvas().unbind("<Button-1>")
    game.getMaster().unbind("<Return>")
    game.getMaster().unbind("<Alt_L>")
    game.getMaster().unbind("c")

    game.getCanvas().bind("<Button-1>", lambda e: previewObject(e, game))


def deletePreviewForm() -> None:
    global last_form
    if (last_form):
        last_form.destroy()


def deletePreviewObject(game: GameScreen) -> None:
    global last_object 
    if (last_object.ID != -1):
        game.delete_object(last_object)
        last_object.ID = -1


def deletePreview(game: GameScreen) -> None:
    global last_form
    deletePreviewObject(game)
    deletePreviewForm()

    resetBinding(game) 


def createForm(game: GameScreen) -> None:
    global last_form

    deletePreviewForm()

    last_form = ObjectForm(game.getMaster())
    last_form.pack("left")


def showPreviewObject(e: tk.Event | None, game: GameScreen) -> None:
    global last_object
    global last_form
    deletePreviewObject(game)

    values: list[str] = last_form.get()

    mass = float(values[0])
    color = values[1]
    radius = float(values[2])
    velX = float(values[3])
    velY = float(values[4])
    coordX = float(values[5])
    coordY = float(values[6])

    scale: float = game.getScale()

    if (e is not None):
        last_object = game.create_object(mass, radius, color, [e.x * scale, e.y * scale])
        last_form.e6.setvar("coordX", str(e.x * scale))
        last_form.e7.setvar("coordY", str(e.y * scale))
    else:
        last_object = game.create_object(mass, radius, color, [coordX, coordY])

    last_object.velocity = [velX, velY]

    game.changeObject(last_object)


def setUpObjectFromId(game: GameScreen, ID: int) -> None:
    global last_form
    global last_object

    o = game.getObject(ID)
    last_form.mass.set(o.mass)
    last_form.color.set(o.color)
    last_form.radius.set(o.radius)
    last_form.velX.set(o.velocity[0])
    last_form.velY.set(o.velocity[1])
    last_form.coordX.set(o.center[0])
    last_form.coordY.set(o.center[1])


def copyObject(game: GameScreen) -> None:
    global last_object

    last_object.ID = -1


def previewObject(e: tk.Event, game: GameScreen) -> None:
    global last_object
    global last_form

    selected = game.getCanvas().find_overlapping(e.x, e.y, e.x, e.y)

    game.getMaster().bind("<Return>", lambda ee: showPreviewObject(None, game))
    game.getMaster().bind("<Alt_L>", lambda ee: createObject(game))
    game.getMaster().bind("c", lambda ee: copyObject(game))
    game.getCanvas().unbind("<Button-1>")
    game.getCanvas().bind("<Button-1>", lambda ee: showPreviewObject(ee, game))
    createForm(game)

    if (len(selected) != 0):
        # (objectX, current)
        tags = game.getCanvas().gettags(selected[0])
        if (tags[0][:6] != "object"): showPreviewObject(e, game)

        setUpObjectFromId(game, int(tags[0][6:]))
        last_object.ID = int(tags[0][6:])
    else:
        showPreviewObject(e, game)


def createObject(game: GameScreen) -> None:
    global last_object
    showPreviewObject(None, game)

    last_object.ID = -1

    deletePreviewForm()
    resetBinding(game)