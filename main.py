#Project Title: No Means No!
#Team Viper: Arhum(Programmer), Erin(Level Design/Website), Jessica(Sprite Design), Saheed(Information and Website)
#Python 3.6 using PyCharm IDE (https://www.jetbrains.com/pycharm/)
#Date created: 4/6/19
#Special thanks to my team and also Prof. Yan and Prof. Azhar for introducing me to the Hackathon and recommending me to apply.
#Thank you to the rest of the staff and community of BMCC for hosting and organizing this event!

from pygame_functions import *
import pygame

pygame.init() # always initialize
pygame.display.set_caption("No Means No!")  # create title for window TODO: Remove

screenSize(600, 600)
pygame.display.set_caption("No Means No!") # call after screenSize because func defines its own
setAutoUpdate(False) # we want frames to update on our own set time
BGM = makeMusic("elevator.mp3")
playMusic()

setBackgroundImage( [  ["images/room1.png", "images/room2.png"] ])
#setBackgroundImage("images/room1.png") why am i alive :(

#global variable we change throughout the code using changeLabel func
harass = makeLabel("*Smooch Smooch* Come here girl", 32, 40, 40, fontColour=(255, 0, 63), font='Arial', background='clear')


class Enemy(): # TODO: Redundant for now...will add new features I.E: move/interact/health

    def speech(self):
        if clock() > 0:
           harrass1 = makeLabel("*Smooch Smooch* Come here girl", 12, 40, 40, fontColour='black', font='Arial', background='clear')
           showLabel(harrass1)


class Player():
    def __init__(self):
        self.xpos = 300
        self.ypos = 300
        self.speed = 3 # probably the best otherwise use 1-2 for walking
        self.health = 100
        self.xdir = 0
        self.ydir = 0
        self.currentWeapon = 0 # TODO: remove soon we fight with words
        self.sprite = makeSprite("images/FemaleSprite.gif",32) # 32 = # of animations
        showSprite(self.sprite) # who me?
        self.frame = 0 # start frames at 0 because when we refresh it will reset frame count
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()

    def move(self):
        if clock() > self.timeOfNextFrame:  # animate our char every 80ms
            self.frame = (self.frame + 1) % 8  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop

        if keyPressed("left"):
           # self.xpos -= self.speed TODO: will remove soon because we side scroll differently now
            changeSpriteImage(self.sprite,  2*8+self.frame) # starts at set [2] * 8 frames. Set [0,1,2,3] Refer to map.
            scrollBackground(5, 0)  # Could possibly use in scripts/scenes ? O_O ?
            changeLabel(harass, "Go make me a sandwich!", fontColour=(255, 0, 93), background=None)
            #harass2 = makeLabel("Go make me a sandwich!", 22, 40, 40, fontColour='black', font='Arial', background='clear')
            #showLabel(harass2)
            self.xdir = -1
        elif keyPressed("right"):
          #  self.xpos += self.speed
            changeSpriteImage(self.sprite,  0*8+self.frame)
            changeLabel(harass, "*Smooch Smooch* Come here girl", fontColour=None, background=None)
            #harrass1 = makeLabel("*Smooch Smooch* Come here girl", 22, 40, 40, fontColour='black', font='Arial', background='clear')
            showLabel(harass)
            scrollBackground(-5, 0)
            self.xdir = 1
        else:
            self.xdir = 0

        if keyPressed("up"):
           # self.ypos -= self.speed
            changeSpriteImage(self.sprite, 3*8+self.frame)
            scrollBackground(0, 5)
            changeLabel(harass, "Can I touch your hair?", fontColour=None, background=None)
            #harass3 = makeLabel("Can i touch your hair?", 22, 40, 40, fontColour='black', font='Arial', background='clear')
            #showLabel(harass3)
            self.ydir = -1
        elif keyPressed("down"):
           # self.ypos += self.speed
            changeSpriteImage(self.sprite, 1*8+self.frame)
            scrollBackground(0, -5)
            changeLabel(harass, "Are you PMSing?", fontColour=None, background=None)
            #harass4 = makeLabel("Are you PMSing?", 22, 40, 40, fontColour='black', font='Arial', background='clear')
            #showLabel(harass4)
            self.ydir = 1
        else:
            self.ydir = 0

        moveSprite(self.sprite, self.xpos, self.ypos)

    def update(self):
        self.move()
        if keyPressed("space"):
            if clock() > self.lastBulletTime + 30:
                # add a new bullet to the list of bullets
                if self.xdir != 0 or self.ydir != 0:
                    bullets.append(Projectile(self.xpos + 20, self.ypos + 20, self.xdir * 10, self.ydir * 10, 0))
                    self.lastBulletTime = clock()


class Projectile():
    def __init__(self, xpos, ypos, xspeed, yspeed, damage):
        self.xpos = xpos
        self.ypos = ypos
        self.xspeed = xspeed
        self.yspeed = yspeed

        self.sprite = makeSprite("images/No.png")
        self.move()
        showSprite(self.sprite)

    def move(self):
        self.xpos += self.xspeed
        self.ypos += self.yspeed
        if self.xpos < 0 or self.xpos > 800 or self.ypos < 0 or self.ypos > 800: #out of boudns dont shoot
            return False
        moveSprite(self.sprite, self.xpos, self.ypos) # shoot using moveSprite TODO: implement bounding boxes(hitbox) so it damages and collision
        return True

p = Player()
bullets = []  # make an empty array of bullets
while True:
    p.update()

    # loop bullets
    for bullet in bullets:  # ask each bullet in the array to move
        if bullet.move() == False:

            hideSprite(bullet.sprite)
            bullets.remove(bullet) #must remove from list

    updateDisplay()#update drawings
    tick(60)# update tick