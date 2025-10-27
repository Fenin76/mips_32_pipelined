"""
MIPS 32-bit 5-stage Pipelined Processor
Integrates all components and implements the pipeline
"""

from .alu import ALU
from .register_file import RegisterFile
from .instruction_memory import InstructionMemory
from .data_memory import DataMemory
from .control_unit import ControlUnit
from .pipeline_registers import IF_ID_Register, ID_EX_Register, EX_MEM_Register, MEM_WB_Register
from .hazard_unit import HazardDetectionUnit, ForwardingUnit


class MIPSPipeline:
    """5-stage pipelined MIPS processor"""
    
    def __init__(self, instr_mem_size=1024, data_mem_size=1024):
        """
        Initialize MIPS pipeline processor
        Args:
            instr_mem_size: Size of instruction memory (in words)
            data_mem_size: Size of data memory (in words)
        """
        # Components
        self.alu = ALU()
        self.registers = RegisterFile()
        self.instr_mem = InstructionMemory(instr_mem_size)
        self.data_mem = DataMemory(data_mem_size)
        self.control = ControlUnit()
        
        # Pipeline registers
        self.if_id = IF_ID_Register()
        self.id_ex = ID_EX_Register()
        self.ex_mem = EX_MEM_Register()
        self.mem_wb = MEM_WB_Register()
        
        # Hazard handling
        self.hazard_unit = HazardDetectionUnit()
        self.forwarding_unit = ForwardingUnit()
        
        # Program counter
        self.pc = 0
        
        # Statistics
        self.cycle_count = 0
        self.instruction_count = 0
        self.stall_count = 0
    
    def load_program(self, instructions, start_address=0):
        """
        Load program into instruction memory
        Args:
            instructions: List of 32-bit instructions
            start_address: Starting byte address
        """
        self.instr_mem.load_program(instructions, start_address)
        self.pc = start_address
    
    def run(self, max_cycles=1000, verbose=False):
        """
        Run the processor for a specified number of cycles
        Args:
            max_cycles: Maximum number of cycles to run
            verbose: Print debug information
        """
        for cycle in range(max_cycles):
            self.cycle_count = cycle
            
            if verbose:
                print(f"\n=== Cycle {cycle} ===")
                print(f"PC: {self.pc}")
            
            # Check for program termination (all stages idle)
            if self._is_pipeline_idle():
                break
            
            # Stage 1: Compute next values for all stages (in reverse order)
            wb_updates = self.writeback_stage(verbose)
            mem_updates = self.memory_stage(verbose)
            ex_updates = self.execute_stage(verbose)
            id_updates = self.decode_stage(verbose)
            if_updates = self.fetch_stage(verbose)
            
            # Stage 2: Update pipeline registers (clock edge)
            self._update_pipeline_registers(if_updates, id_updates, ex_updates, mem_updates)
        
        if verbose:
            print(f"\n=== Execution Complete ===")
            print(f"Total cycles: {self.cycle_count}")
            print(f"Instructions executed: {self.instruction_count}")
            print(f"Stalls: {self.stall_count}")
    
    def fetch_stage(self, verbose=False):
        """IF: Instruction Fetch stage"""
        # Check for stall
        if self.hazard_unit.should_stall():
            # Don't fetch new instruction
            if verbose:
                print("IF: Stalled")
            return None  # Don't update IF/ID
        
        # Fetch instruction
        instruction = self.instr_mem.read(self.pc)
        
        if verbose:
            print(f"IF: Fetching instruction 0x{instruction:08x} from address {self.pc}")
        
        # Prepare IF/ID update
        if_id_update = {
            'pc': self.pc,
            'instruction': instruction
        }
        
        # Increment PC
        self.pc += 4
        
        return if_id_update
    
    def decode_stage(self, verbose=False):
        """ID: Instruction Decode stage"""
        if_id_data = self.if_id.read()
        instruction = if_id_data.get('instruction', 0)
        pc = if_id_data.get('pc', 0)
        
        if instruction == 0:
            # NOP (no operation)
            return {}
        
        # Decode instruction fields
        opcode = (instruction >> 26) & 0x3F
        rs = (instruction >> 21) & 0x1F
        rt = (instruction >> 16) & 0x1F
        rd = (instruction >> 11) & 0x1F
        shamt = (instruction >> 6) & 0x1F
        funct = instruction & 0x3F
        immediate = instruction & 0xFFFF
        
        # Sign extend immediate
        if immediate & 0x8000:
            immediate = immediate | 0xFFFF0000
        
        # Get control signals
        control_signals = self.control.decode(instruction)
        
        # Read registers
        read_data1 = self.registers.read(rs)
        read_data2 = self.registers.read(rt)
        
        # Detect hazards
        hazard = self.hazard_unit.detect_load_use_hazard(self.id_ex, self.if_id)
        if hazard:
            self.stall_count += 1
            if verbose:
                print(f"ID: Load-use hazard detected, stalling")
            # Insert bubble (nop)
            # Stall PC and IF/ID
            self.pc -= 4
            return {}
        
        if verbose:
            print(f"ID: Decoded opcode={opcode:02x}, rs=${rs}, rt=${rt}, rd=${rd}")
        
        # Prepare ID/EX update
        id_ex_update = {
            'pc': pc,
            'read_data1': read_data1,
            'read_data2': read_data2,
            'immediate': immediate,
            'rs': rs,
            'rt': rt,
            'rd': rd,
            'funct': funct,
            'control': control_signals
        }
        
        return id_ex_update
    
    def execute_stage(self, verbose=False):
        """EX: Execute stage"""
        id_ex_data = self.id_ex.read()
        
        if not id_ex_data:
            return {}
        
        control = id_ex_data.get('control', {})
        
        # Get forwarding signals
        forward_a, forward_b = self.forwarding_unit.detect_forwarding(
            self.id_ex, self.ex_mem, self.mem_wb
        )
        
        # Select ALU input A (with forwarding)
        alu_input_a = id_ex_data.get('read_data1', 0)
        if forward_a == ForwardingUnit.FORWARD_EX_MEM:
            alu_input_a = self.ex_mem.read().get('alu_result', 0)
        elif forward_a == ForwardingUnit.FORWARD_MEM_WB:
            mem_wb_data = self.mem_wb.read()
            mem_wb_control = mem_wb_data.get('control', {})
            if mem_wb_control.get('mem_to_reg', 0):
                alu_input_a = mem_wb_data.get('mem_data', 0)
            else:
                alu_input_a = mem_wb_data.get('alu_result', 0)
        
        # Select ALU input B (with forwarding)
        alu_input_b = id_ex_data.get('read_data2', 0)
        if forward_b == ForwardingUnit.FORWARD_EX_MEM:
            alu_input_b = self.ex_mem.read().get('alu_result', 0)
        elif forward_b == ForwardingUnit.FORWARD_MEM_WB:
            mem_wb_data = self.mem_wb.read()
            mem_wb_control = mem_wb_data.get('control', {})
            if mem_wb_control.get('mem_to_reg', 0):
                alu_input_b = mem_wb_data.get('mem_data', 0)
            else:
                alu_input_b = mem_wb_data.get('alu_result', 0)
        
        # Save forwarded value for store instructions (write_data needs forwarding too)
        write_data_forwarded = alu_input_b
        
        # Use immediate if ALUSrc is 1
        if control.get('alu_src', 0):
            alu_input_b = id_ex_data.get('immediate', 0)
        
        # Get ALU control signal
        alu_op = control.get('alu_op', 0)
        funct = id_ex_data.get('funct', 0)
        alu_control = self.control.get_alu_control(alu_op, funct)
        
        # Perform ALU operation
        alu_result, zero_flag = self.alu.execute(alu_input_a, alu_input_b, alu_control)
        
        # Determine write register
        if control.get('reg_dst', 0):
            write_reg = id_ex_data.get('rd', 0)
        else:
            write_reg = id_ex_data.get('rt', 0)
        
        if verbose:
            print(f"EX: ALU operation ({alu_input_a}, {alu_input_b}) -> result={alu_result}, zero={zero_flag}")
        
        # Prepare EX/MEM update
        ex_mem_update = {
            'pc': id_ex_data.get('pc', 0),
            'alu_result': alu_result,
            'write_data': write_data_forwarded,  # Use forwarded value for stores
            'write_reg': write_reg,
            'zero_flag': zero_flag,
            'branch_offset': id_ex_data.get('immediate', 0),  # Store offset for branches
            'control': control
        }
        
        return ex_mem_update
    
    def memory_stage(self, verbose=False):
        """MEM: Memory Access stage"""
        ex_mem_data = self.ex_mem.read()
        
        if not ex_mem_data:
            return {}
        
        control = ex_mem_data.get('control', {})
        alu_result = ex_mem_data.get('alu_result', 0)
        
        # Memory operations
        mem_data = 0
        if control.get('mem_read', 0):
            mem_data = self.data_mem.read(alu_result)
            if verbose:
                print(f"MEM: Reading from address {alu_result}, data={mem_data}")
        
        if control.get('mem_write', 0):
            write_data = ex_mem_data.get('write_data', 0)
            self.data_mem.write(alu_result, write_data)
            if verbose:
                print(f"MEM: Writing {write_data} to address {alu_result}")
        
        # Handle branches
        branch_taken = False
        branch_target = 0
        if control.get('branch', 0):
            zero_flag = ex_mem_data.get('zero_flag', False)
            if (control['branch'] == 1 and zero_flag) or \
               (control['branch'] == 2 and not zero_flag):
                # Branch taken
                branch_taken = True
                branch_offset = ex_mem_data.get('branch_offset', 0)
                branch_target = ex_mem_data.get('pc', 0) + 4 + (branch_offset << 2)
                if verbose:
                    print(f"MEM: Branch taken to {branch_target}")
        
        # Prepare MEM/WB update
        mem_wb_update = {
            'alu_result': alu_result,
            'mem_data': mem_data,
            'write_reg': ex_mem_data.get('write_reg', 0),
            'control': control,
            'branch_taken': branch_taken,  # Pass branch info to update logic
            'branch_target': branch_target
        }
        
        return mem_wb_update
    
    def writeback_stage(self, verbose=False):
        """WB: Write Back stage"""
        mem_wb_data = self.mem_wb.read()
        
        if not mem_wb_data:
            return None
        
        control = mem_wb_data.get('control', {})
        
        if control.get('reg_write', 0):
            write_reg = mem_wb_data.get('write_reg', 0)
            
            # Select data to write back
            if control.get('mem_to_reg', 0):
                write_data = mem_wb_data.get('mem_data', 0)
            else:
                write_data = mem_wb_data.get('alu_result', 0)
            
            self.registers.write(write_reg, write_data)
            self.instruction_count += 1
            
            if verbose:
                print(f"WB: Writing {write_data} to register ${write_reg}")
        
        return None
    
    def _update_pipeline_registers(self, if_updates, id_updates, ex_updates, mem_updates):
        """Update all pipeline registers (simulates clock edge)"""
        # Check if branch was taken
        branch_taken = mem_updates and mem_updates.get('branch_taken', False)
        
        if branch_taken:
            # Update PC to branch target (will be used by IF in next cycle)
            branch_target = mem_updates.get('branch_target', 0)
            self.pc = branch_target
            
            # Flush instructions after branch (IF, ID, EX stages)
            self.if_id.update({})
            self.id_ex.update({})
            self.ex_mem.update({})
        else:
            # Normal update
            if if_updates is not None:
                self.if_id.update(if_updates)
            
            if id_updates is not None:
                self.id_ex.update(id_updates)
            
            if ex_updates is not None:
                self.ex_mem.update(ex_updates)
        
        # Always update MEM/WB
        if mem_updates is not None:
            self.mem_wb.update(mem_updates)
    
    def _is_pipeline_idle(self):
        """Check if pipeline is completely idle"""
        return (self.if_id.read().get('instruction', 0) == 0 and
                not self.id_ex.read() and
                not self.ex_mem.read() and
                not self.mem_wb.read())
    
    def get_register_state(self):
        """Return current register file state"""
        return self.registers.get_all_registers()
    
    def get_statistics(self):
        """Return execution statistics"""
        return {
            'cycles': self.cycle_count,
            'instructions': self.instruction_count,
            'stalls': self.stall_count,
            'cpi': self.cycle_count / max(self.instruction_count, 1)
        }
