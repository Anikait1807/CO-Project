import sys
from pprint import pprint


class BINARY:
    # Binary number will be stored as a string
    def __init__(self, val: str = None, bits=None):
        self.val = val

        if bits is None:
            self.bits = 16
        else:
            self.bits = bits

        self.normalized = False
        if self.bits and self.val:
            self.limit_bits()
            self.normalized = True

    def get_int_val(self):
        if self.check_valid_binary():
            return int(self.val, 2)

    def check_valid_binary(self):
        allowed_set = {0, 1}
        for cur_char in self.val:
            if cur_char not in allowed_set:
                return False

    def limit_bits(self, bits_arg=None):
        if bits_arg is not None:
            self.bits = bits_arg

        if len(self.val) < self.bits:
            self.val = ("0" * (self.bits - len(self.val))) + self.val

        elif len(self.val) > self.bits:
            bits_not_sufficient = False
            removed = self.val[:-(self.bits)]
            for cur_char in removed:
                if cur_char == "1":
                    bits_not_sufficient = True
                    break

            self.val = self.val[-(self.bits):]

    def add_three_binary(self, bin_2, bin_3):
        added_val = int(self.val, 2) + int(bin_2.val, 2) + int(bin_3.val, 2)
        if self.bits is not None:
            if added_val > (2 ** self.bits):
                return "overflow"

        # return BINARY(str(added_val))

    def add(self, bin_2):
        added_val = int(self.val, 2) + int(bin_2.val, 2)
        if self.bits is not None:
            if added_val > (2 ** self.bits):
                return "overflow"

        return BINARY(bin(added_val)[2:], self.bits)

    def sub(self, bin_2):
        result_val = int(self.val, 2) - int(bin_2.val, 2)
        if self.bits is not None:
            if result_val > (2 ** self.bits):
                return "overflow"

        # TODO: See what has to be done in underflow
        if result_val < 0:
            return "underflow"

        return BINARY(bin(result_val)[2:], self.bits)

    def mul_three_binary(self, bin_2, bin_3):
        multiplied_val = int(self.val, 2) * int(bin_2.val, 2) * int(bin_3.val, 2)
        if self.bits is not None:
            if multiplied_val > (2 ** self.bits):
                return "overflow"

        # return BINARY(str(multiplied_val))

    def mult(self, bin_2):
        multiplied_val = int(self.val, 2) * int(bin_2.val, 2)
        if self.bits is not None:
            if multiplied_val > (2 ** self.bits):
                return "overflow"

        print("Multiplied value here is", multiplied_val)
        return BINARY(bin(multiplied_val)[2:], self.bits)

    def comp(bin_1, bin_2):
        val1 = int(bin_1.val, 2)
        val2 = int(bin_2.val, 2)

        if val1 > val2:
            return 1

        elif val1 == val2:
            return 0

        elif val1 < val2:
            return -1

    def div_two_binary(bin_1, bin_2):
        a = BINARY.get_int_val(bin_1)
        b = BINARY.get_int_val(bin_2)
        quotient = a // b
        remainder = a % b
        return {"quotient": BINARY(bin(quotient)[2:]), "remainder": BINARY(bin(remainder)[2:])}

    def xorb(bin1, bin2):
        answer = ""
        for i in range(len(bin1.val)):
            val1 = int(bin1.val[i])
            val2 = int(bin2.val[i])
            if (val1 or val2) and not (val1 and val2):
                answer = "1" + answer
            else:
                answer = "0" + answer
        return BINARY(answer)

    def orb(bin1, bin2):
        answer = ""
        for i in range(len(bin1.val)):
            val1 = int(bin1.val[i])
            val2 = int(bin2.val[i])
            answer = answer + str(val1 or val2)

        return BINARY(answer)

    def andb(bin1, bin2):
        answer = ""
        for i in range(len(bin1.val)):
            val1 = int(bin1.val[i])
            val2 = int(bin2.val[i])
            answer = answer + str(val1 and val2)

        return BINARY(answer)

    def notb(bin1):
        invert = {
            "0": "1",
            "1": "0",
        }

        answer = ""
        for i in range(len(bin1.val)):
            answer = invert[bin1.val[i]] + answer

        return BINARY(answer)


