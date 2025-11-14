"""
Instruction Memory for MIPS processor
Stores program instructions
"""

class InstructionMemory:
    """Instruction memory module"""
    
    def __init__(self, size=1024):
        """
        Initialize instruction memory
        Args:
            size: Number of 32-bit instruction words
        """
        self.memory = [0] * size
        self.size = size
    
    def read(self, address):
        """
        Read instruction at given address
        Args:
            address: Byte address (must be word-aligned)
        Returns:
            32-bit instruction
        """
        # Convert byte address to word address
        word_addr = address // 4
        if 0 <= word_addr < self.size:
            return self.memory[word_addr]
        return 0
    
    def write(self, address, instruction):
        """
        Write instruction to memory
        Args:
            address: Byte address (must be word-aligned)
            instruction: 32-bit instruction
        """
        word_addr = address // 4
        if 0 <= word_addr < self.size:
            self.memory[word_addr] = instruction & 0xFFFFFFFF
    
    def load_program(self, instructions, start_address=0):
        """
        Load a program into instruction memory
        Args:
            instructions: List of 32-bit instructions
            start_address: Starting byte address
        """
        word_addr = start_address // 4
        for i, instr in enumerate(instructions):
            if word_addr + i < self.size:
                self.memory[word_addr + i] = instr & 0xFFFFFFFF
