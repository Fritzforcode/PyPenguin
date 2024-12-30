# Test program to validate the emulator

# Initialize state
#register_names = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
#register_map = {f"x{i}": i for i in range(32)} 
#register_map |= dict(zip(  register_names, range(len(register_names))  ))
#register_map["fp"] = 8 # Third name for x8

register_map = {"x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, "x8": 8, "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, "x16": 16, "x17": 17, "x18": 18, "x19": 19, "x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24, "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29, "x30": 30, "x31": 31, "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4, "t0": 5, "t1": 6, "t2": 7, "s0": 8, "s1": 9, "a0": 10, "a1": 11, "a2": 12, "a3": 13, "a4": 14, "a5": 15, "a6": 16, "a7": 17, "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23, "s8": 24, "s9": 25, "s10": 26, "s11": 27, "t3": 28, "t4": 29, "t5": 30, "t6": 31, "fp": 8}

registers = [0] * 32  # Simulated registers
memory = {}  # Simulated memory as a dictionary
program_counter = 0  # Instruction pointer (PC)


def set_register(register, value):
    """Set the value of a register."""
    if register in register_map:
        index = register_map[register]  # Translate to index
        if index != 0:  # x0 (zero) is read-only
            registers[index] = value
    else:
        raise ValueError(f"Invalid register key: {register}")


def get_register(register):
    """Get the value of a register."""
    if register in register_map:
        index = register_map[register]  # Translate to index
        return registers[index]
    else:
        raise ValueError(f"Invalid register key: {register}")


def set_memory(address, value):
    """Set a value in memory."""
    memory[address] = value


def get_memory(address):
    """Get a value from memory."""
    return memory.get(address, 0)


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
        if instr == "li":  # Load Immediate
            set_register(arg0, arg1)

    elif instr_type == "arith":
        value1 = get_register(arg1)
        value2 = arg2 if isinstance(arg2, int) else get_register(arg2)

        if instr == "add":
            result = value1 + value2
        elif instr == "addi":
            result = value1 + value2
        elif instr == "sub":
            result = value1 - value2

        set_register(arg0, result)

    elif instr_type == "branch":
        value1 = get_register(arg0)
        value2 = get_register(arg1)
        offset = arg2

        if instr == "beq" and value1 == value2:
            program_counter += offset
            return
        elif instr == "bne" and value1 != value2:
            program_counter += offset
            return
        elif instr == "ble" and value1 <= value2:
            program_counter += offset
            return

    program_counter += 1


def run_program(json_data):
    """Run the RISC-V program."""
    global program_counter
    instructions = load_instructions(json_data)

    while program_counter < len(instructions):
        current_instruction = instructions[program_counter]
        execute_instruction(current_instruction)


# Test Programs
test_programs = [
    {
        "description": "Sum of numbers 1 to 10",
        "instructions": [
            {"type": "load", "instr": "li", "arg0": "x10", "arg1": 0, "arg2": None},  # x10 = 0
            {"type": "load", "instr": "li", "arg0": "x11", "arg1": 1, "arg2": None},  # x11 = 1
            {"type": "load", "instr": "li", "arg0": "x12", "arg1": 10, "arg2": None},  # x12 = 10
            {"type": "arith", "instr": "add", "arg0": "x10", "arg1": "x10", "arg2": "x11"},  # x10 += x11
            {"type": "arith", "instr": "addi", "arg0": "x11", "arg1": "x11", "arg2": 1},  # x11++
            {"type": "branch", "instr": "ble", "arg0": "x11", "arg1": "x12", "arg2": -2},  # Loop back
        ],
        "expected": {"x10": 55},  # Sum of 1 to 10
    },
    {
        "description": "Simple branch test",
        "instructions": [
            {"type": "load", "instr": "li", "arg0": "x5", "arg1": 5, "arg2": None},  # x5 = 5
            {"type": "load", "instr": "li", "arg0": "x6", "arg1": 5, "arg2": None},  # x6 = 5
            {"type": "branch", "instr": "beq", "arg0": "x5", "arg1": "x6", "arg2": 2},  # Skip next instruction
            {"type": "load", "instr": "li", "arg0": "x7", "arg1": 0, "arg2": None},  # x7 = 0 (skipped)
            {"type": "load", "instr": "li", "arg0": "x7", "arg1": 1, "arg2": None},  # x7 = 1
        ],
        "expected": {"x7": 1},
    },
]

# Run Tests
for i, test in enumerate(test_programs):
    # Reset state
    registers = [0] * 32
    memory = {}
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
