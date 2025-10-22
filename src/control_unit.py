"""
Control Unit for MIPS processor
Decodes instructions and generates control signals
"""

class ControlUnit:
    """Control unit for generating control signals"""
    
    # Opcode definitions
    OPCODE_R_TYPE = 0x00
    OPCODE_LW = 0x23
    OPCODE_SW = 0x2B
    OPCODE_BEQ = 0x04
    OPCODE_BNE = 0x05
    OPCODE_ADDI = 0x08
    OPCODE_ANDI = 0x0C
    OPCODE_ORI = 0x0D
    OPCODE_SLTI = 0x0A
    OPCODE_J = 0x02
    
    # Function codes for R-type instructions
    FUNCT_ADD = 0x20
    FUNCT_SUB = 0x22
    FUNCT_AND = 0x24
    FUNCT_OR = 0x25
    FUNCT_SLT = 0x2A
    FUNCT_NOR = 0x27
    
    def __init__(self):
        self.control_signals = {}
    
    def decode(self, instruction):
        """
        Decode instruction and generate control signals
        Args:
            instruction: 32-bit instruction
        Returns:
            Dictionary of control signals
        """
        opcode = (instruction >> 26) & 0x3F
        funct = instruction & 0x3F
        
        signals = {
            'reg_dst': 0,      # 0: rt, 1: rd
            'alu_src': 0,      # 0: register, 1: immediate
            'mem_to_reg': 0,   # 0: ALU result, 1: memory
            'reg_write': 0,    # Write to register file
            'mem_read': 0,     # Read from memory
            'mem_write': 0,    # Write to memory
            'branch': 0,       # Branch instruction
            'alu_op': 0,       # ALU operation type
            'jump': 0          # Jump instruction
        }
        
        if opcode == self.OPCODE_R_TYPE:
            # R-type instruction
            signals['reg_dst'] = 1
            signals['reg_write'] = 1
            signals['alu_op'] = 2  # Use funct field
            
        elif opcode == self.OPCODE_LW:
            # Load word
            signals['alu_src'] = 1
            signals['mem_to_reg'] = 1
            signals['reg_write'] = 1
            signals['mem_read'] = 1
            signals['alu_op'] = 0  # Add
            
        elif opcode == self.OPCODE_SW:
            # Store word
            signals['alu_src'] = 1
            signals['mem_write'] = 1
            signals['alu_op'] = 0  # Add
            
        elif opcode == self.OPCODE_BEQ:
            # Branch if equal
            signals['branch'] = 1
            signals['alu_op'] = 1  # Subtract
            
        elif opcode == self.OPCODE_BNE:
            # Branch if not equal
            signals['branch'] = 2
            signals['alu_op'] = 1  # Subtract
            
        elif opcode == self.OPCODE_ADDI:
            # Add immediate
            signals['alu_src'] = 1
            signals['reg_write'] = 1
            signals['alu_op'] = 0  # Add
            
        elif opcode == self.OPCODE_ANDI:
            # And immediate
            signals['alu_src'] = 1
            signals['reg_write'] = 1
            signals['alu_op'] = 3  # And
            
        elif opcode == self.OPCODE_ORI:
            # Or immediate
            signals['alu_src'] = 1
            signals['reg_write'] = 1
            signals['alu_op'] = 4  # Or
            
        elif opcode == self.OPCODE_SLTI:
            # Set less than immediate
            signals['alu_src'] = 1
            signals['reg_write'] = 1
            signals['alu_op'] = 5  # SLT
            
        elif opcode == self.OPCODE_J:
            # Jump
            signals['jump'] = 1
        
        self.control_signals = signals
        return signals
    
    def get_alu_control(self, alu_op, funct):
        """
        Generate ALU control signal based on ALU op and function code
        Args:
            alu_op: ALU operation type from control unit
            funct: Function field from instruction
        Returns:
            ALU control code
        """
        if alu_op == 0:  # Load/Store (Add)
            return 2  # ALU_ADD
        elif alu_op == 1:  # Branch (Subtract)
            return 6  # ALU_SUB
        elif alu_op == 2:  # R-type
            if funct == self.FUNCT_ADD:
                return 2  # ALU_ADD
            elif funct == self.FUNCT_SUB:
                return 6  # ALU_SUB
            elif funct == self.FUNCT_AND:
                return 0  # ALU_AND
            elif funct == self.FUNCT_OR:
                return 1  # ALU_OR
            elif funct == self.FUNCT_SLT:
                return 7  # ALU_SLT
            elif funct == self.FUNCT_NOR:
                return 12  # ALU_NOR
        elif alu_op == 3:  # ANDI
            return 0  # ALU_AND
        elif alu_op == 4:  # ORI
            return 1  # ALU_OR
        elif alu_op == 5:  # SLTI
            return 7  # ALU_SLT
        
        return 2  # Default to ADD
