"""Emulation of the MOT-6502 Processor."""

ADDRESSING = [
    # 0   |  1   |  2   |  3   |  4   |  5   |  6   |  7   |  8   |  9   |  A   |  B   |  C   |  D   |  E   |  F   |
    "imp", "inx", "   ", "   ", "   ", "zp",  "zp",  "   ", "imp", "imm", "acc", "   ", "   ", "abs", "abs", "   ",  # 0
    "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ",  # 1
    "abs", "inx", "   ", "   ", "zp",  "zp",  "zp",  "   ", "imp", "imm", "acc", "   ", "abs", "abs", "abs", "   ",  # 2
    "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ",  # 3
    "imp", "inx", "   ", "   ", "   ", "zp",  "zp",  "   ", "imp", "imm", "acc", "   ", "abs", "abs", "abs", "   ",  # 4
    "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ",  # 5
    "imp", "inx", "   ", "   ", "   ", "zp",  "zp",  "   ", "imp", "imm", "acc", "   ", "ind", "abs", "abs", "   ",  # 6
    "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ",  # 7
    "   ", "inx", "   ", "   ", "zp",  "zp",  "zp",  "   ", "imp", "   ", "imp", "   ", "abs", "abs", "abs", "   ",  # 8
    "rel", "iny", "   ", "   ", "zpx", "zpx", "zpy", "   ", "imp", "aby", "imp", "   ", "   ", "abx", "   ", "   ",  # 9
    "imm", "inx", "imm", "   ", "zp",  "zp",  "zp",  "   ", "imp", "imm", "imp", "   ", "abs", "abs", "abs", "   ",  # A
    "rel", "iny", "   ", "   ", "zpx", "zpx", "zpy", "   ", "imp", "aby", "imp", "   ", "abx", "abx", "aby", "   ",  # B
    "imm", "inx", "   ", "   ", "zp",  "zp",  "zp",  "   ", "imp", "imm", "imp", "   ", "abs", "abs", "abs", "   ",  # C
    "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ",  # D
    "imm", "inx", "   ", "   ", "zp",  "zp",  "zp",  "   ", "imp", "imm", "imp", "   ", "abs", "abs", "abs", "   ",  # E
    "rel", "iny", "   ", "   ", "   ", "zpx", "zpx", "   ", "imp", "aby", "   ", "   ", "   ", "abx", "abx", "   ",  # F
]

OPCODES = [
    #  0  |  1   |  2   |  3   |  4   |  5   |  6   |  7   |  8   |  9   |  A   |  B   |  C   |  D   |  E   |  F   |
    "brk", "ora", "   ", "   ", "   ", "ora", "asl", "   ", "php", "ora", "asl", "   ", "   ", "ora", "asl", "   ",  # 0
    "bpl", "ora", "   ", "   ", "   ", "ora", "asl", "   ", "clc", "ora", "   ", "   ", "   ", "ora", "asl", "   ",  # 1
    "jsr", "and", "   ", "   ", "bit", "and", "rol", "   ", "plp", "and", "rol", "   ", "bit", "and", "rol", "   ",  # 2
    "bmi", "and", "   ", "   ", "   ", "and", "rol", "   ", "sec", "and", "   ", "   ", "   ", "and", "rol", "   ",  # 3
    "rti", "eor", "   ", "   ", "   ", "eor", "lsr", "   ", "pha", "eor", "lsr", "   ", "jmp", "eor", "lsr", "   ",  # 4
    "bvc", "eor", "   ", "   ", "   ", "eor", "lsr", "   ", "cli", "eor", "   ", "   ", "   ", "eor", "lsr", "   ",  # 5
    "rts", "adc", "   ", "   ", "   ", "adc", "ror", "   ", "pla", "adc", "ror", "   ", "jmp", "adc", "ror", "   ",  # 6
    "bvs", "adc", "   ", "   ", "   ", "adc", "ror", "   ", "sei", "adc", "   ", "   ", "   ", "adc", "ror", "   ",  # 7
    "   ", "sta", "   ", "   ", "sty", "sta", "stx", "   ", "dey", "   ", "txa", "   ", "sty", "sta", "stx", "   ",  # 8
    "bcc", "sta", "   ", "   ", "sty", "sta", "stx", "   ", "tya", "sta", "txs", "   ", "   ", "sta", "   ", "   ",  # 9
    "ldy", "lda", "ldx", "   ", "ldy", "lda", "ldx", "   ", "tay", "lda", "tax", "   ", "ldy", "lda", "ldx", "   ",  # A
    "bcs", "lda", "   ", "   ", "ldy", "lda", "ldx", "   ", "clv", "lda", "tsx", "   ", "ldy", "lda", "ldx", "   ",  # B
    "cpy", "cmp", "   ", "   ", "cpy", "cmp", "dec", "   ", "iny", "cmp", "dex", "   ", "cpy", "cmp", "dec", "   ",  # C
    "bne", "cmp", "   ", "   ", "   ", "cmp", "dec", "   ", "cld", "cmp", "   ", "   ", "   ", "cmp", "dec", "   ",  # D
    "cpx", "sbc", "   ", "   ", "cpx", "sbc", "inc", "   ", "inx", "sbc", "nop", "   ", "cpx", "sbc", "inc", "   ",  # E
    "beq", "sbc", "   ", "   ", "   ", "sbc", "inc", "   ", "sed", "sbc", "   ", "   ", "   ", "sbc", "inc", "   ",  # F
]

