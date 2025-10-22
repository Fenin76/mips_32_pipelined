"""
Example: Fibonacci sequence generator
Calculates the first N Fibonacci numbers
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.processor import MIPSPipeline
from src.asm_utils import *


def fibonacci_program(n=10):
    """Generate program to compute Fibonacci sequence"""
    
    # Program to compute first n Fibonacci numbers
    # Store results in memory starting at address 100
    program = [
        # Initialize
        addi(REGISTERS['t0'], REGISTERS['zero'], 0),    # $t0 = 0 (fib[0])
        addi(REGISTERS['t1'], REGISTERS['zero'], 1),    # $t1 = 1 (fib[1])
        addi(REGISTERS['t2'], REGISTERS['zero'], n),    # $t2 = n (counter)
        addi(REGISTERS['t3'], REGISTERS['zero'], 100),  # $t3 = 100 (base address)
        
        # Store first two values
        sw(REGISTERS['t0'], 0, REGISTERS['t3']),        # Memory[100] = 0
        sw(REGISTERS['t1'], 4, REGISTERS['t3']),        # Memory[104] = 1
        
        # Loop setup
        addi(REGISTERS['t4'], REGISTERS['zero'], 2),    # $t4 = 2 (index)
        addi(REGISTERS['t5'], REGISTERS['zero'], 8),    # $t5 = 8 (offset)
        
        # Loop: for i = 2 to n
        # Loop body starts at instruction 8 (address 32)
        slt(REGISTERS['t6'], REGISTERS['t4'], REGISTERS['t2']),  # $t6 = (i < n)
        beq(REGISTERS['t6'], REGISTERS['zero'], 5),     # if i >= n, exit loop
        
        add(REGISTERS['t7'], REGISTERS['t0'], REGISTERS['t1']),  # $t7 = fib[i-2] + fib[i-1]
        add(REGISTERS['t8'], REGISTERS['t3'], REGISTERS['t5']),  # $t8 = base + offset
        sw(REGISTERS['t7'], 0, REGISTERS['t8']),        # Memory[base + offset] = fib[i]
        
        # Update for next iteration
        add(REGISTERS['t0'], REGISTERS['zero'], REGISTERS['t1']),  # fib[i-2] = fib[i-1]
        add(REGISTERS['t1'], REGISTERS['zero'], REGISTERS['t7']),  # fib[i-1] = fib[i]
        addi(REGISTERS['t4'], REGISTERS['t4'], 1),      # i++
        addi(REGISTERS['t5'], REGISTERS['t5'], 4),      # offset += 4
        
        beq(REGISTERS['zero'], REGISTERS['zero'], -8),  # Jump back to loop start
        
        # End
        nop(),
        nop(),
        nop()
    ]
    
    return program


def main():
    print("=== Fibonacci Sequence Generator ===\n")
    
    n = 10
    processor = MIPSPipeline()
    
    # Load and run program
    program = fibonacci_program(n)
    processor.load_program(program)
    processor.run(max_cycles=200, verbose=False)
    
    # Read results from memory
    print(f"First {n} Fibonacci numbers:")
    for i in range(n):
        addr = 100 + i * 4
        value = processor.data_mem.read(addr)
        print(f"  fib[{i}] = {value}")
    
    # Print statistics
    stats = processor.get_statistics()
    print(f"\nExecution Statistics:")
    print(f"  Total Cycles: {stats['cycles']}")
    print(f"  Instructions Executed: {stats['instructions']}")
    print(f"  Stalls: {stats['stalls']}")
    print(f"  CPI: {stats['cpi']:.2f}")


if __name__ == "__main__":
    main()
