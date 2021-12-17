import numpy as np
from pygame.sndarray import array
import math


class function:
    def __init__(self,func):
        self.func = func
        self.update(-10, 10)
    
    def update(self, a, b):
        self.a = a
        self.b = b
        self.range = np.abs(self.a) + np.abs(self.b)
        self.steps = self.range * 200
        self.dx = self.range / self.steps

        self.points = []
        self.make_graph()
    
    def make_graph(self):
        for i in range(0 , self.steps + 1):
            x = self.a + (i * self.dx)
            y = self.func(x)
            if math.isnan(y) or math.isinf(y):
                continue
            self.points.append([x,self.func(x)])
    
    def return_graph(self):
        return self.points
        