BYTEORDER = "little"

PAGE_WRAPPING_BUG = False

ROM_START = 0x8000 # Shouldn't be at most 0xF000

######################################################################################################## 
#     [For the PenguinMod Version] Here is space for custom blocks, which simplify the code.           #
########################################################################################################

"""MOT-6502 Processor."""

def P___init__(memory: dict) -> dict:
    """
    Initialize the processor.

    :param memory: The memory to use
    :return: None
    """
    self = {}
    self["memory"] = memory
    self["reg_a"] = 0  # Accumlator A
    self["reg_y"] = 0  # Incex Register Y
    self["reg_x"] = 0  # Incex Register X
    
    self["flag_c"] = False # Status flag - Carry Flag
    self["flag_z"] = False # Status flag - Zero Flag
    self["flag_v"] = False # Status flag - Overflow Flag
    self["flag_n"] = False # Status flag - Negative Flag
    self, _ = P_reset(self)
    return self

def P_reset(self: dict) -> None:
    """
    Reset processor to initial state.

    :return: None
    """
    #self["program_counter"] = 0xFCE2  # Hardcoded start vector post-reset
    self, self["program_counter"] = P_read_word(self, 0xFFFC) # Read start vector from 0xFFFC-D
    self["stack_pointer"]   = 0xFD  # Hardcoded stack pointer post-reset
    self["instructions"]    = 0

    self["flag_i"] = True  # Status flag - Interrupt Disable
    self["flag_d"] = False # Status flag - Decimal Mode Flag
    return self, None

def P_fetch_byte(self: dict) -> int:
    """
    Fetch a byte from memory.

    :param address: The address to read from
    :return: int
    """
    self, data = P_read_byte(self, self["program_counter"])
    self["program_counter"] = (self["program_counter"] + 1) and 0xFFFF
    return self, data

def P_fetch_word(self: dict) -> int:
    """
    Fetch a word from memory.

    :param address: The address to read from
    :return: int
    """
    self, data = P_read_word(self, self["program_counter"])
    self["program_counter"] = (self["program_counter"] + 2) and 0xFFFF
    return self, data

def P_read_byte(self: dict, address: int) -> int:
    """
    Read a byte from memory.

    :param address: The address to read from
    :return: int
    """
    data = M___getitem__(self["memory"], address)
    return self, data

def P_read_word(self: dict, address: int, page_wrapping_bug: bool = False) -> int:
    """
    Read a word from memory.

    :param address: The address to read from
    :param page_wrapping_bug: Wether the page wrapping bug affects this read
    :return: int
    """
    if page_wrapping_bug and ((address & 0x00FF) == 0x00FF):
        second_address = address & 0xFF00
        # Read the first byte of the same page
        # instead of the first byte on the next page (which would be correct)
    else:
        second_address = (address + 1) & 0xFFFF
    self, t1 = P_read_byte(self, address       )
    self, t2 = P_read_byte(self, second_address)
    if BYTEORDER == "little":
        data = t1 | (t2 << 8)
    else:
        data = (t1 << 8) | t2
    return self, data

def P_write_byte(self: dict, address: int, value: int) -> None:
    """
    Write a byte to memory.

    :param address: The address to write to
    :param value: The value to write
    :return: None
    """
    self["memory"] = M___setitem__(self["memory"], address, value & 0xFF)
    return self, None

def P_write_word(self: dict, address: int, value: int) -> None:
    """
    Split a word to two bytes and write to memory.

    :param address: The address to write to
    :param value: The value to write
    :return: None
    """
    if BYTEORDER == "little":
        value1 =  value       & 0xFF
        value2 = (value >> 8) & 0xFF
    else:
        value1 = (value >> 8) & 0xFF
        value2 =  value       & 0xFF
    self, _ = P_write_byte(self,  address,                 value1)
    self, _ = P_write_byte(self, (address + 1) and 0xFFFF, value2)
    return self, None

def P_read_flags_register(self: dict, flag_b: bool) -> None:
    return self, (
        int(self["flag_n"]) << 7
      | int(self["flag_v"]) << 6
      | 1                   << 5
      | int(flag_b        ) << 4
      | int(self["flag_d"]) << 3
      | int(self["flag_i"]) << 2
      | int(self["flag_z"]) << 1
      | int(self["flag_c"]) << 0
    )

