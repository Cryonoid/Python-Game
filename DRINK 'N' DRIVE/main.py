import pygame as pg
import os, random
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
pg.init()
width = 800
height = 500

score = 0

GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

gameName = "DRINK 'N' DRIVE"
pg.display.set_caption(gameName)
screen = pg.display.set_mode((width, height))
running = True
whiteLines = -320
roadPositionY = -50
mode = "menu"
playerWidth = 50
playerHeight = 70
assert_url = resource_path("assets/player.gif")
player = pg.image.load(assert_url)
player = pg.transform.scale(player, (playerWidth, playerHeight))
playerPositionX = 320
playerPositionY = 420
playerSpeed = 0.2
playerMovingLeft = False
playerMovingRight = False
enemyWidth = 64
enemyHeight = 64
eny = []
cheat = False
s = ""
for i in os.listdir(".\\assets\\"):
    if "enemy" in i:
        eny.append(pg.image.load(str(resource_path(f"assets/{i}"))))
enemy = [random.choice(eny) for i in range(2)]
enemy = [pg.transform.scale(i, (enemyWidth, enemyHeight)) for i in enemy]
enemySpeed = 0.08
enemyPositionX = [220, 320]
enemyPositionY = [0, -320]

pause = True
font = pg.font.Font(None, 32)
font36 = pg.font.Font(None, 36)
def isCollision(enemyPositionX, playerPositionX, enemyPositionY):
    enemyPositionX2 = enemyPositionX+enemyWidth
    playerPositionX2 = playerPositionX+playerWidth
    if (enemyPositionY+enemyHeight>=playerPositionY and enemyPositionY<playerPositionY+playerHeight) and ((playerPositionX>=enemyPositionX and playerPositionX<=enemyPositionX2) or (playerPositionX2>=enemyPositionX and playerPositionX2<=enemyPositionX2)):
        return True

