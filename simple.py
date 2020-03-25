import sys

if len(sys.argv) != 2:
    print("usage: file.py filename")
    sys.exit(1)

filename = sys.argv[1]

PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4 #saves value to register
PRINT_REGISTER = 5
ADD = 6
PUSH = 7
POP = 8


# memory = [
#     PRINT_BEEJ,
#     SAVE,
#     65,
#     2,
#     SAVE,
#     20,
#     3,
#     ADD,
#     2,
#     3,
#     PRINT_REGISTER,
#     2,
#     HALT



# ]

# #What does this do?
# register = [0] * 8

# #pc is "program counter"
# pc = 0
# running = True

def load_memory(filename):
    try:
        with open(filename) as f:
            for line in f:
                print(line)
                #ignore comments
                comment_split = line.split("#")
                #strip out white space
                num = comment_split.strip() #strip() removes white space
                #ignore blank lines
                if num == "":
                    continue
            
                val = int(num)
    except FileNotFoundError:
        print("File not found")
        sys.exit(2)


while running:
    #REPL: read eval print loop
    command = memory[pc]
    SP = 7

    if command == PRINT_BEEJ:
        print("BEEJ")
        pc += 1
    elif command == HALT:
        running = False
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2
    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2

    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc+=3
    elif command == PUSH:
        reg = memory[pc + 1]
        val = register[reg]
        register[SP] -= 1
        memory[register[SP]] = val
        pc += 2
    elif command == POP:
        reg = memory[pc + 1]
        val = memory[register[SP]]
        register[reg] = val
        register[SP]
        pc += 2

    else:
        print(f"Unknown instruction: {command}")
        sys.exit(1)
