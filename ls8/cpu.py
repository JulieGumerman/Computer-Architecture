"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.counter = 0
        self.address = 0
        self.LDI = 130
        self.HLT = 1
        self.PRN = 71
        self.MUL = 162
        self.ADD = 160
        self.PUSH = 69
        self.POP = 70
        self.SP = 7
        self.CALL = 80
        self.RET = 17
        self.CMP = 167
        self.JMP = 84
        self.JEQ = 85
        self.JNE = 86
        self.equal_flag = 0
#        self.equal_flag = None
#        self.less_than_flag = 

#        self.greater_than_flag = None


    def load(self):
        print(sys.argv)
        filename = sys.argv[1]
        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue
                    val = int(num, 2)
                    self.ram[self.address] = val
                    self.address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
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
            if command == self.LDI:
                register_address = self.ram[pc + 1]
                value = self.ram[pc + 2]
                self.reg[register_address] = value
                pc += 3
            elif command == self.HLT:
                running = False
                pc += 1
                sys.exit(1)
            elif command == self.MUL:
                self.alu("MUL", self.ram[pc+1], self.ram[pc+2])
                pc += 3
            elif command == self.ADD:
                self.alu("ADD", self.ram[pc+1], self.ram[pc+2])
                pc += 3
            elif command == self.PRN:
                register_address = self.ram[pc + 1]
                print(self.reg[register_address])
                pc += 2
            elif command == self.POP:
                reg = self.ram[pc + 1]
                val = self.ram[self.reg[self.SP]]
                self.reg[reg] = val
                self.reg[self.SP] += 1
                pc += 2
            elif command == self.PUSH:
                reg = self.ram[pc + 1]
                val = self.reg[reg]
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = val
                pc += 2
            elif command == self.CALL:
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = pc + 2
                reg = self.ram[pc + 1]
                pc = self.reg[reg]
            elif command == self.RET:
                pc = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
            ###SPRINT IMPLEMENTATION BELOW THIS LINE
            elif command == self.CMP:
                reg_a = self.ram[pc + 1]
                reg_b = self.ram[pc +2]
                if reg_a == reg_b:
                    print("triggered equal")
                    self.equal_flag = 1
                    self.less_than_flag = 0
                    self.greater_than_flag = 0
                elif reg_a < reg_b:
                    self.less_than_flag = 1
                    self.greater_than_flag = 0
                elif reg_a > reg_b:
                    self.less_than_flag = 0
                    self.greater_than_flag = 1
                pc += 3
            elif command == self.JMP:
                """
                JMP register

                Jump to the address stored in the given register.

                Set the PC to the address stored in the given register.

                Machine code:
                """
                address = self.ram[pc + 1]
                pc = self.reg[address]
            elif command == self.JEQ:
                """
                JEQ register

                If equal flag is set (true), jump to the address stored in the given register.

                Machine code:        
                """
                if self.equal_flag == 1:
                    location = pc + 1
                    pc = self.reg[self.ram[location]]
                else:
                    pc += 2
            elif command == self.JNE:
                """
                JNE register

                If E flag is clear (false, 0), jump to the address stored in the given register.

                Machine code:

                01010110 00000rrr
                56 0r
                """
                if self.equal_flag == 0:
                    location = self.ram[pc + 1]
                    pc = self.reg[location]
                else:
                    pc += 2
            ##SPRINT IMPLEMENTATION ABOVE THIS LINE
            else: 
                print("Command not in system. Game over")
                sys.exit(1)
    
    def ram_read(self, mar):
         print(self.ram[mar])
    

    def ram_write(self, mdr):
        self.address += 1
        self.ram[self.address] = mdr
