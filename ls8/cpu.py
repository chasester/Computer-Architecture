"""CPU functionality."""

import sys

#make this constant if exporting
cmds =  { #list of all callable commands and there codes
        #"BYTE_ID": (NUM_BYTES, "COMMMAND")
        0b10100000: (2, "ADD"),
        0b10101000: (2, "AND"),
        0b01010000: (1, "CALL"),
        0b10100111: (2, "CMP"),
        0b01100110: (1, "DEC"),
        0b10100011: (2, "DIV"),
        0b00000001: (0, "HLT"),
        0b01100101: (1, "INC"),
        0b01010010: (1, "INT"),
        0b00010011: (0, "IRET"),
        0b01010101: (1, "JEQ"),
        0b01011010: (1, "JGE"),
        0b01010111: (1, "JGT"),
        0b01011001: (1, "JLE"),
        0b01011000: (1, "JLT"),
        0b01010100: (1, "JMP"),
        0b01010110: (1, "JNE"),
        0b10000011: (2, "LD"),
        0b10000010: (2, "LDI"),
        0b10100100: (2, "MOD"),
        0b10100010: (2, "MUL"),
        0b00000000: (0, "NOP"),
        0b01101001: (1, "NOT"),
        0b10101010: (1, "OR"),
        0b01000110: (1, "POP"),
        0b01001000: (1, "PRA"),
        0b01000111: (1, "PRN"),
        0b01000101: (1, "PUSH"),
        0b00010001: (0, "RET"),
        0b10101100: (2, "SHL"),
        0b10101101: (2, "SHR"),
        0b10000100: (2, "ST"),
        0b10100001: (2, "SUB"),
        0b10101011: (2, "XOR")
    }
