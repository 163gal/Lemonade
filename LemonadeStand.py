#!/usr/bin/env python

import pygame
from fortuneengine.GameEngine import GameEngine
from LemonadeMain import LemonadeMain
from LemonadeGui import LemonadeGui
from optparse import OptionParser

MAXIMUM_FONT_SIZE = 50


class LemonadeStand:
    def __init__(self):
        pygame.init()

    def run(self):
        screen_size = pygame.display.Info()
        self.width = screen_size.current_w
        self.height = screen_size.current_h
        self.difficulty = 0

        # Set font size based on screen size
        self.font_size = MAXIMUM_FONT_SIZE
        max_font_based_on_width = self.width / 35
        while self.font_size > max_font_based_on_width:
            self.font_size -= 1

        ge = GameEngine(self.width, self.height, always_draw=False)
        ge.add_object(
            'font',
            pygame.font.SysFont(pygame.font.get_default_font(), self.font_size))
        ge.add_object('main', LemonadeMain(self.difficulty))
        ge.add_object('gui', LemonadeGui())
        ge.start_main_loop()


if __name__ == "__main__":
    pygame.init()
    parser = OptionParser()
    parser.add_option("", "--width", dest="width", help="window width",
                      metavar="WIDTH", default=640, type="int")
    parser.add_option("", "--height", dest="height", help="window height",
                      metavar="HEIGHT", default=480, type="int")
    parser.add_option("-f", "--font", dest="font", help="font size",
                      metavar="SIZE", default=20, type="int")
    parser.add_option("-d", "--difficulty", dest="difficulty", help="difficulty level",
                      metavar="DIFFICULTY", default=0, type="int")
    (opts, args) = parser.parse_args()
    ge = GameEngine(width=opts.width, height=opts.height, always_draw=False)
    ge.add_object(
        'font', pygame.font.SysFont(pygame.font.get_default_font(), opts.font))
    ge.add_object('main', LemonadeMain(opts.difficulty))
    ge.add_object('gui', LemonadeGui())
    ge.start_main_loop()
