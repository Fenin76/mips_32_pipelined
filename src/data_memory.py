"""
Data Memory for MIPS processor
Stores data for load/store instructions
"""

class DataMemory:
    """Data memory module"""
    
    def __init__(self, size=1024):
        """
        Initialize data memory
        Args:
            size: Number of 32-bit words
        """
        self.memory = [0] * size
        self.size = size
    
    def read(self, address):
        """
        Read word from memory
        Args:
            address: Byte address (must be word-aligned)
        Returns:
            32-bit word
        """
        word_addr = address // 4
        if 0 <= word_addr < self.size:
            return self.memory[word_addr]
        return 0
    
    def write(self, address, data):
        """
        Write word to memory
        Args:
            address: Byte address (must be word-aligned)
            data: 32-bit word to write
        """
        word_addr = address // 4
        if 0 <= word_addr < self.size:
            self.memory[word_addr] = self._to_32bit(data)
    
    def _to_32bit(self, value):
        """Convert to 32-bit signed integer"""
        value = value & 0xFFFFFFFF
        if value & 0x80000000:
            return value - 0x100000000
        return value
