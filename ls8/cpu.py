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
        self.PUSH = 69
        self.POP = 70
        self.SP = 7
        self.CALL = 80
        self.RET = 17


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
                #self.alu("MUL", 0, 1)
                self.alu("MUL", self.ram[pc+1], self.ram[pc+2])
                pc += 3
            elif command == self.PRN:
                register_address = self.ram[self.address + 1]
                print(self.reg[register_address])
                pc += 2
            elif command == self.POP:
                #reg = self.ram[self.address + 1]
                reg = self.ram[pc + 1]
                val = self.ram[self.reg[self.SP]]
                self.reg[reg] = val
                self.reg[self.SP] += 1
                pc += 2
            elif command == self.PUSH:
                reg = self.ram[pc + 1]
                #reg = self.ram[self.address + 1]
                val = self.reg[reg]
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = val
                
                pc += 2
            elif command == self.CALL:
                pass
            elif command == self.RET:
                pass
            else: 
                print("Command not in system. Game over")
                sys.exit(1)
    
    def ram_read(self, mar):
         print(self.ram[mar])
    
    #def ram_write(self, mdr):
    def ram_write(self, mdr):
        self.address += 1
        self.ram[self.address] = mdr

    



##################