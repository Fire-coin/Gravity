from copy import deepcopy
from math import sqrt
import tkinter as tk

G: float = 6.6743e-11

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
        self.__master: tk.Tk = master
        self.__scale = scale
        self.__w = tk.Canvas(master, width= width, height= height, bg= bg)
        self.__w.pack()
        self.__objects: dict[str, Object] = {}
        self.__idCounter = 0
    

    def getCanvas(self) -> tk.Canvas:
        return self.__w

    def getMaster(self) -> tk.Tk:
        return self.__master

    
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
            deltaY = value.center[1] - o.center[1]

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