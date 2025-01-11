# Initialize state
register_names = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
register_map = {f"x{i}": i for i in range(32)} 
register_map |= dict(zip(register_names, range(len(register_names))))
register_map["fp"] = 8  # Third name for x8

def reset():
    global registers, memory, program_counter, DEBUG
    registers = [0] * 32  # Simulated registers
    memory = [0] * 16  # 16 bytes simulated memory
    program_counter = 0  # Instruction pointer (PC)
    DEBUG = False

# Helper functions
def reg_or_imm(value):
    return value if isinstance(value, int) else get_register(value)

# Memory functions
def set_memory(address, value, size):
    """Set a value in memory."""
    if address % size != 0:
        raise ValueError(f"Unaligned memory access at address {address}")
    
    # Store the value byte by byte
    if size >= 1: memory[address + 0] = (value >>  0) & 0xFF
    if size >= 2: memory[address + 1] = (value >>  8) & 0xFF
    if size >= 3: memory[address + 2] = (value >> 16) & 0xFF
    if size >= 4: memory[address + 3] = (value >> 24) & 0xFF
    
def get_memory(address, size, signed):
    """Get a value from memory."""
    if address % size != 0:
        raise ValueError(f"Unaligned memory access at address {address}")

    value = 0
    # Read byte by byte
    if size >= 1: value += memory[address + 0] <<  0
    if size >= 2: value += memory[address + 1] <<  8
    if size >= 2: value += memory[address + 2] <<  16
    if size >= 2: value += memory[address + 3] <<  24
    
    # Convert to signed if necessary
    bits = size * 8
    if signed and (value > ((2**(bits-1)) - 1)): # eg. (2**31)-1 if size=4
        value -= (2**bits)  # Convert to signed
    return value

# Register functions
def set_register(register, value):
    """Set the value of a register."""
    if register in register_map:
        index = register_map[register]
        if index != 0:  # x0 (zero) is read-only
            registers[index] = value
    else:
        raise ValueError(f"Invalid register key: {register}")

def get_register(register):
    """Get the value of a register."""
    if register in register_map:
        return registers[register_map[register]]
    else:
        raise ValueError(f"Invalid register key: {register}")

def execute_instruction(instruction):
    """Execute a single instruction."""
    global program_counter

    instr_type = instruction["type"]
    instr = instruction["instr"]
    arg0 = instruction.get("arg0")
    arg1 = instruction.get("arg1")
    arg2 = instruction.get("arg2")

    if instr_type == "load":
        if instr != "lui":
            address = get_register(arg1) + reg_or_imm(arg2)
        if  instr == "lui":  # Load Upper Immediate
            # arg1 is immediate
            load_value = arg1 << 12
        elif instr == "lw":  # Load Word
            load_value = get_memory(address, size=4, signed=True)
        elif instr == "lh":  # Load Halfword (signed)
            #set_register(arg0, int.from_bytes(memory[address:address + 2], byteorder='little', signed=True))
            load_value = get_memory(address, size=2, signed=True)
        elif instr == "lhu":  # Load Halfword (unsigned)
            #set_register(arg0, int.from_bytes(memory[address:address + 2], byteorder='little', signed=False))
            load_value = get_memory(address, size=2, signed=False)
        elif instr == "lb":  # Load Byte (signed)
            #set_register(arg0, int.from_bytes(memory[address:address + 1], byteorder='little', signed=True))
            load_value = get_memory(address, size=1, signed=True)
        elif instr == "lbu":  # Load Byte (unsigned)
            #set_register(arg0, int.from_bytes(memory[address:address + 1], byteorder='little', signed=False))
            load_value = get_memory(address, size=1, signed=False)
        
        set_register(arg0, load_value)

    elif instr_type == "store":
        address = get_register(arg1) + reg_or_imm(arg2)
        if instr == "sw":  # Store Word
            set_memory(address, get_register(arg0), size=4)
        elif instr == "sh":  # Store Halfword
            #memory[address:address + 2] = get_register(arg0).to_bytes(2, byteorder='little', signed=True)
            set_memory(address, get_register(arg0), size=2)
        elif instr == "sb":  # Store Byte
            #memory[address:address + 1] = get_register(arg0).to_bytes(1, byteorder='little', signed=True)
            set_memory(address, get_register(arg0), size=1)

    elif instr_type == "arith":
        value1 = get_register(arg1)
        value2 = reg_or_imm(arg2)

        if instr == "addi": instr = "add"

        if   instr == "add":
            result = value1 + value2
        elif instr == "sub":
            result = value1 - value2
        elif instr == "and":
            result = value1 & value2
        elif instr == "or":
            result = value1 | value2
        elif instr == "xor":
            result = value1 ^ value2

        set_register(arg0, result)

    elif instr_type == "branch":
        value1 = get_register(arg0)
        value2 = get_register(arg1)
        offset_bytes = arg2 * 2  # Branch offset is in instruction half-words

        if   instr == "beq":
            condition_met = value1 == value2
        elif instr == "bne":
            condition_met = value1 != value2
        elif instr == "blt":
            condition_met = value1 <  value2
        elif instr == "ble":
            condition_met = value1 <= value2
        elif instr == "bgt":
            condition_met = value1 >  value2
        elif instr == "bge":
            condition_met = value1 >= value2
        
        if condition_met:
            program_counter += 4 + offset_bytes
            return

    elif instr_type == "jump":
        if instr == "jal":  # Jump and Link
            set_register(arg0, program_counter + 4)
            program_counter += arg1 * 2  # Jump offset is in instruction half-words
            return
        elif instr == "jalr":  # Jump and Link Register
            temp = program_counter + 4
            program_counter = (get_register(arg1) + arg2) & ~1
            set_register(arg0, temp)
            return
    program_counter += 4  # Increment PC by 4 bytes (size of one instruction)

