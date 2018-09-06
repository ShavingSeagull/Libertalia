import pygame
from pygame.locals import *

pygame.init()

pygame.display.set_caption('Libertalia')
clock = pygame.time.Clock()
display_width = 1200
display_height = 700
game_display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)

intro_background = pygame.image.load('intro_background2.jpg')
button_background = pygame.image.load('button_background.png')

# COLORS
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
red = pygame.Color(200,0,0)
bright_red = pygame.Color(255,0,0)
green = pygame.Color(0,200,0)
bright_green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)

def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def button(msg, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        if click[0] == 1 and action != None:
            action()

    small_text = pygame.font.Font('PirataOne-Regular.ttf', 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    #button_img = game_display.blit(button_background, text_rect)
    game_display.blit(text_surf, text_rect)

def quitgame():
    pygame.quit()
    quit()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == VIDEORESIZE:
                game_display = pygame.display.set_mode(event.dict['size'], RESIZABLE)
                game_display.blit(pygame.transform.scale(intro_background, event.dict['size']), (0, 0))
                pygame.display.update()

        #game_display.fill(white)
        #game_display.blit(intro_background, (0, 0))
        screen_surf = game_display.get_rect()
        # Sets the font size as a percentage of the screen width to make it dynamic
        large_text = pygame.font.Font('PirataOne-Regular.ttf', int(screen_surf[2] / 10))
        text_surf, text_rect = text_objects('Libertalia', large_text, black)
        text_rect.center = ((screen_surf[2] / 1.3), (screen_surf[3] / 8))
        game_display.blit(text_surf, text_rect)

        # Button images
        game_display.blit(pygame.transform.scale(button_background, (int(screen_surf[2] / 6), int(screen_surf[3] / 8))),
                          ((screen_surf[2] / 1.4), (screen_surf[3] / 4)))
        game_display.blit(pygame.transform.scale(button_background, (int(screen_surf[2] / 6), int(screen_surf[3] / 8))),
                          ((screen_surf[2] / 1.4), (screen_surf[3] / 4)))
        game_display.blit(pygame.transform.scale(button_background, (int(screen_surf[2] / 6), int(screen_surf[3] / 8))),
                          ((screen_surf[2] / 1.4), (screen_surf[3] / 4)))
        game_display.blit(pygame.transform.scale(button_background, (int(screen_surf[2] / 6), int(screen_surf[3] / 8))),
                          ((screen_surf[2] / 1.4), (screen_surf[3] / 4)))

        button('Cast Off!', (screen_surf[2] / 1.3), (screen_surf[3] / 6), 50, 50, game_loop)
        button('About', ((display_width / 4) * 2), 450, 100, 50, quitgame)
        button('Controls', ((display_width / 4) * 2.5), 450, 100, 50, quitgame)
        button('Quit', ((display_width / 4) * 3), 450, 100, 50, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
