"""
Example: Array sum calculator
Calculates the sum of an array of numbers
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.processor import MIPSPipeline
from src.asm_utils import *


def array_sum_program():
    """Generate program to compute sum of array"""
    
    # Program to sum an array
    # Array is stored in memory starting at address 200
    # Result stored in $t0
    program = [
        # Initialize
        addi(REGISTERS['t0'], REGISTERS['zero'], 0),    # $t0 = 0 (sum)
        addi(REGISTERS['t1'], REGISTERS['zero'], 200),  # $t1 = 200 (array base)
        addi(REGISTERS['t2'], REGISTERS['zero'], 5),    # $t2 = 5 (array length)
        addi(REGISTERS['t3'], REGISTERS['zero'], 0),    # $t3 = 0 (index)
        
        # Loop: for i = 0 to length
        # Loop body starts at instruction 4 (address 16)
        slt(REGISTERS['t4'], REGISTERS['t3'], REGISTERS['t2']),  # $t4 = (i < length)
        beq(REGISTERS['t4'], REGISTERS['zero'], 5),     # if i >= length, exit
        
        # Calculate address and load element
        add(REGISTERS['t5'], REGISTERS['t1'], REGISTERS['t3']),  # $t5 = base + i*4
        lw(REGISTERS['t6'], 0, REGISTERS['t5']),        # $t6 = array[i]
        add(REGISTERS['t0'], REGISTERS['t0'], REGISTERS['t6']),  # sum += array[i]
        
        # Update index
        addi(REGISTERS['t3'], REGISTERS['t3'], 4),      # i += 4
        beq(REGISTERS['zero'], REGISTERS['zero'], -6),  # Jump back to loop start
        
        # Store result
        sw(REGISTERS['t0'], 0, REGISTERS['zero']),      # Memory[0] = sum
        
        nop(),
        nop(),
        nop()
    ]
    
    return program


def main():
    print("=== Array Sum Calculator ===\n")
    
    processor = MIPSPipeline()
    
    # Initialize array in memory
    array = [10, 20, 30, 40, 50]
    print(f"Array: {array}")
    
    for i, value in enumerate(array):
        processor.data_mem.write(200 + i * 4, value)
    
    # Load and run program
    program = array_sum_program()
    processor.load_program(program)
    processor.run(max_cycles=200, verbose=False)
    
    # Get result
    result = processor.data_mem.read(0)
    expected_sum = sum(array)
    
    print(f"\nResult:")
    print(f"  Sum = {result}")
    print(f"  Expected = {expected_sum}")
    print(f"  {'✓ PASS' if result == expected_sum else '✗ FAIL'}")
    
    # Print statistics
    stats = processor.get_statistics()
    print(f"\nExecution Statistics:")
    print(f"  Total Cycles: {stats['cycles']}")
    print(f"  Instructions Executed: {stats['instructions']}")
    print(f"  Stalls: {stats['stalls']}")
    print(f"  CPI: {stats['cpi']:.2f}")


if __name__ == "__main__":
    main()
