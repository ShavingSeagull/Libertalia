import pygame
from pygame.locals import *

pygame.init()

pygame.display.set_caption('Libertalia')
clock = pygame.time.Clock()
display_width = 1200
display_height = 700
game_display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)

intro_background = pygame.image.load('intro_background.jpg')
button_background = pygame.image.load('button_background.png')
about_background = pygame.image.load('about_background.png')

# COLORS
white = (255,255,255)
black = (0,0,0)
red = (175,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)
blue = (0,0,255)

def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def button(msg, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    screen_surf = game_display.get_rect()
    small_text = pygame.font.Font('PirataOne-Regular.ttf', int(screen_surf[2] / 40))
    img_surf = pygame.transform.scale(button_background, (int(screen_surf[2] / 6), int(screen_surf[3] / 8)))
    img_rect = img_surf.get_rect()
    img_rect.center = ((x + (width / 2)), (y + (height / 2)))

    # Button hovering
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        text_surf, text_rect = text_objects(msg, small_text, red)
        if click[0] == 1 and action != None:
            action()
    else:
        text_surf, text_rect = text_objects(msg, small_text, black)

    text_rect.center = ((x + (width / 2)), (y + (height / 2.5)))
    game_display.blit(img_surf, img_rect)
    game_display.blit(text_surf, text_rect)

def blit_text(surface, text, pos, color=black):
    screen_surf = game_display.get_rect()
    small_text = pygame.font.Font('PirataOne-Regular.ttf', int(screen_surf[2] / 50))
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = small_text.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    max_width -= int(screen_surf[2] / 10 * 1)
    x, y = pos
    for line in words:
        for word in line:
            word_surface = small_text.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row

def about():
    screen_surf = game_display.get_rect()
    text = "Libertalia is a game inspired by the fabled location of Libertalia, Madagascar.\nSupposedly founded by " \
           "Captain James Misson (although other reports cite Henry Avery), Libertalia functioned as a pirate utopia, " \
           "a free man's land away from the oppressive monarchies of Europe. Other pirates are known to have founded " \
           "colonies and cities, so it isn't a stretch of the imagination to think that they may have actually taken " \
           "the opportunity to found their own country, too.\nAs a player, your goal is to trade and pillage your way " \
           "across the Caribbean, amassing your fortune while staying out of the hands of the European authorities!"

    img_surf = pygame.transform.scale(about_background, (int(screen_surf[2] / 10 * 7), int(screen_surf[3] / 10 * 7)))
    img_rect = img_surf.get_rect()
    blit_text(img_surf, text, (img_rect[2] / 10 * 1, img_rect[3] / 8 * 1))
    game_display.blit(img_surf, (screen_surf[2] / 85, screen_surf[3] / 4))


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

        button('Cast Off!', (screen_surf[2] / 1.25), (screen_surf[3] / 4), 50, 50, game_loop)
        button('About', (screen_surf[2] / 1.25), (screen_surf[3] / 2.65), 50, 50, about)
        button('Controls', (screen_surf[2] / 1.25), (screen_surf[3] / 2), 50, 50, quitgame)
        button('Quit', (screen_surf[2] / 1.25), (screen_surf[3] / 1.6), 50, 50, quitgame)

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
