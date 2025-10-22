# MIPS Instruction Reference

## R-Type Instructions

R-type instructions perform register-to-register operations.

### ADD - Add
```
ADD rd, rs, rt
```
Operation: `rd = rs + rt`

Example:
```python
add(REGISTERS['t2'], REGISTERS['t0'], REGISTERS['t1'])  # $t2 = $t0 + $t1
```

### SUB - Subtract
```
SUB rd, rs, rt
```
Operation: `rd = rs - rt`

### AND - Bitwise AND
```
AND rd, rs, rt
```
Operation: `rd = rs & rt`

### OR - Bitwise OR
```
OR rd, rs, rt
```
Operation: `rd = rs | rt`

### NOR - Bitwise NOR
```
NOR rd, rs, rt
```
Operation: `rd = ~(rs | rt)`

### SLT - Set Less Than
```
SLT rd, rs, rt
```
Operation: `rd = (rs < rt) ? 1 : 0`

## I-Type Instructions

I-type instructions use an immediate value.

### ADDI - Add Immediate
```
ADDI rt, rs, immediate
```
Operation: `rt = rs + immediate`

Example:
```python
addi(REGISTERS['t0'], REGISTERS['zero'], 10)  # $t0 = 10
```

### ANDI - AND Immediate
```
ANDI rt, rs, immediate
```
Operation: `rt = rs & immediate`

### ORI - OR Immediate
```
ORI rt, rs, immediate
```
Operation: `rt = rs | immediate`

### SLTI - Set Less Than Immediate
```
SLTI rt, rs, immediate
```
Operation: `rt = (rs < immediate) ? 1 : 0`

### LW - Load Word
```
LW rt, offset(rs)
```
Operation: `rt = Memory[rs + offset]`

Example:
```python
lw(REGISTERS['t0'], 0, REGISTERS['t1'])  # $t0 = Memory[$t1 + 0]
```

### SW - Store Word
```
SW rt, offset(rs)
```
Operation: `Memory[rs + offset] = rt`

Example:
```python
sw(REGISTERS['t0'], 4, REGISTERS['t1'])  # Memory[$t1 + 4] = $t0
```

### BEQ - Branch if Equal
```
BEQ rs, rt, offset
```
Operation: `if (rs == rt) PC = PC + 4 + (offset << 2)`

Example:
```python
beq(REGISTERS['t0'], REGISTERS['t1'], 5)  # if $t0 == $t1, skip 5 instructions
```

### BNE - Branch if Not Equal
```
BNE rs, rt, offset
```
Operation: `if (rs != rt) PC = PC + 4 + (offset << 2)`

## J-Type Instructions

### J - Jump
```
J address
```
Operation: `PC = (PC & 0xF0000000) | (address << 2)`

## Pseudo-Instructions

### NOP - No Operation
```python
nop()  # Encoded as 0x00000000
```

## Register Names

| Register | Number | Usage |
|----------|--------|-------|
| $zero    | 0      | Constant 0 |
| $at      | 1      | Assembler temporary |
| $v0-$v1  | 2-3    | Return values |
| $a0-$a3  | 4-7    | Arguments |
| $t0-$t7  | 8-15   | Temporaries |
| $s0-$s7  | 16-23  | Saved temporaries |
| $t8-$t9  | 24-25  | More temporaries |
| $k0-$k1  | 26-27  | Kernel reserved |
| $gp      | 28     | Global pointer |
| $sp      | 29     | Stack pointer |
| $fp      | 30     | Frame pointer |
| $ra      | 31     | Return address |

## Usage Examples

### Simple Arithmetic
```python
from src.processor import MIPSPipeline
from src.asm_utils import *

processor = MIPSPipeline()

program = [
    addi(REGISTERS['t0'], REGISTERS['zero'], 5),
    addi(REGISTERS['t1'], REGISTERS['zero'], 3),
    add(REGISTERS['t2'], REGISTERS['t0'], REGISTERS['t1']),
    nop(), nop()
]

processor.load_program(program)
processor.run()
```

### Loop Example
```python
# Sum numbers from 1 to 10
program = [
    addi(REGISTERS['t0'], REGISTERS['zero'], 0),   # sum = 0
    addi(REGISTERS['t1'], REGISTERS['zero'], 1),   # i = 1
    addi(REGISTERS['t2'], REGISTERS['zero'], 11),  # limit = 11
    
    # Loop:
    add(REGISTERS['t0'], REGISTERS['t0'], REGISTERS['t1']),  # sum += i
    addi(REGISTERS['t1'], REGISTERS['t1'], 1),     # i++
    bne(REGISTERS['t1'], REGISTERS['t2'], -3),     # if i != limit, loop
    
    nop(), nop()
]
```

### Load/Store Example
```python
program = [
    addi(REGISTERS['t0'], REGISTERS['zero'], 42),  # $t0 = 42
    sw(REGISTERS['t0'], 0, REGISTERS['zero']),     # Memory[0] = 42
    lw(REGISTERS['t1'], 0, REGISTERS['zero']),     # $t1 = Memory[0]
    nop(), nop()
]
```
