from memory import Memory
from display import Display
from keyboard import Keyboard
from pltfm import Platform
from cpu import CPU
from ops import OPS
from clock import Clock
from constants import CPU_FREQ, DT_FREQ, ST_FREQ, REFRESH_RATE

import pygame


key_map = {
    pygame.K_1: 0x1,
    pygame.K_2: 0x2,
    pygame.K_3: 0x3,
    pygame.K_4: 0xC,
    pygame.K_q: 0x4,
    pygame.K_w: 0x5,
    pygame.K_e: 0x6,
    pygame.K_r: 0xD,
    pygame.K_a: 0x7,
    pygame.K_s: 0x8,
    pygame.K_d: 0x9,
    pygame.K_f: 0xE,
    pygame.K_z: 0xA,
    pygame.K_x: 0x0,
    pygame.K_c: 0xB,
    pygame.K_v: 0xF,
}


class Chip8:
    def __init__(self):
        self.mem = Memory()
        self.display = Display()
        self.keyboard = Keyboard()
        self.ops = OPS()
        self.cpu = CPU(self.mem, self.display, self.keyboard, self.ops)
        self.platform = Platform()
        self.cpu_clock = None
        self.dt_clock = None
        self.st_clock = None

    def load_rom(self, path):
        with open(path, 'rb') as f:
            rom_data = list(f.read())

        rom_size = len(rom_data)

        for i in range(rom_size):
            addr = 0x200 + i
            self.mem.write(addr, rom_data[i])

    def idle_event(self):
        if self.st_clock and self.st_clock.tick():
            beep = self.cpu.cycle_st()

        if self.dt_clock and self.dt_clock.tick():
            self.cpu.cycle_dt()

        if self.cpu_clock and self.cpu_clock.tick():
            self.cpu.cycle()

            if self.display.redraw:
                self.platform.clear()
                self.display.draw(self.platform)
                self.platform.present()

    def keydown(self, event):
        if event.key in key_map:
            val = key_map[event.key]
            self.keyboard.push_keypress(val)
            self.keyboard.press_key(val)

    def keyup(self, event):
        if event.key in key_map:
            val = key_map[event.key]
            self.keyboard.lift_key(val)

    def run(self):
        self.cpu_clock = Clock(CPU_FREQ)
        self.dt_clock = Clock(DT_FREQ)
        self.st_clock = Clock(ST_FREQ)

        pygame.init()
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.keydown(event)

                if event.type == pygame.KEYUP:
                    self.keyup(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    done = True

            self.idle_event()
