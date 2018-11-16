import pygame
from pygame.locals import *
from classes import *
from globals import *
from user_data import *

pygame.init()

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

# def button(msg, x, y, width, height, image, action=None):
#     mouse = pygame.mouse.get_pos()
#     click = pygame.mouse.get_pressed()
#
#     small_text = pygame.font.Font(pirata, int(screen_surf[2] / 40))
#     img_surf = pygame.transform.scale(image, (int(screen_surf[2] / 6), int(screen_surf[3] / 8)))
#     img_rect = img_surf.get_rect()
#     img_rect.center = ((x + (width / 2)), (y + (height / 2)))
#
#     # Button hovering
#     if x + width > mouse[0] > x and y + height > mouse[1] > y:
#         text_surf, text_rect = text_objects(msg, small_text, red)
#         if click[0] == 1 and action != None:
#             action()
#     else:
#         text_surf, text_rect = text_objects(msg, small_text, black)
#
#     text_rect.center = ((x + (width / 2)), (y + (height / 2.5)))
#     game_display.blit(img_surf, img_rect)
#     game_display.blit(text_surf, text_rect)

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
    # WILL NEED TO BLIT THE INTRO BACKGROUND HERE TO CLEAR THE SCREEN IF YOU HAVE MORE OPTIONS THAN JUST 'ABOUT'
    # OTHERWISE THE ABOUT SCROLL WILL REMAIN ON THE SCREEN WHEN YOU CHOOSE ANOTHER OPTION
    text = "Libertalia is a game inspired by the fabled location of Libertalia, Madagascar.\n\nSupposedly founded by " \
           "Captain James Misson (although other reports cite Henry Avery), Libertalia functioned as a pirate utopia, " \
           "a free man's land away from the oppressive monarchies of Europe. Other pirates are known to have founded " \
           "colonies and cities, so why couldn't they may have actually taken the opportunity to found their own" \
           " country, too?\n\nAs a player, your goal is to trade and pillage your way " \
           "across the Caribbean, amassing your fortune while staying out of the hands of the European authorities!"

    bg_surf = pygame.transform.scale(about_background, (int((screen_surf[2] / 10) * 7), int((screen_surf[3] / 10) * 7)))
    bg_rect = bg_surf.get_rect()

    blit_text(bg_surf, text, (0, bg_rect[3] / 8 * 1), respira, int(screen_surf[2] / 60), int((screen_surf[2] / 100) * 5))
    game_display.blit(bg_surf, (screen_surf[2] / 85, (screen_surf[3] / 100) * 22))

def quit_game():
    pygame.quit()
    quit()

def game_intro():
    intro = True
    game_display.blit(pygame.transform.scale(intro_background, (info_object.current_w, info_object.current_h)), (0, 0))
    screen_surface = game_display.get_rect()
    button_x = (screen_surface[2] / 100) * 70
    button_w = (screen_surface[2] / 100) * 20
    button_h = (screen_surface[3] / 100) * 10
    button_font_size = int((screen_surface[2] / 100) * 2.5)
    button_rect = close_button_img.get_rect()

    play_button = MenuButton(
        button_x,
        (screen_surface[3] / 100) * 25,
        button_w,
        button_h,
        button_background,
        pirata,
        button_font_size,
        'Cast Off!',
        game_loop
    )
    about_button = MenuButton(
        button_x,
        (screen_surface[3] / 100) * 36,
        button_w,
        button_h,
        button_background,
        pirata,
        button_font_size,
        'About',
        about
    )
    quit_button = MenuButton(
        button_x,
        (screen_surface[3] / 100) * 47,
        button_w,
        button_h,
        button_background,
        pirata,
        button_font_size,
        'Quit',
        quit_game
    )
    close_button = Button(
        (screen_surface[2] / 100) * 58,
        (screen_surface[3] / 100) * 76,
        button_rect[2],
        button_rect[3],
        close_button_img,
        action=game_intro
    )
    buttons = [play_button, about_button, quit_button, close_button]

    while intro:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            for button in buttons:
                button.handle_event(event)
                # Only draws the close button for the about picture if the button is clicked
                if about_button.x + about_button.width > mouse[0] > about_button.x and about_button.y + about_button.height > \
                        mouse[1] > about_button.y:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        close_button.draw(game_display)

            # if event.type == VIDEORESIZE:
            #     game_display = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            #     game_display.blit(pygame.transform.scale(intro_background, event.dict['size']), (0, 0))
            #     pygame.display.update()


        # Sets the font size as a percentage of the screen width to make it dynamic
        small_text = pygame.font.Font(pirata, int(screen_surface[2] / 50))
        large_text = pygame.font.Font(pirata, int(screen_surface[2] / 10))
        title_surf, title_rect = text_objects('Libertalia', large_text, black)
        footer_surf, footer_rect = text_objects('© Pangaea Studios 2018', small_text, black)
        title_rect.center = ((screen_surface[2] / 1.3), (screen_surface[3] / 8))
        footer_rect.center = ((screen_surface[2] / 10), (screen_surface[3] / 10 * 9.5))
        game_display.blits(blit_sequence=((title_surf, title_rect), (footer_surf, footer_rect)))

        play_button.draw(game_display)
        about_button.draw(game_display)
        quit_button.draw(game_display)

        pygame.display.update()
        clock.tick(30)

