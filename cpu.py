from constants import *
import random
import memory as mem


class CPU:
    def __init__(self, memory, display, keyboard, ops):
        self.v = [0] * 16
        self.i = 0
        self.pc = 0x200
        self.sp = 0
        self.dt = 0
        self.st = 0
        self.stack = [0] * 16
        self.memory = memory
        self.display = display
        self.keyboard = keyboard
        self.ops = ops

    def cycle_dt(self):
        if self.dt > 0:
            self.dt -= 1

    def cycle_st(self):
        if self.st > 0:
            self.st -= 1
        return self.st > 0

    def cycle(self):
        opcode = self.memory.bytes[self.pc:self.pc+2]
        self.pc += 2

        self.perform_fn(opcode)

    def perform_fn(self, opcode):
        fn_name, args = self.ops.decode(opcode)
        self.__getattribute__(fn_name)(*args)

    def SYS(self, addr):
        print('sys')

    def CLS(self):
        self.display.clear()

    def RET(self):
        self.sp -= 1
        self.pc = self.stack[self.sp]

    def JP(self, addr):
        self.pc = addr

    def CALL(self, addr):
        self.stack[self.sp] = self.pc
        self.sp += 1
        self.pc = addr

    def SE(self, reg, byte):
        if self.v[reg] == byte:
            self.pc += 2

    def SNE(self, reg, byte):
        if self.v[reg] != byte:
            self.pc += 2

    def SER(self, reg_a, reg_b):
        if self.v[reg_a] == self.v[reg_b]:
            self.pc += 2

    def LD(self, reg, byte):
        self.v[reg] = byte

    def ADD(self, reg, byte):
        self.v[reg] = (self.v[reg] + byte) % BYTE

    def LDR(self, reg_a, reg_b):
        self.v[reg_a] = self.v[reg_b]

    def OR(self, reg_a, reg_b):
        self.v[reg_a] |= self.v[reg_b]

    def AND(self, reg_a, reg_b):
        self.v[reg_a] &= self.v[reg_b]

    def XOR(self, reg_a, reg_b):
        self.v[reg_a] ^= self.v[reg_b]

    def ADDR(self, reg_a, reg_b):
        sum = self.v[reg_a] + self.v[reg_b]
        q = sum // BYTE
        r = sum % BYTE

        self.v[reg_a] = r
        self.v[0xf] = 1 if q else 0

    def SUB(self, reg_a, reg_b):
        sub = self.v[reg_a] - self.v[reg_b]
        flag = False
        if sub < 0:
            sub = (1 << 8) + sub
            flag = True
        self.v[reg_a] = sub
        self.v[0xf] = 0 if flag else 1

    def SHR(self, reg_a, reg_b):
        if SHIFT_QUIRK:
            reg_b = reg_a
        lsb = self.v[reg_b] & 1
        self.v[reg_a] = self.v[reg_b] >> 1
        self.v[0xf] = lsb

    def SUBN(self, reg_a, reg_b):
        sub = self.v[reg_b] - self.v[reg_a]
        flag = False
        if sub < 0:
            sub = (1 << 8) + sub
            flag = True
        self.v[reg_a] = sub
        self.v[0xf] = 0 if flag else 1

    def SHL(self, reg_a, reg_b):
        if SHIFT_QUIRK:
            reg_b = reg_a
        msb = (self.v[reg_b] >> 7) & 1
        self.v[reg_a] = self.v[reg_b] << 1
        self.v[0xf] = msb

    def SNER(self, reg_a, reg_b):
        if self.v[reg_a] != self.v[reg_b]:
            self.pc += 2

    def LDA(self, addr):
        self.i = addr

    def JPO(self, addr):
        self.pc = addr + self.v[0]

    def RND(self, reg, byte):
        self.v[reg] = byte & random.randrange(0, 0xFF)

    def DRW(self, reg_a, reg_b, nibble):
        x = self.v[reg_a]
        y = self.v[reg_b]
        h = nibble

        pixel_erased = False

        for offset_y in range(h):
            px_y = y + offset_y
            if not VERT_WRAP and px_y >= self.display.height():
                break

            byte = self.memory.read(self.i + offset_y)
            for offset_x in range(8):
                pixel = ((byte >> 7 - offset_x) & 1) == 1
                px_x = x + offset_x
                pixel_erased |= self.display.set_pixel(px_x, px_y, pixel)

        self.v[0xf] = 1 if pixel_erased else 0

    def SKP(self, reg):
        if self.keyboard.get_key(self.v[reg]):
            self.pc += 2

    def SKNP(self, reg):
        if not self.keyboard.get_key(self.v[reg]):
            self.pc += 2

    def LDDT(self, reg):
        self.v[reg] = self.dt

    def LDKP(self, reg):
        key = self.keyboard.wait_keypress()
        if key:
            self.v[reg] = key
        else:
            self.pc -= 2

    def STDT(self, reg):
        self.dt = self.v[reg]

    def STST(self, reg):
        self.st = self.v[reg]

    def ADDA(self, reg):
        sum = self.i + self.v[reg]
        q = sum // TWO_BYTES
        r = sum % TWO_BYTES
        self.i = r
        if ADDR_OVERFLOW_QUIRK:
            self.v[0xf] = 1 if q else 0

    def LDSA(self, reg):
        self.i = mem.SPRITES_ADDR + self.v[reg] * 5

    def STDR(self, reg):
        self.memory.write(self.i, self.v[reg] // 100)
        self.memory.write(self.i + 1, (self.v[reg] // 10) % 10)
        self.memory.write(self.i + 2, self.v[reg] % 10)

    def STRR(self, reg):
        for i in range(reg+1):
            addr = self.i + i
            self.memory.write(addr, self.v[i])
        if LOAD_STORE_QUIRK:
            self.i += reg + 1

    def LDRR(self, reg):
        for i in range(reg+1):
            addr = self.i + i
            self.v[i] = self.memory.read(addr)
        if LOAD_STORE_QUIRK:
            self.i += reg + 1

    def INV(self, opcode):
        print('invalid op code', opcode)