def P_set_flags_register(self: dict, data: int) -> None:
    self["flag_n"] = bool((data >> 7) & 0b00000001)
    self["flag_v"] = bool((data >> 6) & 0b00000001)
    # Bit 5: Unused Bit
    # Bit 4: The 'B' Flag can't be set to 1 from the stack
    self["flag_d"] = bool((data >> 3) & 0b00000001)
    self["flag_i"] = bool((data >> 2) & 0b00000001)
    self["flag_z"] = bool((data >> 1) & 0b00000001)
    self["flag_c"] = bool((data >> 0) & 0b00000001)
    return self, None

def P_push_byte(self: dict, data: int) -> None:
    """
    Push a byte to stack.

    :return: None
    """
    self["stack_pointer"] = (self["stack_pointer"] - 1) & 0xFF
    self["memory"] = M___setitem__(self["memory"], (0x0100 + self["stack_pointer"]), data)
    return self, None

def P_push_word(self: dict, data: int) -> None:
    if BYTEORDER == "little":
        value1 =  data       & 0xFF
        value2 = (data >> 8) & 0xFF
    else:
        value1 = (data >> 8) & 0xFF
        value2 =  data       & 0xFF
    self, _ = P_push_byte(self, value1)
    self, _ = P_push_byte(self, value2)
    return self, None

def P_pop_byte(self: dict) -> int:
    """
    Pop data from stack.

    :return: int
    """
    data = M___getitem__(self["memory"], (256 + self["stack_pointer"]))
    self["stack_pointer"] = (self["stack_pointer"] + 1) & 0xFF
    return self, data

def P_pop_word(self: dict) -> None:
    self, t1 = P_pop_byte(self)
    self, t2 = P_pop_byte(self)
    if BYTEORDER == "little":
        data = (t1 << 8) | t2
    else:
        data = t1 | (t2 << 8)
    return self, data

def P_evaluate_flag_n(self: dict, data: int) -> None:
    """
    Evaluate negative flag.

    :param data: The data to evaluate
    :return: None
    """
    self["flag_n"] = bool(data & 0x80)
    return self, None

def P_evaluate_flag_z(self: dict, data: int) -> None:
    """
    Evaluate the Zero Flag.

    :param data: The data to evaluate
    :return: None
    """
    self["flag_z"] = (data == 0)
    return self, None

def P_evaluate_flags_nz(self: dict, data: int) -> None:
    """
    Evaluate the Zero and Negative Flags.

    :param data: The data to evaluate
    :return: None
    """
    self, _ = P_evaluate_flag_n(self, data)
    self, _ = P_evaluate_flag_z(self, data)
    return self, None

def P_evaluate_flags_nz_a(self: dict) -> None:
    """
    Evaluate the Zero and Negative Flags for the Accumulator.

    :return: None
    """
    self, _ = P_evaluate_flags_nz(self, self["reg_a"])
    return self, None

def P_evaluate_flags_nz_x(self: dict) -> None:
    """
    Evaluate the Zero and Negative Flags for the X Register.

    :return: None
    """
    self, _ = P_evaluate_flags_nz(self, self["reg_x"])
    return self, None

def P_evaluate_flags_nz_y(self: dict) -> None:
    """
    Evaluate the Zero and Negative Flags for the Y Register.

    :return: None
    """
    self, _ = P_evaluate_flags_nz(self, self["reg_y"])
    return self, None

def P_execute(self: dict, instructions: int = 0, debug: bool = False) -> None:
    """
    Execute code for x instructions. Or until a breakpoint is rached.
    
    :param instructions: The number of instructions to execute
    :return: None
    """
    while (self["instructions"] < instructions):
        self, opcode_num = P_fetch_byte(self)
        #print(opcode_num)
        opcode = OPCODES[opcode_num].lower()
        addressing_mode = ADDRESSING[opcode_num]
        if opcode == "   ": # Treated as NOP
            opcode = "nop"
            addressing_mode = "imp"
        
        instr_func = "P_ins_" + opcode
        #print(self["instructions"], f"{opcode.upper()}({addressing_mode})[{hex(opcode_num)}]", 50*"=")
        #res = input(">> ")
        #while res != "":
        #    try:
        #        num = int(res, base=16)
        #    except Exception as err:
        #        print(err)
        #    else:
        #        _, value = P_read_byte(self, num)
        #        print(f"Memory[{res}]: {hex(value)} | {value}")
        #    res = input(">> ")
        
        if (addressing_mode == "imp") or (opcode in {"JMP", "JSR"}):
            func_args = [self, addressing_mode, None, None]
        else:
            addressing_func = "P_addressing_" + addressing_mode
            self, operand, args = call_with(addressing_func, [self])
            assert len(args) in {0,1}
            if len(args) == 0: args = [None]
            func_args = [self, addressing_mode, operand, *args]
        self, _ = call_with(instr_func, func_args)
        self["instructions"] += 1
    return self, None

