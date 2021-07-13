import random
import pygame 


class lorenz:
    def __init__(self):
        self.xMin, self.xMax = -30, 30
        self.yMin, self.yMax = -30, 30
        self.zMin, self.zMax = 0, 60
        self.X, self.Y, self.Z = 0.1, 0.0, 0.0 # Initial values.
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.dt = 0.0001 # Time step.
        self.a, self.b, self.c = 10, 28, 8/3 # Parameters 
        self.pixelcolour = (255, 0, 0)
    
    # Formular of the attractor.
    """
        dx / dt = a(y - x)     (1)
        dy / dt = x(b - z) - y (2)
        dz / dt = xy - by      (3)
    """
    def step(self):
        # Increment x,y,z et multiplier dt.
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * self.a * (self.Y - self.X))
        self.Y = self.Y + (self.dt * (self.X * (self.b - self.Z) - self.Y))
        self.Z = self.Z + (self.dt * (self.X * self.Y - self.c * self.Z))

    # Convert The normal coordinates into screen coordinates
    # Using The ConvertToScreen Function 
    def draw(self, displaysuface):
        width, height = displaysuface.get_size()
        oldPos = self.ConvertToScreen(self.oX, self.oY, self.xMin, self.xMax, self.yMin, self.yMax, width, height)
        newPos = self.ConvertToScreen(self.X, self.Y, self.xMin, self.xMax, self.yMin, self.yMax, width, height)

        # Draw The current line segment. 
        newRect = pygame.draw.line(displaysuface, self.pixelcolour, oldPos, newPos, 2)
        
        # Return The bounding rectangle.
        return newRect
    def ConvertToScreen(self, x, y, xMin, xMax, yMin, yMax, width, height):
        newX = width * ((x - xMin) / (xMax - xMin))
        newY = height * ((y - yMin) / (yMax - yMin))
        return round(newX), round(newY)


class Application:
    def __init__(self):
        # Difine and setup variables for The attractor 
        self.isRunning = True
        self.displaySurface = None
        self.fpsClock = None
        self.attractors = []
        self.size = self.width, self.hieght = 1920, 1080
        self.count = 0 
        self.outputCount = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Lorenz Attractor")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.isRunning = True
        self.fpsClock = pygame.time.Clock()

        # Configure the attractor.
        colour = []
        colour.append((51, 128, 204))
        colour.append((255, 128, 0))
        colour.append((255, 191, 0))
        for i in range(0, 3):
            self.attractors.append(lorenz())

            self.attractors[i].X = random.uniform(0.1, 0.101)

            self.attractors[i].pixelcolour = colour[i]

    def on_envent(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        # Call The step method for the attractor
        for x in self.attractors:
            x.step()

    def on_render(self):
        # Draw the attractor / display the attractor 
        for x in self.attractors:
            newRect = x.draw(self.displaySurface)
            pygame.display.update(newRect)

    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False
        # Main Loop 
        while self.isRunning:
            for event in pygame.event.get():
                self.on_envent(event)

            self.on_loop()
            self.on_render()

            self.fpsClock.tick()
            self.count += 1

        pygame.quit()

if __name__ == "__main__":
    t = Application()
    t.on_execute()