EQ = 1 << 0;
GT = 1 << 1;
LT = 1 << 2;

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.index = 0;
        self.mem = -1;
        self.reg = []
        self.ram = [0b00000000 for i in range(256)]; #fill with No code
        self.pc = [];
        self.error = None;
        self.terminate = False;
        self.cmp = 0;

    def load(self, fname):
        """Load a program into memory."""

        self.reg = [0 for i in range(8)]; #times the size of our regerstry or our cpu memory
        self.reg[7] = 0xF4;
        address = 0
        self.index = 0;
        # For now, we've just hardcoded a program:

        """ program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ] """
        program = [];
        f = open(f'ls8/examples/{fname}.ls8', 'r');
        fl = f.readlines();
        for l in fl:
            l = l.split('#')[0];
            l = l.strip();
            if(l == ""):
                continue;
            program.append(int(l,2));
        for instruction in program:
            self.ram[address] = instruction
            address += 1
        #self.ram[address] = 0b00000001; #add a hlt here

    def ram_read(self, reg_a):
        return self.reg[reg_a];
    def ram_assign(self, reg_a, val):
        self.reg[reg_a] = val;
    def ADD(self, reg_a=0, reg_b=0):
        self.reg[reg_a] += self.reg[reg_b]
    def AND(self, reg_a=0, reg_b=0):
        self.reg[reg_a] &= self.reg[reg_b]
    def CALL(self, reg_a=0, reg_b=0):
        self.ram[self.mem] = self.index;#push address onto the stack
        self.mem -= 1;
        self.index = self.reg[reg_a];
        
    def CMP(self, reg_a=0, reg_b=0):
        r = self.reg[reg_a] - self.reg[reg_b]
        self.cmp = EQ if r == 0 else GT if r > 1 else LT;
    def DEC(self, reg_a=0, reg_b=0):
        self.reg[reg_a] -= 1;
    def DIV(self, reg_a=0, reg_b=0):
        self.reg[reg_a] /= self.reg[reg_b]
    def HLT(self, reg_a=0, reg_b=0, code=0): #code is used if called from the assembly due to a coding error
        if(self.error != None):
            print(self.error);
        print("exited with code 0 : sucess" if code == 0 else "exited with code " + str(code) + " see log for error");
        self.terminate = True;
    def INC(self, reg_a=0, reg_b=0):
        self.reg[reg_a] += 1;
    def INT(self, reg_a=0, reg_b=0):
        pass;
    def IRET(self, reg_a=0, reg_b=0):
        pass;
    def JEQ(self, reg_a=0, reg_b=0):
        self.index = self.reg[reg_a] if self.cmp & (EQ) else self.index; 
    def JGE(self, reg_a=0, reg_b=0):
        self.index = self.reg[reg_a] if self.cmp & (EQ|GT) else self.index;
    def JGT(self, reg_a=0, reg_b=0):
        self.index = self.reg[reg_a] if self.cmp & (GT) else self.index;
    def JLE(self, reg_a=0, reg_b=0):
        self.index = self.reg[reg_a] if self.cmp & (EQ|LT) else self.index;
    def JLT(self, reg_a=0, reg_b=0):
        self.index = self.reg[reg_a] if self.cmp & (LT) else self.index;
    def JMP(self, reg_a=0, reg_b=0):
        self.index = self.reg[reg_a];
    def JNE(self, reg_a=0, reg_b=0):
        self.index = self.reg[reg_a] if not(self.cmp & (EQ|LT)) else self.index;
    def LD(self, reg_a=0, reg_b=0):
        self.reg[reg_a] = self.reg[reg_b];
    def LDI(self,reg_a=0, reg_b=0):
        self.reg[reg_a] = int(reg_b); #reg_b is treated as raw data ie a reference not a pointer
    def MOD(self, reg_a=0, reg_b=0):
        self.reg[reg_a] %= self.reg[reg_b];
    def NOP(self, reg_a=0, reg_b=0):
        pass;
    def NOT(self, reg_a=0, reg_b=0):
        self.reg[reg_a] != self.reg[reg_a];
    def OR(self, reg_a=0, reg_b=0):
        self.reg[reg_a] |= self.reg[reg_b];
    def POP(self, reg_a=0, reg_b=0):
        self.mem += 1;
        self.reg[reg_a] = self.ram[self.mem]
    def PRA(self, reg_a=0, reg_b=0):
        print(chr(self.ram[self.reg[reg_a]]));
    def PRN(self,reg_a=0, reg_b=0):
        print(self.reg[reg_a]);
    def PUSH(self, reg_a=0, reg_b=0):
        self.ram[self.mem] = self.reg[reg_a];
        self.mem -= 1;
    def RET(self, reg_a=0, reg_b=0):
        self.mem += 1;
        self.index = self.ram[self.mem]; #pop the return address;
    def SHL(self, reg_a=0, reg_b=0):
        self.reg[reg_a] <<= self.reg[reg_b];
    def SHR(self, reg_a=0, reg_b=0):   
        self.reg[reg_a] >>= self.reg[reg_b];
    def ST(self, reg_a=0, reg_b=0):
        pass
    def SUB(self, reg_a=0, reg_b=0):
        self.reg[reg_a] -= self.reg[reg_b];
    def XOR(self, reg_a=0, reg_b=0):
        self.reg[reg_a] ^= self.reg[reg_b];

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
        """Run the CPU."""
        self.error = None; #reset from last command
        self.terminate = False;
        self.index = 0;
        self.mem = -1;
        if(len(self.ram) < 1):
            self.error = "Bind program to ram by calling CPU::Load() before runing code"
        while len(self.ram) > 0: #code out each instuction here
            #instead of doing some weird if elif chain we are gonna fake an enum with a dictionary
            if(self.terminate == True):
                break;
        
            try:
                bcmd = self.ram[self.index]
                blu = cmds[bcmd];
                reg = [0,0];
                self.index += 1;
                for i in range(blu[0]):
                    reg[i] = self.ram[self.index];
                    self.index += 1;
                cmd = blu[1];
                #print(cmd, reg);
                try:
                    getattr(self, cmd)(reg[0], reg[1]);
                except:
                    self.error = "Error inside the comand " + str(cmd);
                    self.HLT(0,0,3);
            except KeyError:
                self.error = "unknow command " + str(bcmd);
                self.HLT(0,0,2); #trigger a syntax error here; then exit;
                break;
            except KeyboardInterrupt:
                self.error = "unknow user interupt"
                self.HLT(1); #trigger a user kill here
                break;

cpu = CPU()

cpu.load("printstr");
cpu.run()