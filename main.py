from pygame import *
from time import time as timer
from random import randint

mixer.init()

hit = mixer.Sound("pong.mp3")
death = mixer.Sound("Звучание старой игры.mp3")
damage = mixer.Sound("ВЬП.mp3")

window = display.set_mode((1000,700))
display.set_caption("WIWIWI")

plrsprite = transform.scale(image.load("ищщые.jpg"),(50,50))
enemysprite = transform.scale(image.load("мячик.jpg"),(50,50))
bg = transform.scale(image.load("фон.jpg"),(1000,700))
bulsprite = transform.scale(image.load("мячик.jpg"),(15,15))

stages = {
    1: {
        "Basic" : 1
    },
    2: {
        "Basic" : 2
    },
    3: {
        "Basic" : 2
    },
    4: {
        "Basic" : 3
    },
    5: {
        "Basic" : 3
    }
}

class GameSprite(sprite.Sprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__()
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
        self.lastShootTime = timer()
    def move(self):
        krey = key.get_pressed()
        if krey[K_w] and self.rect.y > 15:
            self.rect.y -= self.speed
        elif krey[K_s] and self.rect.y < 700 - 50:
            self.rect.y += self.speed
        if krey[K_a] and self.rect.x > 15:
            self.rect.x -= self.speed
        elif krey[K_d] and self.rect.x < 1000 - 50:
            self.rect.x += self.speed
        if timer() - self.lastShootTime > 0.5:
            if krey[K_LEFT]:
                self.shoot("Left") 
            elif krey[K_UP]:
                self.shoot("Up")
            elif krey[K_RIGHT]:
                self.shoot("Right")
            elif krey[K_DOWN]:
                self.shoot("Down")
    def shoot(self,direction):
        self.lastShootTime = timer()
        bullet = Bullet(bulsprite,bleh.rect.x,bleh.rect.y,5,direction)
        bullets.add(bullet)
        hit.play()
        

bullets = sprite.Group()

class Bullet(GameSprite):
    def __init__(self,image,x,y,speed,direction):
        super().__init__(image,x,y,speed)
        self.direction = direction
    def update(self):
        if self.direction == "Up":
            self.rect.y -= self.speed
        elif self.direction == "Down":
            self.rect.y += self.speed
        elif self.direction == "Left":
            self.rect.x -= self.speed
        elif self.direction == "Right":
            self.rect.x += self.speed

class Enemy(GameSprite):
    def __init__(self,sprite,x,y,speed):
        super().__init__(sprite,x,y,speed)
        self.XDir = "Left"
        self.YDir = "Up"
        self.hp = 100
    def update(self):
        global bleh
        if bleh.rect.x > self.rect.x:
            self.XDir = "Left"
        elif bleh.rect.x < self.rect.x:
            self.XDir = "Right"
        if bleh.rect.y > self.rect.y:
            self.YDir = "Down"
        elif bleh.rect.y < self.rect.y:
            self.YDir = "Up"
        if self.YDir == "Up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if self.XDir == "Left":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed


bleh = Player(plrsprite,500,350,5)
enemis = sprite.Group()


stage = 1
curstage = stage
monsterHP = 100

clock = time.Clock()
FPS = 60
game = True
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
    if stage != 0:
        for i in range(stages[stage]["Basic"]):
            enemyi = Enemy(enemysprite,randint(0,700),0,2)
            enemis.add(enemyi)
        stage = 0
    window.blit(bg,(0,0))
    enemis.draw(window)
    enemis.update()
    bleh.reset()
    bleh.move()
    bullets.draw(window)
    bullets.update()
    display.update()
    clock.tick(FPS)
    enemy_bullets = sprite.groupcollide(enemis, bullets,False,True)
    for i in enemy_bullets:
        i.hp -= 10
        damage.play()
        if i.hp <= 0:
            i.kill()
            death.play()
    if len(enemis) <= 0:
        curstage += 1
        stage = curstage
    if sprite.spritecollide(bleh,enemis,False):
        game = False