"""Addressing for the MOT-6502"""
def P_addressing_imm(self: dict):
    """Immediate Addressing - Fetches operand directly from the instruction."""
    self, operand = P_fetch_byte(self)
    return self, operand, ()  # No memory address involved

def P_addressing_zp(self: dict):
    """Zero Page Addressing - Fetches operand from zero page address."""
    self, address = P_fetch_byte(self)
    self, operand = P_read_byte(self, address)
    return self, operand, (address,)

def P_addressing_zpx(self: dict):
    """Zero Page,X Addressing - Fetches operand from zero page address + X (wraps at 0xFF)."""
    self, base_address = P_fetch_byte(self)
    address = (base_address + self["reg_x"]) & 0xFF  # Zero-page wrap-around
    self, operand = P_read_byte(self, address)
    return self, operand, (address,)

def P_addressing_zpy(self: dict):
    """Zero Page,Y Addressing - Fetches operand from zero page address + Y (wraps at 0xFF)."""
    self, base_address = P_fetch_byte(self)
    address = (base_address + self["reg_y"]) & 0xFF  # Zero-page wrap-around
    self, operand = P_read_byte(self, address)
    return self, operand, (address,)

def P_addressing_abs(self: dict):
    """Absolute Addressing - Fetches operand from a full 16-bit address."""
    self, address = P_fetch_word(self)
    self, operand = P_read_byte(self, address)
    return self, operand, (address,)

def P_addressing_abx(self: dict):
    """Absolute,X Addressing - Adds X to a 16-bit base address."""
    self, base_address = P_fetch_word(self)
    address = (base_address + self["reg_x"]) & 0xFFFF  # Full address wrap-around
    self, operand = P_read_byte(self, address)
    return self, operand, (address,)

def P_addressing_aby(self: dict):
    """Absolute,Y Addressing - Adds Y to a 16-bit base address."""
    self, base_address = P_fetch_word(self)
    address = (base_address + self["reg_y"]) & 0xFFFF
    self, operand = P_read_byte(self, address)
    return self, operand, (address,)

def P_addressing_ind(self: dict):
    """ Indexed Indirect Addressing. """
    self, address = P_fetch_word(self)  # Fetch 16-bit address
    self, operand = P_read_byte(self, address)  # Read from computed address
    return self, operand, (address,)

def P_addressing_inx(self: dict):
    """
    Indexed Indirect Addressing (Indirect,X) - Fetches a 16-bit pointer from zero-page.

    Steps:
    1. Fetch zero-page base address.
    2. Add X to base address (wrap at 0xFF).
    3. Fetch 16-bit pointer from zero-page.
    4. Read operand from final address.
    """
    self, base_address = P_fetch_byte(self)
    zp_address = (base_address + self["reg_x"]) & 0xFF  # Zero-page wrap-around
    self, final_address = P_read_word(self, zp_address)  # Fetch 16-bit address
    self, operand = P_read_byte(self, final_address)  # Read from computed address
    return self, operand, (final_address,)

def P_addressing_iny(self: dict):
    """
    Indirect Indexed Addressing (Indirect),Y - Reads 16-bit pointer from zero-page, then adds Y.

    Steps:
    1. Fetch zero-page base address.
    2. Read 16-bit pointer from zero-page.
    3. Add Y to pointer to get final address.
    4. Read operand from final address.
    """
    self, base_address = P_fetch_byte(self)
    self, zp_address = P_read_word(self, base_address)  # Fetch 16-bit address
    final_address = (zp_address + self["reg_y"]) & 0xFFFF  # Handle wrapping
    self, operand = P_read_byte(self, final_address)  # Read from computed address
    return self, operand, (final_address,)

def P_addressing_rel(self: dict):
    self, operand = P_fetch_byte(self)
    return self, operand, ()

def P_addressing_acc(self: dict):
    return self, self["reg_a"], ()

"""Subroutines for the MOT-6502"""
def call_with(func_name: str, args: list):
    try:
        func = eval(func_name)    
    except NameError:
        if func_name.startswith("P_ins_"):
            raise NotImplementedError(f"Opcode '{func_name.removeprefix('P_ins_')}' doesn't exist or isn't implemented.")
        else:
            raise NotImplementedError(f"Counldn't find function '{func_name}'")
    return func(*args)

def help_bcd_to_decimal(bcd):
    tens = bcd >> 4  # Extract the tens digit
    ones = bcd & 0xF # Extract the ones digit
    return tens * 10 + ones

def help_decimal_to_bcd(decimal):
    tens = decimal // 10     # Extract the tens digit
    ones = decimal % 10      # Extract the ones digit
    return (tens << 4) | ones  # Combine into BCD format

