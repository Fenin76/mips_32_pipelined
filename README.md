# MIPS 32-bit 5-Stage Pipelined Processor

A comprehensive Python implementation of a 32-bit MIPS processor with a classic 5-stage pipeline architecture.

## Features

- **5-Stage Pipeline**: Instruction Fetch (IF), Instruction Decode (ID), Execute (EX), Memory Access (MEM), Write Back (WB)
- **Data Hazard Detection**: Automatic detection of load-use hazards with pipeline stalling
- **Data Forwarding**: EX-to-EX and MEM-to-EX forwarding to minimize stalls
- **Branch Handling**: Support for BEQ and BNE instructions with branch flushing
- **Complete Instruction Set**: R-type, I-type, and J-type instruction support

## Supported Instructions

### R-Type Instructions
- `ADD`, `SUB`, `AND`, `OR`, `SLT`, `NOR`

### I-Type Instructions
- `ADDI`, `ANDI`, `ORI`, `SLTI`
- `LW`, `SW` (Load/Store)
- `BEQ`, `BNE` (Branch)

### J-Type Instructions
- `J` (Jump)

## Architecture

The processor implements the classic MIPS 5-stage pipeline:

1. **IF (Instruction Fetch)**: Fetch instruction from instruction memory
2. **ID (Instruction Decode)**: Decode instruction and read registers
3. **EX (Execute)**: Perform ALU operations
4. **MEM (Memory Access)**: Access data memory for load/store
5. **WB (Write Back)**: Write results back to register file

### Pipeline Registers
- `IF/ID`: Stores PC and instruction between IF and ID stages
- `ID/EX`: Stores decoded instruction data and control signals
- `EX/MEM`: Stores ALU results and memory control signals
- `MEM/WB`: Stores data for write back to registers

### Hazard Handling
- **Data Hazards**: Resolved through forwarding or stalling
- **Control Hazards**: Handled by flushing pipeline on branch

## Installation

No external dependencies required! Just Python 3.6+

```bash
git clone https://github.com/Fenin76/mips_32_pipelined.git
cd mips_32_pipelined
```

## Usage

### Basic Example

```python
from src.processor import MIPSPipeline
from src.asm_utils import *

# Create processor
processor = MIPSPipeline()

# Write a simple program
program = [
    addi(REGISTERS['t0'], REGISTERS['zero'], 10),  # $t0 = 10
    addi(REGISTERS['t1'], REGISTERS['zero'], 20),  # $t1 = 20
    add(REGISTERS['t2'], REGISTERS['t0'], REGISTERS['t1']),  # $t2 = $t0 + $t1
    nop(),
    nop()
]

# Load and run program
processor.load_program(program)
processor.run(max_cycles=20, verbose=True)

# Check results
regs = processor.get_register_state()
print(f"Result: $t2 = {regs[REGISTERS['t2']]}")  # Should be 30
```

### Running Tests

```bash
# Run unit tests
python tests/test_alu.py
python tests/test_register_file.py
python tests/test_processor.py

# Run example programs
python examples/fibonacci.py
python examples/array_sum.py
```

## Examples

### Fibonacci Sequence
```bash
python examples/fibonacci.py
```
Computes the first 10 Fibonacci numbers using the pipelined processor.

### Array Sum
```bash
python examples/array_sum.py
```
Calculates the sum of an array using load/store instructions.

## Project Structure

```
mips_32_pipelined/
├── src/
│   ├── __init__.py
│   ├── processor.py         # Main pipeline processor
│   ├── alu.py              # Arithmetic Logic Unit
│   ├── register_file.py    # Register file (32 registers)
│   ├── instruction_memory.py
│   ├── data_memory.py
│   ├── control_unit.py     # Instruction decoder
│   ├── pipeline_registers.py
│   ├── hazard_unit.py      # Hazard detection and forwarding
│   └── asm_utils.py        # Assembly helper functions
├── tests/
│   ├── test_alu.py
│   ├── test_register_file.py
│   └── test_processor.py
├── examples/
│   ├── fibonacci.py
│   └── array_sum.py
├── docs/
└── README.md
```

## Performance Metrics

The processor tracks and reports:
- **Total Cycles**: Number of clock cycles executed
- **Instructions Executed**: Number of instructions completed
- **Stalls**: Number of pipeline stalls due to hazards
- **CPI (Cycles Per Instruction)**: Average cycles per instruction

## Documentation

For detailed documentation on the architecture and implementation, see the [docs](docs/) directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Created by Fenin76

## Acknowledgments

Based on the classic MIPS architecture as described in "Computer Organization and Design" by Patterson and Hennessy.
