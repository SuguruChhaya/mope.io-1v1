'''
This is the main file of this project.
I will eventually make an online version of this game, but I will make it 1 player for now. 
Since I can only make 1 now, I will make one player with the mouse and 1 bot to play with. 
I will make a triangle object with 3 polygons on each other. 

For the graphics, I have 2 options. 
1. Use the default pygame draw method. 
2. Use the turtle module and blit it somehow.
'''


import pygame
pygame.init()

class MainGame():
    window = pygame.display.set_mode((800, 800))
    
    def __init__(self):
        self.FPS = 60
        self.run = True
        self.clock = pygame.time.Clock()
        self.GREEN_IMAGE = pygame.transform.scale(pygame.image.load('images/green_triangle.png'), (200, 200))
        self.GREEN_IMAGE.set_colorkey((255,255,255))
        self.GREY_IMAGE = pygame.transform.scale(pygame.image.load('images/grey_triangle.png'), (200, 200))
        self.GREY_IMAGE.set_colorkey((255,255,255))
        self.RED_IMAGE = pygame.transform.scale(pygame.image.load('images/red_triangle.png'), (200, 200))
        self.RED_IMAGE.set_colorkey((255,255,255))
        #*The self.player_list will contain nested lists of three triangles in the orger of green, grey, and red
        self.player_list = []

    def redraw(self):
        for player in self.player_list:
            for triangle in player:
                triangle.draw()
        pygame.display.update()

    def game_display(self):
        self.clock.tick(self.FPS)
        self.green_triangle = Triangles(4, 5, self.GREEN_IMAGE)
        self.grey_triangle = Triangles(4,5,self.GREY_IMAGE)
        self.red_triangle = Triangles(4, 5, self.RED_IMAGE)
        self.player_list.append([self.green_triangle, self.grey_triangle, self.red_triangle])
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            self.redraw()

class Triangles():
    #*I would rather manage all the triangles as a class variable rather than managing it in the main game. 
    #*I will make an enemy list in the future

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        
    
    def draw(self):
        #*I can adjust this based on the self.x and self.y variables. I have to make sure they can check for collisions tho
        MainGame.window.blit(self.image, (self.x, self.y))


game = MainGame()
game.game_display()