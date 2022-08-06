import sys 
import fileinput


def Overflow(value):
    if(value > 2**16 - 1):
        return True
    else:
        return False
    

class Memory:
    inputMemory = []

    def initialize(self):
        for line in sys.stdin:
            self.inputMemory.append(line.rstrip())
        
        if(len(self.inputMemory)<256):
            for i in range(len(self.inputMemory),256):
                self.inputMemory.append("0"*16)
        
    def dump(self):
        for i in range(len(self.inputMemory)):
           print(self.inputMemory[i])
    
    def getData(self, address):
        return self.inputMemory[address]


class ProgramCounters:
    Counter=0
    PrevCounter=0
    Jump=False
    def update(self,new_PC):
        self.Counter = new_PC

    def dump(self):
        if(not self.Jump):
            binary=bin(self.Counter)[2::]
            print('0'*(8- len(binary)) + binary,end=' ')
        elif(self.Jump):
            binary=bin(self.PrevCounter)[2::]
            print('0'*(8- len(binary)) + binary,end=' ')
            self.Jump=False
    



class RegisterFiles:
    Registers={
        '000':0,
        '001':0,
        '010':0,
        '011':0,
        '100':0,
        '101':0,
        '110':0,
        '111':'0000000000000000'
    }
    # Flags='0000000000000000'

    def updateRegister(self,register,value):
        if(type(value)==str):
            self.Registers[register]=int(value,2)
        elif(value in self.Registers and register in self.Registers):
            self.Registers[register]=value
        else:
            self.Registers[register]=value
    
    def retrieveRegister(self,register):
        return self.Registers[register]

    def setOverflow(self):
        # self.Flags='0000000000001000'
        self.Registers['111']='0000000000001000'

    def setLessThan(self):
        # self.Flags='0000000000000100'
        self.Registers['111']='0000000000000100'
    
    def setGreaterThan(self):
        # self.Flags='0000000000000010'
        self.Registers['111']='0000000000000010'
    
    def setEqual(self):
        # self.Flags='0000000000000001'
        self.Registers['111']='0000000000000001'
    
    def resetFlags(self):
        # self.Flags='0000000000000000'
        self.Registers['111']='0000000000000000'

    def dump(self):
        for i in (self.Registers):
            if i=='111':
                print(self.Registers[i])
                break
            print('0'*(16-len(bin(self.Registers[i])[2::]))+bin(self.Registers[i])[2::], end=' ')
        # print(self.Flags)

