import pygame
import sys
import random


# Window
WIDTH = 1288
HEIGHT = 738
DEFAULT_WIDTH = 40
DEFAULT_HEIGHT = 40
DEFAULT_SPEED = 50
# Clock
clock = pygame.time.Clock()
FPS = 100
# Window background
R = 50
G = 50
B = 50


def collision_entities(A, B):
    if (A.positionX < B.positionX + B.width and
            A.positionX + A.width > B.positionX and
            A.positionY < B.positionY + B.height and
            A.positionY + A.height > B.positionY):
        return True

class Entity():
    def __init__(self, x, y, r=200, g=200, b=50, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        self.positionX = x
        self.positionY = y
        self.tempX = x
        self.tempY = y
        self.width = width
        self.height = height
        self.direction = "right"
        self.r = r
        self.g = g
        self.b = b

    def render(self, screen):
        pygame.draw.rect(screen, (self.r, self.g, self.b),
                         rect=(self.positionX, self.positionY, self.width, self.height))

    def keys(self, event):

        # Keylogger
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and (self.direction != "down"):
                self.direction = "up"
            elif event.key == pygame.K_s and (self.direction != "up"):
                self.direction = "down"
            elif event.key == pygame.K_d and (self.direction != "left"):
                self.direction = "right"
            elif event.key == pygame.K_a and (self.direction != "right"):
                self.direction = "left"

    def movement(self):
        if self.direction == "right":
            self.positionX += DEFAULT_SPEED
        elif self.direction == "down":
            self.positionY += DEFAULT_SPEED
        elif self.direction == "left":
            self.positionX -= DEFAULT_SPEED
        elif self.direction == "up":
            self.positionY -= DEFAULT_SPEED

    def collision_wall(self):
        if (self.positionX < 25 or
                self.positionX > 1288 - 30):
            return True
        if (self.positionY < 25 or
                self.positionY > 738 - 30):
            return True
        return False

# Entities
Player = Entity(275, 275, r=100, g=100, b=100)
Apple = Entity(640, 360, width=25, height=25, r=255, g=50)
Tail = [Entity(225, 275), Entity(175, 275), Entity(125, 275)]

class Snake:
    global points
    global Points
    global Arial
    global tick
    global tailtick
    global game
    global Player
    global FPS
    game = True
    points = 0
    tailtick = 0
    tick = 0

    def __init__(self):
        # Screen,Clock and
        global Arial
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT))
        pygame.display.set_caption("Snek")
        pygame.font.init()
        Arial = pygame.font.SysFont('arial', 40)

    def _check_events(self):
        global Player
        global Apple
        global Tail
        global points
        global game
        global tick
        global tailtick
        global FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            Player.keys(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    Player = Entity(275, 275, r=100, g=100, b=100)
                    Apple = Entity(640, 360, width=25, height=25, r=255, g=50)
                    Tail = [Entity(225, 275), Entity(175, 275), Entity(125, 275)]
                    points = 0
                    game = True
                    tick = 0
                    tailtick = 0
                if event.key == pygame.K_UP:
                    FPS+=10
                if event.key == pygame.K_DOWN:
                    FPS-=10
        print(FPS)

    def _update_screen(self):
        global Arial
        global points
        global game
        global FPS
        Points = Arial.render(('Points: '+str(points)), True, (255, 255, 255))
        SpeedText = Arial.render(('Speed:'+str(f'{FPS/100:.2f}')),True, (255, 255, 255))
        GameOver = Arial.render(("You lost :("), True, (255, 255, 255))
        global tick
        self.screen.fill((R, G, B))
        pygame.draw.lines(self.screen, (0, 0, 0), closed=True,
                          points=((0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)),
                          width=40)
        if collision_entities(Player, Apple):
            Apple.positionY = random.randint(1, 13) * 50 - 20
            Apple.positionX = random.randint(1, 24) * 50 - 20
            points += 1
            FPS+=5
            Tail.append(Entity(Tail[0].positionX, Tail[0].positionY))

        Apple.render(self.screen)
        for element in Tail:
            if collision_entities(Apple, element):
                Apple.positionY = random.randint(2, 10) * 70+40
                Apple.positionX = random.randint(2, 10) * 100+40
            if collision_entities(Player, element):
                game = False
            element.render(self.screen)
        if Player.collision_wall():
            game = False
        Player.render(self.screen)
        self.screen.blit(Points, (30, 30))
        self.screen.blit(SpeedText,(30,70))
        if game == False:
            self.screen.blit(GameOver, (WIDTH / 2 - 100, 100))

        pygame.display.flip()


    def tail_update(self):
        global tick
        global tailtick
        global posX
        global posY
        global game

        if game and not Player.collision_wall():
            if tailtick == 59:
                posX = Player.positionX
                posY = Player.positionY
                for segment in range(len(Tail)):
                    if segment >= 1:
                        Tail[segment].tempX = Tail[segment - 1].positionX
                        Tail[segment].tempY = Tail[segment - 1].positionY
            if tailtick == 60:
                Tail[0].positionX = posX
                Tail[0].positionY = posY
                for segment in range(len(Tail)):
                    if segment >= 1:
                        Tail[segment].positionX = Tail[segment].tempX
                        Tail[segment].positionY = Tail[segment].tempY

                Player.movement()
                tick = 0
                tailtick = 0

    def run_game(self):
        global tick
        global tailtick
        global Player
        global Apple
        global Tail
        global points
        global game
        while True:
            tick += 1
            tailtick += 1
            clock.tick(FPS)
            self._check_events()
            self._update_screen()
            self.tail_update()




if __name__ == '__main__':
    snake_game = Snake()
    snake_game.run_game()
