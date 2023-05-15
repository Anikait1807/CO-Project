from random import randint
from typing import List

PC = 0
FILE = []
OUTPUT = []

INSTRUCTIONS = {
    "add": {
        "type": "A",
        "opcode": "00000",
    },
    "sub": {
        "type": "A",
        "opcode": "00001",
    },
    "mov $Imm": {
        "type": "B",
        "opcode": "00010",
    },
    "mov": {
        "type": "C",
        "opcode": "00011",
    },
    "ld": {
        "type": "D",
        "opcode": "00100",
    },
    "st": {
        "type": "D",
        "opcode": "00101",
    },
    "mul": {
        "type": "A",
        "opcode": "00110",
    },
    "div": {
        "type": "C",
        "opcode": "00111",
    },
    "rs": {
        "type": "B",
        "opcode": "01000",
    },
    "ls": {
        "type": "B",
        "opcode": "01001",
    },
    "xor": {
        "type": "A",
        "opcode": "01010",
    },
    "or": {
        "type": "A",
        "opcode": "01011",
    },
    "and": {
        "type": "A",
        "opcode": "01100",
    },
    "not": {
        "type": "C",
        "opcode": "01101",
    },
    "cmp": {
        "type": "C",
        "opcode": "01110",
    },
    "jmp": {
        "type": "E",
        "opcode": "01111",
    },
    "jlt": {
        "type": "E",
        "opcode": "11100",
    },
    "jgt": {
        "type": "E",
        "opcode": "11101",
    },
    "je": {
        "type": "E",
        "opcode": "11111",
    },
    "hlt": {
        "type": "F",
        "opcode": "11010",
    },
}

REGISTERS = {
    "R0": {
        "address": "000",
        "value": "",
    },
    "R1": {
        "address": "001",
        "value": "",
    },
    "R2": {
        "address": "010",
        "value": "",
    },
    "R3": {
        "address": "011",
        "value": "",
    },
    "R4": {
        "address": "100",
        "value": "",
    },
    "R5": {
        "address": "101",
        "value": "",
    },
    "R6": {
        "address": "110",
        "value": "",
    },
    "FLAGS": {
        "address": "111",
        "value": "",
    },
}

LABELS = {}

LABEL_LINES = set()

VARIABLES = {}

MEMORY_ADDRESSES = set()

VARIABLES_USED = []

# Type A: 3 Register Type
# def type_a(opcode: str, reg1: str, reg2: str, reg3: str) -> str:
def type_a(opcode, line_split: List[str]) -> str:
    reg1 = REGISTERS[line_split[1]]["address"]
    reg2 = REGISTERS[line_split[2]]["address"]
    reg3 = REGISTERS[line_split[3]]["address"]
    return f"{opcode}00{reg1}{reg2}{reg3}"


def int_to_bin_imm(imm_val: str) -> str:
    if ("." in imm_val){
        
    }
    return bin(imm_val)


# Type B : Register and Immediate Type
# def type_b(opcode: str, reg1: str, imm_val: str) -> str:
def type_b(opcode, line_split: List[str]) -> str:
    reg1 = REGISTERS[line_split[1]]["address"]
    imm_val = line_split[2][1:]
    imm_val = int_to_bin_imm(imm_val)
    if int(line_split[2][1:]) > 127:
        return "Error: Immediate value is more than 7 bits"
    return f"{opcode}0{reg1}{imm_val}"

# Type C : 2 registers type
# def type_c(opcode: str, reg1: str, reg2: str) -> str:
def type_c(opcode, line_split: List[str]) -> str:
    reg1 = REGISTERS[line_split[1]]["address"]
    reg2 = REGISTERS[line_split[2]]["address"]
    return f"{opcode}00000{reg1}{reg2}"


# Type D : Register and Memory Address Type
# def type_d(opcode: str, reg1: str, mem_add: str) -> str:
def type_d(opcode, line_split: List[str]) -> str:
    reg1 = REGISTERS[line_split[1]]["address"]
    mem_add = line_split[2]
    return f"{opcode}0{reg1}{mem_add}"


# Type E : Memory Address Type
# def type_e(opcode: str, mem_add: str) -> str:
def type_e(opcode, line_split: List[str]) -> str:
    mem_add = line_split[1]
    return f"{opcode}0000{mem_add}"


# Type F : Halt
# def type_f(opcode: str) -> str:
def type_f(opcode, line_split: List[str]) -> str:
    return opcode + ("0" * 11)


# Storing function references
FUNCTION_TYPES = {
    "A": type_a,
    "B": type_b,
    "C": type_c,
    "D": type_d,
    "E": type_e,
    "F": type_f,
}


def gen_random_memory_address():
    address = bin(randint(20, 127))[2:]
    address = (7 - len(address)) * "0" + address
    # TODO: Create a memory address dictionary and check if address is unique or not
    while (address in MEMORY_ADDRESSES):
        address = bin(randint(20, 127))[2:]
        address = (7 - len(address)) * "0" + address
    return address


def assign_variable(var_name: str):
    VARIABLES[var_name] = {}
    VARIABLES[var_name]["address"] = gen_random_memory_address()
    VARIABLES_USED.append(var_name)


