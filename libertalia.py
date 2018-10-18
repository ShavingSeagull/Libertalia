from pygame_text_input import pygame_textinput
import pygame
from pygame.locals import *

pygame.init()

# IMAGES
icon = pygame.image.load('logo.jpg')
intro_background = pygame.image.load('intro_background.jpg')
button_background = pygame.image.load('button_background.png')
about_background = pygame.image.load('about_background.png')
wood_background = pygame.image.load('wood_background.jpg')
char_background = pygame.image.load('character_background.png')

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
scroll_beige = (236, 181, 65)

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
    """
    Function for setting surface fading. Useful for transitions.
    Doesn't need a predetermined surface, just the width and height
    of the area required to fade.

    width: the width required to fade
    height: the height required to fade
    delay: the delay in milliseconds between blits
    """
    fade = pygame.Surface((width, height))
    fade.fill(black)
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        game_display.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(delay)

# def text_fade(text, color, font, size, display_delay, fade_delay):
#     custom_font = pygame.font.Font(font, size)
#     label = custom_font.render(text, 1, color)
#     new_surf = pygame.Surface(custom_font.size(text))
#     new_surf.blit(label,(0,0))
#     game_display.blit(new_surf, (100,100))
#     pygame.display.update()
#
#     for x in range (255):
#         game_display.fill(black)
#         new_surf.set_alpha(0 + x)
#         game_display.blit(new_surf, (100,100))
#         pygame.display.update()
#         pygame.time.delay(fade_delay)
#
#     pygame.time.delay(display_delay)
#
#     for y in range (255):
#         game_display.fill(black)
#         new_surf.set_alpha(255 - y)
#         game_display.blit(new_surf, (100,100))
#         pygame.display.update()
#         pygame.time.delay(fade_delay)

def blit_text(surface, text, pos, font, size, buffer, color=black, fade=False, display_delay=3000, fade_delay=10):
    """
    Function for blitting blocks of text. Includes a word wrapping feature to
    ensure contents stays within the screen boundaries. Also includes an
    optional fade feature for fading blocks of text in and out.

    Normal text is blitted straight to the surface when the wrapping calculations
    have been completed. Faded text, however, blits to an invisible temporary
    surface first, then that surface is blitted to the screen. This is because
    each word in the text block is blitted one at a time after passing through
    the wrapping calculation. This is fine for normal text, but for faded text
    the result is one word fading in and out at a time. The temporary surface
    allows all words to be blitted to it first (one at a time), thus afterward
    allowing the whole text faded block to be blitted to the screen when that
    process has completed.

    surface: the chosen surface to blit to (usually the screen surface)
    text: the text block to blit
    pos: (x, y) coords. Must be a tuple
    font: the required font
    size: the required font size
    color: the required font color. Black (custom variable) by default
    fade: whether or not the fade effect is required. False by default
    display_delay: the required time allowance for the faded text to appear at full
                     opacity value. 3 seconds by default
    fade_delay: the required time allowance between blits for the text to fade in and out.
                  10 milliseconds by default
    """
    custom_font = pygame.font.Font(font, size)
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = custom_font.size(' ')[0]  # The width of a space.
    buffer = buffer
    max_width, max_height = surface.get_size()
    x, y = pos
    x_buffer = x + buffer
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

        x = x_buffer  # Reset the x.
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

    blit_text(
        game_display,
        text,
        (0, screen_surface[3] / 4),
        pinyon,
        int(screen_surface[2] / 40),
        int((screen_surface[2] / 100) * 5),
        red,
        True,
        3000,
        5
    )

def about():
    # WILL NEED TO BLIT THE INTRO BACKGROUND HERE IF YOU HAVE MORE OPTIONS THAN JUST 'ABOUT'
    # OTHERWISE THE ABOUT SCROLL WILL REMAIN ON THE SCREEN WHEN YOU CHOOSE ANOTHER OPTION
    text = "Libertalia is a game inspired by the fabled location of Libertalia, Madagascar.\n\nSupposedly founded by " \
           "Captain James Misson (although other reports cite Henry Avery), Libertalia functioned as a pirate utopia, " \
           "a free man's land away from the oppressive monarchies of Europe. Other pirates are known to have founded " \
           "colonies and cities, so why couldn't they may have actually taken the opportunity to found their own" \
           " country, too?\n\nAs a player, your goal is to trade and pillage your way " \
           "across the Caribbean, amassing your fortune while staying out of the hands of the European authorities!"

    img_surf = pygame.transform.scale(about_background, (int(screen_surf[2] / 10 * 7), int(screen_surf[3] / 10 * 7)))
    img_rect = img_surf.get_rect()
    blit_text(img_surf, text, (0, img_rect[3] / 8 * 1), respira, int(screen_surf[2] / 60), int((screen_surf[2] / 100) * 5))
    game_display.blit(img_surf, (screen_surf[2] / 85, screen_surf[3] / 4))

def quitgame():
    pygame.quit()
    quit()

def game_intro():
    intro = True
    game_display.blit(pygame.transform.scale(intro_background, (info_object.current_w, info_object.current_h)), (0, 0))

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if event.type == VIDEORESIZE:
            #     game_display = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            #     game_display.blit(pygame.transform.scale(intro_background, event.dict['size']), (0, 0))
            #     pygame.display.update()

        screen_surface = game_display.get_rect()
        # Sets the font size as a percentage of the screen width to make it dynamic
        small_text = pygame.font.Font(pirata, int(screen_surface[2] / 50))
        large_text = pygame.font.Font(pirata, int(screen_surface[2] / 10))
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

def char_creation_text_input(surface, pos):
    while True:
        events = pygame.event.get()
        text_input = pygame_textinput.TextInput(" ", pirata, int(screen_surf[2] / 50), 0, black, black)
        text_input.update(events)
        surface.blit(text_input.get_surface(), (pos))
        pygame.display.update()
        clock.tick(15)
        if text_input.update(events):
            input = text_input.get_text()
            return input

def character_creation():
    """
    Function for creating the playable character and ship.
    """
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.blit(wood_background, (0, 0))
        game_display.blit(pygame.transform.scale(char_background, (int(screen_surf[2] / 4 * 2), int(screen_surf[3] / 100 * 90))),
                          (screen_surf[2] / 4, screen_surf[3] / 100 * 5))

        header_text = pygame.font.Font(pirata, int(screen_surf[2] / 25))
        label_text = pygame.font.Font(pirata, int(screen_surf[2] / 50))
        header = header_text.render('Character Creation', 0, black)
        header_rect = header.get_rect()

        name = label_text.render('Pirate Name:', 0, black)
        age = label_text.render('Age:', 0, black)


        game_display.blit(header, (screen_surf[2] / 2 - header_rect[2] / 2, screen_surf[3] / 100 * 18))
        game_display.blit(name, (screen_surf[2] / 100 * 32, screen_surf[3] / 100 * 30))
        game_display.blit(age, (screen_surf[2] / 100 * 32, screen_surf[3] / 100 * 35))

        pygame.display.update()

        char_creation_text_input(game_display, (screen_surf[2] / 100 * 45, screen_surf[3] / 100 * 30))

        pygame.display.update()
        clock.tick(15)

def game_loop():
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        fade(info_object.current_w, info_object.current_h, 8)
        game_loop_intro_text()
        character_creation()

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
