import pygame as p
from random import choice, uniform, randint
import math
from time import time


class Player(p.sprite.Sprite):
    def __init__(self, group, player, direction):
        super().__init__(group)
        self.image = p.Surface((10, 70))
        self.name = player
        self.direction = direction
        self.ball = None

        self.playing = None
        self.choicePlayer = None
        self.startTime = None




        if self.name == "pOne":
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(midleft=(20, screenHeight / 2))
            self.useKey = p.K_e
            self.color = (255, 0, 0)
        else:
            self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect(midright=(screenWidth - 20, screenHeight / 2))
            self.useKey = p.K_k
            self.color =(0, 255, 0)

        self.posY = float(self.rect.y)

    def input(self):
        keys = p.key.get_pressed()
        speed = 200
        global startTime


        if self.name == "pOne":
            playerDirection = int(keys[p.K_s]) - int(keys[p.K_w])
        elif self.name == "pTwo":
            playerDirection = int(keys[p.K_l]) - int(keys[p.K_o])

        self.posY += playerDirection * speed * dt

        if self.posY < 0:
            self.posY = 0
        if self.posY > screenHeight - self.rect.height:
            self.posY = screenHeight - self.rect.height

        self.rect.y = int(self.posY) 

        if self.playing == False and self.choicePlayer.name == self.name:
            if keys[self.useKey]:
                self.ball.playing = True
                startTime = p.time.get_ticks()

        if keys[p.K_r]:
            restart(self.ball)
        """ global squarePause
            global spellActive
            global spellGroup
            spellGroup.empty()
            spellActive = True
            squarePause = False
            startTime = None
            self.ball.playing = False
            self.ball.ready = False
            self.posY = screenHeight // 2
            self.image = p.transform.scale(self.image, (10, 70))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.ball.restart()"""


    def update(self):
        self.input()
        self.playing = self.ball.playing
        self.choicePlayer = self.ball.choicePlayer


class Ball(p.sprite.Sprite):
    def __init__(self, group, players):
        super().__init__(group)
        self.image = p.Surface((15, 15))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(0,0))
        self.name = "ball"
        self.lastPlayerTouchColor = None
        self.lastPlayerTouchName = None
        self.speed = 200
        self.players = players
        self.ready = False
        self.playing = False
        self.choicePlayer = None
        self.direction = p.Vector2(1, 0)

    def restart(self):
        global gameTime
        global gridGroup

        for square in gridGroup:
            square.image.fill((0,0,0))
        gameTime = 120000
        self.choicePlayer = choice(self.players)
        angleDeg = uniform(-60, 60)
        baseDirection = 1 if self.choicePlayer.name == "pOne" else -1
        self.direction = p.Vector2(baseDirection, 0).rotate(angleDeg).normalize()
        self.lastPlayerTouchColor = self.choicePlayer.color
        self.ready = True

    def movement(self):
        global squarePause
        global finalScore
        global check

        #top bottom wall
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction.y *= -1
            
        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
            self.direction.y *= -1

        #left right wall
        if self.rect.left <= 19:
            finalScore = checkSquareGrid("Green wins")

        if self.rect.right >= screenWidth - 19:
            finalScore = checkSquareGrid("Red wins")

        for player in self.players:
            if self.rect.colliderect(player.rect):
                offset = (self.rect.centery - player.rect.centery) / (player.rect.height / 2)
                maxBounceAngle = 60
                bounceAngle = offset * maxBounceAngle

                playerDirection = 1 if player.name == "pOne" else -1
                self.direction = p.Vector2(playerDirection, 0).rotate(bounceAngle * player.direction).normalize()
                self.lastPlayerTouchColor = player.color
                self.lastPlayerTouchName = player.name

        self.rect.center += self.direction * self.speed * dt

    def update(self):
        if squarePause == False:
            if self.ready and not self.playing:
                if self.choicePlayer.name == "pOne":
                    self.pos = (self.choicePlayer.rect.midright[0] + 30, self.choicePlayer.rect.center[1])
                else:
                    self.pos = (self.choicePlayer.rect.midleft[0] - 30, self.choicePlayer.rect.center[1])
                self.rect.center = self.pos
        

            if self.playing:
                self.movement()

            if not self.ready:
                self.restart()



