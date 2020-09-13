def gen_decode_dict():
    ret = {}

    addr_fn = lambda x: ((x[0] & 0xF) << 8) + x[1]
    reg_fn = lambda x: x[0] & 0xF
    reg_b_fn = lambda x: (x[1] & 0xF0) >> 4
    byte_fn = lambda x: x[1]
    nibble_fn = lambda x: x[1] & 0xF
    opcode_fn = lambda x: x

    def set_all_but_first(first, name, fns):
        for i in range(0x10):
            for j in range(0x10):
                for k in range(0x10):
                    ret[first, i, j, k] = (name, fns)

    def set_all_but_first_and_last(first, last, name, fns):
        for i in range(0x10):
            for j in range(0x10):
                ret[first, i, j, last] = (name, fns)

    def set_second(first, third, fourth, name, fns):
        for i in range(0x10):
            ret[first, i, third, fourth] = (name, fns)

    # 0
    set_all_but_first(0, 'SYS', (addr_fn,))
    ret[0, 0, 0xe, 0] = 'CLS', ()
    ret[0, 0, 0xe, 0xe] = 'RET', ()

    # 1
    set_all_but_first(1, 'JP', (addr_fn,))

    # 2
    set_all_but_first(2, 'CALL', (addr_fn,))

    # 3
    set_all_but_first(3, 'SE', (reg_fn, byte_fn))

    # 4
    set_all_but_first(4, 'SNE', (reg_fn, byte_fn))

    # 5
    set_all_but_first(5, 'INV', (opcode_fn,))
    set_all_but_first_and_last(5, 0, 'SER', (reg_fn, reg_b_fn))

    # 6
    set_all_but_first(6, 'LD', (reg_fn, byte_fn))

    # 7
    set_all_but_first(7, 'ADD', (reg_fn, byte_fn))

    # 8
    set_all_but_first(8, 'INV', (opcode_fn,))
    set_all_but_first_and_last(8, 0, 'LDR', (reg_fn, reg_b_fn))
    set_all_but_first_and_last(8, 1, 'OR', (reg_fn, reg_b_fn))
    set_all_but_first_and_last(8, 2, 'AND', (reg_fn, reg_b_fn))
    set_all_but_first_and_last(8, 3, 'XOR', (reg_fn, reg_b_fn))
    set_all_but_first_and_last(8, 4, 'ADDR', (reg_fn, reg_b_fn))
    set_all_but_first_and_last(8, 5, 'SUB', (reg_fn, reg_b_fn))
    set_all_but_first_and_last(8, 6, 'SHR', (reg_fn, reg_b_fn))
    set_all_but_first_and_last(8, 7, 'SUBN', (reg_fn, reg_b_fn))
    set_all_but_first_and_last(8, 0xe, 'SHL', (reg_fn, reg_b_fn))

    # 9
    set_all_but_first(9, 'INV', (opcode_fn,))
    set_all_but_first_and_last(9, 0, 'SNER', (reg_fn, reg_b_fn))

    # A
    set_all_but_first(0xa, 'LDA', (addr_fn,))

    # B
    set_all_but_first(0xb, 'JPO', (addr_fn,))

    # C
    set_all_but_first(0xc, 'RND', (reg_fn, byte_fn))

    # D
    set_all_but_first(0xd, 'DRW', (reg_fn, reg_b_fn, nibble_fn))

    # E
    set_all_but_first(0xe, 'INV', (opcode_fn,))
    set_second(0xe, 9, 0xe, 'SKP', (reg_fn,))
    set_second(0xe, 0xa, 1, 'SKNP', (reg_fn,))

    # F
    set_all_but_first(0xf, 'INV', (opcode_fn,))
    set_second(0xf, 0, 7, 'LDDT', (reg_fn,))
    set_second(0xf, 0, 0xa, 'LDKP', (reg_fn,))
    set_second(0xf, 1, 5, 'STDT', (reg_fn,))
    set_second(0xf, 1, 8, 'STST', (reg_fn,))
    set_second(0xf, 1, 0xe, 'ADDA', (reg_fn,))
    set_second(0xf, 2, 9, 'LDSA', (reg_fn,))
    set_second(0xf, 3, 3, 'STDR', (reg_fn,))
    set_second(0xf, 5, 5, 'STRR', (reg_fn,))
    set_second(0xf, 6, 5, 'LDRR', (reg_fn,))

    return ret


class OPS:
    def __init__(self):
        self.decode_dict = gen_decode_dict()

    def decode(self, opcode):
        first = (opcode[0] & 0xF0) >> 4
        second = opcode[0] & 0xF
        third = (opcode[1] & 0xF0) >> 4
        fourth = (opcode[1] & 0xF)

        fn_name, fns = self.decode_dict[first, second, third, fourth]
        args = tuple([x(opcode) for x in fns])
        return fn_name, args
