#!/usr/bin/env python3
"""
Demo script for MIPS 32-bit pipelined processor
Showcases the main features of the processor
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.processor import MIPSPipeline
from src.asm_utils import *


def demo_arithmetic():
    """Demonstrate basic arithmetic operations"""
    print("=" * 60)
    print("DEMO 1: Basic Arithmetic Operations")
    print("=" * 60)
    
    processor = MIPSPipeline()
    
    # Program: Compute (a + b) * c where a=5, b=3, c=2
    program = [
        addi(REGISTERS['t0'], REGISTERS['zero'], 5),    # a = 5
        addi(REGISTERS['t1'], REGISTERS['zero'], 3),    # b = 3
        add(REGISTERS['t2'], REGISTERS['t0'], REGISTERS['t1']),  # t2 = a + b = 8
        addi(REGISTERS['t3'], REGISTERS['zero'], 2),    # c = 2
        # Multiply by repeated addition (2 iterations)
        add(REGISTERS['t4'], REGISTERS['t2'], REGISTERS['t2']),  # t4 = t2 * 2 = 16
        nop(), nop(), nop()
    ]
    
    processor.load_program(program)
    processor.run(max_cycles=20, verbose=False)
    
    regs = processor.get_register_state()
    stats = processor.get_statistics()
    
    print(f"\nProgram: (a + b) * 2 where a=5, b=3")
    print(f"Results:")
    print(f"  a ($t0) = {regs[REGISTERS['t0']]}")
    print(f"  b ($t1) = {regs[REGISTERS['t1']]}")
    print(f"  a+b ($t2) = {regs[REGISTERS['t2']]}")
    print(f"  (a+b)*2 ($t4) = {regs[REGISTERS['t4']]}")
    print(f"\nPerformance:")
    print(f"  Cycles: {stats['cycles']}")
    print(f"  Instructions: {stats['instructions']}")
    print(f"  CPI: {stats['cpi']:.2f}")
    print()


def demo_memory():
    """Demonstrate memory operations"""
    print("=" * 60)
    print("DEMO 2: Memory Load/Store Operations")
    print("=" * 60)
    
    processor = MIPSPipeline()
    
    # Initialize memory with some values
    processor.data_mem.write(0, 100)
    processor.data_mem.write(4, 200)
    processor.data_mem.write(8, 300)
    
    # Program: Sum three numbers from memory
    program = [
        lw(REGISTERS['t0'], 0, REGISTERS['zero']),      # t0 = Memory[0] = 100
        lw(REGISTERS['t1'], 4, REGISTERS['zero']),      # t1 = Memory[4] = 200
        lw(REGISTERS['t2'], 8, REGISTERS['zero']),      # t2 = Memory[8] = 300
        add(REGISTERS['t3'], REGISTERS['t0'], REGISTERS['t1']),  # t3 = t0 + t1 = 300
        add(REGISTERS['t3'], REGISTERS['t3'], REGISTERS['t2']),  # t3 = t3 + t2 = 600
        sw(REGISTERS['t3'], 12, REGISTERS['zero']),     # Memory[12] = t3 = 600
        nop(), nop(), nop()
    ]
    
    processor.load_program(program)
    processor.run(max_cycles=30, verbose=False)
    
    regs = processor.get_register_state()
    stats = processor.get_statistics()
    
    print(f"\nProgram: Sum three numbers from memory")
    print(f"Input:")
    print(f"  Memory[0] = 100")
    print(f"  Memory[4] = 200")
    print(f"  Memory[8] = 300")
    print(f"\nResults:")
    print(f"  Sum ($t3) = {regs[REGISTERS['t3']]}")
    print(f"  Memory[12] = {processor.data_mem.read(12)}")
    print(f"\nPerformance:")
    print(f"  Cycles: {stats['cycles']}")
    print(f"  Instructions: {stats['instructions']}")
    print(f"  Stalls: {stats['stalls']} (load-use hazards)")
    print(f"  CPI: {stats['cpi']:.2f}")
    print()


def demo_branching():
    """Demonstrate branch instructions"""
    print("=" * 60)
    print("DEMO 3: Conditional Branching")
    print("=" * 60)
    
    processor = MIPSPipeline()
    
    # Program: Find maximum of two numbers
    program = [
        addi(REGISTERS['t0'], REGISTERS['zero'], 15),   # a = 15
        addi(REGISTERS['t1'], REGISTERS['zero'], 20),   # b = 20
        slt(REGISTERS['t2'], REGISTERS['t1'], REGISTERS['t0']),  # t2 = (b < a)?
        bne(REGISTERS['t2'], REGISTERS['zero'], 2),     # if b < a, skip next 2
        add(REGISTERS['t3'], REGISTERS['zero'], REGISTERS['t1']),  # max = b
        beq(REGISTERS['zero'], REGISTERS['zero'], 1),   # jump over next
        add(REGISTERS['t3'], REGISTERS['zero'], REGISTERS['t0']),  # max = a
        nop(), nop(), nop()
    ]
    
    processor.load_program(program)
    processor.run(max_cycles=30, verbose=False)
    
    regs = processor.get_register_state()
    stats = processor.get_statistics()
    
    print(f"\nProgram: max = (a > b) ? a : b")
    print(f"Input:")
    print(f"  a ($t0) = {regs[REGISTERS['t0']]}")
    print(f"  b ($t1) = {regs[REGISTERS['t1']]}")
    print(f"\nResult:")
    print(f"  max ($t3) = {regs[REGISTERS['t3']]}")
    print(f"\nPerformance:")
    print(f"  Cycles: {stats['cycles']}")
    print(f"  Instructions: {stats['instructions']}")
    print(f"  CPI: {stats['cpi']:.2f}")
    print()


def demo_forwarding():
    """Demonstrate data forwarding"""
    print("=" * 60)
    print("DEMO 4: Data Forwarding")
    print("=" * 60)
    
    processor = MIPSPipeline()
    
    # Program with data dependencies (requires forwarding)
    program = [
        addi(REGISTERS['t0'], REGISTERS['zero'], 10),   # t0 = 10
        addi(REGISTERS['t1'], REGISTERS['t0'], 5),      # t1 = t0 + 5 (forwarding from t0)
        add(REGISTERS['t2'], REGISTERS['t1'], REGISTERS['t0']),  # t2 = t1 + t0 (forwarding from t1)
        sub(REGISTERS['t3'], REGISTERS['t2'], REGISTERS['t1']),  # t3 = t2 - t1 (forwarding from t2)
        nop(), nop(), nop()
    ]
    
    processor.load_program(program)
    processor.run(max_cycles=20, verbose=False)
    
    regs = processor.get_register_state()
    stats = processor.get_statistics()
    
    print(f"\nProgram with data dependencies:")
    print(f"  t0 = 10")
    print(f"  t1 = t0 + 5  (requires t0 from EX/MEM)")
    print(f"  t2 = t1 + t0 (requires t1 from EX/MEM)")
    print(f"  t3 = t2 - t1 (requires t2 from EX/MEM)")
    print(f"\nResults:")
    print(f"  $t0 = {regs[REGISTERS['t0']]}")
    print(f"  $t1 = {regs[REGISTERS['t1']]}")
    print(f"  $t2 = {regs[REGISTERS['t2']]}")
    print(f"  $t3 = {regs[REGISTERS['t3']]}")
    print(f"\nPerformance:")
    print(f"  Cycles: {stats['cycles']}")
    print(f"  Instructions: {stats['instructions']}")
    print(f"  Stalls: {stats['stalls']} (forwarding eliminates most stalls!)")
    print(f"  CPI: {stats['cpi']:.2f}")
    print()


def main():
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  MIPS 32-bit 5-Stage Pipelined Processor Demo".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    demo_arithmetic()
    input("Press Enter to continue...")
    
    demo_memory()
    input("Press Enter to continue...")
    
    demo_branching()
    input("Press Enter to continue...")
    
    demo_forwarding()
    
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print()
    print("Key Features Demonstrated:")
    print("  ✓ 5-stage pipeline (IF, ID, EX, MEM, WB)")
    print("  ✓ Data forwarding for hazard resolution")
    print("  ✓ Pipeline stalling for load-use hazards")
    print("  ✓ Branch prediction and flushing")
    print("  ✓ Memory load/store operations")
    print("  ✓ Arithmetic and logical operations")
    print()
    print("For more information, see README.md and docs/")
    print()


if __name__ == "__main__":
    main()