def help_is_greater_equal(a, b, bcd:bool):
    if bcd:
        a = help_bcd_to_decimal(a)
        b = help_bcd_to_decimal(b)
    return a >= b

def help_twos_complement(num):
    return (num - 0x100) if (num >= 0b10000000) else (num)

############################################################################################################
#                                          MOT-6502 Instructions.                                          #
###########################################################################################################
def P_ins_nop(self: dict, mode: str) -> None:
    """
    NOP - No Operation.

    :return: None
    """
    return self, None

def P_ins_adc(self: dict, mode: str, operand: int, *args) -> None:
    """
    ADC - Add with Carry.
    :return: None
    """
    if self["flag_d"]:
        low_nibble  = (self["reg_a"] & 0x0F) + (operand & 0x0F) + int(self["flag_c"])
        high_nibble = (self["reg_a"] >>   4) + (operand >>   4)
        if low_nibble > 9:
            low_nibble -= 10
            high_nibble += 1

        if high_nibble > 9:
            high_nibble -= 10
            self["flag_c"] = True
        else:
            self["flag_c"] = False
        final_result = (high_nibble << 4) | low_nibble
    else:
        intermediary_result = self["reg_a"] + operand + int(self["flag_c"])
        final_result   = intermediary_result & 0xFF
        self["flag_c"] = intermediary_result > 0xFF

    self["flag_v"] = bool((self["reg_a"] ^ operand) & (self["reg_a"] ^ final_result) & 0x80)
    self["reg_a"] = final_result
    self, _ = P_evaluate_flags_nz_a(self)
    return self, None

def P_ins_and(self: dict, mode: str, operand: int, *args) -> None:
    """
    AND - Logical AND.
    :return: None
    """
    self["reg_a"] &= operand
    self, _ = P_evaluate_flags_nz_a(self)
    return self, None

def P_ins_asl(self: dict, mode: str, operand: int, address: int, *args) -> None:
    """
    ASL - Arithmetic Shift Left.
    :return: None
    """
    self["flag_c"] = bool(operand & 0b10000000)
    result = operand << 1
    if mode == "acc":
        self["reg_a"] = result
    else:
        self, _ = P_write_byte(self, address, result)
    self, _ = P_evaluate_flags_nz(self, result)
    return self, None

def P_ins_bcc(self: dict, mode: str, operand: int, *args) -> None:
    """
    BCC - Branch if Carry Clear.
    :return: None
    """
    if not self["flag_c"]:
        self["program_counter"] = (self["program_counter"] + help_twos_complement(operand)) and 0xFFFF
    return self, None

def P_ins_bcs(self: dict, mode: str, operand: int, *args) -> None:
    """
    BCS - Branch if Carry Set.
    :return: None
    """
    if self["flag_c"]:
        self["program_counter"] = (self["program_counter"] + help_twos_complement(operand)) and 0xFFFF
    return self, None

def P_ins_beq(self: dict, mode: str, operand: int, *args) -> None:
    """
    BEQ - Branch if Equal.
    :return: None
    """
    if self["flag_z"]:
        self["program_counter"] = (self["program_counter"] + help_twos_complement(operand)) and 0xFFFF
    return self, None

def P_ins_bit(self: dict, mode: str, operand: int, *args) -> None:
    """
    BIT - Bit Test.
    :return: None
    """
    self["flag_n"] = bool(self["reg_a"] & 0b10000000)
    self["flag_v"] = bool(self["reg_a"] & 0b01000000)
    self["flag_z"] = (self["reg_a"] & operand) == 0
    return self, None

def P_ins_bmi(self: dict, mode: str, operand: int, *args) -> None:
    """
    BMI - Branch if Minus.
    :return: None
    """
    if self["flag_n"]:
        self["program_counter"] = (self["program_counter"] + help_twos_complement(operand)) and 0xFFFF
    return self, None

def P_ins_bne(self: dict, mode: str, operand: int, *args) -> None:
    """
    BNE - Branch if Not Equal.
    :return: None
    """
    if not self["flag_z"]:
        self["program_counter"] = (self["program_counter"] + help_twos_complement(operand)) and 0xFFFF
    return self, None

def P_ins_bpl(self: dict, mode: str, operand: int, *args) -> None:
    """
    BPL - Branch if Positive.
    :return: None
    """
    if not self["flag_n"]:
        self["program_counter"] = (self["program_counter"] + help_twos_complement(operand)) and 0xFFFF
    return self, None

def P_ins_brk(self: dict, mode: str) -> None:
    """
    BRK - Force Interrupt.
    :return: None
    """
    # Push the pc onto the stack
    self, _ = P_push_word(self, self["program_counter"])

    # Push the Status Register onto the stack with Break flag set (B = 1)
    self, status_register = P_read_flags_register(self, flag_b=True)
    self, _ = P_push_byte(self, status_register)

    # Fetch the IRQ/BRK vector at 0xFFFE-0xFFFF
    self, self["program_counter"] = P_read_word(self, 0xFFFE) # Set PC to the interrupt handler address

    # Set Interrupt Disable flag (I = 1)
    self["flag_i"] = True
    return self, None