def character_creation():
    """
    Function for creating the playable character and ship.
    """
    label_width = (screen_surf[2] / 100) * 32

    input_x = (screen_surf[2] / 100) * 42
    input_width = 200
    input_height = 30
    input_font_size = screen_surf[2] / 50

    nation_y = (screen_surf[3] / 100) * 40.5
    nation_font_size = screen_surf[2] / 60

    name_input = InputBox(input_x, (screen_surf[3] / 100) * 30, input_width, input_height, pirata, input_font_size)
    age_input = InputBox(input_x, (screen_surf[3] / 100) * 35, input_width, input_height, pirata, input_font_size)
    ship_name_input = InputBox(input_x, (screen_surf[3] / 100) * 45, input_width, input_height, pirata, input_font_size)
    input_boxes = [name_input, age_input, ship_name_input]

    def next_screen():
        global char_name
        global age
        global ship_name

        char_name = name_input.return_input()
        age = age_input.return_input()
        ship_name = ship_name_input.return_input()

    british = NationSelect((screen_surf[2] / 100) * 42,
                           nation_y,
                           pirata,
                           'British',
                           nation_font_size,
                           'british',
                           )

    dutch = NationSelect((screen_surf[2] / 100) * 47.5,
                         nation_y,
                         pirata,
                         'Dutch',
                         nation_font_size,
                         'dutch',
                         )

    spanish = NationSelect((screen_surf[2] / 100) * 52.5,
                           nation_y,
                           pirata,
                           'Spanish',
                           nation_font_size,
                           'spanish',
                           )

    french = NationSelect((screen_surf[2] / 100) * 59,
                          nation_y,
                          pirata,
                          'French',
                          nation_font_size,
                          'french',
                          )
    nation_boxes = [british, dutch, spanish, french]

    next_button = Button((screen_surf[2] / 100) * 62,
                         (screen_surf[3] / 100) * 77,
                         (screen_surf[2] / 100) * 7,
                         (screen_surf[3] / 100) * 5,
                         skel_hand_right,
                         action=next_screen
    )

    header_text = pygame.font.Font(pirata, int(screen_surf[2] / 25))
    label_text = pygame.font.Font(pirata, int(screen_surf[2] / 50))
    header = header_text.render('Character Creation', 0, black)
    header_rect = header.get_rect()

    name = label_text.render('Pirate Name:', 0, black)
    age = label_text.render('Age:', 0, black)
    nationality = label_text.render('Nationality:', 0, black)
    ship_name = label_text.render('Ship Name:', 0, black)

    run = True
    while run:

        # Have to blit the contents first so that the event handler in the NationSelect class has a txt_rect
        # measurement populated to work with in accordance with its logic to change the color of the text to red or black.
        # Running the handler first means it's looking for a txt_rect measurement that doesn't yet exist - causing errors

        game_display.blit(wood_background, (0, 0))
        game_display.blit(
            pygame.transform.scale(char_background, (int(screen_surf[2] / 4 * 2), int(screen_surf[3] / 100 * 90))),
            (screen_surf[2] / 4, screen_surf[3] / 100 * 5)
        )
        game_display.blit(header, (screen_surf[2] / 2 - header_rect[2] / 2, screen_surf[3] / 100 * 18))
        game_display.blit(name, (label_width, (screen_surf[3] / 100) * 30))
        game_display.blit(age, (label_width, (screen_surf[3] / 100) * 35))
        game_display.blit(nationality, (label_width, (screen_surf[3] / 100) * 40))
        game_display.blit(ship_name, (label_width, (screen_surf[3] / 100) * 45))

        for box in input_boxes:
            box.draw(game_display)

        for box in nation_boxes:
            box.draw(game_display)

        # for x, y in nations.items():
        #     print(x, y)

        next_button.draw(game_display)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            for box in input_boxes:
                box.handle_event(event)

            for box in nation_boxes:
                box.handle_event(event)

            next_button.handle_event(event)

        for box in input_boxes:
            box.update()

        pygame.display.update()
        clock.tick(10)

def game_loop():
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        fade(info_object.current_w, info_object.current_h, 8)
        #game_loop_intro_text()
        character_creation()

        pygame.display.update()
        clock.tick(30)

game_intro()
game_loop()
pygame.quit()
quit()
