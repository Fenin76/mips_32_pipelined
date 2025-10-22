# MIPS Pipeline Architecture Documentation

## Overview

This document describes the architecture and implementation details of the 32-bit MIPS 5-stage pipelined processor.

## Pipeline Stages

### 1. Instruction Fetch (IF)
- Reads instruction from instruction memory using PC
- Updates IF/ID pipeline register with instruction and PC+4
- PC is incremented by 4 (one word) for next instruction

### 2. Instruction Decode (ID)
- Decodes instruction into fields (opcode, rs, rt, rd, immediate, etc.)
- Generates control signals using Control Unit
- Reads source registers from Register File
- Sign-extends immediate values
- Detects load-use hazards

### 3. Execute (EX)
- Performs ALU operations based on ALU control signal
- Implements data forwarding from later stages
- Selects ALU inputs based on instruction type
- Determines destination register (rd for R-type, rt for I-type)

### 4. Memory Access (MEM)
- Reads from or writes to Data Memory for load/store instructions
- Handles branch instructions by updating PC if branch is taken
- Flushes pipeline on taken branches

### 5. Write Back (WB)
- Writes result to destination register
- Selects between ALU result and memory data
- Updates instruction completion count

## Hazard Detection and Resolution

### Data Hazards

**Types of Data Hazards:**

1. **RAW (Read After Write)**: An instruction tries to read a register before a previous instruction writes to it.

**Detection:**
The Hazard Detection Unit checks if the previous instruction is a load and the current instruction uses the loaded data.

**Resolution:**
- **Forwarding**: Data is forwarded from later pipeline stages (EX/MEM or MEM/WB) to the EX stage
- **Stalling**: For load-use hazards, the pipeline is stalled for one cycle

### Control Hazards

**Branch Instructions:**
When a branch is taken, instructions that have entered the pipeline must be flushed.

**Resolution:**
- Branch decision is made in the MEM stage
- If branch is taken, IF/ID and ID/EX registers are flushed
- PC is updated to branch target

## Control Signals

The Control Unit generates the following signals:

- `reg_dst`: Select destination register (0=rt, 1=rd)
- `alu_src`: Select second ALU input (0=register, 1=immediate)
- `mem_to_reg`: Select write-back data (0=ALU result, 1=memory)
- `reg_write`: Enable register write
- `mem_read`: Enable memory read
- `mem_write`: Enable memory write
- `branch`: Branch instruction (1=BEQ, 2=BNE)
- `alu_op`: ALU operation type
- `jump`: Jump instruction

## Instruction Encoding

### R-Type Format
```
[opcode(6)] [rs(5)] [rt(5)] [rd(5)] [shamt(5)] [funct(6)]
```

### I-Type Format
```
[opcode(6)] [rs(5)] [rt(5)] [immediate(16)]
```

### J-Type Format
```
[opcode(6)] [address(26)]
```

## Register File

- 32 general-purpose 32-bit registers
- Register $0 is hardwired to 0
- Two read ports and one write port
- Registers are named: $zero, $at, $v0-$v1, $a0-$a3, $t0-$t9, $s0-$s7, $k0-$k1, $gp, $sp, $fp, $ra

## Memory Organization

### Instruction Memory
- Word-addressed (addresses must be multiple of 4)
- Stores program instructions
- Read-only during execution

### Data Memory
- Word-addressed (addresses must be multiple of 4)
- Stores program data
- Supports read and write operations

## Pipeline Performance

### Ideal CPI
In an ideal pipeline with no hazards: CPI = 1.0

### Actual CPI
```
CPI = (Total Cycles) / (Instructions Executed)
```

Factors affecting CPI:
- Data hazards requiring stalls
- Control hazards (branches)
- Structural hazards (not present in this implementation)

### Example Performance
For a program with:
- 10 instructions
- 2 stalls
- 5 pipeline fill cycles

Total cycles = 10 + 2 + 5 = 17
CPI = 17 / 10 = 1.7

## Implementation Details

### Python Simulation
This implementation is a functional simulator written in Python:
- Clock cycles are simulated explicitly
- Pipeline registers update on each cycle
- All operations complete within their designated stage
- Timing is cycle-accurate

### Limitations
- No cache hierarchy (instructions and data access in 1 cycle)
- Simplified memory model (infinite memory)
- No interrupts or exceptions
- Simplified branch prediction (always not-taken)

## Future Enhancements

Potential improvements:
- Branch prediction (static or dynamic)
- More advanced forwarding
- Cache simulation
- Exception handling
- Performance counters
- Visualization of pipeline state
