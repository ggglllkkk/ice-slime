import pygame
import math as m

import gameItems
from inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("data/images/player.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.maxPv = 20
        self.pv = self.maxPv
        self.speed = 3
        self.detectRange=400
        self.isDead = False
        self.target = None
        self.inv = Inventory()
        self.inv.changeCurrentItem(gameItems.weapons["long-sword"], self.inv.inv)
        self.i = 0
    
    #update
    def update(self, collisions, hostileMobs, screen):
        self.collisions = collisions
        self.feet = pygame.Rect(self.rect.midbottom+(0,0))
        if self.pv <= 0: self.isDead = True
        if self.isDead: self.died(screen)
        
        #choisi sa victime la + proche
        for k in hostileMobs:
            a=m.sqrt(abs((self.rect.center[0]-k.rect.center[0])**2)+abs((self.rect.center[1]-k.rect.center[1])**2))
            if a<self.detectRange:
                if k.isDead:
                    self.target=None
                    continue
                if not self.target or self.target.distance>a: self.target = k
                self.target.distance=a
            else: self.target=None
        self.updateWeapon()

        if self.target: self.attack(hostileMobs)
        else: self.inv.currentItem.update(pygame.Rect(self.rect.x+self.rect.width, self.rect.y+self.rect.height-10,0,0))
    
    #attaque
    def attack(self, hostileMobs):
        if self.inv.currentItem.activeAttackRect.colliderect(self.target.rect):
            if (self.inv.currentItem.isRecharging or self.inv.currentItem.isAttacking): return
            self.inv.currentItem.attack()
            for k in hostileMobs:
                if self.inv.currentItem.activeAttackRect.colliderect(k.rect):
                    k.pv-=self.inv.currentItem.damage

    #met à jour son arme: fait suivre sa position+gauche/droite+la tourne (trigo) pour être en phase avec le monstre qu'il attaque
    def updateWeapon(self):
        a=0
        c=-1
        if self.target:
            if self.rect.center[0]-self.target.rect.center[0] != 0: 
                a=m.atan((self.target.rect.center[1]-self.rect.center[1])/(self.rect.center[0]-self.target.rect.center[0]))

            if (self.rect.center[0]-self.target.rect.center[0])<=0: 
                c=1

            if (self.inv.currentItem.isReversed and (self.rect.center[0]-self.target.rect.center[0])>0) or (not self.inv.currentItem.isReversed and (self.rect.center[0]-self.target.rect.center[0])<0): self.inv.currentItem.reverse()

        a=-a
        b=self.rect.copy()

        b.x+=(b.width)*m.cos(a)*c
        b.y+=(b.height-10)*m.sin(a)*c

        a=a*(180/m.pi)
        self.inv.currentItem.update(b, -a-90*c)
        #self.inv.currentItem.update(b, a)

        pass

    def up(self):
        if pygame.Rect(self.rect.x, self.rect.y-self.speed, self.rect.width, self.rect.height).collidelist(self.collisions) ==-1: self.rect.y-=self.speed
    def down(self):
        if pygame.Rect(self.rect.x, self.rect.y+self.speed, self.rect.width, self.rect.height).collidelist(self.collisions) ==-1: self.rect.y+=self.speed
    def left(self):
        if pygame.Rect(self.rect.x-self.speed, self.rect.y, self.rect.width, self.rect.height).collidelist(self.collisions) ==-1: self.rect.x-=self.speed
    def right(self):
        if pygame.Rect(self.rect.x+self.speed, self.rect.y, self.rect.width, self.rect.height).collidelist(self.collisions) ==-1: self.rect.x+=self.speed
    
    def selfCoos(self, screenSize): return (screenSize[0]//2-(self.rect[2]//2), screenSize[1]//2-(self.rect[3]//2))
    
    #affiche le menu de mort (copie de celui de dark souls)
    def died(self, screen):
        c=150
        screen.fill((0,0,0))
        a=pygame.image.load("data/images/uDied.png")
        b=((screen.get_size()[0]//2-a.get_size()[0]//2), (screen.get_size()[1]//2-a.get_size()[1]//2))
        screen2 = pygame.Surface(screen.get_size())
        screen2.set_alpha(255*(self.i/c))
        screen2.blit(a, b)
        screen.blit(screen2, (0,0))
        if self.i <= c: self.i += 1