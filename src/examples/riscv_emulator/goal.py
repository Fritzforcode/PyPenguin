# Initialize state
register_names = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
register_map = {f"x{i}": i for i in range(32)} 
register_map |= dict(zip(register_names, range(len(register_names))))
register_map["fp"] = 8  # Third name for x8

registers = [0] * 32  # Simulated registers
memory = bytearray(16)  # 16 bytes simulated memory
program_counter = 0  # Instruction pointer (PC)

DEBUG = False

# Memory functions
def set_memory(address, value, size=4):
    """Set a value in memory."""
    if address % size != 0:
        raise ValueError(f"Unaligned memory access at address {address}")
    memory[address:address + size] = value.to_bytes(size, byteorder='little', signed=True)

def get_memory(address, size=4):
    """Get a value from memory."""
    if address % size != 0:
        raise ValueError(f"Unaligned memory access at address {address}")
    return int.from_bytes(memory[address:address + size], byteorder='little', signed=True)

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

# Load and execute functions
def load_instructions(json_data):
    """Load and parse JSON instructions."""
    return json_data["instructions"]

def execute_instruction(instruction):
    """Execute a single instruction."""
    global program_counter

    instr_type = instruction["type"]
    instr = instruction["instr"]
    arg0 = instruction.get("arg0")
    arg1 = instruction.get("arg1")
    arg2 = instruction.get("arg2")

    if instr_type == "load":
        if instr == "lui":  # Load Upper Immediate
            # arg1 is immediate
            set_register(arg0, (arg1 << 12))
        elif instr == "lw":  # Load Word
            address = get_register(arg1) + (arg2 if isinstance(arg2, int) else get_register(arg2))
            set_register(arg0, get_memory(address))

    elif instr_type == "store":
        if instr == "sw":  # Store Word
            address = get_register(arg1) + (arg2 if isinstance(arg2, int) else get_register(arg2))
            set_memory(address, get_register(arg0))

    elif instr_type == "arith":
        value1 = get_register(arg1)
        value2 = arg2 if isinstance(arg2, int) else get_register(arg2)

        if instr == "add":
            result = value1 + value2
        elif instr == "addi":
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
        offset_bytes = arg2 * 4  # Branch offset is in instruction half-words

        if instr == "beq":
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
            program_counter = program_counter + 4 + offset_bytes
            return
        
    program_counter += 4  # Increment PC by 4 bytes (size of one instruction)

def run_program(json_data):
    """Run the RISC-V program."""
    global program_counter, DEBUG
    instructions = load_instructions(json_data)

    while program_counter // 4 < len(instructions):
        current_instruction = instructions[program_counter // 4]
        if DEBUG:
            #print(dict(zip(register_names, registers)))
            print(dict(zip([f"x{i}" for i in range(32)], registers)))
            print(300*"-")
            print(program_counter, current_instruction)
            input()
        execute_instruction(current_instruction)


# Test Programs
test_programs = [
    {
        "description": "Sum of numbers 1 to 10",
        "instructions": [
            {"type": "load", "instr": "li", "arg0": "x10", "arg1": 0},  # x10 = 0
            {"type": "load", "instr": "li", "arg0": "x11", "arg1": 1},  # x11 = 1
            {"type": "load", "instr": "li", "arg0": "x12", "arg1": 10},  # x12 = 10
            {"type": "arith", "instr": "add", "arg0": "x10", "arg1": "x10", "arg2": "x11"},  # x10 += x11
            {"type": "arith", "instr": "addi", "arg0": "x11", "arg1": "x11", "arg2": 1},  # x11++
            {"type": "branch", "instr": "ble", "arg0": "x11", "arg1": "x12", "arg2": -4},  # Loop back
        ],
        "expected": {"x10": 55},  # Sum of 1 to 10,
        "pseudo": """
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
            {"type": "load", "instr": "li", "arg0": "x5", "arg1": 100},  # x5 = 100
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
        registers = [0] * 32
        memory = bytearray(16) # 16 bytes
        program_counter = 0
    
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

run_program({"instructions": [{"type": "load", "instr": "lui", "arg0": "x0", "arg1": 0xFFFFF}]})
print(hex(registers[1]))
