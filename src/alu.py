"""
ALU (Arithmetic Logic Unit) for MIPS processor
Performs arithmetic and logical operations
"""

class ALU:
    """32-bit ALU with common MIPS operations"""
    
    # ALU Control codes
    ALU_AND = 0
    ALU_OR = 1
    ALU_ADD = 2
    ALU_SUB = 6
    ALU_SLT = 7
    ALU_NOR = 12
    
    def __init__(self):
        self.result = 0
        self.zero_flag = False
    
    def execute(self, a, b, alu_control):
        """
        Execute ALU operation
        Args:
            a: First operand (32-bit)
            b: Second operand (32-bit)
            alu_control: Operation code
        Returns:
            result: 32-bit result
            zero_flag: True if result is zero
        """
        # Ensure operands are 32-bit signed integers
        a = self._to_signed_32(a)
        b = self._to_signed_32(b)
        
        if alu_control == self.ALU_AND:
            self.result = a & b
        elif alu_control == self.ALU_OR:
            self.result = a | b
        elif alu_control == self.ALU_ADD:
            self.result = a + b
        elif alu_control == self.ALU_SUB:
            self.result = a - b
        elif alu_control == self.ALU_SLT:
            self.result = 1 if a < b else 0
        elif alu_control == self.ALU_NOR:
            self.result = ~(a | b)
        else:
            self.result = 0
        
        # Mask to 32 bits
        self.result = self._to_signed_32(self.result)
        self.zero_flag = (self.result == 0)
        
        return self.result, self.zero_flag
    
    def _to_signed_32(self, value):
        """Convert to 32-bit signed integer"""
        # Mask to 32 bits
        value = value & 0xFFFFFFFF
        # Convert to signed
        if value & 0x80000000:
            return value - 0x100000000
        return value
