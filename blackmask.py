'''
In this file, I am going to try to use a black circle to try the mask idea. 
'''
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
    WIDTH = 800
    HEIGHT = 800
    window = pygame.display.set_mode((WIDTH, HEIGHT))
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
        
        self.RING_IMAGE = pygame.transform.scale(pygame.image.load('images/black_circle.png'), (800, 800))
        #self.RING_IMAGE.set_colorkey((0, 0, 0))

        self.FIRE_IMAGE = pygame.transform.scale(pygame.image.load('images/fire.png'), (300, 200))
        self.FIRE_IMAGE.set_colorkey((0, 0, 0))
        self.FIRE_IMAGE_COPY = self.FIRE_IMAGE.copy()
        self.FIRE_IMAGE_COPY.set_colorkey((0, 0, 0))

        self.player_list = []

    def redraw(self):
        #!I have to clean up the dust created by rotating the images a lot. 
        MainGame.window.fill((255, 0, 0))
        #?The order of this will change once I make a client side.
        #pygame.draw.circle(MainGame.window, (0, 0, 0), (400, 400), 400)
        self.ring.shrink()
        self.ring.draw()
        self.bot.draw()
        self.player.move()
        
        if self.player.collision(self.bot):
            print('bite')


        

        
        self.player.draw()

        #!Has to be after self.player.draw because fire must show on top of player
        if self.ring.collision(self.player):
            #*I need to make a health losing counter
            self.player.health -= 3
            self.player.draw_fire()

        if self.player.health < 0:
            #*Have to import font and all that. 
            pass

        
        pygame.display.update()



    def game_display(self):
        self.clock.tick(MainGame.FPS)
    
        self.player = Player(400, 400, [self.GREEN_IMAGE, self.GREY_IMAGE, self.RED_IMAGE, self.BIGFOOT, self.FIRE_IMAGE])
        self.player_list.append(self.player)
        #!Making copy so that images don't have 2 masks
        self.bot = Bot(400, 400, [self.GREEN_IMAGE_COPY, self.GREY_IMAGE_COPY, self.RED_IMAGE_COPY, self.TREX, self.FIRE_IMAGE_COPY])
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
        self.fire = images[4]
        #!I need this to bring it back to the original
        self.original_green = images[0]
        self.original_grey = images[1]
        self.original_red = images[2]
        self.original_animal = images[3]
    
        self.green_mask = pygame.mask.from_surface(self.green_diamond)
        self.red_mask = pygame.mask.from_surface(self.red_diamond)
        #*I need to create a mask for the grey diamond too to check for wall collisions. 
        self.grey_mask = pygame.mask.from_surface(self.grey_diamond)

        #!To prevent stand still glitch in the move method
        self.ban_degree = 999999
        self.previous_degree = None

        #*Health bar
        self.max_health = 100
        self.health = 100

        #*Fire related variables
        
        self.fire_cool = MainGame.FPS * 1

        #*3 seconds to cool down
        #self.max_cool_down = MainGame.FPS * 3
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

        #*Health bar
        #Red bar
        rect_width = 50
        rect_height = 5
        red_location = (self.x - 25, self.y - self.original_grey.get_height() / 2 - rect_height - 10, rect_width, rect_height)
        pygame.draw.rect(MainGame.window, (255, 0, 0), red_location)

        #Green bar
        rect_width = rect_width * self.health / self.max_health
        green_location = (self.x - 25, self.y - self.original_grey.get_height() / 2 - rect_height - 10, rect_width, rect_height)
        pygame.draw.rect(MainGame.window, (0, 255, 0), green_location)

    def draw_fire(self):
        if self.fire_cool > 0:
            MainGame.window.blit(self.fire, (self.x - self.grey_diamond.get_width() / 2, self.y - self.grey_diamond.get_height() / 2))
            self.fire_cool -= 1
        else:
            self.fire_cool = MainGame.FPS * 1

    def move(self):
        #!To prevent the moving glitch, I will store the previous degree measure as self.previous_degree. 
        #*This way, if the degree is equal to ban degree, I can make degree equal the self.previous_degree


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

                self.check_ban(180)


            elif self.y_difference > 0:
                self.Q2 = True
                #!Since the self.degree * 180 / math.pi part is negative, this is correct
                self.degree = 180 + (self.degree * 180 / math.pi)
                self.degree -= 90

                self.check_ban(180)

            elif self.y_difference == 0:
                self.one_eighty = True
                self.degree = 180
                #*Into pygame
                self.degree -= 90

                self.check_ban(180)

        elif self.x_difference > 0:

            if self.y_difference < 0:
                
                self.Q4 = True
                self.degree = 360 + (self.degree * 180 / math.pi)
                self.degree -= 90

                self.check_ban(-180)
                
            elif self.y_difference > 0:
                self.Q1 = True
                self.degree = 360 + self.degree * 180 / math.pi
                self.degree -= 90
                #print(f'Q3 ban degree: {self.ban_degree}')
                #print(f'Q3 degree: {self.degree}')
                self.check_ban(-180)

            elif self.y_difference == 0:
                self.zero = True
                self.degree = 0
                #*Into pygame
                self.degree = 270
                self.check_ban(-180)
            

        elif self.x_difference == 0:
            if self.y_difference < 0:
                self.two_seventy = True
                self.degree = 270
                #*Into pygame
                self.degree -= 90

                self.check_ban(-180)

            elif self.y_difference > 0:
                self.ninty = True
                self.degree = 90
                #*Into pygame
                self.degree -= 90

                self.check_ban(180)

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
            self.grey_mask = pygame.mask.from_surface(self.grey_diamond)
            self.previous_degree = self.degree
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
        self.speed = 1
        self.x += self.x_difference * (self.speed / self.distance)
        #!Remember that the y_difference was put as negative!!
        self.y += -self.y_difference * (self.speed / self.distance)

    def check_ban(self, plus_minus):
        #!converting to int to so that small differences don't count
        if int(self.degree) == int(self.ban_degree):
            self.degree = self.previous_degree
        
        #*self.previous degree cannot be none
        self.ban_degree = self.degree + plus_minus


    def collision(self, obj):
        #?Instead of using masks, I could use color detection 
        #!The offset_x must be at left corner, but currently, it is at middle!!
        #!offset must be calculated by the top left coordinates!! Careful on where it is blitted!!
        offset_x = (obj.x - obj.green_diamond.get_width() / 2) - (self.x - self.green_diamond.get_width() / 2)
        offset_y = (obj.y - obj.green_diamond.get_height() / 2)  - (self.y - self.green_diamond.get_height() / 2)
        #? The problem might be that there are 2 masks for the same image object

        #?Now it isn't showing overlap at the same time
        return self.green_mask.overlap(obj.red_mask, (int(offset_x), int(offset_y))) != None
    


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
        self.scale_x = 800
        self.scale_y = 800
        #At first, placed at full screen

        #self.mask = pygame.mask.from_threshold(self.image, (255, 0, 0))
        
        
        
    def shrink(self):
        #*This method is going to shrink the image based on how much time has passed. 
        #?In terms of rings, I think it is good to have a center measure and subtract the radius from it. 
        #*This is because the center will always be the center and I don't have to do many complex calculations.
        self.image = pygame.transform.scale(self.image, (self.scale_x, self.scale_y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        #*This way, all I have to adjust is the scaling
        MainGame.window.blit(self.image, (MainGame.WIDTH / 2 - self.image.get_width() / 2, MainGame.HEIGHT / 2 - self.image.get_height() / 2))
        

    def collision(self, obj):

        #*For collision, I could slap a black image in the middle and create a mask.
        #*I could use the mask.overlap.area method to check if any of the body went outside of the black circle. 

        
        
        '''
        #!Rather than using a mask, I am going to check whether the color of the coordinates
        #!Remember where the actual coordinates were!!

        #*Storing in a list just so I can change values when the points don't exist on the screen. 
        topleft = [int(obj.x - obj.grey_diamond.get_width() / 2) + 80, int(obj.y - obj.grey_diamond.get_height() / 2)]
        topright = [int(obj.x + obj.grey_diamond.get_width() / 2), int(obj.y - obj.grey_diamond.get_height() / 2)] 
        bottom_left = [int(obj.x - obj.grey_diamond.get_width() / 2) + 80, int(obj.y + obj.grey_diamond.get_height() / 2)]
        bottom_right = [int(obj.x + obj.grey_diamond.get_width() / 2), int(obj.y + obj.grey_diamond.get_height() / 2)]

        #!Have to prevent getting the attribute of a non-existing point
        if topleft[0] < 0:
            topleft[0] = 0
            bottom_left[0] = 0
        if topleft[1] < 0:
            topleft[1] = 0
            topright[1] = 0
        if bottom_right[0] >= MainGame.WIDTH:
            bottom_right[0] = MainGame.WIDTH - 1
            topright[0] = MainGame.WIDTH - 1
        if bottom_right[1] >= MainGame.HEIGHT:
            bottom_right[1] = MainGame.HEIGHT - 1 
            bottom_left[1] = MainGame.HEIGHT - 1
        
        #!Cannot be 800 must be smaller
        #*can be 0


        return (255, 0, 0, 255) in [MainGame.window.get_at(topleft), MainGame.window.get_at(topright), MainGame.window.get_at(bottom_left), MainGame.window.get_at(bottom_right)]
        '''

        

        
        blit_x = MainGame.WIDTH / 2 - self.image.get_width() / 2
        blit_y = MainGame.HEIGHT / 2 - self.image.get_height() / 2
        #*We know that obj is going to be the player or the bot
        offset_x = (obj.x - obj.grey_diamond.get_width() / 2) - blit_x
        offset_y = (obj.y - obj.grey_diamond.get_height() / 2) - blit_y
        
        return self.mask.overlap_area(obj.grey_mask, (int(offset_x), int(offset_y))) < 11800
        






game = MainGame()
game.game_display()
