"""
MIPS Assembly Utilities
Helper functions to create MIPS instructions
"""

def r_type(opcode, rs, rt, rd, shamt, funct):
    """
    Create R-type instruction
    Format: opcode(6) | rs(5) | rt(5) | rd(5) | shamt(5) | funct(6)
    """
    instruction = (
        ((opcode & 0x3F) << 26) |
        ((rs & 0x1F) << 21) |
        ((rt & 0x1F) << 16) |
        ((rd & 0x1F) << 11) |
        ((shamt & 0x1F) << 6) |
        (funct & 0x3F)
    )
    return instruction


def i_type(opcode, rs, rt, immediate):
    """
    Create I-type instruction
    Format: opcode(6) | rs(5) | rt(5) | immediate(16)
    """
    instruction = (
        ((opcode & 0x3F) << 26) |
        ((rs & 0x1F) << 21) |
        ((rt & 0x1F) << 16) |
        (immediate & 0xFFFF)
    )
    return instruction


def j_type(opcode, address):
    """
    Create J-type instruction
    Format: opcode(6) | address(26)
    """
    instruction = (
        ((opcode & 0x3F) << 26) |
        (address & 0x3FFFFFF)
    )
    return instruction


# R-type instructions
def add(rd, rs, rt):
    """ADD: rd = rs + rt"""
    return r_type(0x00, rs, rt, rd, 0, 0x20)


def sub(rd, rs, rt):
    """SUB: rd = rs - rt"""
    return r_type(0x00, rs, rt, rd, 0, 0x22)


def and_inst(rd, rs, rt):
    """AND: rd = rs & rt"""
    return r_type(0x00, rs, rt, rd, 0, 0x24)


def or_inst(rd, rs, rt):
    """OR: rd = rs | rt"""
    return r_type(0x00, rs, rt, rd, 0, 0x25)


def slt(rd, rs, rt):
    """SLT: rd = (rs < rt) ? 1 : 0"""
    return r_type(0x00, rs, rt, rd, 0, 0x2A)


def nor(rd, rs, rt):
    """NOR: rd = ~(rs | rt)"""
    return r_type(0x00, rs, rt, rd, 0, 0x27)


# I-type instructions
def addi(rt, rs, immediate):
    """ADDI: rt = rs + immediate"""
    return i_type(0x08, rs, rt, immediate)


def andi(rt, rs, immediate):
    """ANDI: rt = rs & immediate"""
    return i_type(0x0C, rs, rt, immediate)


def ori(rt, rs, immediate):
    """ORI: rt = rs | immediate"""
    return i_type(0x0D, rs, rt, immediate)


def slti(rt, rs, immediate):
    """SLTI: rt = (rs < immediate) ? 1 : 0"""
    return i_type(0x0A, rs, rt, immediate)


def lw(rt, offset, rs):
    """LW: rt = Memory[rs + offset]"""
    return i_type(0x23, rs, rt, offset)


def sw(rt, offset, rs):
    """SW: Memory[rs + offset] = rt"""
    return i_type(0x2B, rs, rt, offset)


def beq(rs, rt, offset):
    """BEQ: if (rs == rt) PC = PC + 4 + (offset << 2)"""
    return i_type(0x04, rs, rt, offset)


def bne(rs, rt, offset):
    """BNE: if (rs != rt) PC = PC + 4 + (offset << 2)"""
    return i_type(0x05, rs, rt, offset)


# J-type instructions
def j(address):
    """J: PC = (PC & 0xF0000000) | (address << 2)"""
    return j_type(0x02, address)


def nop():
    """NOP: No operation"""
    return 0x00000000


# Register names for convenience
REGISTERS = {
    'zero': 0, 'at': 1,
    'v0': 2, 'v1': 3,
    'a0': 4, 'a1': 5, 'a2': 6, 'a3': 7,
    't0': 8, 't1': 9, 't2': 10, 't3': 11, 't4': 12, 't5': 13, 't6': 14, 't7': 15,
    's0': 16, 's1': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21, 's6': 22, 's7': 23,
    't8': 24, 't9': 25,
    'k0': 26, 'k1': 27,
    'gp': 28, 'sp': 29, 'fp': 30, 'ra': 31
}
