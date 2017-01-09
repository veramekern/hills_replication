#! /usr/bin/env python

import pygame
import random
import sys
from math import sin, cos, radians
import numpy as np
from pygame.locals import *
from timeit import default_timer as timer


def rotatePolygon(polygon, theta):
    """Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees"""
    theta = radians(theta)
    rotatedPolygon = []
    for corner in polygon:
        rotatedPolygon.append((corner[0]*cos(theta)-corner[1]*sin(theta),
                               corner[0]*sin(theta)+corner[1]*cos(theta)))
    return rotatedPolygon


def movePolygon(polygon, x, y):
    """Moves the given polygon which consists of corners represented as (x, y)"""
    movedPolygon = []
    for corner in polygon:
        movedPolygon.append((corner[0]+x, corner[1]+y))
    return movedPolygon


def clockHand(size, theta, xloc, yloc):
    dx = int(cos(radians(-theta)) * size)
    dy = int(sin(radians(-theta)) * size)
    return xloc + dx, yloc + dy


class Agent:
    def __init__(self):
        self.position = (100.0, 100.0)
        self.speed = 0
        self.direction = random.randint(0, 359)
        self.total_turned = 0
        self.total_food = 0
        self.total_turned_after_food = 0
        self.last_food_time = 0
        self.last_angle = self.direction
        self.last_angle_timestamp = timer()
        self.total_avg_turned = 0

    def move(self):
        self.position = (self.position[0] + self.speed * cos(radians(self.direction)),
                         self.position[1] + self.speed * sin(radians(self.direction)))
        self.position = np.clip(self.position, 0, 199)


class Environment:
    def __init__(self):
        self.map = np.zeros((200, 200))

    def gen_diffuse(self, num_patches=624):
        mapSurface = pygame.Surface((200, 200), flags=0)
        mapSurface.fill((0, 0, 0))
        for i in range(num_patches):
            xpos = random.randint(0, 200)
            ypos = random.randint(0, 200)
            pygame.draw.polygon(mapSurface, (0, 0, 255),
                                ((xpos-1, ypos), (xpos, ypos-1),
                                 (xpos+1, ypos), (xpos, ypos+1)))
        return mapSurface

    def gen_patchy(self, num_patches=4):
        mapSurface = pygame.Surface((200, 200), flags=0)
        overlaps = True
        while overlaps is True:
            mapSurface.fill((0, 0, 0))
            for i in range(num_patches):
                xpos = random.randint(0+19, 200-19)
                ypos = random.randint(0+19, 200-19)
                pygame.draw.polygon(mapSurface, (0, 0, 255),
                                    ((xpos-19, ypos), (xpos, ypos-19),
                                     (xpos+19, ypos), (xpos, ypos+19)))
            pxarray = pygame.PixelArray(mapSurface)
            if np.count_nonzero(np.array(pxarray) == 0) == 36956:  # If patches don't overlap there are 36956 black pixels
                overlaps = False
        return mapSurface