def P_ins_bvc(self: dict, mode: str, operand: int, *args) -> None:
    """
    BVC - Branch if Overflow Clear.
    :return: None
    """
    if not self["flag_v"]:
        self["program_counter"] = (self["program_counter"] + help_twos_complement(operand)) and 0xFFFF
    return self, None

def P_ins_bvs(self: dict, mode: str, operand: int, *args) -> None:
    """
    BVS - Branch if Overflow Set.
    :return: None
    """
    if self["flag_v"]:
        self["program_counter"] = (self["program_counter"] + help_twos_complement(operand)) and 0xFFFF
    return self, None

def P_ins_clc(self: dict, mode: str) -> None:
    """
    CLC - Clear Carry Flag.

    :return: None
    """
    self["flag_c"] = False
    return self, None

def P_ins_cld(self: dict, mode: str) -> None:
    """
    CLD - Clear Decimal Mode.

    :return: None
    """
    self["flag_d"] = False
    return self, None

def P_ins_cli(self: dict, mode: str) -> None:
    """
    CLI - Clear Interrupt Disable.

    :return: None
    """
    self["flag_i"] = False
    return self, None

def P_ins_clv(self: dict, mode: str) -> None:
    """
    CLV - Clear Overflow Flag.

    :return: None
    """
    self["flag_v"] = False
    return self, None

def P_ins_cmp(self: dict, mode: str, operand: int, *args) -> None:
    """
    CMP - Compare.
    :return: None
    """
    self, _ = P_evaluate_flags_nz(self, self["reg_a"] - operand)
    self["flag_c"] = help_is_greater_equal(self["reg_a"], operand, bcd=self["flag_d"])
    return self, None

def P_ins_cpx(self: dict, mode: str, operand: int, *args) -> None:
    """
    CPX - Compare X Register.
    :return: None
    """
    self, _ = P_evaluate_flags_nz(self, self["reg_x"] - operand)
    self["flag_c"] = help_is_greater_equal(self["reg_x"], operand, bcd=self["flag_d"])
    return self, None

def P_ins_cpy(self: dict, mode: str, operand: int, *args) -> None:
    """
    CPY - Compare Y Register.
    :return: None
    """
    self, _ = P_evaluate_flags_nz(self, self["reg_y"] - operand)
    self["flag_c"] = help_is_greater_equal(self["reg_y"], operand, bcd=self["flag_d"])
    return self, None

def P_ins_dec(self: dict, mode: str, operand: int, address: int, *args) -> None:
    """
    DEC - Decrement Memory.

    :return: None
    """
    self, _ = P_write_byte(self, address, (operand - 1) & 0xFF)
    self, _ = P_evaluate_flags_nz(self  , (operand - 1) & 0xFF)
    return self, None

def P_ins_dex(self: dict, mode: str) -> None:
    """
    DEX - Decrement X Register.

    :return: None
    """
    self["reg_x"] = (self["reg_x"] - 1) and 0xFF
    self, _ = P_evaluate_flags_nz_x(self)
    return self, None

def P_ins_dey(self: dict, mode: str) -> None:
    """
    DEY - Decrement Y Register.

    :return: None
    """
    self["reg_y"] = (self["reg_y"] - 1) and 0xFF
    self, _ = P_evaluate_flags_nz_y(self)
    return self, None

def P_ins_eor(self: dict, mode: str, operand: int, *args) -> None:
    """
    EOR - Logical XOR.
    :return: None
    """
    self["reg_a"] ^= operand
    self, _ = P_evaluate_flags_nz_a(self)
    return self, None

def P_ins_inc(self: dict, mode: str, operand: int, address: int, *args) -> None:
    """
    INC - Increment Memory.

    :return: None
    """
    self, _ = P_write_byte(self, address, (operand + 1) & 0xFF)
    self, _ = P_evaluate_flags_nz(self  , (operand + 1) & 0xFF)
    return self, None

def P_ins_inx(self: dict, mode: str) -> None:
    """
    INX - Increment X Register.

    :return: None
    """
    self["reg_x"] = (self["reg_x"] + 1) and 0xFF
    self, _ = P_evaluate_flags_nz_x(self)
    return self, None

def P_ins_iny(self: dict, mode: str) -> None:
    """
    INY - Increment Y Register.

    :return: None
    """
    self["reg_y"] = (self["reg_y"] + 1) and 0xFF
    self, _ = P_evaluate_flags_nz_y(self)
    return self, None

