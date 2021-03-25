import pygame
import sys  # damit wir das Programm ohne Fehler schliessen können
import random


def floor_logic():  # zwei Böden die wir sich rotierend abwechseln lassen
    screen.blit(floor_surface, (floor_x, 860))
    screen.blit(floor_surface, (floor_x + 576, 860))


def create_pipe():  # Pipes spawnen
    random_pos = random.choice(pipe_height)
    bottom_pipe = pipe_sur.get_rect(midtop=(700, random_pos))
    top_pipe = pipe_sur.get_rect(midtop=(700, random_pos - 900))
    return bottom_pipe, top_pipe


def move_pipe(pipes):  # Pipes bewegen
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):  # Pipe manipulation
    for pipe in pipes:
        screen.blit(pipe_sur, pipe)


def check_collision(pipes):  # Berührungen überprüfen
    for pipe in pipes:
        if lennart_rect.colliderect(pipe):
            return True
    if lennart_rect.top <= -100 or lennart_rect.bottom >= 900:
        return True

    return False


def lennart_logic():
    new_lennart = lennart_animation[lennart_index]
    new_lennart_rect = new_lennart.get_rect(center=(100, lennart_rect.centery))
    return new_lennart, new_lennart_rect


pygame.init()
screen = pygame.display.set_mode((576, 1024))  # unser Fenster
clock = pygame.time.Clock()  # Framerate limitierung

# Spielvariabeln
downforce = 0.25  # Schwerkraft
lennart_movement = 0  # bewegung die wir mit Schwerkraft manipulieren
game_over = False

bg_surface = pygame.image.load(
    'assets/sprites/background-day.png').convert()  # läd unseren Hintergrund und konvertiert ihn in etwas mit dem man in Pygame arbeiten kann
floor_surface = pygame.image.load('assets/sprites/base.png').convert()
floor_x = 0

# der folgende Block code sind die import Befehle und ähnliches für den kopf
lennart_midflap = pygame.image.load('assets/sprites/lennart-midflap.png').convert_alpha()
lennart_downflap = pygame.image.load('assets/sprites/lennart-downflap.png').convert_alpha()
lennart_upflap = pygame.image.load('assets/sprites/lennart-upflap.png').convert_alpha()
lennart_animation = [lennart_downflap, lennart_midflap, lennart_upflap]
lennart_index = 0
lennart_sur = lennart_animation[lennart_index]
lennart_rect = lennart_sur.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1  # Neues Userevent für die Animation
pygame.time.set_timer(BIRDFLAP, 150)

pipe_sur = pygame.image.load('assets/sprites/pipe-vodka.png').convert()
pipe_ls = []  # Liste um alle Pipes zu speichern
SPAWNPIPE = pygame.USEREVENT  # Event das hilft Pipes zu spawnen
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 450, 550, 600, 500]  # höhe der Pipes

# end screen
game_over_sur = pygame.image.load('assets/sprites/gameOverOne.png')
game_over_rect = game_over_sur.get_rect(center=(288, 512))

while True:  # the game loop

    for event in pygame.event.get():  # event loop, schaut nach clicks, bewegungen etc
        if event.type == pygame.QUIT:  # X knopf oben rechts
            pygame.quit()  # closes das Fenster
            sys.exit()  # schließt endgültig, verhindert einen traceback Fehler
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over == False:  # wenn wir space drücken, springt lennart hoch
                lennart_movement = 0
                lennart_movement -= 10
            if event.key == pygame.K_SPACE and game_over == True:  # spiel neustart
                game_over = False
                pipe_ls.clear()
                lennart_rect.center = (100, 512)
                lennart_movement = 0
        if event.type == SPAWNPIPE:
            pipe_ls.extend(create_pipe())  # hängt die neuen Pipes an die Liste an
        if event.type == BIRDFLAP:  # hier wird durch die eigentlichen Animationen gewechselt
            if lennart_index < 2:
                lennart_index += 1
            else:
                lennart_index = 0
            lennart_sur, lennart_rect = lennart_logic()

    screen.blit(bg_surface, (0, 0))  # platziert den Hintergrund

    if game_over is False:
        # lennart
        lennart_movement += downforce
        lennart_rect.centery += lennart_movement
        screen.blit(lennart_sur, lennart_rect)
        game_over = check_collision(pipe_ls)

        # pipes
        pipe_ls = move_pipe(pipe_ls)
        draw_pipes(pipe_ls)
    else:
        screen.blit(game_over_sur, game_over_rect)

    # floor, nicht in der IF Bedingung damit sich der Boden weiter bewegt auch wenn man ein game over bekommt
    floor_x -= 1
    floor_logic()
    if floor_x <= -576:  # rotiert den Boden
        floor_x = 0

    pygame.display.update()  # updated jedes Frame vom Game
    clock.tick(120)  # 120 fps
