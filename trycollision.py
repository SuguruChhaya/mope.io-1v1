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
    FPS = 60
    #FIRE = pygame.transform.scale(pygame.image.load('images/fire.png'), (300, 200))
    def __init__(self):

        self.run = True
        self.clock = pygame.time.Clock()
        self.GREEN_IMAGE = pygame.transform.scale(pygame.image.load('images/green_top.png'), (300, 200))
        self.GREEN_IMAGE.set_colorkey((255,255,255))
        self.GREY_IMAGE = pygame.transform.scale(pygame.image.load('images/grey_full.png'), (300, 200))
        self.GREY_IMAGE.set_colorkey((255,255,255))
        self.RED_IMAGE = pygame.transform.scale(pygame.image.load('images/red_bottom.png'), (300, 200))
        self.RED_IMAGE.set_colorkey((255,255,255))
        self.GREEN_IMAGE_COPY = self.GREEN_IMAGE.copy()
        self.GREEN_IMAGE_COPY.set_colorkey((255,255,255))
        self.GREY_IMAGE_COPY = self.GREY_IMAGE.copy()
        self.GREY_IMAGE_COPY.set_colorkey((255,255,255))
        self.RED_IMAGE_COPY = self.RED_IMAGE.copy()
        self.RED_IMAGE_COPY.set_colorkey((255,255,255))
        self.BIGFOOT = pygame.transform.scale(pygame.image.load('images/adjusted_bigfoot.png'), (300, 200))
        self.BIGFOOT.set_colorkey((255, 255, 255))
        self.TREX = pygame.transform.scale(pygame.image.load('images/adjusted_trex.png'), (300, 200))
        self.TREX.set_colorkey((255,255, 255))
        #*The self.player_list will contain nested lists of three triangles in the orger of green, grey, and red
        
        self.RING_IMAGE = pygame.transform.scale(pygame.image.load('images/circle.png'), (800, 800))
        
        self.player_list = []

    def redraw(self):
        #!I have to clean up the dust created by rotating the images a lot. 
        MainGame.window.fill((0, 0, 0))
        #?The order of this will change once I make a client side.
        self.ring.draw()
        self.bot.draw()
        self.player.move()
        if self.player.collision(self.bot):
            pass
        self.player.draw()

        

        
        pygame.display.update()

    def game_display(self):
        self.clock.tick(MainGame.FPS)
    
        self.player = Player(400, 400, [self.GREEN_IMAGE, self.GREY_IMAGE, self.RED_IMAGE, self.BIGFOOT])
        self.player_list.append(self.player)
        #!Making copy so that images don't have 2 masks
        self.bot = Bot(400, 400, [self.GREEN_IMAGE_COPY, self.GREY_IMAGE_COPY, self.RED_IMAGE_COPY, self.TREX])
        self.player_list.append(self.bot)

        self.ring = Ring(self.RING_IMAGE)
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
        self.animal = images[3]
        #!I need this to bring it back to the original
        self.original_green = images[0]
        self.original_grey = images[1]
        self.original_red = images[2]
        self.original_animal = images[3]
    
        self.green_mask = pygame.mask.from_surface(self.green_diamond)
        self.red_mask = pygame.mask.from_surface(self.red_diamond)
        #!To prevent stand still glitch in the move method
        self.ban_degree = 999999

        #*3 seconds to cool down
        self.max_cool_down = MainGame.FPS * 3
        self.cool_down = MainGame.FPS * 3
        #*To check whether player has bitten a tail
    
    
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
        
        
        MainGame.window.blit(self.grey_diamond, (self.x - self.grey_diamond.get_width() / 2, self.y - self.grey_diamond.get_height() / 2))
        MainGame.window.blit(self.green_diamond, (self.x - self.green_diamond.get_width() / 2, self.y - self.green_diamond.get_height() / 2))
        MainGame.window.blit(self.red_diamond, (self.x - self.red_diamond.get_width() / 2, self.y - self.red_diamond.get_height() / 2))
        MainGame.window.blit(self.animal, (self.x - self.red_diamond.get_width() / 2, self.y - self.red_diamond.get_height() / 2))

        #*Play gif if animal touched wall
        #MainGame.window.blit(MainGame.FIRE, (self.x - self.red_diamond.get_width() / 2, self.y - self.red_diamond.get_height() / 2))

    
        pass

    def move(self):
        #!I need to first return to the original green image
        self.green_diamond = self.original_green
        self.red_diamond = self.original_red
        self.grey_diamond = self.original_grey
        self.animal = self.original_animal
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        #!Since I am blitting based on the center, self.center_x can just be the x and the y

        self.x_difference = self.mouse_x - self.x
        #!Because of the pygame gridding system, I have to *-1 the y_difference. (Has to be positive when cursor is above the object)
        self.y_difference = -(self.mouse_y - self.y)
        #*Find the degree and times *-1 it. 
        #*I can find it by using the arctan from the math module
        #*Have to convert to degree
        #!Have to error check undefined tan
        '''
        1. I will arctan and multiply by 180/pi to convert to degrees. 
        3. Then I check whether self.y_difference was negative and whether self.x_difference was negative. Based on that, I will find its true degree measure. 
        4. Then I will convert to pygame rotation by -(90 -self.degree)
        '''
        self.Q1 = False
        self.Q2 = False
        self.Q3 = False
        self.Q4 = False
        self.zero = False
        self.ninty = False
        self.one_eighty = False
        self.two_seventy = False
        self.origin = False
        

        try:
            self.degree = math.atan(self.y_difference / self.x_difference) 
        except ZeroDivisionError:
            pass

        #!I need to fix the bug of the animal consistently glitching back and forth of the mouse. 
        if self.x_difference < 0:
            if self.y_difference < 0:
                self.Q3 = True
                self.degree = 180 + (self.degree * 180 / math.pi)
                #*Into pygame
                self.degree -= 90
                #!I have to ban the self.degree - 180 option from the next move
                #*This prevents glitching between Q1 and Q3, Q2 and Q4

                #print(f'Q1 ban degree: {self.ban_degree}')
                #print(f'Q1 degree: {self.degree}')
                if int(self.degree) == int(self.ban_degree):
                    #self.degree = 0
                    pass
                self.ban_degree = self.degree + 180




            elif self.y_difference > 0:
                self.Q2 = True
                #!Since the self.degree * 180 / math.pi part is negative, this is correct
                self.degree = 180 + (self.degree * 180 / math.pi)
                self.degree -= 90

            elif self.y_difference == 0:
                self.one_eighty = True
                self.degree = 180
                #*Into pygame
                self.degree -= 90

        elif self.x_difference > 0:

            if self.y_difference < 0:
                
                self.Q4 = True
                self.degree = 360 + (self.degree * 180 / math.pi)
                self.degree -= 90
                
            elif self.y_difference > 0:
                self.Q1 = True
                self.degree = 360 + self.degree * 180 / math.pi
                self.degree -= 90
                #print(f'Q3 ban degree: {self.ban_degree}')
                #print(f'Q3 degree: {self.degree}')
                if int(self.degree) == int(self.ban_degree):
                    #print('True')
                    pass
                self.ban_degree = self.degree - 180

            elif self.y_difference == 0:
                self.zero = True
                self.degree = 0
                #*Into pygame
                self.degree -= 90

        elif self.x_difference == 0:
            if self.y_difference < 0:
                self.two_seventy = True
                self.degree = 270
                #*Into pygame
                self.degree -= 90
            elif self.y_difference > 0:
                self.ninty = True
                self.degree = 90
                #*Into pygame
                self.degree -= 90

            elif self.y_difference == 0:
                self.origin = True


        try:
            self.green_diamond = pygame.transform.rotate(self.green_diamond, self.degree)
            self.grey_diamond = pygame.transform.rotate(self.grey_diamond, self.degree)
            self.red_diamond = pygame.transform.rotate(self.red_diamond, self.degree)
            self.animal = pygame.transform.rotate(self.animal, self.degree)
            #!I might want to redo the mask here
            self.green_mask = pygame.mask.from_surface(self.green_diamond)
            self.red_mask = pygame.mask.from_surface(self.red_diamond)
    #*Handles the case when the image becomes too large
        except Exception:
            pass

        #*Actually moving the shapes
        '''
        1. I am going to use the Pythagorean Theorem to calculate the actual distance between my mouse and the diamond. 
        2. Compare lengths with a similar triangle with the hypotenuse of 1. 
        '''
        #?Not moving down
        #?I have a weird shaking bug when computer is on the middle. 
        self.distance = math.sqrt(self.x_difference ** 2 + self.y_difference ** 2)
        self.speed = 0.3
        self.x += self.x_difference * (self.speed / self.distance)
        #!Remember that the y_difference was put as negative!!
        self.y += -self.y_difference * (self.speed / self.distance)


    def collision(self, obj2):
        #?Instead of using masks, I could use color detection 
        #!The offset_x must be at left corner, but currently, it is at middle!!
        #!offset must be calculated by the top left coordinates!! Careful on where it is blitted!!
        offset_x = (obj2.x - obj2.green_diamond.get_width() / 2) - (self.x - self.green_diamond.get_width() / 2)
        offset_y = (obj2.y - obj2.green_diamond.get_height() / 2)  - (self.y - self.green_diamond.get_height() / 2)
        #? The problem might be that there are 2 masks for the same image object

        #?Now it isn't showing overlap at the same time
        return self.green_mask.overlap(obj2.red_mask, (int(offset_x), int(offset_y))) != None
    


class Bot(Player):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        

    def move(self):
        pass


#*Just to re-test the issue, I am going to create a second bot
#!I am going to use color collision for the second one. 
#https://www.youtube.com/watch?v=JW_H7o-MmtI

class Bot2():
    def __init__(self, images):
        pass

class Ring():
    def __init__(self, image):
        self.image = image
        self.scale_x = 200
        self.scale_y = 200
        #At first, placed at full screen
        self.x = 0
        self.y = 0
        pass
        
    def shrink(self):
        #*This method is going to shrink the image based on how much time has passed. 
        self.image = pygame.transform.scale(self.image, (self.scale_x, self.scale_y))

    def draw(self):
        MainGame.window.blit(self.image, (self.x, self.y))


game = MainGame()
game.game_display()