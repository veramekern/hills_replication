#! /usr/bin/env python

import pygame
import os

# Constants
color_font = (30, 30, 30)
background_color = (255, 255, 255)
screen_w = 640
screen_h = 500
fps = 60
screen = pygame.display.set_mode((screen_w, screen_h), pygame.HWSURFACE |
                                 pygame.DOUBLEBUF | pygame.FULLSCREEN)


class Stimulus:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.font = pygame.font.Font(None, 30)

    def intro(self):
        self.surface.fill(background_color)
        text = self.font.render("Dat was de visuele zoektaak!",
                                1, color_font)
        self.surface.blit(text, (self.x - 135, self.y - 50))
        text = self.font.render("We gaan nu verder met de tweede scrabbletaak",
                                1, color_font)
        self.surface.blit(text, (self.x - 225, self.y - 15))
        text = self.font.render("Druk op de spatiebalk om verder te gaan",
                                1, color_font)
        self.surface.blit(text, (self.x - 195, self.y + 50))

        pygame.display.flip()
        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


class Main:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.surface = screen
        self.surface.fill(background_color)
        self.stimulus = Stimulus(screen)

    def main(self):
        self.stimulus.intro()
        clock = pygame.time.Clock()
        clock.tick(fps)

if __name__ == '__main__':
    run = Main()
    run.main()
