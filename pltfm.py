from constants import DISPLAY_W, DISPLAY_H, W_MULT, H_MULT, BLACK, WHITE
import pygame
import tkinter as tk


class Platform:
    def __init__(self):
        self.window = tk.Tk()
        self.h = H_MULT * DISPLAY_H
        self.w = W_MULT * DISPLAY_W
        self.display_surface = pygame.display.set_mode((self.w, self.h))
        self.pxarray = pygame.PixelArray(self.display_surface)

    def draw_pixel(self, x, y):
        start_x = W_MULT * x
        end_x = start_x + W_MULT
        start_y = H_MULT * y
        end_y = start_y + H_MULT
        self.pxarray[start_x:end_x, start_y:end_y] = WHITE

    def clear(self):
        self.pxarray[:, :] = BLACK

    def present(self):
        pygame.display.update()
