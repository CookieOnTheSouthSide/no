import pygame
from pygame.math import Vector2
from random import randint
import sys

from widgets import Label


class Ramen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = Vector2(randint(40, 560), -20)
        self.velocity = Vector2(0, randint(4, 8))

        self.image = pygame.Surface((40, 40))
        self.image.fill("#FFFF00")
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self):
        self.pos += self.velocity
        self.rect = self.image.get_rect(topleft=self.pos)

        if self.pos.y > 610:
            self.kill()

    def render(self, surface):
        surface.blit(self.image, self.pos)


# Bowl class. Defines all functions of the bowl entity.
class Bowl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = Vector2(300, 500)
        self.velocity = Vector2()

        self.image = pygame.Surface((80, 60))
        self.image.fill("black")

        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self):
        self.pos += self.velocity
        self.pos.x = (self.pos.x % 590)

        self.rect = self.image.get_rect(topleft=self.pos)

    def event_handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.velocity.x = -5
            if event.key == pygame.K_d:
                self.velocity.x = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.velocity.x = max(self.velocity.x, 0)
            if event.key == pygame.K_d:
                self.velocity.x = min(self.velocity.x, 0)

    def render(self, surface):
        surface.blit(self.image, self.pos)


# Game manager/handler
class Game:
    def __init__(self):
        # Pygame setup
        pygame.init()
        pygame.display.set_caption("How Much Raman?")
        self.screen = pygame.display.set_mode((600, 600))

        self.clock = pygame.time.Clock()

        # Timer
        self.spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_timer, 400)

        # Characters
        self.bowl = Bowl()
        self.ramens = pygame.sprite.Group()
        self.ramens.add(Ramen())

        self.score = 0
        self.score_label = Label((240, 0), f"Score: {self.score}", 48)

    def run(self):
        while True:
            # Drawing
            self.screen.fill("#0AEEEE")
            self.score_label.render(self.screen)
            self.bowl.render(self.screen)

            for ramen in self.ramens:
                ramen.render(self.screen)

            # Event handling
            for event in pygame.event.get():
                self.bowl.event_handle(event)

                if event.type == self.spawn_timer:
                    self.ramens.add(Ramen())

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Updating
            self.bowl.update()

            for ramen in self.ramens:
                ramen.update()

            collisions = pygame.sprite.spritecollide(self.bowl, self.ramens, True)
            for _ in collisions:
                self.score += 1

            self.score_label.update(f"Score: {self.score}")

            self.clock.tick(60)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