class REGISTERS:
    def __init__(self, name=None, val=None, address=None):
        self.val = BINARY("0", 16)  # Initializing by 0
        self.name = name
        self.address = None


class FLAG_REGISTERS:
    def __init__(self, name=None, val=None, address=None):
        self.val = BINARY("0" * 16)
        self.overflow = False
        self.greater_than = False
        self.less_than = False
        self.equal_to = False
        self.update_val()

    def reset_val(self):
        self.val = BINARY("0" * 16)
        self.overflow = False
        self.greater_than = False
        self.less_than = False
        self.equal_to = False
        self.update_val()

    def get_flag_content(self):
        contents = "0" * 12
        contents = contents + f"{int(self.overflow)}{int(self.less_than)}{int(self.greater_than)}{int(self.equal_to)}"
        return contents

    def update_val(self):
        old_val = self.val
        self.val = BINARY(self.get_flag_content())
        if self.val.val != old_val.val:
            return 1
        return 0


def fetch_register(address: str) -> REGISTERS:
    return REGISTERS_DICT[address]


class MEMORY:
    def __init__(self):
        self.data = dict()
        self.total_bytes = 256
        # address (7 bit) : value


class PROGRAM_COUNTER:
    def __init__(self):
        self.val = 0
        self.next = 1
        self.max_len = 0
        self.end_reached = False
        self.halted = False

    def go_to_next(self):
        if self.halted:
            print("Program halted")
            return

        if self.next >= self.max_len:
            # TODO: remove these comments
            # print("self.val is", self.val)
            # print("self.next is", self.next)
            # print("max len is", self.max_len)
            # print("End of program reached")
            self.end_reached = True
            return

        self.val = self.next
        self.next = self.val + 1


FLAG = FLAG_REGISTERS()
REGISTERS_DICT = {"111": FLAG_REGISTERS()}
MEM = MEMORY()
FILE = []
OUTPUT = []
PC = PROGRAM_COUNTER()

# CURRENT_STATUS = {
#     "PC": PC.val,
#     "R0": REGISTERS_DICT["00000"],
#     "R1": REGISTERS_DICT["00001"],
#     "R2": REGISTERS_DICT["00010"],
#     "R3": REGISTERS_DICT["00011"],
#     "R4": REGISTERS_DICT["00100"],
#     "R5": REGISTERS_DICT["00101"],
#     "R6": REGISTERS_DICT["00110"],
#     "FLAGS_VAL": FLAG.val,
#     "FLAGS_GT": FLAG.greater_than,
#     "FLAGS_LT": FLAG.less_than,
#     "FLAGS_EQ": FLAG.equal_to,
# }

CURRENT_STATUS = dict()


def update_current_status():
    CURRENT_STATUS["PC"] = PC.val
    CURRENT_STATUS["R0"] = REGISTERS_DICT["000"].val.val
    CURRENT_STATUS["R1"] = REGISTERS_DICT["001"].val.val
    CURRENT_STATUS["R2"] = REGISTERS_DICT["010"].val.val
    CURRENT_STATUS["R3"] = REGISTERS_DICT["011"].val.val
    CURRENT_STATUS["R4"] = REGISTERS_DICT["100"].val.val
    CURRENT_STATUS["R5"] = REGISTERS_DICT["101"].val.val
    CURRENT_STATUS["R6"] = REGISTERS_DICT["110"].val.val
    REGISTERS_DICT["111"].update_val()
    CURRENT_STATUS["FLAG_CONTENT"] = REGISTERS_DICT["111"].get_flag_content()
    CURRENT_STATUS["FLAGS_VAL"] = REGISTERS_DICT["111"].val.val
    CURRENT_STATUS["FLAGS_GT"] = REGISTERS_DICT["111"].greater_than
    CURRENT_STATUS["FLAGS_LT"] = REGISTERS_DICT["111"].less_than
    CURRENT_STATUS["FLAGS_EQ"] = REGISTERS_DICT["111"].equal_to


# TODO: Fix this function
def add_to_output():
    update_current_status()
    OUTPUT.append(CURRENT_STATUS)


def init_registers():
    for i in range(7):
        address = BINARY(bin(i)[2:], 3)
        REGISTERS_DICT[address.val] = REGISTERS()
    REGISTERS_DICT["111"] = FLAG_REGISTERS()


