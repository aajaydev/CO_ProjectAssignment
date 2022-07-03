import sys
import fileinput

Assembly_Code=[]

Machine_Code=[]

Errors=[]

def getRegister(reg):
        registers = {'R0': '000','R1': '001','R2': '010','R3': '011','R4': '100','R5': '101','R6': '110','FLAGS': '111'}
        if reg in registers:
            return registers[reg]
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
    

for line in fileinput.input():
    Assembly_Code.append(line.rstrip())
    
Variables={}

var_Address=len(Assembly_Code)
for line in Assembly_Code:
    codeline=line.split()
    if(codeline==[]):
        var_Address-=1
    elif(codeline[0]=='var'):
        var_Address-=1


countLine_var=0
Varlines_ToBeRemoved=[]
for line in Assembly_Code:
    countLine_var+=1
    codeline=line.split()
    if(codeline==[]):
        continue
    elif(codeline[0]=="var" and len(codeline)==2 and (codeline[1] not in Variables)):
        Variables[codeline[1]]=format(var_Address,'08b')
        Varlines_ToBeRemoved.append(line)
        var_Address+=1

    elif(codeline[0]=="var" and len(codeline)==2 and (codeline[1] in Variables)):
        Errors.append("Error: "+"Line n.o : "+(countLine_var)+" Duplicate Variable Declaration"+" ("+line+")")
        Varlines_ToBeRemoved.append(line)

    elif(codeline[0]=="var" and len(codeline)!=2):
        Errors.append("Error: " +"Line n.o: "+str(countLine_var)+ " Invalid variable declaration"+" ("+line+")")
        Varlines_ToBeRemoved.append(line)

    else:
        break

for varLine in Varlines_ToBeRemoved:
    Assembly_Code.remove(varLine)

labels={}
line_address=-1

countLine_label=len(Variables)
for line in Assembly_Code:
    line_address+=1
    newline=""
    countLine_label+=1
    codeline=line.split()
    if(codeline==[]):
        continue

    elif(codeline[0][-1] == ":" and line.count(":")==1):
        if(codeline[0][:len(codeline[0])-1:] in Variables):
            Errors.append("Error: " +"Line n.o: "+str(countLine_label)+ " Misuse of Variable as Label"+" ("+line+")")

        elif(codeline[0][-1] == ":" and len(codeline)==1):
            Errors.append("Error: " +"Line n.o: "+str(countLine_label)+ " Invalid Syntax of Label Declaration"+" ("+line+")")
            Assembly_Code[line_address]=''

        elif(codeline[0][:len(codeline[0])-1:] in labels):
            Errors.append("Error: " +"Line n.o: "+str(countLine_label)+ " Duplicate Label Declaration"+" ("+line+")")
            Assembly_Code[line_address]=''

        elif(codeline[0][:len(codeline[0])-1:] not in labels):
            labels[codeline[0][:len(codeline[0])-1:]] = line_address
            for element in range(1,len(codeline)):
                newline += codeline[element] + " "
            Assembly_Code[line_address] = newline
            
    elif(codeline[0][-1] == ":" and line.count(":")>1):
        Errors.append("Error: " +"Line n.o: "+str(countLine_label)+ " Invalid Syntax of Label Declaration"+" ("+line+")")
        Assembly_Code[line_address]=''
            
    
def typeA_Error(codeLine,line_Number):
    if len(codeline)!=4:
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Syntax - Type A Error"+" ("+line+")")
        return True
    elif (getRegister(codeLine[1])=='Error' or getRegister(codeLine[2])=='Error' or getRegister(codeLine[3])=='Error'):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Register - Type A Error"+" ("+line+")")
        return True
    elif(getRegister(codeLine[1])=='111' or getRegister(codeLine[2])=='111' or getRegister(codeLine[3])=='111'):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Illegal use of FLAGS register - Type A Error"+" ("+line+")")
        return True


def typeB_Error(codeLine,line_Number):
    if len(codeline)!=3:
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Syntax - Type B Error"+" ("+line+")")
        return True
    elif (getRegister(codeLine[1])=='Error'):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Register - Type B Error"+" ("+line+")")
        return True
    elif((codeLine[2][0])!='$'):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Syntax - Type B Error"+" ("+line+")")
        return True
    elif(not codeLine[2][1::].isdecimal()):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Immediate value is not an integer - Type B Error"+" ("+line+")")
        return True
    elif(codeLine[2][1::].isdecimal() and int(codeLine[2][1::])<0 or int(codeLine[2][1::])>255):
        Errors.append("Error: Line n.o: "+(line_Number)+" immediate value '"+str(codeline[2][1::])+"' is out of range - Type B Error"+" ("+line+")")
        return True

def typeC_Error(codeLine,line_Number):
    if len(codeline)!=3:
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Syntax - Type C Error"+" ("+line+")")
        return True
    elif(getRegister(codeline[1])=='Error' or getRegister(codeline[2])=='Error'):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Register - Type C Error"+" ("+line+")")
        return True
    elif (codeLine[0] in ['div','not','cmp'] and (getRegister(codeLine[1])=='111' or getRegister(codeLine[2])=='111')):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Illegal use of FLAGS register - Type C Error"+" ("+line+")")
        return True
    elif (getRegister(codeLine[2])=='111'):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Illegal use of FLAGS register - Type C Error"+" ("+line+")")
        return True