class GridSquare(p.sprite.Sprite):
    def __init__(self, group, players,ball):
        super().__init__(group)        
        self.image = p.Surface((12,12))
        self.image.fill((0,0,0))

        self.players = players
        self.ball = ball

    def coloring(self):
        if self.rect.colliderect(self.ball.rect):
            self.image.fill(self.ball.lastPlayerTouchColor)
    
    def update(self):
        self.coloring()




class Spell(p.sprite.Sprite):
    def __init__(self, group, ball, players):
        super().__init__(group)
        self.image = p.Surface((70,70))
        self.image.fill((200,0,200))
        self.spellActive = False
        self.players = players
        box = (70,100,200,500)
        chosenBox = choice([box[0], screenWidth - box[0] - box[2]])
        self.ball = ball

        x = randint(chosenBox,chosenBox + box[2])
        y = randint(box[1], box[3])

        self.rect = self.image.get_rect(center=(x,y))



    def collisions(self):
        if self.rect.colliderect(self.ball.rect):
            self.wichPlayer = self.ball.lastPlayerTouchName

            if self.spellActive == False:
                self.allSpells = ["invisible", "large", "small", "bomb"]
                self.spell = choice(self.allSpells)
                self.spellActive = True
                for pla in players:
                    if pla.name != self.wichPlayer:
                        self.opponentPlayer = pla
                print(self.spell)

                match self.spell:
                    case "invisible":
                        self.invisible()
                    case "large":
                        self.large()
                    case "small":
                        self.small()
                    case "bomb":
                        self.bomb()
                self.kill()

    def invisible(self):
        global invisiblePlayerTimer
        global invisiblePlayer
        self.opponentPlayer.image.fill((255,255,255))
        invisiblePlayer = self.opponentPlayer
        invisiblePlayerTimer = p.time.get_ticks() + 10000

    def large(self):
        global ballNeedScale
        self.scale = 2
        self.scaleTimer = 1
        scaleBall(self.ball,2,2)
        ballNeedScale = True

    def small(self):
        global smallPlayerTimer
        smallPlayerTimer = p.time.get_ticks() + 15000
        scaleBall(self.opponentPlayer, 1, 0.6)
    
    def bomb(self):
        bombX = randint(screenWidth // 2 - 227,827)
        bombY = randint(screenHeight // 2 - 240,590)
        bombSprite(bombX, bombY, self.ball.lastPlayerTouchColor)
        


    def update(self): 
        self.collisions()





def calculateBallDirection(angleRad, speed, direction):
    velocityX = math.cos(angleRad) * speed * direction
    velocityY = math.sin(angleRad) * speed * direction

    ball.rect.x += velocityX * dt
    ball.rect.y += velocityY * dt


def checkSquareGrid(winType):
    global startTime
    global check
    global squarePause

    startTime = False
    ball.playing = False
    squarePause = True
    if winType == "time":
        red = 0
        green = 0
        for square in gridGroup:
            squareColor = square.image.get_at((0,0))
            if squareColor == (255,0,0,255):
                red += 1
            if squareColor == (0,255,0,255):
                green += 1
            square.image.fill((0,0,0))
        allColored = red + green
        if allColored != 0:
            redProcentages = round(red / allColored * 100)
            greenProcentages = 100 - redProcentages
        else:
            redProcentages = 0
            greenProcentages = 0
       
        if redProcentages > greenProcentages:
            winnerText = "Red wins"
        elif greenProcentages > redProcentages:
            winnerText = "Green wins"
        else:
            winnerText = "Draw"
        

        scoreText = f"{str(redProcentages)}%    {winnerText}    {str(greenProcentages)}%"
    
    else:
        scoreText = str(winType)
        
        
    ball.rect.center = ((-20,-20))
        
    score = scoreFont.render(scoreText, True, (0,50,200))
    check = True
    return score
    
def scaleBall(self,scaleX, scaleY):
    global ballNeedScale
    global scaleBallPlayer
    global smallPlayer
    if self.name == "ball" or self.image.get_height() == 70 or (scaleY == 1.55 and self.image.get_height() != 70):
        w = int(self.image.get_width() * scaleX)
        h = int(self.image.get_height() * scaleY)
        self.image = p.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.name == "ball":
            scaleBallPlayer = self.lastPlayerTouchName
            ballNeedScale = False
        elif scaleY == 0.6:
            smallPlayer = self


def bombSprite(x,y,color):
    global bomb
    bomb['sprite'] = p.Surface((50,50))
    bomb['sprite'].fill((255,255,255))
    bomb['rect'] = bomb['sprite'].get_rect(center=(x, y))
    for sq in gridGroup:
        if sq.rect.colliderect(bomb['rect']):
            sq.image.fill(color)


def restart(ball):
    global squarePause
    global spellActive
    global spellGroup
    global startTime
    global check
    spellGroup.empty()
    spellActive = True
    check = False
    squarePause = False
    startTime = None
    ball.playing = False
    ball.ready = False
    for player in players:
        player.image.fill(player.color)
        player.posY = screenHeight // 2
        player.image = p.transform.scale(player.image, (10, 70))
        player.rect = player.image.get_rect(center=player.rect.center)
    ball.restart()

p.init()

clock = p.time.Clock()

screenWidth = 1200
screenHeight = 700
screen = p.display.set_mode((screenWidth, screenHeight), p.NOFRAME)
p.display.set_caption("PongX")

startTime = None
gameTime = 120000
squarePause = False
check = False
finalScore = None
scaleBallPlayer = None
spellActive = True
ballNeedScale = False

smallPlayer = None
smallPlayerTimer = None
invisiblePlayerTimer = None
invisiblePlayer = None
bomb = {
    "sprite": None,
    "rect": None
}

#text
timeFont = p.font.SysFont("Arial", 60)
scoreFont = p.font.SysFont("Arial", 100)


#groups
playerGroup = p.sprite.Group()
player1 = Player(playerGroup, "pOne", 1)
player2 = Player(playerGroup, "pTwo", -1)
players = [player1, player2]

ballGroup = p.sprite.GroupSingle()
ball = Ball(ballGroup, players)

for player in players:
    player.ball = ball


#center grid
gridGroup = p.sprite.Group()
for x in range(screenWidth // 2 - 227,827,13):
    for y in range(screenHeight // 2 - 240,590,13):
        square = GridSquare(gridGroup, players, ball)
        square.rect = square.image.get_rect(topleft=(x,y))

spellGroup = p.sprite.Group()


running = True
while running:
    dt = clock.tick(60) / 1000
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
            
    
        if event.type == p.KEYDOWN:
            if squarePause:
                if event.key == p.K_SPACE:
                    restart(ball)
                """squarePause = False
                    ball.ready = False
                    ball.playing = False
                    startTime = None
                    check = False
                    spellGroup.empty()
                    spellActive = True
                    for player in players:
                        player.image.fill(player.color)
                        player.posY == screenHeight // 2
                    invisiblePlayerTimer = 0
                    smallPlayerTimer = None"""



    screen.fill((255,255,255))

    if startTime:
        elapsed = p.time.get_ticks() - startTime
        remaining = max(0,gameTime - elapsed)
        remaSeconds = remaining // 1000

        timeSecText = timeFont.render(str(remaSeconds), True, (255,0,255))
        timeSecRect = timeSecText.get_rect(center=(screenWidth//2, 50))
        screen.blit(timeSecText, timeSecRect)

        if remaSeconds <= 0 and check == False:
            finalScore = checkSquareGrid("time")
        
        if not spellActive and time() >= spellSpawnTime:
            spellGroup.add(Spell(spellGroup, ball, players))
            spellActive = True

        
        if spellActive and len(spellGroup) == 0:
            spellActive = False
            spellSpawnTime = time() + uniform(20,25)

        if ballNeedScale:
            if scaleBallPlayer != ball.lastPlayerTouchName:
                scaleBall(ball, 0.5, 0.5)

        if invisiblePlayerTimer:
            if invisiblePlayerTimer <= p.time.get_ticks():
                invisiblePlayer.image.fill((invisiblePlayer.color))
                invisiblePlayerTimer = None
        if smallPlayerTimer:
            if smallPlayerTimer <= p.time.get_ticks():
                scaleBall(smallPlayer,1,1.55)
                smallPlayerTimer = None
        if bomb['sprite']:
            screen.blit(bomb['sprite'], bomb['rect'])


    playerGroup.draw(screen)

    ballGroup.draw(screen)
    ballGroup.update()
    playerGroup.update()
    gridGroup.draw(screen)
    gridGroup.update()
    spellGroup.draw(screen)
    spellGroup.update()
    if squarePause:
        finalScoreRect = finalScore.get_rect(center=(screenWidth//2, 60))
        screen.blit(finalScore, finalScoreRect)
    
    p.display.update()

p.quit()