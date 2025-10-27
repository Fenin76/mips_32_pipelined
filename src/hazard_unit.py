"""
Hazard Detection Unit for MIPS pipeline
Detects data hazards and control hazards
"""

class HazardDetectionUnit:
    """Detects and handles pipeline hazards"""
    
    def __init__(self):
        self.stall_signal = False
    
    def detect_load_use_hazard(self, id_ex_reg, if_id_reg):
        """
        Detect load-use data hazard
        Occurs when an instruction tries to use data being loaded
        
        Args:
            id_ex_reg: ID/EX pipeline register
            if_id_reg: IF/ID pipeline register
        Returns:
            True if hazard detected, False otherwise
        """
        id_ex_data = id_ex_reg.read()
        if_id_data = if_id_reg.read()
        
        # Check if previous instruction is a load
        if id_ex_data.get('control', {}).get('mem_read', 0) == 1:
            # Extract rs and rt from current instruction
            instruction = if_id_data.get('instruction', 0)
            rs = (instruction >> 21) & 0x1F
            rt = (instruction >> 16) & 0x1F
            
            # Check if load destination matches current source
            id_ex_rt = id_ex_data.get('rt', 0)
            if id_ex_rt != 0 and (id_ex_rt == rs or id_ex_rt == rt):
                self.stall_signal = True
                return True
        
        self.stall_signal = False
        return False
    
    def should_stall(self):
        """Return current stall signal"""
        return self.stall_signal


class ForwardingUnit:
    """Handles data forwarding to resolve hazards"""
    
    # Forwarding control values
    FORWARD_NONE = 0  # No forwarding
    FORWARD_EX_MEM = 1  # Forward from EX/MEM
    FORWARD_MEM_WB = 2  # Forward from MEM/WB
    
    def __init__(self):
        self.forward_a = self.FORWARD_NONE
        self.forward_b = self.FORWARD_NONE
    
    def detect_forwarding(self, id_ex_reg, ex_mem_reg, mem_wb_reg):
        """
        Detect if forwarding is needed for ALU inputs
        
        Args:
            id_ex_reg: ID/EX pipeline register
            ex_mem_reg: EX/MEM pipeline register
            mem_wb_reg: MEM/WB pipeline register
        Returns:
            (forward_a, forward_b): Forwarding control signals
        """
        id_ex_data = id_ex_reg.read()
        ex_mem_data = ex_mem_reg.read()
        mem_wb_data = mem_wb_reg.read()
        
        rs = id_ex_data.get('rs', 0)
        rt = id_ex_data.get('rt', 0)
        
        ex_mem_write_reg = ex_mem_data.get('write_reg', 0)
        mem_wb_write_reg = mem_wb_data.get('write_reg', 0)
        
        ex_mem_reg_write = ex_mem_data.get('control', {}).get('reg_write', 0)
        mem_wb_reg_write = mem_wb_data.get('control', {}).get('reg_write', 0)
        
        # Forward A (for rs)
        self.forward_a = self.FORWARD_NONE
        if ex_mem_reg_write and ex_mem_write_reg != 0 and ex_mem_write_reg == rs:
            # EX hazard
            self.forward_a = self.FORWARD_EX_MEM
        elif mem_wb_reg_write and mem_wb_write_reg != 0 and mem_wb_write_reg == rs:
            # MEM hazard
            self.forward_a = self.FORWARD_MEM_WB
        
        # Forward B (for rt)
        self.forward_b = self.FORWARD_NONE
        if ex_mem_reg_write and ex_mem_write_reg != 0 and ex_mem_write_reg == rt:
            # EX hazard
            self.forward_b = self.FORWARD_EX_MEM
        elif mem_wb_reg_write and mem_wb_write_reg != 0 and mem_wb_write_reg == rt:
            # MEM hazard
            self.forward_b = self.FORWARD_MEM_WB
        
        return self.forward_a, self.forward_b
    
    def get_forwarding_signals(self):
        """Return current forwarding signals"""
        return self.forward_a, self.forward_b