def typeD_Error(codeLine,line_Number):
    if len(codeline)!=3:
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Syntax - Type D Error"+" ("+line+")")
        return True
    elif(codeLine[2] in labels):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Misuse of Labels as Variable - Type D Error"+" ("+line+")")
        return True
    elif (codeLine[2] not in Variables):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Undefined Variable - Type D Error"+" ("+line+")")
        return True

def typeE_Error(codeLine,line_Number):
    if(len(codeline))!=2:
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Syntax - Type E Error"+" ("+line+")")
        return True
    elif(codeLine[1] in Variables):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Misuse of Variable as Label - Type E Error"+" ("+line+")")
        return True
    elif (codeLine[1] not in labels):
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Undefined Label - Type E Error"+" ("+line+")")
        return True

def typeF_Error(codeLine,line_Number):
    if len(codeline)!=1:
        Errors.append("Error: "+"Line n.o : "+(line_Number)+" Invalid Syntax of hlt instruction - Type F Error"+" ("+line+")")
        return True
    
        
hlt_Present=False
hlt_Count=0

for Line_No in range(0,len(Assembly_Code)):
    codeline=Assembly_Code[Line_No].split()
    if(codeline!=[]):
        if(codeline[0]=='hlt' and Line_No!=len(Assembly_Code)-1):
            Errors.append("Error: "+"Line n.o: "+ str(Line_No+1+len(Variables))+ " hlt not being used as the last instruction"+" ("+line+")")
            hlt_Count=hlt_Count+1

        elif(codeline[0]=='hlt' and Line_No==len(Assembly_Code)-1):
            hlt_Count=hlt_Count+1
            hlt_Present=True
    else:
        continue

if(hlt_Count==0 and hlt_Present==False):
    Errors.append("Error: hlt instruction not found")


lineCount=0
for line in Assembly_Code:
    
    codeline=line.split()
    lineCount+=1
    Line_Number=str(lineCount+len(Variables))


    if (codeline==[]):
        continue
    
    elif codeline[0]=='var':
        Errors.append("Error: " +"Line n.o: "+str(lineCount+len(Variables))+ " Invalid Variable declaration "+" ("+line+")")
    
    
    elif(codeline[0]=='mov'):
        if(codeline[2][0]=='$'):
            if(typeB_Error(codeline,Line_Number)):
                continue
            else:
                Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1]) + format(int(codeline[2][1::]),'08b'))
        
        elif len(codeline)==3:
            if(typeC_Error(codeline,Line_Number)):
                continue
            else:
                Machine_Code.append(getOpcode(codeline)+ "0"*5 + getRegister(codeline[1]) + getRegister(codeline[2]))


    elif(codeline[0]=="rs" and codeline[2][1::].isdecimal()):
        if(typeB_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1]) + format(int(codeline[2][1::]),'08b'))

    elif(codeline[0]=="ls" and codeline[2][1::].isdecimal()):
        if(typeB_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1]) + format(int(codeline[2][1::]),'08b'))


    elif(codeline[0]=="st"):
        if(typeD_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1])+Variables[codeline[2]])

    elif(codeline[0]=="ld"):
        if(typeD_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline) + getRegister(codeline[1])+Variables[codeline[2]])

    elif codeline[0]=="div":
        if(typeC_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+ "0"*5 + getRegister(codeline[1]) + getRegister(codeline[2]))

    elif codeline[0]=="not":
        if(typeC_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+ "0"*5 + getRegister(codeline[1]) + getRegister(codeline[2]))

    elif codeline[0]=="cmp":
        if(typeC_Error(codeline,Line_Number)):
                continue
        else:    
            Machine_Code.append(getOpcode(codeline)+ "0"*5 + getRegister(codeline[1]) + getRegister(codeline[2]))

    elif codeline[0]=="add":
        if(typeA_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="sub":
        if(typeA_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="mul":
        if(typeA_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="xor":
        if(typeA_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="and":
        if(typeA_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))
        
    elif codeline[0]=="or":
        if(typeA_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*2+getRegister(codeline[1])+getRegister(codeline[2])+getRegister(codeline[3]))

    elif codeline[0]=="jmp":
        if(typeE_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*3+format(labels[codeline[1]],'08b'))

    elif codeline[0]=="jlt":
        if(typeE_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*3+format(labels[codeline[1]],'08b'))
    
    elif codeline[0]=="jgt":
        if(typeE_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*3+format(labels[codeline[1]],'08b'))
    
    elif codeline[0]=="je":
        if(typeE_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline)+"0"*3+format(labels[codeline[1]],'08b'))

    elif(codeline[0]=='hlt'):
        if(typeF_Error(codeline,Line_Number)):
                continue
        else:
            Machine_Code.append(getOpcode(codeline) + "0"*11 ) 

    else:
        Errors.append("Error: "+"Line n.o: "+ Line_Number + " Invalid Instruction")
        continue


if Errors!=[]:
    for line in Errors:
        # print(line)
        sys.stdout.write(line+"\n")
else:
    for line in Machine_Code:
        # print(line)
        sys.stdout.write(line+"\n")