def load_file():
    file_temp = sys.stdin.readlines()
    # with open(filename, "r") as f:
    #     file_temp = f.readlines()

    for i in range(len(file_temp)):
        line_split = file_temp[i].strip().split()

        # if line_split[0][-1] == ":":
        #     LABELS[line_split[0][:-1]] = {}  # Check -1 or not
        #     LABEL_LINES.add(len(FILE))

        # if line_split[0] == "var":
        #     VARIABLES[line_split[1]] = {}

        FILE.append(line_split)


def print_output():
    for o in OUTPUT:
        sys.stdout.write(o + "\n")


def init():
    global MEM
    MEM = MEMORY()
    global PC
    PC = PROGRAM_COUNTER()
    global FILE
    FILE = []
    global REGISTERS_DICT
    REGISTERS_DICT = {}
    init_registers()
    update_current_status()


# --------- TYPE A INSTRUCTIONS ---------

def add_a(reg1_add: str, reg2_add: str, reg3_add: str):
    reg3_val = REGISTERS_DICT[reg3_add].val
    added_val = REGISTERS_DICT[reg2_add].val.add(reg3_val)

    if added_val == "overflow":
        REGISTERS_DICT[reg1_add].val = BINARY("0", 16)
        REGISTERS_DICT["111"].overflow = True
    else:
        REGISTERS_DICT[reg1_add].val = added_val
        REGISTERS_DICT[reg1_add].val.limit_bits(16)


# TODO: Fix this function as it is subtract and not add
def sub_a(reg1_add: str, reg2_add: str, reg3_add: str):
    reg2_val = REGISTERS_DICT[reg2_add].val
    reg3_val = REGISTERS_DICT[reg3_add].val
    sub_val = REGISTERS_DICT[reg2_add].val.sub(reg3_val)

    if sub_val == "overflow":
        REGISTERS_DICT[reg1_add].val = BINARY("0", 16)
        REGISTERS_DICT["111"].overflow = True

    elif sub_val == "underflow":
        REGISTERS_DICT[reg1_add].val = BINARY("0", 16)

    else:
        REGISTERS_DICT[reg1_add].val = sub_val
        REGISTERS_DICT[reg1_add].val.limit_bits(16)


def mult_a(reg1_add: str, reg2_add: str, reg3_add: str):
    reg3_val = REGISTERS_DICT[reg3_add].val
    mult_val = REGISTERS_DICT[reg2_add].val.mult(reg3_val)

    if mult_val == "overflow":
        REGISTERS_DICT[reg1_add].val = BINARY("0", 16)
        REGISTERS_DICT["111"].overflow = True
    else:
        REGISTERS_DICT[reg1_add].val = mult_val
        REGISTERS_DICT[reg1_add].val.limit_bits(16)


def xor_a(reg1_add: str, reg2_add: str, reg3_add: str):
    reg2_val = REGISTERS_DICT[reg2_add].val
    reg3_val = REGISTERS_DICT[reg3_add].val
    REGISTERS_DICT[reg1_add].val = BINARY.xorb(reg2_val, reg3_val)


def or_a(reg1_add: str, reg2_add: str, reg3_add: str):
    reg2_val = REGISTERS_DICT[reg2_add].val
    reg3_val = REGISTERS_DICT[reg3_add].val
    REGISTERS_DICT[reg1_add].val = BINARY.orb(reg2_val, reg3_val)


def and_a(reg1_add: str, reg2_add: str, reg3_add: str):
    reg2_val = REGISTERS_DICT[reg2_add].val
    reg3_val = REGISTERS_DICT[reg3_add].val
    REGISTERS_DICT[reg1_add].val = BINARY.andb(reg2_val, reg3_val)


type_a = {
    "00000": add_a,
    "00001": sub_a,
    "00110": mult_a,
    "01010": xor_a,
    "01011": or_a,
    "01100": and_a,
}


def execute_type_a(instruction: str):
    # | opcode x 5 | unused x 2 | reg1 x 3 | reg2 x 3 | reg3 x 3|
    opcode = instruction[:5]
    r1_address = instruction[7:10]
    r2_address = instruction[10:13]
    r3_address = instruction[13:16]
    type_a[opcode](r1_address, r2_address, r3_address)


# --------- TYPE B INSTRUCTIONS ---------


