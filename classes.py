import pygame
from globals import *

class InputBox:

    def __init__(self, x, y, w, h, font, size, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = black
        self.rect_color = black
        self.text = text
        self.font = pygame.font.Font(font, size)
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

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.rect_color, self.rect, 2)

class Button:

    def __init__(self, x, y, w, h, font, size, image, text='', action=None):
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
