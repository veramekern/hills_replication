#! /usr/bin/env python

import pygame
import os

# Constants
background_color = (255, 255, 255)
screen_w = 640
screen_h = 500
fps = 60
screen = pygame.display.set_mode((screen_w, screen_h), pygame.HWSURFACE |
                                 pygame.DOUBLEBUF | pygame.FULLSCREEN)


class Stimulus:
    def __init__(self, surface):
        self.surface = surface

    def intro(self):
        self.surface.fill(background_color)
        image = pygame.image.load(os.path.join("images",
                                               "intro_foraging.jpg")).convert()
        self.surface.blit(image, (50, 50))
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
