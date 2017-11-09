import pygame,random
import sys
###############
## CONSTANTS ##
###############
RED =   (255,   0,  0)
BLACK = (   0,  0,  0)
WHITE = (255, 255,255)
BLUE =  (   0,  0,255)
GREEN = (   0,255,  0)

size = SW, SH = 800,650
border = (5,5,SW-10,SH-60)
MAX_SCORE = 10
FPS =60

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PING PONG")
clock = pygame.time.Clock()
game_Running = False

class Player(pygame.sprite.Sprite):
    # Create the players bar for playing
    def __init__(self,width,height,color):
        super(Player, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.score = 0
        self.change = [0,0]
        self.speed = 2

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.speed = [5,5]
        self.image = pygame.image.load('intro_ball1.gif').convert_alpha()
        self.rect = self.image.get_rect()

# Create sprites for player bars of 70x15
Player1 = Player(15,70,RED)
Player2 = Player(15,70,BLUE)
football = Ball()

player_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

player_list.add(Player1,Player2)
all_sprites_list.add(Player1,Player2,football)

def print_text(text,pos,size,color):
    # Function to print the text on screen
    textobj = pygame.font.Font(None, size)
    text_toprint = textobj.render(text,True,color)
    screen.blit(text_toprint, pos)
    return text_toprint

def bgrnd():
    # Function to draw the background
    screen.fill(pygame.Color('Dark Green'))
    print_text("SCORE : " + str(Player1.score) + " : " + str(Player2.score), (600,600),40, WHITE)
    pygame.draw.rect(screen, BLUE, border, 5)
    pygame.draw.line(screen, BLUE, ((SW-20) / 2, 10), ((SW-20) / 2, SH-60), 4)
    pygame.draw.circle(screen, BLUE, ((SW-20)/2, (SH-70)/2), 40, 4)

def check_score():
    # TO check if ball touches the base and increment opponent score
    if football.rect.x < 8:
        reset_pos()
        Player2.score += 1

    elif football.rect.x > SW - 35:
        reset_pos()
        Player1.score += 1

def reset_pos():
    print_text(" Press Enter to", (SW / 2 - 80, SH / 2 - 50), 30, pygame.Color('yellow'))
    print_text("    Continue ", (SW / 2 - 80, SH / 2 - 30), 30, pygame.Color('yellow'))
    pygame.display.flip()

    football.speed = random.choice([[5, 5], [5, -5], [-5, 5], [-5, -5]])
    football.rect.x = random.randrange(360, 430)
    football.rect.y = random.randrange(50, SH - 120)
    Player1.rect.center = 18, (SH - 70) / 2
    Player2.rect.center = SW - 18, (SH - 70) / 2
    global paused
    paused = True

def gameplay():
    # Game logic
    global game_Running,paused
    while not game_Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_Running = True

            keys = pygame.key.get_pressed()
            # Check for any player movements
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_w]: Player1.change[1] = -5
                if keys[pygame.K_s]: Player1.change[1] = 5
                if keys[pygame.K_UP]: Player2.change[1] = -5
                if keys[pygame.K_DOWN]: Player2.change[1] = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    Player1.change[1] = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Player2.change[1] = 0

        # Restrain the players from moving beyond the border
        Player1.rect = Player1.rect.move(Player1.change)
        if Player1.rect.y < 5: Player1.rect.y = 6
        elif Player1.rect.y > 520: Player1.rect.y = 519
        Player2.rect = Player2.rect.move(Player2.change)
        if Player2.rect.y < 5: Player2.rect.y = 6
        elif Player2.rect.y > 520: Player2.rect.y = 519

        if football.rect.y < 5 or football.rect.y > SH-85:
            football.speed[1] *= -1

        bgrnd()

        keys = pygame.key.get_pressed()
        if football.rect.colliderect(Player1.rect) or football.rect.colliderect(Player2.rect):
            football.speed[0] = -football.speed[0]
            if football.speed[1] < 0:
                if (football.rect.colliderect(Player1.rect) and keys[pygame.K_s]) or (football.rect.colliderect(Player2.rect) and keys[pygame.K_DOWN]):
                    football.speed[1] = -football.speed[1]
            else:
                if (football.rect.colliderect(Player1.rect) and keys[pygame.K_w]) or (football.rect.colliderect(Player2.rect) and keys[pygame.K_UP]):
                    football.speed[1] = -football.speed[1]

        football.rect = football.rect.move(football.speed)
        all_sprites_list.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
        if football.rect.x < 8 or football.rect.x > SW - 35 :
            check_score()
            if Player1.score == MAX_SCORE or Player2.score == MAX_SCORE:
                game_Running = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    paused = False
                    Player1.change[1] = Player2.change[1] = 0

def intro():
    bgrdIMG = pygame.image.load('pingpong.png').convert()
    bgrdIMG_center = bgrdIMG.get_rect().center
    screen.blit(bgrdIMG, (SW/2-bgrdIMG_center[0], SH/2-bgrdIMG_center[1]))
    print_text("WELCOME TO PING PONG GAME", (220, 280), 32, (0, 255, 255))
    text2 = print_text("PRESS ENTER TO START", (270, 310), 28, GREEN)
    text3 = print_text("PRESS ENTER TO START", (270, 310), 28, (255, 0, 255))

    flag =0
    while True:
        if not flag:
            screen.blit(text2, (270, 310))
            pygame.display.flip()
            pygame.time.wait(30)
            screen.blit(text3, (270, 310))
            # pygame.display.flip()

        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            screen.fill(pygame.Color("Dark Green"))
            flag = 1
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    intro()
    reset_pos()
    gameplay()
    while True:
        for event in pygame.event.get():
            screen.fill(BLACK)
            print_text("##### SCORE #####", (300, 100), 30, pygame.Color('yellow'))
            print_text("PLAYER1 :" + str(Player1.score) + " - PLAYER2 :" + str(Player2.score), (265, 150), 30, WHITE)
            winner = "Player1" if Player1.score > Player2.score else "Player2"
            print_text(winner + " WINNER", (280, 300), 40, BLUE)
            clock.tick(FPS)
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_q] or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
