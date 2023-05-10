FILE = []

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
    "R7": {
        "address": "111",
        "value": "",
    },

}

LABELS = {}

# Type A: 3 Register Type
def type_a(opcode: str, reg1: str, reg2: str, reg3: str) -> str:
    return f"{opcode}00{reg1}{reg2}{reg3}"


# Type B : Register and Immediate Type
def type_b(opcode: str, reg1: str, imm_val: str) -> str:
    return f"{opcode}0{reg1}{imm_val}"


# Type C : 2 registers type
def type_c(opcode: str, reg1: str, reg2: str) -> str:
    return f"{opcode}00000{reg1}{reg2}"


# Type D : Register and Memory Address Type
def type_d(opcode: str, reg1: str, mem_add: str) -> str:
    return f"{opcode}0{reg1}{mem_add}"


# Type E : Memory Address Type
def type_e(opcode: str, mem_add: str) -> str:
    return f"{opcode}0000{mem_add}"


# Type F : Halt
def type_f(opcode: str) -> str:
    return opcode + ("0" * 11)

def load_file(filename: str):
    with open(filename, "r") as f:
        FILE_TEMP = f.readlines()
        for i in range(len(FILE_TEMP)):
            line = FILE_TEMP[i].stirp()
            if line == "":
                continue
            FILE[i] = line
            if FILE[i][0] == ".":
                LABELS[FILE[i]] = i

                  
def execute_instruction(line: str):
    pass

def assemble(filename: str):
    line_no = 0
    while (line_no < len(FILE)):
        #Handle case for jump/branch statements
        execute_instruction(FILE[line_no])
        i = i+1


def main():
    pass


if __name__ == "__main__":
    main()