def P_ins_jmp(self: dict, mode: str) -> None:
    """
    JMP - Jump to New Location.
    :return: None
    """
    match mode:
        case "abs":
            self, program_counter = P_fetch_word(self)
        case "ind":
            self, pointer_address = P_fetch_word(self)
            self, program_counter = P_read_word(self, pointer_address, page_wrapping_bug=PAGE_WRAPPING_BUG)
    self["program_counter"] = program_counter
    return self, None

def P_ins_jsr(self: dict, mode: str) -> None:
    """
    JSR - Jump to New Location Saving Return Addres.
    :return: None
    """
    match mode:
        case "abs":
            self, program_counter = P_fetch_word(self)
    self, _ = P_push_word(self, self["program_counter"]) # P_fetch_word changes self["program_counter"], so push here
    self["program_counter"] = program_counter
    return self, None

def P_ins_lda(self: dict, mode: str, operand: int, *args) -> None:
    """
    LDA - Load Accumulator.

    :return: None
    """
    self["reg_a"] = operand
    self, _ = P_evaluate_flags_nz_a(self)
    return self, None

def P_ins_ldx(self: dict, mode: str, operand: int, *args) -> None:
    """
    LDX - Load X Register.

    :return: None
    """
    self["reg_x"] = operand
    self, _ = P_evaluate_flags_nz_x(self)
    return self, None

def P_ins_ldy(self: dict, mode: str, operand: int, *args) -> None:
    """
    LDY - Load Y Register.

    :return: None
    """
    self["reg_y"] = operand
    self, _ = P_evaluate_flags_nz_y(self)
    return self, None

def P_ins_lsr(self: dict, mode: str, operand: int, address: int, *args) -> None:
    """
    LSR - Logical Shift Right.
    :return: None
    """
    self["flag_c"] = bool(operand & 0b00000001)
    result = (operand >> 1)
    if mode == "acc":
        self["reg_a"] = result
    else:
        self, _ = P_write_byte(self, address, result)
    self, _ = P_evaluate_flag_z(self, result)
    return self, None

def P_ins_ora(self: dict, mode: str, operand: int, *args) -> None:
    """
    ORA - Logical OR.
    :return: None
    """
    self["reg_a"] |= operand
    self, _ = P_evaluate_flags_nz_a(self)

def P_ins_pha(self: dict, mode: str) -> None:
    """
    PHA - Push Accumulator.

    TODO: Add check to not cross page

    :return: None
    """
    self, _ = P_push_byte(self, self["reg_a"])
    return self, None

def P_ins_php(self: dict, mode: str) -> None:
    """
    Push Processor Status.

    return: None
    """
    self, status_register = P_read_flags_register(self, flag_b=True)
    self, _ = P_push_byte(self, status_register)
    return self, None

def P_ins_pla(self: dict, mode: str) -> None:
    """
    PLA - Pull Accumulator.

    TODO: Add check to not cross page

    :return: None
    """
    self, self["reg_a"] = P_pop_byte(self)
    self, _ = P_evaluate_flags_nz_a(self)
    return self, None

def P_ins_plp(self: dict, mode: str) -> None:
    """
    Pull Processor Status.

    TODO: Implement instruction and test
    TODO: Add check to not cross page

    :return: None
    """
    self, status_register = P_pop_byte(self)
    self, _ = P_set_flags_register(self, status_register)
    return self, None

def P_ins_rol(self: dict, mode: str, operand: int, address: int, *args) -> None:
    """
    ROL - Rotate One Bit Left.
    :return: None
    """
    result = ((operand << 1) & 0xFF) | int(self["flag_c"])
    self["flag_c"] = bool(operand & 0b10000000)
    if mode == "acc":
        self["reg_a"] = result
    else:
        self, _ = P_write_byte(self, address, result)
    self, _ = P_evaluate_flags_nz(self, result)
    return self, None

def P_ins_ror(self: dict, mode: str, operand: int, address: int, *args) -> None:
    """
    ROR - Rotate One Bit Right.
    :return: None
    """
    result = (int(self["flag_c"]) << 7) | (operand >> 1)
    self["flag_c"] = bool(operand & 0b00000001)
    if mode == "acc":
        self["reg_a"] = result
    else:
        self, _ = P_write_byte(self, address, result)
    self, _ = P_evaluate_flags_nz(self, result)
    return self, None

def P_ins_rti(self: dict, mode: str) -> None:
    """
    RTI - Return from Interrupt.
    :return: None
    """
    self, status_register = P_pop_byte(self)
    self, _ = P_set_flags_register(self, status_register)
    self, self["program_counter"] = P_pop_word(self)
    return self, None

def P_ins_rts(self: dict, mode: str) -> None:
    """
    RTI - Return from Subroutine.
    :return: None
    """
    self, return_address = P_pop_word(self)
    self["program_counter"] = (return_address + 1) & 0xFFFF
    return self, None