class App:
    def __init__(self, subject, condition, trial_time, debug=False):
        self._running = True
        self._display_surf = None
        self.debug = debug
        self.size = self.width, self.height = 600, 600
        self.subjectID = subject
        self.condition = condition
        self.trialNum = 0
        self.trialStartTime = 0
        self.trial_time = trial_time
        if self.debug is True:
            self.visiblePath = True
        else:
            self.visiblePath = False

    def draw_info_overlay(self):
        loc = (int(round(self.agent.position[0]*3)),
               int(round(self.agent.position[1]*3)))
        polygon_points = rotatePolygon([[0, 10], [-5, -10], [5, -10]],
                                       (self.agent.direction + 270) % 360)
        polygon_points = movePolygon(polygon_points, loc[0], loc[1])
        pygame.draw.polygon(self._display_surf, (0, 0, 0),
                            polygon_points, 0)

        # font = pygame.font.Font(None, 40)
        # text = font.render("score: " + str(self.agent.total_food), 1,
        #                    (100, 100, 100))
        # textpos = text.get_rect(topleft=(10, 10))
        # self._display_surf.blit(text, textpos)

        if timer() - self.trialStartTime < 3:
            font = pygame.font.Font(None, 40)
            text = font.render("Klaar?", 1, (200, 200, 200))
            textpos = text.get_rect(center=(self._display_surf.get_width() / 2,
                                            self._display_surf.get_height() / 3))
            self._display_surf.blit(text, textpos)

        if timer() - self.trialStartTime >= 3:
            pygame.draw.circle(self._display_surf, (128, 128, 128),
                               (self._display_surf.get_width() - 30, 30), 15)
            xpos, ypos = clockHand(15, (timer()*180) % 360,
                                   self._display_surf.get_width() - 30, 30)
            pygame.draw.line(self._display_surf, (255, 255, 255),
                             (self._display_surf.get_width() - 30, 30),
                             (xpos, ypos), 2)

    def init_datafile(self, filename=None):
        if filename is None:
            filename = str(self.subjectID) + "_foraging" + ".txt"
        f = open(filename, 'w')
        output = 'subjectID,condition,trial_num,timespent,food_eaten,turn_angle,angle_after_food,total_avg_turned\n'
        f.write(output)
        f.close()

    def write_data(self, filename=None):
        if filename is None:
            filename = str(self.subjectID) + "_foraging" + ".txt"
        f = open(filename, 'a')
        output = str(self.subjectID) + "," + \
                 self.condition + "," + \
                 str(self.trialNum) + "," + \
                 str(timer() - self.trialStartTime) + "," + \
                 str(self.agent.total_food) + "," + \
                 str(self.agent.total_turned) + "," + \
                 str(self.agent.total_turned_after_food) + "," + \
                 str(self.agent.total_avg_turned) + "\n"
        f.write(output)
        f.close()

    def on_init(self):
        pygame.init()
        self.init_datafile()
        self.clock = pygame.time.Clock()
        self._display_surf = pygame.display.set_mode(self.size,
                                                     pygame.HWSURFACE |
                                                     pygame.DOUBLEBUF |
                                                     pygame.FULLSCREEN)


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == KEYDOWN and event.key == K_j:
            self.agent.direction = (self.agent.direction - 35)%360
            self.agent.total_turned += 35
            if timer() - self.agent.last_food_time < 0.3 and self.agent.last_food_time > 0:
                self.agent.total_turned_after_food += 35
        elif event.type == KEYDOWN and event.key == K_l:
            self.agent.direction = (self.agent.direction + 35)%360
            self.agent.total_turned += 35
            if timer() - self.agent.last_food_time < 0.3 and self.agent.last_food_time > 0:
                self.agent.total_turned_after_food += 35

    def on_loop(self):
        pygame.mouse.set_visible(False)
        if self.agent.speed == 0 and timer() - self.trialStartTime > 3:
            self.agent.speed = 0.333
        self.agent.move()
        if timer() - self.agent.last_angle_timestamp > 0.3:
            self.agent.total_avg_turned += abs((((self.agent.direction - self.agent.last_angle) + 180) % 360) - 180)
            self.agent.last_angle = self.agent.direction
            self.agent.last_angle_timestamp = timer()
        position = (int(round(self.agent.position[0])),
                    int(round(self.agent.position[1])))
        mappxarray = pygame.PixelArray(self.mapSurface)
        seenpxarray = pygame.PixelArray(self.seenSurface)
        if self.visiblePath is True: seenpxarray[position[0], position[1]] = pygame.Color(255, 255, 255)
        if mappxarray[position[0], position[1]] > 0:
            if seenpxarray[position[0],position[1]] == self.seenSurface.map_rgb((255,255,255)):
                self.agent.total_food += 1
                self.agent.last_food_time = timer()
            seenpxarray[position[0], position[1]] = pygame.Color(0, 255, 0)

    def on_render(self):
        black = 0, 0, 0
        self._display_surf.fill(black)
        self._display_surf.blit(pygame.transform.scale(self.seenSurface,
                                                       (600, 600)), (0, 0))
        self.draw_info_overlay()
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def run_trial(self, trialNum):
        self._running = True
        self.trialNum = trialNum
        self.env = Environment()
        if self.condition == "d":
            self.mapSurface = self.env.gen_diffuse()
        elif self.condition == "c":
            self.mapSurface = self.env.gen_patchy()
        self.seenSurface = pygame.Surface((200, 200), flags=0)
        self.seenSurface.fill((255, 255, 255))
        self.agent = Agent()
        self.trialStartTime = timer()
        while self._running:
            self.clock.tick(60)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            if timer()-self.trialStartTime > self.trial_time:
                self._running = False
        self.write_data()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        for trialNum in range(5):
            self.run_trial(trialNum)

        self.on_cleanup()


if __name__ == "__main__":
    debug = sys.argv[3]
    if debug == "f":
        trial_time = 120.0
    else:
        trial_time = 5.0

    subject_ID = sys.argv[1]
    if sys.argv[2] == "r":
        condition = random.choice(("c", "d"))
    else:
        condition = sys.argv[2]

    theApp = App(subject_ID, condition, trial_time, debug=False)
    theApp.on_execute()
