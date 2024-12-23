# Initialize state
register_map = {
    # General-purpose registers
    "r0": 0, "zero": 0,
    "r1": 1,
    "r2": 2,
    "r3": 3,
    "r4": 4,
    "r5": 5,
    "r6": 6,
    "r7": 7,
    "r8": 8,
    "r9": 9, "sb": 9,  # Static Base alias
    "r10": 10, "sl": 10,  # Stack Limit alias
    "r11": 11, "fp": 11,  # Frame Pointer alias
    "r12": 12, "ip": 12,  # Intra-Procedure Call scratch register alias

    # Special-purpose registers
    "r13": 13, "sp": 13,  # Stack Pointer
    "r14": 14, "lr": 14,  # Link Register
    "r15": 15, "pc": 15   # Program Counter
}

registers = [0] * 16  # Simulated registers
memory = {}  # Simulated memory as a dictionary
flags = {"zero": False, "negative": False}  # Condition flags
program_counter = 0  # Instruction pointer (PC)


def set_register(register, value):
    """Set the value of a register."""
    if register in register_map:
        index = register_map[register]  # Translate to index
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

    if instr_type == "move":
        # MOV: arg0 = destination, arg1 = immediate value
        set_register(arg0, arg1)

    elif instr_type == "alu":
        # ALU operations: arg0 = destination, arg1 = source register, arg2 = immediate or register
        value1 = get_register(arg1)  # Source value from a register
        if isinstance(arg2, int):  # Immediate value
            value2 = arg2
        else:  # Register index
            value2 = get_register(arg2)

        # Perform the ALU operation
        if   instr == "addi":
            instr = "add"
        if   instr == "add":
            result = value1 + value2
        elif instr == "sub":
            result = value1 - value2
        elif instr == "mul":
            result = value1 * value2
        elif instr == "div":
            if value2 == 0: # Handle divide by zero
                result = 0
            else:
                result = value1 
        elif instr == "and":
            result = value1 & value2
        elif instr == "orr":
            result = value1 | value2
        elif instr == "eor":
            result = value1 ^ value2
        elif instr == "lsl":
            result = value1 << value2
        elif instr == "lsr":
            result = value1 >> value2

        # Store the result in the destination register
        set_register(arg0, result)

    elif instr_type == "memory":
        # LDR or STR: arg0 = register, arg1 = base address, arg2 = offset
        address = get_register(arg1)
        if arg2 != None:
            address += arg2
        if   instr == "ldr":
            set_register(arg0, get_memory(address))  # Load from memory
        elif instr == "str":
            set_memory(address, get_register(arg0))  # Store to memory

    elif instr_type == "comparison":
        # CMP: arg0 = register, arg1 = immediate value
        if instr == "cmp":
            comparison_result = get_register(arg0) - arg1
            flags["zero"] = (comparison_result == 0)
            flags["negative"] = (comparison_result < 0)

    elif instr_type == "branch":
        # BGE: arg0 = label or instruction index
        if instr == "bge":
            do_jump = not flags["negative"]
            jump_target = arg0

            if do_jump:
                program_counter = jump_target
                return  # Skip the default PC increment

    # Default: move to the next instruction
    program_counter += 1


def run_program(json_data):
    """Run the ARM program."""
    global program_counter
    instructions = load_instructions(json_data)

    while program_counter < len(instructions):
        current_instruction = instructions[program_counter]
        execute_instruction(current_instruction)


# Example program in JSON
json_program = {
    "instructions": [
        {"type": "move", "instr": "mov", "arg0": "r0", "arg1": 10},  # r0 = 10
        {"type": "alu", "instr": "addi", "arg0": "r1", "arg1": "r0", "arg2": 5},  # r1 = r0 + 5
        {"type": "alu", "instr": "sub", "arg0": "r2", "arg1": "r1", "arg2": 3},  # r2 = r1 - 3
        {"type": "alu", "instr": "mul", "arg0": "r3", "arg1": "r2", "arg2": 2},  # r3 = r2 * 2
        {"type": "memory", "instr": "str", "arg0": "r3", "arg1": "r0", "arg2": 4},  # Store r3 at r0 + 4
        {"type": "comparison", "instr": "cmp", "arg0": "r3", "arg1": 14},  # Compare r3 with 14
        {"type": "branch", "instr": "bge", "arg0": 9},  # Branch if r3 >= 14
        {"type": "move", "instr": "mov", "arg0": "r4", "arg1": 1},  # r4 = 1 (won't execute if branch is taken)
        {"type": "branch", "instr": "b", "arg0": 10},  # Unconditional branch
        {"type": "move", "instr": "mov", "arg0": "r4", "arg1": 0},  # r4 = 0
    ]
}

# Run the program
run_program(json_program)

# Print the results
print("Registers:", registers)
print("Memory:", memory)
print("Flags:", flags)
