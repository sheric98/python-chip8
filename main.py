import os
from chip8 import Chip8


if __name__ == '__main__':
    rom = input('What ROM would you like to play?\n').upper()
    path = os.path.join('ROMS', rom)
    chip8 = Chip8()
    chip8.load_rom(path)
    chip8.run()