def mov_i_b(reg1_add: str, imm_val: str):
    REGISTERS_DICT[reg1_add].val = BINARY(imm_val)


def rs_b(reg1_add: str, imm_val: str):
    original_val = REGISTERS_DICT[reg1_add].val.val
    new_val = original_val

    for _ in range(int(imm_val)):
        new_val = "0" + new_val[:-1]

    REGISTERS_DICT[reg1_add].val = BINARY(new_val)


def ls_b(reg1_add: str, imm_val: str):
    original_val = REGISTERS_DICT[reg1_add].val.val
    new_val = original_val

    for _ in range(int(imm_val)):
        new_val = new_val[1:] + "0"

    REGISTERS_DICT[reg1_add].val = BINARY(new_val)


type_b = {
    "00010": mov_i_b,
    "01000": rs_b,
    "01001": ls_b,
}


def execute_type_b(instruction: str):
    # | opcode x 5 | unused x 1 | reg1 x 3 | imm_val x 7 |
    opcode = instruction[:5]
    r1_address = instruction[6:9]
    imm_val = instruction[9:16]
    type_b[opcode](r1_address, imm_val)


# --------- TYPE C INSTRUCTIONS ---------
def mov_c(reg1_add: str, reg2_add: str):
    # Doing this to make sure a copy of the binary object is created
    # Rather than two registers pointing to the same binary object
    REGISTERS_DICT[reg1_add].val = BINARY(REGISTERS_DICT[reg2_add].val.val)


def div_c(reg1_add: str, reg2_add: str):
    if REGISTERS_DICT[reg2_add].val.get_int_val() == 0:
        REGISTERS_DICT["111"].overflow = True
        REGISTERS_DICT["00000"].val = BINARY("0", 16)
        REGISTERS_DICT["00001"].val = BINARY("0", 16)
        return

    result = BINARY.div_two_binary(
        REGISTERS_DICT[reg1_add].val, REGISTERS_DICT[reg2_add].val
    )
    REGISTERS_DICT["00000"].val = result["quotient"]
    REGISTERS_DICT["00000"].val.limit_bits(16)
    REGISTERS_DICT["00001"].val = result["remainder"]


def not_c(reg1_add: str, reg2_add: str):
    REGISTERS_DICT[reg1_add].val = BINARY.notb(REGISTERS_DICT[reg2_add].val)


def cmp_c(reg1_add: str, reg2_add: str):
    result = BINARY.comp(REGISTERS_DICT[reg1_add].val, REGISTERS_DICT[reg2_add].val)
    if result == 1:
        REGISTERS_DICT["111"].greater_than = True
        # Should reset other flags ---v
        REGISTERS_DICT["111"].less_than = False
        REGISTERS_DICT["111"].equal_to = False

    elif result == 0:
        REGISTERS_DICT["111"].equal_to = True
        # Should reset other flags ---v
        REGISTERS_DICT["111"].less_than = False
        REGISTERS_DICT["111"].greater_than = False

    elif result == -1:
        REGISTERS_DICT["111"].less_than = True
        # Should reset other flags ---v
        REGISTERS_DICT["111"].greater_than = False
        REGISTERS_DICT["111"].equal_to = False


type_c = {
    "00011": mov_c,
    "00111": div_c,
    "01101": not_c,
    "01110": cmp_c,
}


def execute_type_c(instruction: str):
    # | opcode x 5 | unused x 5 | reg1 x 3 | reg2 x 3 |
    opcode = instruction[:5]
    r1_address = instruction[10:13]
    r2_address = instruction[13:16]
    type_c[opcode](r1_address, r2_address)


# --------- TYPE D INSTRUCTIONS ---------
def ld(reg1_add: str, mem_add: str):
    REGISTERS_DICT[reg1_add].val = BINARY(MEM.data[mem_add].val)


def st(reg1_add: str, mem_add: str):
    MEM.data[mem_add] = BINARY(REGISTERS_DICT[reg1_add].val.val)


type_d = {
    "00100": ld,
    "00101": st,
}


def execute_type_d(instruction: str):
    # | opcode x 5 | unused x 1 | reg1 x 3 | mem_add x 7 |
    opcode = instruction[:5]
    r1_address = instruction[6:9]
    mem_add = instruction[9:16]
    type_d[opcode](r1_address, mem_add)


