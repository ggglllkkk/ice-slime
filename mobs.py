import pygame
import math as m

import gameItems

class hostileMob(pygame.sprite.Sprite):
    def __init__(self, atk, pvs, speed, imgPath, weapon, detectRange, deathWorth):
        super().__init__()

        self.atk = atk
        self.pv = pvs
        self.speed = speed
        self.image = pygame.image.load(imgPath)
        self.rect = self.image.get_rect()
        self.weapon = weapon
        self.detectRange = detectRange
        self.deathWorth = deathWorth
        self.spawnPoint = (0,0)
        self.playerDistance = int
        self.tag = "hostileMob"
        self.isReversed = True
        self.target = pygame.Rect(0,0,0,0)
        self.isDead = False
        
        self.weapon.reverse()

    #update
    def update(self, collisions, player):

        if self.isDead: self.died()
        if self.pv<=0: self.isDead=True

        self.updateWeapon()

        self.playerDistance = self.detection(player.rect)
        self.collisions = collisions
        
        #Prise de décision
        b=self.isReversed
        if self.playerDistance and self.playerDistance < self.detectRange:
            self.target = player
            if self.rect.x-player.rect.x > 0: self.isReversed = True
            elif self.rect.x-player.rect.x < 0: self.isReversed = False
            self.move(player.rect)
        elif self.rect[:2] != self.spawnPoint:
            self.move(self.spawnPoint)

        if b!= self.isReversed: self.reverse()
    
    #update l'arme (position, etc...)
    def updateWeapon(self):
        if not self.isReversed: a=+12
        else: a=-30
        
        c = self.rect.x + self.rect.width//2+a
        d = self.rect.y + self.rect.height-self.weapon.rect.width-(self.weapon.rect.height//2)
        
        b=pygame.Rect(c,d,0,0)
        
        self.weapon.update(b)
    
    #retourne l'image
    def reverse(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.weapon.reverse()
        
    #attaque le joueur
    def attack(self):
        if (self.weapon.isRecharging or self.weapon.isAttacking): return
        self.weapon.attack()
        self.target.pv-=self.weapon.damage+self.atk

    #se déplca ou attaque
    def move(self, destination):
        if self.target:
            if self.weapon.rect.colliderect(self.target.rect): 
                self.attack()
                return
        
        if abs(self.rect.x-destination[0]) > self.speed:
            if self.rect.x-destination[0] > 0: self.left()
            else: self.right()
        
        if abs(self.rect.y-destination[1]) > self.speed:
            if self.rect.y-destination[1] > 0: self.up()
            else: self.down()

        return 0

    def up(self):
        if pygame.Rect(self.rect.x, self.rect.y-self.speed, self.rect.width, self.rect.height).collidelist(self.collisions) ==-1: self.rect.y-=self.speed
    def down(self):
        if pygame.Rect(self.rect.x, self.rect.y+self.speed, self.rect.width, self.rect.height).collidelist(self.collisions) ==-1: self.rect.y+=self.speed
    def left(self):
        if pygame.Rect(self.rect.x-self.speed, self.rect.y, self.rect.width, self.rect.height).collidelist(self.collisions) ==-1: self.rect.x-=self.speed
    def right(self):
        if pygame.Rect(self.rect.x+self.speed, self.rect.y, self.rect.width, self.rect.height).collidelist(self.collisions) ==-1: self.rect.x+=self.speed
    
    #cherche le joueur
    def detection(self, playerRect):
        if playerRect.x > self.rect.x-self.detectRange and playerRect.x < self.rect.x+self.detectRange:
            a=m.sqrt(abs((self.rect.center[0]-playerRect.center[0])**2)+abs((self.rect.center[1]-playerRect.center[1])**2))
            return a

    #modifie le point d'apparition
    def setSpawnPoint(self, spawnPoint):
        self.spawnPoint = spawnPoint
        self.rect.x = self.spawnPoint[0]
        self.rect.y = self.spawnPoint[1]

    #si mort
    def died(self):
        #self.isDead = True
        self.target.inv.currentMoney += self.deathWorth
        self.weapon.kill()
        self.kill()


#plusieurs instances
hostileMobs = {
    "fighter": hostileMob(1,10,1.5,"data/images/deep_elf_fighter_new.png",gameItems.weapons["sword"],200, 10),
    "assassin": hostileMob(2,5,3,"data/images/deep_elf_fighter_new2.png",gameItems.weapons["dagger"],100, 10)
}