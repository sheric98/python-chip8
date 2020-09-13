from constants import DISPLAY_H, DISPLAY_W
import numpy as np


class Display:
    def __init__(self):
        self.pixels = np.zeros((DISPLAY_W, DISPLAY_H), dtype=bool)
        self.redraw = True

    def clear(self):
        self.pixels = np.zeros((DISPLAY_W, DISPLAY_H), dtype=bool)

    def set_pixel(self, x, y, pixel):
        x = x % DISPLAY_W
        y = y % DISPLAY_H
        if self.pixels[x, y] != pixel:
            self.redraw = True

        erased = self.pixels[x, y] and pixel
        self.pixels[x, y] ^= pixel
        return erased

    def height(self):
        return DISPLAY_H

    def draw(self, pltfrm):
        for y in range(DISPLAY_H):
            for x in range(DISPLAY_W):
                if self.pixels[x, y]:
                    pltfrm.draw_pixel(x, y)
        self.redraw = False
