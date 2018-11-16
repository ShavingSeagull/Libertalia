import pygame
from globals import *
from user_data import nations

class InputBox:

    def __init__(self, x, y, w, h, font, size, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = black
        self.rect_color = black
        self.text = text
        self.size = int(size)
        self.font = pygame.font.Font(font, self.size)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.rect_color = red if self.active else black
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    user_input = self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def return_input(self):
        return self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, surface):
        # Blit the text.
        surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+1))
        # Blit the rect.
        pygame.draw.rect(surface, self.rect_color, self.rect, 2)

class Button:

    def __init__(self, x, y, w, h, image, font=None, size=32, text='', action=None):
        self.x = x
        self.y = y
        self.width = int(w)
        self.height = int(h)
        self.image = image
        self.img_surface = pygame.transform.scale(image, (self.width, self.height))
        self.img_rect = self.img_surface.get_rect()
        self.color = black
        self.text = text
        self.font = pygame.font.Font(font, size)
        self.action = action

    def handle_event(self, event):
        self.mouse = pygame.mouse.get_pos()
        if self.x + self.width > self.mouse[0] > self.x and self.y + self.height > self.mouse[1] > self.y:
            self.color = red
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.action()
        else:
            self.color = black

    def draw(self, surface):
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.txt_rect = self.txt_surface.get_rect()
        self.img_surface.blit(
            self.txt_surface, (self.img_rect[2] / 2 - self.txt_rect[2] / 2, self.img_rect[3] / 2 - self.txt_rect[3] / 2)
        )
        surface.blit(self.img_surface, (self.x, self.y))

class MenuButton(Button):
    def draw(self, surface):
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.txt_rect = self.txt_surface.get_rect()
        self.img_surface.blit(
            self.txt_surface, (self.img_rect[2] / 2 - self.txt_rect[2] / 2, self.img_rect[3] / 2 - (self.txt_rect[3] / 100) * 60)
        )
        surface.blit(self.img_surface, (self.x, self.y))

class NationSelect:
    def __init__(self, x, y, font, text, size, nation):
        self.x = x
        self.y = y
        self.color = black
        self.text = text
        self.size = int(size)
        self.font = pygame.font.Font(font, self.size)
        self.nation = nation

    def handle_event(self, event):
        self.mouse = pygame.mouse.get_pos()
        if nations[self.nation] == True:
            self.color = red
        else:
            self.color = black

        if self.x + self.txt_rect[2] > self.mouse[0] > self.x and self.y + self.txt_rect[3] > self.mouse[1] > self.y:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if nations[self.nation] == False:
                    for i in nations:
                        if nations[i] == True:
                            nations[i] = False
                    nations[self.nation] = True

    def draw(self, surface):
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.txt_rect = self.txt_surface.get_rect()
        surface.blit(self.txt_surface, (self.x, self.y))
