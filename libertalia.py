import pygame
from pygame.locals import *

pygame.init()

# IMAGES
icon = pygame.image.load('logo.jpg')
intro_background = pygame.image.load('intro_background.jpg')
button_background = pygame.image.load('button_background.png')
about_background = pygame.image.load('about_background.png')

# FONTS
pirata = 'PirataOne-Regular.ttf'
respira = 'DellaRespira-Regular.ttf'
pinyon = 'PinyonScript-Regular.ttf'

# COLORS
white = (255,255,255)
black = (0,0,0)
red = (175,0,0)
bright_red = (255,0,0)
green = (0,200,0)
bright_green = (0,255,0)
blue = (0,0,255)

# GENERAL SETUP
pygame.display.set_caption('Libertalia')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
info_object = pygame.display.Info()
display_width = 1200
display_height = 700
game_display = pygame.display.set_mode((info_object.current_w, info_object.current_h), pygame.FULLSCREEN)
#game_display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
screen_surf = game_display.get_rect()


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def button(msg, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    small_text = pygame.font.Font(pirata, int(screen_surf[2] / 40))
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

def fade(width, height, delay):
    fade = pygame.Surface((width, height))
    fade.fill(black)
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        game_display.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(delay)

def text_fade(text, color, font, size, display_delay, fade_delay):
    custom_font = pygame.font.Font(font, size)
    label = custom_font.render(text, 1, color)
    new_surf = pygame.Surface(custom_font.size(text))
    new_surf.blit(label,(0,0))
    game_display.blit(new_surf, (100,100))
    pygame.display.update()

    for x in range (255):
        game_display.fill(black)
        new_surf.set_alpha(0 + x)
        game_display.blit(new_surf, (100,100))
        pygame.display.update()
        pygame.time.delay(fade_delay)

    pygame.time.delay(display_delay)

    for y in range (255):
        game_display.fill(black)
        new_surf.set_alpha(255 - y)
        game_display.blit(new_surf, (100,100))
        pygame.display.update()
        pygame.time.delay(fade_delay)

# def blit_text(surface, text, pos, font, size, color=black):
#     custom_font = pygame.font.Font(font, size)
#     words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
#     space = custom_font.size(' ')[0]  # The width of a space.
#     max_width, max_height = surface.get_size()
#     max_width -= int(screen_surf[2] / 10 * 1)
#     x, y = pos
#     for line in words:
#         for word in line:
#             word_surface = custom_font.render(word, 0, color)
#             word_width, word_height = word_surface.get_size()
#             if x + word_width >= max_width:
#                 x = pos[0]  # Reset the x.
#                 y += word_height  # Start on new row.
#             surface.blit(word_surface, (x, y))
#             x += word_width + space
#         x = pos[0]  # Reset the x.
#         y += word_height  # Start on new row

def blit_text(surface, text, pos, font, size, color=black, fade=False, display_delay=3000, fade_delay=10):
    custom_font = pygame.font.Font(font, size)
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = custom_font.size(' ')[0]  # The width of a space.
    buffer = (screen_surf[2] / 100) * 5
    max_width, max_height = surface.get_size()
    x, y = pos
    x_buffer = x + (screen_surf[2] / 100) * 5
    x += x_buffer
    temp_surface = pygame.Surface((max_width, max_height))
    for line in words:
        for word in line:
            word_surface = custom_font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width + buffer >= max_width:
                x = x_buffer  # Reset the x.
                y += word_height  # Start on new row.

            if not fade:
                surface.blit(word_surface, (x, y))
            else:
                temp_surface.blit(word_surface, (x, y))

            x += word_width + space

        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row

    if fade == True:
        for alpha in range(255):
            surface.fill(black)
            temp_surface.set_alpha(0 + alpha)
            surface.blit(temp_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(fade_delay)

        pygame.time.delay(display_delay)

        for alpha2 in range(255):
            surface.fill(black)
            temp_surface.set_alpha(255 - alpha2)
            surface.blit(temp_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(fade_delay)


def game_loop_intro_text():
    screen_surface = game_display.get_rect()
    text = "Yes, I do heartily repent. I repent I had not done more mischief; and that we did not cut the throats of " \
           "them that took us, and I am extremely sorry that you aren't hanged as well as we.\n\n\n" \
           "                                - Anonymous pirate, asked on the gallows if he repented."

    blit_text(game_display, text, (0, screen_surface[3] / 4), pinyon, int(screen_surface[2] / 40), red, True, 3000, 5)

def about():
    text = "Libertalia is a game inspired by the fabled location of Libertalia, Madagascar.\nSupposedly founded by " \
           "Captain James Misson (although other reports cite Henry Avery), Libertalia functioned as a pirate utopia, " \
           "a free man's land away from the oppressive monarchies of Europe. Other pirates are known to have founded " \
           "colonies and cities, so why couldn't they may have actually taken the opportunity to found their own" \
           " country, too?\nAs a player, your goal is to trade and pillage your way " \
           "across the Caribbean, amassing your fortune while staying out of the hands of the European authorities!"

    img_surf = pygame.transform.scale(about_background, (int(screen_surf[2] / 10 * 7), int(screen_surf[3] / 10 * 7)))
    img_rect = img_surf.get_rect()
    blit_text(img_surf, text, (img_rect[2] / 10 * 1, img_rect[3] / 8 * 1), respira, int(screen_surf[2] / 60))
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

        screen_surface = game_display.get_rect()
        # Sets the font size as a percentage of the screen width to make it dynamic
        small_text = pygame.font.Font('PirataOne-Regular.ttf', int(screen_surface[2] / 50))
        large_text = pygame.font.Font('PirataOne-Regular.ttf', int(screen_surface[2] / 10))
        title_surf, title_rect = text_objects('Libertalia', large_text, black)
        footer_surf, footer_rect = text_objects('© Pangaea Studios 2018', small_text, black)
        title_rect.center = ((screen_surface[2] / 1.3), (screen_surface[3] / 8))
        footer_rect.center = ((screen_surface[2] / 10), (screen_surface[3] / 10 * 9.5))
        game_display.blits(blit_sequence=((title_surf, title_rect), (footer_surf, footer_rect)))

        button('Cast Off!', (screen_surface[2] / 1.25), (screen_surface[3] / 4), 50, 50, game_loop)
        button('About', (screen_surface[2] / 1.25), (screen_surface[3] / 2.65), 50, 50, about)
        button('Controls', (screen_surface[2] / 1.25), (screen_surface[3] / 2), 50, 50, quitgame)
        button('Quit', (screen_surface[2] / 1.25), (screen_surface[3] / 1.6), 50, 50, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    game_exit = False
    fade(info_object.current_w, info_object.current_h, 8)
    game_loop_intro_text()
    while not game_exit:
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
