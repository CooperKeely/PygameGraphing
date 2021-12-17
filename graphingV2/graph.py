import pygame as pg
import numpy as np

class graph:
    def __init__(self, height : int, width : int, step : int):
        # screen data
        self.height = height
        self.width = width
        self.step = step
        
        # colors
        self.GREEN = (0,255,0)
        self.RED = (255,0,0)
        self.WHITE = (255,255,255)
        self.GRAY = (128,128,128)
        self.YELLOW = (255,255,0)
        self.BLACK= (0,0,0)
        self.function_thickness = 4
        self.axis_thickness = 3
        self.minor_grid_thickness = 2

        # graphing settings
        self.running = True
    
        # mouse movement
        self.prev_mouse_cords = []
        self.current_mouse_cords = []
        self.drag = False

        # function graphing settings
        self.center_x = width // 2
        self.center_y = height // 2
        self.functions = []
        self.plot = []

        # pygame
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
    
    def recenter(self, width, height):
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.screen = pg.display.set_mode((width, height), pg.RESIZABLE)

    def translate(self, dx, dy):
        self.center_x -= dx
        self.center_y -= dy

    def draw_grid(self):
        # vertical lines
        # left side of y axis  
        for i in range(self.center_x, 0, -self.step):
            pg.draw.line(self.screen,self.GRAY,(i, 0), (i, self.height), self.minor_grid_thickness)
        # right side of y axis
        for i in range(self.center_x, self.width, self.step):
            pg.draw.line(self.screen,self.GRAY,(i, 0), (i, self.height), self.minor_grid_thickness)
        
        # horizontal lines
        # upward side of x axis
        for j in range(self.center_y, 0,-self.step):
            pg.draw.line(self.screen,self.GRAY,(0, j), (self.width, j), self.minor_grid_thickness)
        # downward wide of y axis
        for j in range(self.center_y, self.height, self.step):
            pg.draw.line(self.screen,self.GRAY,(0, j), (self.width, j),self.minor_grid_thickness)
        
    def draw_axis(self):
        # y axis
        pg.draw.line(self.screen,self.GREEN,(self.center_x, 0), (self.center_x, self.height), self.axis_thickness)
        # x axis
        pg.draw.line(self.screen,self.RED,(0, self.center_y), (self.width, self.center_y), self.axis_thickness)

    def convert_points(self, p: list):
        return [int(p[0] * self.step) + self.center_x,  -1 * int(p[1] * self.step) + self.center_y]

    def add_function(self,func):
        self.functions.append(func)
        self.update_plot()
    
    def update_plot(self):
        #clear the previous plots
        self.plot.clear()

        for func in self.functions:
            # changing the bounds of the function to match the screen size
            range_a = -1 * (self.center_x) // self.step
            range_b = -1 * self.center_x // self.step + self.width // self.step + 1
            
            func.update(range_a, range_b)

            # create a new set of points to be drawn
            function_plot = []

            # convert each point into a screen coordinate
            for point in func.return_graph():
                function_plot.append(self.convert_points(point))
            
            # add the new set of points to the ones to be drawn
            self.plot.append(function_plot)
            
    def loop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.VIDEORESIZE:
                    self.recenter(event.w, event.h)
                elif event.type == pg.MOUSEBUTTONUP:
                    self.drag = False
                elif event.type == pg.MOUSEBUTTONDOWN :
                    self.drag = True
                    self.prev_mouse_cords = pg.mouse.get_pos()
                elif self.drag and event.type == pg.MOUSEMOTION:
                    self.current_mouse_cords = pg.mouse.get_pos()
                    dx = self.prev_mouse_cords[0] - self.current_mouse_cords[0]
                    dy = self.prev_mouse_cords[1] - self.current_mouse_cords[1]
                    self.prev_mouse_cords = self.current_mouse_cords
                    self.translate(dx, dy)

                

            self.update_plot()
            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_axis()
            
            # draw plots
            for point in self.plot:
                pg.draw.lines(self.screen, self.BLACK, False, point, self.function_thickness)
            
            pg.display.update()
            self.clock.tick(60)
    