RegisterFile=RegisterFiles()
ProgramCounter=ProgramCounters()
class ExecuteEngine:
    
    Memory_ValueDict={}

    def execute(self,Instruction):
        opcode=Instruction[0:5]
        # print(self.Memory_ValueDict)
        if(opcode=='10000'):
            #ADD
            reg1=Instruction[7:10:]
            reg2=Instruction[10:13:]
            reg3=Instruction[13::]

            value=RegisterFile.retrieveRegister(reg1)+RegisterFile.retrieveRegister(reg2)
            if(Overflow(value)):
                RegisterFile.setOverflow()
            else:
                RegisterFile.resetFlags()

            RegisterFile.updateRegister(reg3,value)

            return False, ProgramCounter.Counter+1
        
        elif(opcode=='10001'):
            #SUB
            reg1=Instruction[7:10:]
            reg2=Instruction[10:13:]
            reg3=Instruction[13::]

            value=RegisterFile.retrieveRegister(reg1)-RegisterFile.retrieveRegister(reg2)
            if(value<0):
                RegisterFile.setLessThan()
                RegisterFile.updateRegister(reg3,0)
            else:
                RegisterFile.resetFlags()
                RegisterFile.updateRegister(reg3,value)

            return False, ProgramCounter.Counter+1
        
        elif(opcode=='10010'):
            #MOVImm
            reg1=Instruction[5:8:]
            Imm=Instruction[8::]
            value=int(Imm,2)
            if(Overflow(value)):
                RegisterFile.setOverflow()
            else:
                RegisterFile.resetFlags()
            RegisterFile.updateRegister(reg1,value)
            return False, ProgramCounter.Counter+1
        
        elif(opcode=='10011'):
            #MOVReg
            reg1=Instruction[10:13:]
            reg2=Instruction[13::]
            RegisterFile.updateRegister(reg2,RegisterFile.retrieveRegister(reg1))
            RegisterFile.resetFlags()
            return False, ProgramCounter.Counter+1
        
        elif(opcode=='10110'):
            #Mul
            reg1=Instruction[7:10:]
            reg2=Instruction[10:13:]
            reg3=Instruction[13::]
            value=RegisterFile.retrieveRegister(reg1)*RegisterFile.retrieveRegister(reg2)
            if(Overflow(value)):
                RegisterFile.setOverflow()
            else:
                RegisterFile.resetFlags()
            RegisterFile.updateRegister(reg3,value)
            return False, ProgramCounter.Counter+1
        
        elif(opcode=='10111'):
            #Div
            reg1=Instruction[10:13:]
            reg2=Instruction[13::]
            quotient=RegisterFile.retrieveRegister(reg1)//RegisterFile.retrieveRegister(reg2)
            remainder=RegisterFile.retrieveRegister(reg1)%RegisterFile.retrieveRegister(reg2)
            RegisterFile.updateRegister('000',quotient)
            RegisterFile.updateRegister('001',remainder)
            RegisterFile.resetFlags()
        
            return False, ProgramCounter.Counter+1

        elif(opcode=='11000'):
            #RShift
            reg1=Instruction[10:13:]
            Imm=Instruction[13::]
            value=RegisterFile.retrieveRegister(reg1)>>int(Imm,2)
            RegisterFile.updateRegister(reg1,value)
            RegisterFile.resetFlags()
            return False, ProgramCounter.Counter+1

        elif(opcode=='11001'):
            #LShift
            reg1=Instruction[10:13:]
            Imm=Instruction[13::]
            value=RegisterFile.retrieveRegister(reg1)<<int(Imm,2)
            RegisterFile.updateRegister(reg1,value)
            RegisterFile.resetFlags()
            return False, ProgramCounter.Counter+1
        
        elif(opcode=='11010'):
            #Xor
            reg1=Instruction[7:10:]
            reg2=Instruction[10:13:]
            reg3=Instruction[13::]
            value=RegisterFile.retrieveRegister(reg1)^RegisterFile.retrieveRegister(reg2)
            if(Overflow(value)):
                RegisterFile.setOverflow()
            else:
                RegisterFile.resetFlags()
            RegisterFile.updateRegister(reg3,value)
            return False, ProgramCounter.Counter+1
        
        elif(opcode=='11011'):
            #Or
            reg1=Instruction[7:10:]
            reg2=Instruction[10:13:]
            reg3=Instruction[13::]
            value=RegisterFile.retrieveRegister(reg1)|RegisterFile.retrieveRegister(reg2)
            if(Overflow(value)):
                RegisterFile.setOverflow()
            else:
                RegisterFile.resetFlags()
            RegisterFile.updateRegister(reg3,value)
            return False, ProgramCounter.Counter+1

        elif(opcode=='11100'):
            #And
            reg1=Instruction[7:10:]
            reg2=Instruction[10:13:]
            reg3=Instruction[13::]
            value=RegisterFile.retrieveRegister(reg1)&RegisterFile.retrieveRegister(reg2)
            if(Overflow(value)):
                RegisterFile.setOverflow()
            else:
                RegisterFile.resetFlags()
            RegisterFile.updateRegister(reg3,value)
            return False, ProgramCounter.Counter+1
        
        elif(opcode=='11101'):
            #Invert
            reg1=Instruction[10:13:]
            reg2=Instruction[13::]
            value= ~RegisterFile.retrieveRegister(reg1)
            if(Overflow(value)):
                RegisterFile.setOverflow()
            else:
                RegisterFile.resetFlags()
            RegisterFile.updateRegister(reg2,value)
            return False, ProgramCounter.Counter+1
        
        elif(opcode=='11110'):
            #Cmp
            reg1=Instruction[10:13:]
            reg2=Instruction[13::]
            if(RegisterFile.retrieveRegister(reg1)>RegisterFile.retrieveRegister(reg2)):
                RegisterFile.setGreaterThan()
            elif(RegisterFile.retrieveRegister(reg1)<RegisterFile.retrieveRegister(reg2)):
                RegisterFile.setLessThan()
            elif(RegisterFile.retrieveRegister(reg1)==RegisterFile.retrieveRegister(reg2)):
                RegisterFile.setEqual()

            return False, ProgramCounter.Counter+1
            
        elif(opcode=='11111'):
            #Jump
            Imm=Instruction[8::]
            # print("hi")
            value=int(Imm,2)
            ProgramCounter.PrevCounter=ProgramCounter.Counter+1
            ProgramCounter.Jump=True
            ProgramCounter.Counter=value
            RegisterFile.resetFlags()
            return False, ProgramCounter.Counter
        
        elif(opcode=='01100'):
            #JumpIfLessThan
            Imm=Instruction[8::]
            value=int(Imm,2)
            if(RegisterFile.Registers['111']=='0000000000000100'):
                RegisterFile.resetFlags()
                ProgramCounter.Counter=value
                return False, ProgramCounter.Counter
            else:
                RegisterFile.resetFlags()
                return False, ProgramCounter.Counter+1
        
        elif(opcode=='01101'):
            # print("gmm")
            #JumpIfGreaterThan
            Imm=Instruction[8::]
            value=int(Imm,2)
            # print(RegisterFile.Registers['011'],RegisterFile.Registers['001'])
            if(RegisterFile.Registers['111']=='0000000000000010'):
                RegisterFile.resetFlags()
                ProgramCounter.Counter=value
                return False, ProgramCounter.Counter
            else:
                RegisterFile.resetFlags()
                return False, ProgramCounter.Counter+1
        
        elif(opcode=='01111'):
            #JumpIfEqual
            Imm=Instruction[8::]
            value=int(Imm,2)
            if(RegisterFile.Registers['111']=='0000000000000001'):
                RegisterFile.resetFlags()
                ProgramCounter.Counter=value
                return False, ProgramCounter.Counter
            else:
                RegisterFile.resetFlags()
                return False, ProgramCounter.Counter+1
        
        elif(opcode=='10100'):
            #Load
            reg1=Instruction[5:8:]
            reg2=Instruction[8::]
            # self.Memory_ValueDict[reg2]=RegisterFile.retrieveRegister(reg1)
            if(reg2 in self.Memory_ValueDict):
                RegisterFile.updateRegister(reg1,self.Memory_ValueDict[reg2])
                RegisterFile.resetFlags()
                return False, ProgramCounter.Counter+1
            elif(reg2 not in self.Memory_ValueDict):
                self.Memory_ValueDict[reg2]=0
                RegisterFile.updateRegister(reg1,0)
                RegisterFile.resetFlags()
                return False, ProgramCounter.Counter+1
        
        elif(opcode=='10101'):
            #Store
            reg1=Instruction[5:8:]
            reg2=Instruction[8::]
            # RegisterFile.updateRegister(reg1,self.Memory_ValueDict[reg2])
            # print(RegisterFile.retrieveRegister('011'),reg2)
            self.Memory_ValueDict[reg2]=RegisterFile.retrieveRegister(reg1)
            RegisterFile.resetFlags()
            return False, ProgramCounter.Counter+1
        
        elif(opcode=='01010'):
            #Halt
            RegisterFile.resetFlags()
            return True, ProgramCounter.Counter

        


MEM=Memory()

EE=ExecuteEngine()
MEM.initialize()
ProgramCounter.Counter=0
halted= False

# while(not halted):
while (not halted):
    Instruction = MEM.getData(ProgramCounter.Counter)
    halted, new_PC = EE.execute(Instruction)
    ProgramCounter.dump()
    RegisterFile.dump()
    ProgramCounter.update(new_PC)
MEM.dump()