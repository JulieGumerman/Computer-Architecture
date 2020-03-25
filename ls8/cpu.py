"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.counter = 0
        self.address = [0]


    #I'm not quite sure what this does yet....Maybe I should check...
    if len(sys.argv) != 2: 
        print("usage: file.py filename")
        sys.exit(1)
    filename = sys.argv[1]

    def load(self):
        """Load a program into memory."""

        self.address = 0

        # For now, we've just hardcoded a program:
        LDI = 0b10000010
        PRN = 0b01000111
        HALT = 0b00000001


        program = [
            # From print8.ls8
            LDI, # LDI R0,8
            #0b00000000,
            #0b00001000,
            PRN,
            #0b00000000,
            HALT, # HLT
        ]



        for instruction in program:
            self.ram[self.address] = instruction
            self.address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        pc = 0
        running = True
        while running:
            command = self.ram[pc]
            #LDI
            if command == 130:
                self.ram_write(8)
                pc += 1
            #HALT
            elif command == 1:
                running = False
                pc += 1
            #PRN
            elif command == 71:
                self.ram_read(self.address)
                pc +=1

    
    def ram_read(self, mar):
        print(self.ram[mar])
    
    def ram_write(self, mdr):
        self.address += 1
        self.ram[self.address] = mdr
    
    def load(filename):
        try:
            with open(filename) as f:
                for line in f:
                    print(line)
                    comment_split = line.split("#")
                    num = comment_split.strip()
                    if num == "":
                        continue

                    val = int(num)
        
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)


##################