def P_ins_sbc(self: dict, mode: str, operand: int, *args) -> None:
    """
    SBC - Subtract with Carry.
    :return: None
    """
    if self["flag_d"]:
        low_nibble  = (self["reg_a"] & 0x0F) - (operand & 0x0F) - int(not self["flag_c"])
        high_nibble = (self["reg_a"] >>   4) - (operand >>   4)
        
        if low_nibble < 0:
            low_nibble += 10
            high_nibble -= 1
        
        if high_nibble < 0:
            nigh_nibble += 10
            self["flag_c"] = False
        else:
            self["flag_c"] = True
        
        final_result = (high_nibble << 4) | low_nibble
    else:
        intermediary_result = self["reg_a"] - operand - int(not self["flag_c"])
        final_result   = intermediary_result & 0xFF
        self["flag_c"] = not (intermediary_result < 0)
    
    self["flag_v"] = bool((self["reg_a"] ^ operand) & (self["reg_a"] ^ final_result) & 0x80)
    self["reg_a"] = final_result
    self, _ = P_evaluate_flags_nz_a(self)
    return self, None

def P_ins_sec(self: dict, mode: str) -> None:
    """
    SEC - Set Carry Flag.

    :return: None
    """
    self["flag_c"] = True
    return self, None

def P_ins_sed(self: dict, mode: str) -> None:
    """
    SED - Set Decimal Mode.

    :return: None
    """
    self["flag_d"] = True
    return self, None

def P_ins_sei(self: dict, mode: str) -> None:
    """
    SEI - Set Interrupt Disable.

    :return: None
    """
    self["flag_i"] = True
    return self, None

def P_ins_sta(self: dict, mode: str, operand: int, address:int, *args) -> None:
    """
    STA - Store Accumulator.

    :return: None
    """
    self, _ = P_write_byte(self, address, self["reg_a"])
    return self, None

def P_ins_stx(self: dict, mode: str, operand: int, address:int, *args) -> None:
    """
    STA - Store X Register.

    :return: None
    """
    self, _ = P_write_byte(self, address, self["reg_x"])
    return self, None

def P_ins_sty(self: dict, mode: str, operand: int, address:int, *args) -> None:
    """
    STA - Store Y Register.

    :return: None
    """
    self, _ = P_write_byte(self, address, self["reg_y"])
    return self, None

def P_ins_tax(self: dict, mode: str) -> None:
    """
    TAX - Transfer Accumulator to X.

    :return: None
    """
    self["reg_x"] = self["reg_a"]
    self, _ = P_evaluate_flags_nz_x(self)
    return self, None

def P_ins_tay(self: dict, mode: str) -> None:
    """
    TAY - Transfer Accumulator to Y.

    :return: None
    """
    self["reg_y"] = self["reg_a"]
    self, _ = P_evaluate_flags_nz_y(self)
    return self, None

def P_ins_tsx(self: dict, mode: str) -> None:
    """
    TSX - Transfer Stack Pointer to X.

    :return: None
    """
    self["reg_x"] = self["stack_pointer"]
    self, _ = P_evaluate_flags_nz_x(self)
    return self, None

def P_ins_txa(self: dict, mode: str) -> None:
    """
    TXA - Transfer Register X to Accumulator.

    :return: None
    """
    self["reg_a"] = self["reg_x"]
    self, _ = P_evaluate_flags_nz_a(self)
    return self, None

def P_ins_txs(self: dict, mode: str) -> None:
    """
    TXS - Transfer Register X to Stack Pointer.

    :return: None
    """
    self["stack_pointer"] = self["reg_x"]
    return self, None

def P_ins_tya(self: dict, mode: str) -> None:
    """
    TYA - Transfer Register Y to Accumulator.

    :return: None
    """
    self["reg_a"] = self["reg_y"]
    self, _ = P_evaluate_flags_nz_a(self)
    return self, None

############################################################################################################
#                                     Emulation of the MOT-6502 memory.                                    #
############################################################################################################

"""Memory bank for MOT-6502 systems."""

def M___init__(rom) -> dict:
    """
    Initialize the memory.

    :param size: The size of the memory
    :return: None
    """
    mself = {}
    mself["size"] = 0x10000
    mself["memory"] = rom
    return mself

def M___getitem__(mself: dict, address: int) -> int:
    """
    Get the value at the specified address.

    :param address: The address to read from
    :return: The value at the specified address
    """
    if 0x0000 < address > 0xFFFF:
        raise ValueError("Memory address is not valid")
    return mself["memory"].get(address, 0)

def M___setitem__(mself: dict, address: int, value: int) -> dict:
    """
    Set the value at the specified address.

    :param address: The address to write to
    :param value: The value to write to the address
    :return: None
    """
    if 0x0000 < address > 0xFFFF:
        raise ValueError("Memory address is not valid")
    if value > 2**8:
        raise ValueError("Value too large")
    if address >= ROM_START:
        raise ValueError("Can't write to read-only addresses")
    
    if address < ROM_START:
        mself["memory"][address] = value
    return mself