def run_program(json_data):
    """Run the RISC-V program."""
    global program_counter, DEBUG
    instructions = json_data["instructions"]

    while program_counter // 4 < len(instructions):
        current_instruction = instructions[program_counter // 4]
        if DEBUG:
            #print(dict(zip(register_names, registers)))
            print(dict(zip([f"x{i}" for i in range(32)], registers)))
            print(list(memory))
            print(300*"-")
            print(program_counter, current_instruction)
            input()
        execute_instruction(current_instruction)


# Test Programs
test_programs = [
    {
        "description": "Sum of numbers 1 to 10",
        "instructions": [
            {"type": "arith" , "instr": "addi", "arg0": "x10", "arg1": "x0" , "arg2": 0},  # x10 = 0
            {"type": "arith" , "instr": "addi", "arg0": "x11", "arg1": "x0" , "arg2": 1},  # x11 = 1
            {"type": "arith" , "instr": "addi", "arg0": "x12", "arg1": "x0" , "arg2": 10},  # x12 = 10
            {"type": "arith" , "instr": "add" , "arg0": "x10", "arg1": "x10", "arg2": "x11"},  # x10 += x11
            {"type": "arith" , "instr": "addi", "arg0": "x11", "arg1": "x11", "arg2": 1},  # x11++
            {"type": "branch", "instr": "ble" , "arg0": "x11", "arg1": "x12", "arg2": -6},  # Loop back
        ],
        "expected": {"x10": 55},  # Sum of 1 to 10,
        "pseudo": """
            addi x10, x0, #0
            addi x11, x0, #1
            addi x12, x0, #10
            loop:
                add x10, x10, x11
                addi x11, x11, #1
                ble x11, x12, loop

            x10 = 0
            x11 = 1
            x12 = 10
            loop:
                x10 = x10 + x11
                x11 = x11 + 1
                if x11 <= x12: goto loop
        """
    },
    {
        "description": "Memory load/store test",
        "instructions": [
            {"type": "arith", "instr": "addi", "arg0": "x5", "arg1": "x0", "arg2": 100},  # x5 = 100
            {"type": "store", "instr": "sw", "arg0": "x5", "arg1": "x0", "arg2": 0},  # Memory[0] = x5
            {"type": "load", "instr": "lw", "arg0": "x6", "arg1": "x0", "arg2": 0},  # x6 = Memory[0]
        ],
        "expected": {"x6": 100},  # x6 should be 100
    },
]

def run_tests():
    # Run Tests
    for i, test in enumerate(test_programs):
        # Reset state
        reset()
    
        # Run the test program
        print(f"Running test {i + 1}: {test['description']}")
        run_program(test)
        # Check results
        passed = True
        for reg, expected_value in test["expected"].items():
            if get_register(reg) != expected_value:
                print(f"  Test failed: {reg} = {get_register(reg)}, expected {expected_value}")
                passed = False
        if passed:
            print("  Test passed!")
        

run_tests()

#reset()
#run_program()