while running:
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            running = False
            pg.quit()

        if evt.type == pg.KEYDOWN:
            if evt.key == pg.K_p:
                if pause == True:
                    pause = False
                elif pause == False:
                    pause = True
            if evt.key == pg.K_q:
                running = False
                pg.quit()
            if evt.key in [pg.K_LEFT, pg.K_a]:
                playerMovingLeft = True
            if evt.key in [pg.K_RIGHT, pg.K_d]:
                playerMovingRight = True
            if mode=="complete":
                if evt.key>=pg.K_a and evt.key<=pg.K_z:
                    s+=chr(evt.key)
                if "iamaloser" in s:
                    mode = "playing"
                    s = ""
                    cheat = True
        if evt.type == pg.KEYUP:
            if evt.key in [pg.K_LEFT, pg.K_a]:
                playerMovingLeft = False
            if evt.key in [pg.K_RIGHT, pg.K_d]:
                playerMovingRight = False
        
        if evt.type == pg.MOUSEBUTTONDOWN or cheat:
            try:
                x, y = evt.pos
            except:
                x, y = width//2, height//2+30
            if mode=="menu":
                if (x>20 and x<100) and (y>95 and y<95+17):
                    mode = "playing"
                elif (x>20 and x<100) and (y>120 and y<147):
                    running = False
                    pg.quit()
            if mode == "complete" or cheat:
                if x>width//2-60 and x<width//2+160 and y>height//2+25 and y<height//2+25+17:
                    gameName = "DRINK 'N' DRIVE"
                    score = score if cheat else 0
                    running = True
                    playerSpeed = playerSpeed if cheat else 0.2
                    enemySpeed = enemySpeed if cheat else 0.08
                    cheat = False
                    whiteLines = -320
                    roadPositionY = -50
                    playerWidth = 50
                    playerHeight = 70
                    player = pg.image.load(".\\assets\\player.gif")
                    player = pg.transform.scale(player, (playerWidth, playerHeight))
                    playerPositionX = 320
                    playerPositionY = 420
                    playerMovingLeft = False
                    playerMovingRight = False
                    enemyWidth = 64
                    enemyHeight = 64
                    eny = []
                    for i in os.listdir(".\\assets\\"):
                        if "enemy" in i:
                            eny.append(pg.image.load(str(".\\assets\\"+i)))
                    enemy = [random.choice(eny) for i in range(2)]
                    enemy = [pg.transform.scale(i, (enemyWidth, enemyHeight)) for i in enemy]
                    enemyPositionX = [220, 320]
                    enemyPositionY = [0, -320]
                    pause = True
                    font = pg.font.Font(None, 32)
                    font36 = pg.font.Font(None, 36)
                    mode = "playing"
    if running and mode=="playing":
        pg.draw.rect(screen, (124, 252, 0), (0, 0, width, height))
        pg.draw.rect(screen, GREY, (200, roadPositionY, 300, 600))
        pg.draw.rect(screen, WHITE, (200, 0, 5, 600))
        pg.draw.rect(screen, WHITE, (498, 0, 5, 600))
        for i in range(6):
            pg.draw.rect(screen, WHITE, (295, whiteLines+i*160, 10, 80))
            pg.draw.rect(screen, WHITE, (395, whiteLines+i*160, 10, 80))
        screen.blit(player, (playerPositionX, playerPositionY))
        for i in range(len(enemyPositionX)):
            screen.blit(enemy[i], (enemyPositionX[i], enemyPositionY[i]))
            # pg.draw.rect(screen, BLUE, (enemyPositionX[i], enemyPositionY[i], enemyWidth, 70))

        if running and pause:
            for i in range(len(enemyPositionY)):
                enemyPositionY[i]+=enemySpeed
            whiteLines+=playerSpeed
            for i in range(len(enemyPositionY)):
                enemyPositionY[i]+=playerSpeed
            if whiteLines>0:
                whiteLines = -320
            if playerMovingLeft and int(playerPositionX)>205:
                playerPositionX-=playerSpeed
            if playerMovingRight and int(playerPositionX)<500-5-playerWidth:
                playerPositionX+=playerSpeed

            for i in range(len(enemyPositionY)):
                if isCollision(enemyPositionX[i], playerPositionX, enemyPositionY[i]):
                    mode = "complete"
                    screen.fill(BLACK)
                    break
                if enemyPositionY[i]>500:
                    enemyPositionY[i] = -320
                    enemyPositionX[i] = random.choice([220, 320, 420])
                    enemy[i] = random.choice(eny)
                    score+=1

            if score>0 and score in [10, 20, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 2000, 3000, 5000, 10000, 50000, 100000]:
                playerSpeed+=0.05
                enemySpeed+=0.002
                score+=5

            if running:
                f1 = font.render(f"Score: {score}", True, BLACK)
                screen.blit(f1, (210, 20))
                pg.display.update()
    if running and mode=="menu":
        t1 = font36.render(gameName, True, WHITE)
        t2 = font.render("------------------------------------", True, WHITE)
        t3 = font.render("PLAY", True, WHITE)
        t4 = font.render("QUIT", True, WHITE)
        t5 = font36.render("HOW TO PLAY", True, WHITE)
        t6 = font.render("PRESS LEFT KEY OR A TO MOVE LEFT", True, WHITE)
        t7 = font.render("PRESS RIGHT KEY OR D TO MOVE RIGHT", True, WHITE)
        t8 = font.render("PRESS P TO PAUSE AND RESUME GAME", True, WHITE)
        t9 = font.render("AVOID HITTING OTHER CARS", True, WHITE)
        screen.blit(t1, (25, 25))
        screen.blit(t2, (25, 65))
        screen.blit(t3, (25, 95))
        screen.blit(t4, (25, 125))
        screen.blit(t5, (25, 155))
        screen.blit(t6, (25, 185))
        screen.blit(t7, (25, 215))
        screen.blit(t8, (25, 245))
        screen.blit(t9, (25, 275))
        pg.display.update()
    if running and mode=="complete":
        if "hs" not in os.listdir():
            f = open("hs", "w")
            f.write("")
            f.close()
        hscore = open("hs", "r").read()
        hscore = -1 if hscore.strip()=="" else int(hscore)
        if int(hscore)>score:
            screen.blit(font.render(f"SCORE: {score}", True, WHITE), (width//2-100, height//2-25))
            screen.blit(font.render(f"HIGHSCORE SCORE: {hscore}", True, WHITE), (width//2-100, height//2))
        else:
            screen.blit(font.render(f"NEW HIGHSCORE: {score}", True, WHITE), (width//2-100, height//2))
            f = open("hs", "w")
            f.write(str(score))
            f.close()
        screen.blit(font.render("PLAY AGAIN", False, WHITE), (width//2-55, height//2+25))
        pg.display.update()