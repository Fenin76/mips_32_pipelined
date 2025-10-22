"""
Register File for MIPS processor
32 general-purpose registers (32-bit each)
"""

class RegisterFile:
    """MIPS register file with 32 registers"""
    
    def __init__(self):
        # 32 registers, each 32-bit, $0 is always 0
        self.registers = [0] * 32
    
    def read(self, reg_num):
        """
        Read from a register
        Args:
            reg_num: Register number (0-31)
        Returns:
            32-bit value from register
        """
        if 0 <= reg_num < 32:
            return self.registers[reg_num]
        return 0
    
    def write(self, reg_num, value):
        """
        Write to a register
        Args:
            reg_num: Register number (0-31)
            value: 32-bit value to write
        Note: $0 is always 0 and cannot be written
        """
        if 0 < reg_num < 32:  # Register 0 is hardwired to 0
            self.registers[reg_num] = self._to_32bit(value)
    
    def _to_32bit(self, value):
        """Convert to 32-bit signed integer"""
        value = value & 0xFFFFFFFF
        if value & 0x80000000:
            return value - 0x100000000
        return value
    
    def get_all_registers(self):
        """Return a copy of all registers for debugging"""
        return self.registers.copy()
    
    def reset(self):
        """Reset all registers to 0"""
        self.registers = [0] * 32
