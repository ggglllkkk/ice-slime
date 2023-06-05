import pygame
from pygame.locals import *
import math as m
import pytmx, pyscroll

import manager, mobs, gameItems, menu, maps
from player import Player

#Variables
buttonActions = []
username = "Slime"
gamePaused = False
pressedKeys = {}
pressedKeys2 = {}

#Initialisation de pygame
pygame.init()
sounds = {"oof":pygame.mixer.Sound("data/sounds/oof.wav")}
for key in sounds.keys(): sounds[key].set_volume(0.001)
pygame.mixer.init()
gameClock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), RESIZABLE)
pygame.display.set_caption('Slime')
pygame.display.set_icon(pygame.image.load("data/images/player.png"))

#Initialisation du module musique (non implémenté encore)
music = {"rush E": pygame.mixer.Sound("data/sounds/rush_E.wav"), "bombjack": pygame.mixer.Sound("data/sounds/bombjack.wav")}
musicChannel = pygame.mixer.Channel(1)
musicChannel.set_volume(0.001)
musicChannel.play(music["bombjack"])

#Initialisation des polices
police = pygame.font.Font("data/fonts/alagard.ttf", 20)

#Création des variables pour la carte
group=None
tmx_data=None
map_data=None
map_layer=None
collisions=None
hostileMobs=None
hostileMobsItems=None

#Création des instances
player = Player()
gameMenu = menu.pauseMenu(screen.get_size())


#Charge une carte selon son nom
def loadMap(map):
    global group, player, tmx_data, map_data, map_layer, collisions, hostileMobs, hostileMobsItems
    map = maps.Map(map)
    tmx_data=map.tmx_data
    map_data=map.map_data
    map_layer=map.map_layer

    collisions=map.collisions

    player.rect.x=map.playerSpawnpoint.x
    player.rect.y=map.playerSpawnpoint.y

    hostileMobs=map.hostileMobs
    hostileMobsItems=map.hostileMobsItems

    group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=0)
    group.add(player)
    group.add(player.inv.currentItem)
    group.add(hostileMobs)
    group.add(hostileMobsItems)

    groupReset()

#Update à chaque actualisation
def update():
    hostileMobs.update(collisions, player)

    player.update(collisions, hostileMobs, screen)
    keyEventsManager(pressedKeys)

#Ré-importe les sprites si changement dans l'affichage
def groupReset():
    group2 = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
    for k in group:
        group2.add(k)
        print(k)
    a = screen.get_width()/854
    b = screen.get_height()/480
    if a>b: map_layer.zoom = a
    else: map_layer.zoom = b

    return group2

#Dessin de la barre de vie
def healthBar(x,y):
    a=8
    pygame.draw.rect(screen, (0,0,0), (x-11, y-11, 93, 23))
    pygame.draw.rect(screen, (255,0,0), (x+2, y-a, 76*(player.pv/player.maxPv), 2*a))
    pygame.draw.polygon(screen, (215,200,140), ((x,y), (x,y+10), (x+80, y+10), (x+80,y-10), (x, y-10), (x,y), (x+2, y), (x+2, y-a), (x+80-2, y-a), (x+80-2*a, y+a), (x+2, y+a), (x+2, y)))
    pygame.draw.circle(screen, (0,0,0),(x-30, y),30)
    screen.blit(player.image, (x-45,y-15))

#Reçoit les inputs pressés et les analyse
def keyEventsManager(events):
    global pressedKeys2
    toDo = {"up":player.up, "down":player.down, "left":player.left, "right":player.right, "inventory":player.inv.openInv, "pickUp":player.inv.pickUp}
    dico=manager.getKeys()
    for key, active in pressedKeys.items():
        a=False
        for k,n in dico.items():
            if n[1]==key: a=k
        if not a: continue
        if dico[a][0]==1 or (dico[a][0]==0 and (not key in pressedKeys2.keys())):
            toDo[a]()
    pressedKeys2 = pressedKeys.copy()

    return

#Dessine tout sur l'écran
def drawAll():
    screen.fill((255,255,255))
    group.center(player.rect)
    group.draw(screen)
    healthBar(80,50)
    player.inv.update(screen)
    if player.inv.changed:
        groupReset()
        player.inv.changed = False

#Gérer le menu
def fpausedMenu(menuId):
    global gamePaused
    if menuId == 5: 
        gamePaused = False
        m=gameMenu.activeMenu = None
        gameMenu.i = 0
    else: 
        gameMenu.activeMenu = gameMenu.menus[menuId]

#Boucle principale
loadMap("carte")
doContinue = True
while doContinue:
    gameClock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            doContinue = False
        if event.type == VIDEORESIZE:
            map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
            group = groupReset()
            gameMenu = menu.pauseMenu(screen.get_size())
        
        #Si touches pressées
        if event.type == KEYDOWN:
            pressedKeys[event.dict["key"]] = True
        if event.type == KEYUP:
            
            del pressedKeys[event.dict["key"]]
            
            # si "échap" pressée
            if event.scancode == 41:
                if not gamePaused: gamePaused = True
        
        #Si click détecté
        if event.type == MOUSEBUTTONUP:
            if gamePaused:
                gameMenu.gettingClicked()
            if player.inv.isOpen:
                player.inv.gettingClicked(screen, player.rect)
    
    if not gamePaused: update()

    if not player.isDead: drawAll()
    if gamePaused:
        a=gameMenu.update(screen, police)
        if a: fpausedMenu(a)
    pygame.display.flip()


pygame.quit()