# --------- TYPE E INSTRUCTIONS ---------
def jmp(mem_add: str):
    PC.next = int(mem_add, 2)


def jlt(mem_add: str):
    if REGISTERS_DICT["111"].less_than:
        PC.next = int(mem_add, 2)
        REGISTERS_DICT["111"].less_than = False


def jgt(mem_add: str):
    if REGISTERS_DICT["111"].greater_than:
        PC.next = int(mem_add, 2)
        REGISTERS_DICT["111"].greater_than = False


def je(mem_add: str):
    if REGISTERS_DICT["111"].equal_to:
        PC.next = int(mem_add, 2)
        REGISTERS_DICT["111"].equal_to = False


type_e = {
    "01111": jmp,
    "11100": jlt,
    "11101": jgt,
    "11111": je,
}


def execute_type_e(instruction: str):
    # | opcode x 5 | unused x 4 | mem_add x 7 |
    opcode = instruction[:5]
    mem_add = instruction[9:16]
    type_e[opcode](mem_add)


# --------- MAIN EXECUTE BODY ---------


def halt():
    PC.halted = True


def execute(instruction: str):
    opcode = instruction[:5]
    if opcode in type_a:
        execute_type_a(instruction)
    elif opcode in type_b:
        execute_type_b(instruction)
    elif opcode in type_c:
        execute_type_c(instruction)
    elif opcode in type_d:
        execute_type_d(instruction)
    elif opcode in type_e:
        execute_type_e(instruction)


def append_output():
    bin_pc = BINARY(bin(PC.val)[2:], 7)
    bgap = "       "
    cur_out = f"{bin_pc.val}{bgap}"
    for i in range(7):
        reg_key = "R" + str(i)
        cur_out = cur_out + f" {CURRENT_STATUS[reg_key]}"

    cur_out = cur_out + f" {CURRENT_STATUS['FLAG_CONTENT']}"
    cur_out = cur_out + f"\n"
    OUTPUT.append(cur_out)


def read_from_file():
    global FILE
    with open("in.txt", "r") as f:
        FILE = f.readlines()


def init_memory():
    global MEM
    MEM = MEMORY()

    i_b = BINARY("0")
    i_b.limit_bits(7)
    incrementer = BINARY("1")
    incrementer.limit_bits(7)
    for i in range(len(FILE)):
        MEM.data[i_b.val] = BINARY(FILE[i].strip(), 16)
        i_b = i_b.add(incrementer)

    empty = BINARY("0" * 16, 16)
    for i in range(len(FILE), 128):
        MEM.data[i_b.val] = empty
        i_b = i_b.add(incrementer)


def dump_code():
    for mem_add in sorted(MEM.data):
        to_append = MEM.data[mem_add].val + "\n"
        OUTPUT.append(to_append)
    OUTPUT[-1] = OUTPUT[-1].strip()


def write_output_to_file():
    # pprint(OUTPUT)
    with open("out.txt", "w") as f:
        f.writelines(OUTPUT)


def print_output_sys():
    for o in OUTPUT:
        sys.stdout.write(o)


def load_file_sys():
    file_temp = sys.stdin.readlines()
    for line in file_temp:
        line = line.strip()
        FILE.append(line)


def file_based():
    init()
    update_current_status()
    read_from_file()
    init_memory()
    PC.max_len = len(FILE)
    while not PC.end_reached and not PC.halted:
        print("v-------------------------v")
        instruction = FILE[PC.val]
        print(instruction)
        execute(instruction)
        REGISTERS_DICT["111"].update_val()
        update_current_status()
        pprint(CURRENT_STATUS)
        append_output()
        PC.go_to_next()
        print("^-------------------------^")

    # pprint(MEM.data)
    dump_code()
    write_output_to_file()


def sys_based():
    init()
    update_current_status()
    load_file_sys()
    init_memory()
    PC.max_len = len(FILE)
    while not PC.end_reached and not PC.halted:
        instruction = FILE[PC.val]
        execute(instruction)
        result = REGISTERS_DICT["111"].update_val()
        if result == 0:
            REGISTERS_DICT["111"].reset_val()
        update_current_status()
        append_output()
        PC.go_to_next()

    dump_code()
    print_output_sys()


def main():
    file_based()
    # sys_based()


if __name__ == "__main__":
    main()