def load_file(filename: str):
    with open(filename, "r") as f:
        FILE_TEMP = f.readlines()

    for i in range(len(FILE_TEMP)):
        line_split = FILE_TEMP[i].strip().split()

        if line_split[0][-1] == ":":
            LABELS[line_split[0][:-1]] = len(FILE)  # Check -1 or not
            LABEL_LINES.add(len(FILE))

        FILE.append(line_split)

def read_file():
    for i in range(len(FILE)):
        pass


def write_file(filename: str):
    with open(filename, "w") as f:
        for o in OUTPUT:
            f.write(o)
            f.write("\n")

FLAGS = {"V": 0, "L": 0, "G": 0, "E": 0}

def execute_instruction(line_split: List[str]):
    global FLAGS
    global VARIABLES_USED
    # Label statement encountered
    if PC in LABEL_LINES:
        line_split = line_split[1:]

    # Blank line encountered
    if len(line_split) == 1 and line_split[0] == "":
        return PC + 1

    # Variable assignment instruction
    if line_split[0] == "var":
        if (line_split[1] in VARIABLES_USED):
            print("Error: Variable already used")
            return None
        assign_variable(line_split[1])
        return PC + 1

    instruction = line_split[0]
    type_of_instruction = INSTRUCTIONS[instruction]["type"]
    opcode_of_instruction = INSTRUCTIONS[instruction]["opcode"]

    # If halt instruction encountered
    if instruction == "hlt":
        return len(FILE) + 1

    # Since mov has 2 types of instructions
    if instruction == "mov":
        if line_split[2][0] == "$": #Immediate value used
            if int(line_split[2][1:], 2) > 127: # check if the immediate value is more than 7 bits
                print("Error: Illegal Immediate value (more than 7 bits)")
                return None
            elif ((line_split[2][1:], 2) in MEMORY_ADDRESSES):
                print("Error: Address already occupied")
                return None
            opcode_of_instruction = "00010"
            result = type_b(opcode_of_instruction, line_split)
            OUTPUT.append(result)
        else: #Register used
            result = type_c(opcode_of_instruction, line_split)
            OUTPUT.append(result)
        return PC + 1

    # Check if register name is valid or not
    r = [all for all in line_split if "R" in all]
    for element in r:
        if element not in REGISTERS.keys():
            print("Error: Invalid register name")
            return None 

    # Check if variables are defined
    VARIABLES_USED = [a[1:] for a in line_split[1:] if a.startswith("$")]
    for variable in VARIABLES_USED:
        if variable not in VARIABLES and variable in LABELS:
            print("Error: Label used as variable")
            return None
        elif variable not in VARIABLES and variable not in LABELS:
            print("Error: Undefined variable")
            return None

    # Check if labels are defined
    labels_used = [a[:-1] for a in line_split if a.endswith(":")]
    for label in labels_used:
        if label not in LABELS and label in VARIABLES:
            print("Error: Variable used as label")
            return None
        elif label not in LABELS and label not in VARIABLES:
            print("Error: Undefined label")
            return None

    function_to_call = FUNCTION_TYPES[type_of_instruction]
    # Set flags register
    if instruction in ["add", "sub", "mul", "div"]:
        if instruction in ["add", "sub", "mul"]:
            # check if FLAGS is used as a destination register
            if line_split[1] == "FLAGS":
                print("Error: Illegal use of FLAGS register")
                return None
        result = function_to_call(opcode_of_instruction, line_split)
        if int(result) >= 2**16-1:
            FLAGS["V"] = 1
        else:
            FLAGS["V"] = 0
    elif instruction == "cmp":
        if line_split[1] == "FLAGS": # check if FLAGS is used as a destination register
            print("Error: Illegal use of FLAGS register")
            return None
        if REGISTERS[line_split[1]] < REGISTERS[line_split[2]]:
            FLAGS["L"] = 1
            FLAGS["G"] = 0
            FLAGS["E"] = 0
        elif REGISTERS[line_split[1]] > REGISTERS[line_split[2]]:
            FLAGS["L"] = 0
            FLAGS["G"] = 1
            FLAGS["E"] = 0
        else:
            FLAGS["L"] = 0
            FLAGS["G"] = 0
            FLAGS["E"] = 1

    result = function_to_call(opcode_of_instruction, line_split)
    OUTPUT.append(result)
    return PC + 1



def assemble():
    global PC
    global VARIABLES_USED
    while PC < len(FILE):
        line = FILE[PC]
        line_split = line

        # Check for missing hlt instruction
        if PC == len(FILE) - 1 and line_split[0] != "hlt":
            print("Error: Missing hlt instruction")
            return

        execute_instruction(line_split)
        PC += 1

    # Check if hlt instruction was used as the last instruction
    #if PC == len(FILE) and FILE[PC - 1].split()[0] != "hlt":
    #    print("Error: hlt not used as the last instruction")
    #    return


def init():
    global PC, FILE, OUTPUT, LABELS, VARIABLES, LABEL_LINES
    PC = 0
    FILE, OUTPUT = [], []
    LABELS, VARIABLES = {}, {}
    LABEL_LINES = set()

    for r in REGISTERS:
        REGISTERS[r]["value"] = ""

def print_output():
    for o in OUTPUT:
        print(o)

def main():
    init()
    load_file("sample.txt")
    assemble()
    print_output()
    write_file("output.txt")

if __name__ == "__main__":
    main()
