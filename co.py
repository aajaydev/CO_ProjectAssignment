import sys

Assembly_Code=[]

Machine_Code=[]

Errors=[]

def getRegister(reg):
        registers = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100','R5': '101','R6': '110','FLAGS': '111'}
        if reg in registers:
            return registers[reg]
        else:
            return 'Error'

def getInstructionType(instruction):
    if instruction[0] in ["add","sub","mul","xor","or","and"]:
        return 'a'
    elif (instruction[0] in ["mov"] and instruction[2][1::].isdecimal()) or (instruction[0] in ["ls","rs"]):
        return 'b'
    elif instruction[0] in ["mov","div"]:
        return 'c'
    elif instruction[0] in ["ld","st"]:
        return 'd'
    elif instruction[0] in ["jmp","jlt","jgt","je"]:
        return 'e'
    elif instruction[0] in ["hlt"]:
        return 'f'
    else:
        return 'Error'

def getOpcode(line):
    opcodes={
        'add':'10000',
        'sub':'10001',
        'ld':'10100',
        'st':'10101',
        'mul':'10110',
        'div':'10111',
        'ls':'11001',
        'rs':'11000',
        'xor':'11010',
        'or':'11011',
        'and':'11100',
        'not':'11101',
        'cmp':'11110',
        'jmp':'11111',
        'jlt':'01100',
        'jgt':'01101',
        'je':'01111',
        'hlt':'01010'
    }
    if line[0]=="mov" and line[2][1::].isdecimal():
        return "10010"

    elif line[0]=="mov" and line[2].startswith('R'):
        return "10011"

    elif line[0] in opcodes:
        return opcodes[line[0]]

    else:
        return 'Error'
    

# for line in sys.stdin:
#     if line=="\n":
#         break
#     if(line):
#         Assembly_Code.append(line.rstrip())

file=open("input.txt","r")
for line in file:
    Assembly_Code.append(line.rstrip())


hlt_encountered=False
count=0

for line in Assembly_Code:
    codeline=line.split()
    for i in codeline:
        if(i=='hlt'):
            count=count+1
            hlt_encountered=True
    
if(count==0 and hlt_encountered==False):
    Errors.append("Error: hlt instruction not found")
    
    
elif(count==1 and Assembly_Code[-1]!='hlt'):
    Errors.append("Error : hlt not being used as the last instruction")
    



Variables={}
# print(Assembly_Code)

var_Address=len(Assembly_Code)
for line in Assembly_Code:
    codeline=line.split()
    if(codeline[0]=='var'):
        var_Address-=1
    elif(codeline==[]):
        var_Address-=1


for line in Assembly_Code:
    codeline=line.split()
    if(codeline[0]=="var"):
        Variables[codeline[1]]=format(var_Address,'08b')
        var_Address+=1
        Assembly_Code.pop(0)
labels={}
#print(Variables)
line_address=0
newline=""
for line in Assembly_Code:
    codeline=line.split()
    if(codeline[0][-1] == ":"):
        if(codeline[0][:len(codeline[0])-1:] not in labels):
            labels[codeline[0][:len(codeline[0])-1:]] = line_address
            for element in range(1,len(codeline)):
                newline += codeline[element] + " "
            Assembly_Code[line_address] = newline
    line_address+=1


#print(Assembly_Code)
#print(labels)

lineCount=0
for line in Assembly_Code:
    lineCount+=1
    codeline=line.split()
    #print(codeline)
    if(codeline[0]=='mov'):
        if(codeline[2][1::].isdecimal()):
            if(int(codeline[2][1::])<0 or int(codeline[2][1::])>255):
                Errors.append("Error: Line n.o: "+str(lineCount+len(Variables))+" immediate value '"+str(codeline[2][1::])+"' is out of range")

            Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1]) + format(int(codeline[2][1::]),'08b'))
        
        elif len(codeline)==3:
            Machine_Code.append(getOpcode(codeline)+ "0"*5 + getRegister(codeline[1]) + getRegister(codeline[2]))




    elif(codeline[0]=="rs" and codeline[2][1::].isdecimal()):
        Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1]) + format(int(codeline[2][1::]),'08b'))

    elif(codeline[0]=="ls" and codeline[2][1::].isdecimal()):
        Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1]) + format(int(codeline[2][1::]),'08b'))

    elif(codeline[0]=='hlt'):
        Machine_Code.append(getOpcode(codeline) + "0"*11 ) 

    elif(codeline[0]=="st"):
        Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1])+Variables[codeline[2]])

    elif(codeline[0]=="ld"):
        Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1])+Variables[codeline[2]])

    elif codeline[0]=="div":
        Machine_Code.append(getOpcode(codeline)+ "0"*5 + getRegister(codeline[1]) + getRegister(codeline[2]))

    elif codeline[0]=="not":
        Machine_Code.append(getOpcode(codeline)+ "0"*5 + getRegister(codeline[1]) + getRegister(codeline[2]))

    elif codeline[0]=="cmp":
        Machine_Code.append(getOpcode(codeline)+ "0"*5 + getRegister(codeline[1]) + getRegister(codeline[2]))

    elif codeline[0]=="add":
        Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="sub":
        Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="mul":
        Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="xor":
        Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="and":
        Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))
        
    elif codeline[0]=="or":
        Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="jmp":
        Machine_Code.append(getOpcode(codeline)+"0"*3+format(labels[codeline[1]],'08b'))

    elif codeline[0]=="jlt":
        Machine_Code.append(getOpcode(codeline)+"0"*3+format(labels[codeline[1]],'08b'))
    
    elif codeline[0]=="jgt":
        Machine_Code.append(getOpcode(codeline)+"0"*3+format(labels[codeline[1]],'08b'))
    
    elif codeline[0]=="je":
        Machine_Code.append(getOpcode(codeline)+"0"*3+format(labels[codeline[1]],'08b'))

    



if Errors!=[]:
    for line in Errors:
        print(line)
else:
    for line in Machine_Code:
        print(line)

# print(Machine_Code[0])