import pygame
from pygame.math import Vector2


class Label:
    def __init__(self, pos, text, text_size, text_color=(0, 0, 0), bg_color=None, bold=False, italic=False):
        self.pos = Vector2(pos)

        self.text_color = text_color
        self.bg_color = bg_color

        self.font = pygame.font.SysFont("Arial", text_size, bold, italic)
        self.text = self.font.render(text, True, text_color, bg_color)
        self.rect = self.text.get_rect(topleft=self.pos)

    def update(self, text):
        self.text = self.font.render(text, True, self.text_color, self.bg_color)

    def render(self, surface):
        surface.blit(self.text, self.rect)