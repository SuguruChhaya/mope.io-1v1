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
import math

class MainGame():
    window = pygame.display.set_mode((800, 800))
    
    def __init__(self):
        self.FPS = 60
        self.run = True
        self.clock = pygame.time.Clock()
        self.GREEN_IMAGE = pygame.transform.scale(pygame.image.load('images/green_diamond.png'), (300, 200))
        self.GREEN_IMAGE.set_colorkey((255,255,255))
        self.GREY_IMAGE = pygame.transform.scale(pygame.image.load('images/grey_diamond.png'), (300, 200))
        self.GREY_IMAGE.set_colorkey((255,255,255))
        self.RED_IMAGE = pygame.transform.scale(pygame.image.load('images/red_diamond.png'), (300, 200))
        self.RED_IMAGE.set_colorkey((255,255,255))
        #*The self.player_list will contain nested lists of three triangles in the orger of green, grey, and red
        self.player_list = []

    def redraw(self):
        self.player.move()
        self.player.draw()

        pygame.display.update()

    def game_display(self):
        self.clock.tick(self.FPS)
        self.player = Player(400, 400, [self.GREEN_IMAGE, self.GREY_IMAGE, self.RED_IMAGE])
        self.player_list.append(self.player)
        '''
        self.bot = Bot(400, 400, [self.GREEN_IMAGE, self.GREY_IMAGE, self.RED_IMAGE])
        self.player_list.append(self.bot)
        '''
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            self.redraw()

class Player():
    #*I would rather manage all the triangles as a class variable rather than managing it in the main game. 
    #*I will make an enemy list in the future

    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.green_diamond = images[0]
        self.grey_diamond = images[1]
        self.red_diamond = images[2]
        self.green_mask = pygame.mask.from_surface(self.green_diamond)
        self.red_mask = pygame.mask.from_surface(self.red_diamond)
        
    
    def draw(self):
        #*I can adjust this based on the self.x and self.y variables. I have to make sure they can check for collisions tho
        '''
        self.grey_x = self.green_x + (self.green_triangle.get_width() - self.grey_triangle.get_width()) / 2
        self.grey_y = self.green_y + self.green_triangle.get_height() - self.grey_triangle.get_height()
        self.red_x = self.green_x + (self.green_triangle.get_width() - self.red_triangle.get_width()) / 2
        self.red_y = self.green_y + self.green_triangle.get_height() - self.red_triangle.get_height()
        '''
        '''
        print(self.diamond_list)
        for diamond in self.diamond_list:
            MainGame.window.blit(diamond, (self.x - diamond.get_width() / 2, self.y - diamond.get_height() / 2))
        '''
        
        MainGame.window.blit(self.green_diamond, (self.x - self.green_diamond.get_width() / 2, self.y - self.green_diamond.get_height() / 2))
        '''
        MainGame.window.blit(self.grey_diamond, (self.x, self.y))
        MainGame.window.blit(self.red_diamond, (self.x, self.y))
        '''

    def move(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.center_x = self.x + self.green_diamond.get_width() / 2
        self.center_y = self.y + self.green_diamond.get_height() / 2
        self.x_difference = self.mouse_x - self.center_x
        #!Because of the pygame gridding system, I have to *-1 the y_difference. (Has to be positive when cursor is above the object)
        self.y_difference = -(self.mouse_y - self.center_y)
        #*Find the degree and times *-1 it. 
        #*I can find it by using the arctan from the math module
        #*Have to convert to degree
        #!Have to error check undefined tan
        '''
        1. I will arctan and multiply by 180/pi to convert to degrees. 
        3. Then I check whether self.y_difference was negative and whether self.x_difference was negative. Based on that, I will find its true degree measure. 
        4. Then I will convert to pygame rotation by -(90 -self.degree)
        '''
        try:
            print(f'self.x_distance: {self.x_difference}')
            print(f'self.y_distance: {self.y_difference}')
            self.degree = math.atan2(self.y_difference , self.x_difference) * 180 / math.pi
            print(f'first atan: {self.degree}')
            if self.x_difference < 0:
                if self.y_difference < 0:
                    #Q3
                    self.degree = 180 + self.degree
                else:
                    #Q2
                    self.degree = 180 - self.degree
            else:
                
                if self.y_difference < 0:
                    #Q4
                    self.degree = 360 - self.degree
                else:
                    #Q1
                    pass
        except ZeroDivisionError:
            if self.y_difference < 0:
                self.degree = 270
            else:
                self.degree = 90

        #*Convert to pygame rotation
        print(f'before pygame conversion: {self.degree}')
        self.degree = -(90 - self.degree)

        try:
            print(f'final degree: {self.degree}')
            self.green_diamond = pygame.transform.rotate(self.diamond_list[0], self.degree)
        #*Handles the case when the image becomes too large
        except Exception:
            pass

class Bot(Player):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

    def move(self):
        pass
        



game = MainGame()
game.game_display()