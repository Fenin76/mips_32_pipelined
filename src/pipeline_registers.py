"""
Pipeline Registers for 5-stage MIPS pipeline
Stores data between pipeline stages
"""

class PipelineRegister:
    """Base class for pipeline registers"""
    
    def __init__(self):
        self.data = {}
        self.stall = False
        self.flush = False
    
    def update(self, new_data):
        """Update register with new data (on clock edge)"""
        if not self.stall:
            if self.flush:
                self.data = {}
                self.flush = False
            else:
                self.data = new_data.copy()
    
    def read(self):
        """Read current register data"""
        return self.data
    
    def set_stall(self, stall):
        """Set stall signal"""
        self.stall = stall
    
    def set_flush(self, flush):
        """Set flush signal"""
        self.flush = flush


class IF_ID_Register(PipelineRegister):
    """IF/ID pipeline register"""
    
    def __init__(self):
        super().__init__()
        self.data = {
            'pc': 0,
            'instruction': 0
        }


class ID_EX_Register(PipelineRegister):
    """ID/EX pipeline register"""
    
    def __init__(self):
        super().__init__()
        self.data = {
            'pc': 0,
            'read_data1': 0,
            'read_data2': 0,
            'immediate': 0,
            'rs': 0,
            'rt': 0,
            'rd': 0,
            'funct': 0,
            'control': {}
        }


class EX_MEM_Register(PipelineRegister):
    """EX/MEM pipeline register"""
    
    def __init__(self):
        super().__init__()
        self.data = {
            'pc': 0,
            'alu_result': 0,
            'write_data': 0,
            'write_reg': 0,
            'zero_flag': False,
            'control': {}
        }


class MEM_WB_Register(PipelineRegister):
    """MEM/WB pipeline register"""
    
    def __init__(self):
        super().__init__()
        self.data = {
            'alu_result': 0,
            'mem_data': 0,
            'write_reg': 0,
            'control': {}
        }
