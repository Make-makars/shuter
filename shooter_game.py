from pygame import *
from random import randint

font.init()

wind = display.set_mode((800, 800))
display.set_caption("aaaaaaa")
bacG = transform.scale(image.load("galaxy.jpg"), (800, 800))
FS = 40
Kn = 0
Dn = 0
firer = 0
fps = 1
hp = 10

font = font.SysFont("Arial", FS)
win = font.render("you win", True, (0, 255, 0))
lose = font.render("you lose", True, (255, 0, 0))
kills = font.render("попаданий - " + str(Kn), True, (255,255,255))
death = font.render("пропущенно - "+ str(Dn), True, (255,255,255))

class GSprite(sprite.Sprite):
    def __init__(self, pla_image, pla_x, pla_y, zmih_x, zmih_y, pla_speed, three):
        super().__init__()
        self.zmih_x = zmih_x
        self.zmih_y = zmih_y
        self.image = transform.scale(image.load(pla_image), (self.zmih_x, self.zmih_y))
        self.speed = pla_speed
        self.rect = self.image.get_rect()
        self.rect.x = pla_x
        self.rect.y = pla_y
        self.three = three
    def SH(self):
        wind.blit(self.image, (self.rect.x, self.rect.y))

monsters = sprite.Group()
bullets = sprite.Group()
bosss = sprite.Group()
scraps = sprite.Group()

class Monster(GSprite):
    def update(self):
        global Dn
        self.rect.y += self.speed
        if self.rect.y >= 800:
            self.rect.y = -10
            self.rect.x = randint(0,730)
            Dn += self.three

class scrap(GSprite):
    def wew(self):
        if self.three == 0:
            self.rect.x += 3
        if self.three == 1:
            self.rect.x -= 4
        if self.three == 2:
            self.rect.y -= 3
        if self.three == 3:
            self.rect.x += 4
            self.rect.y -= 3
        if self.three == 4:
            self.rect.x -= 4
            self.rect.y -= 3
    def tunud(self):
        self.rect.y += self.speed
            

class Bull(GSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class ContrP(GSprite):
    def control(self):
        kep = key.get_pressed()
        if kep[K_d] and self.rect.x < 750:
            self.rect.x += self.speed

        if kep[K_a] and self.rect.x > -20:
            self.rect.x -= self.speed

        if kep[K_LSHIFT]:
            self.speed = 7
        if kep[K_LSHIFT] == False:
            self.speed = 3

    def fire(self):
        bullet = Bull("bullet.png", self.rect.centerx, self.rect.top, 5, 10, 4, 0)
        bullets.add(bullet)

scrap1 = scrap("bullet.png", 380, -100, 30, 50, 1, 0)
scrap2 = scrap("bullet.png", 380, -100, 20, 60, 1, 1)
scrap3 = scrap("bullet.png", 380, -100, 50, 20, 1, 2)
scrap4 = scrap("bullet.png", 380, -100, 20, 40, 1, 3)
scrap5 = scrap("bullet.png", 380, -100, 50, 50, 1, 4)
playr = ContrP("rocket.png", randint(0, 750), 700, 65, 65, 3, 0)
for nmon in range(5):
    one = randint(5,8)
    two = 5
    if one >= 7:
        two = 1
        three = 3
    if one == 5:
        two = 3
        three = 1
    if one == 6:
        two = 2
        three = 2
    one *= 10
    enemy = Monster("ufo.png", randint(0,730), -40, one+35, one, two, three)
    monsters.add(enemy)

BF = 0
end = True
Game = True
while Game:
    wind.blit(bacG, (0, 0))
    playr.SH()
    wind.blit(kills, (5,5))
    wind.blit(death, (5,40))
    bullets.draw(wind)
    monsters.draw(wind)
    monsters.update()
    kep = key.get_pressed()
    bullets.update()
    bosss.draw(wind)
    bosss.update()

    death = font.render("пропущенно - " + str(Dn), True, (255,255,255))

    if Kn == 10:
        boss = Monster("ufo.png", 200, -200, 395, 350, 1, 10)
        bosss.add(boss)
        Kn = -10
        BF = 1

    if BF == 1:
        scrap1.tunud()
        scrap2.tunud()
        scrap3.tunud()
        scrap4.tunud()
        scrap5.tunud()

    if BF == 2:
        scrap1.SH()
        scrap2.SH()
        scrap3.SH()
        scrap4.SH()
        scrap5.SH()
        scrap1.wew()
        scrap2.wew()
        scrap3.wew()
        scrap4.wew()
        scrap5.wew()
        wind.blit(win, (300, 450))

    if kep[K_SPACE]:
        firer = 1

    if kep[K_SPACE] == False and firer == 1:
        playr.fire()
        firer = 0

    if end:
        playr.control()

    if sprite.groupcollide(monsters, bullets, True, True) and Kn >= 0:
        one = randint(5,8)
        two = 5
        if one >= 7:
            two = 1
            three = 3
        if one == 5:
            two = 3
            three = 1
        if one == 6:
            two = 2
            three = 2
        one *= 10
        enemy = Monster("ufo.png", randint(0,730), -100, one+35, one, two, three)
        monsters.add(enemy)
        Kn += 1
        kills = font.render("попаданий - " + str(Kn), True, (255,255,255))

    if sprite.groupcollide(bosss, bullets, False, True):
        hp -= 1
        dama1 = scrap("bullet.png", 400, boss.rect.x, 50,50,3,randint(0,10))

        if hp == 0:
            boss.kill()
            BF = 2
        
        
    for e in event.get():
        if e.type == QUIT:
            Game = False 

    if Dn >= 10:
        wind.blit(lose, (300, 450))
        Game = False

    display.update()
    time.delay(fps)
