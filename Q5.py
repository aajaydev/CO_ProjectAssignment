
#5
import math as m
print("--------------------------------------------")
print("               Question 5  Part-1           ")
print("--------------------------------------------")
mem_space=input("Memory space: ")
mem_space=mem_space.split(" ")
if(mem_space[1]=="kb"):
    mem_space[1]=2**10
if(mem_space[1]=="kB"):
    mem_space[1]=2**13
if(mem_space[1]=="Mb"):
    mem_space[1]=2**20
if(mem_space[1]=="MB"):
    mem_space[1]=2**23
if(mem_space[1]=="Gb"):
    mem_space[1]=2**30
if(mem_space[1]=="GB"):
    mem_space[1]=2**33

mem_space[0]=2**(m.log(int(mem_space[0]),2))
mem_space=mem_space[0]*mem_space[1]
print()

print("Types of Memory")
print("Bit Addressable Memory: bit")
print("Nibble Addressable Memory: nibble")
print("Byte Addressable Memory: byte")
print("Word Addressable Memory: word")


print()
typeofmem_input=input("Type of memory: ")

types_of_memory={"bit":1,"byte":8,"nibble":4}

no_instr=int(input("Length of Instructions: "))
reg_length=int(input("Register Length: "))

mem_type_value=types_of_memory[typeofmem_input]

print()
#initialize address pins
address_pins=mem_space/mem_type_value
address_pins=m.log(int(address_pins),2)
print("No. of address pins - ",int(address_pins)) #no. of address pins (How many minimum bits are needed to represent an address in this architecture)

opcode=no_instr-address_pins-reg_length #Number of bits needed by opcode
print("No. of bits needed by opcode - ",int(opcode))
print()
print("No. of filler bits in both types")
print("Type A")
print(int(no_instr-reg_length-opcode))
print("Type B")
print(int(no_instr-2*reg_length-opcode))

print()

print("Maximum numbers of instructions this ISA can support - ",int(2**opcode)) #Maximum numbers of instructions this ISA can support

print('Maximum numbers of registers this ISA can support - ',int(2**reg_length)) #Maximum numbers of registers this ISA can support

print()

print("--------------------------------------------")
print("              Question 5  Part-1 Type 1           ")
print("--------------------------------------------")

cpu_bits=int(input("No. of bits in CPU: "))

memtype_input=input("Type of memory: ")

final_cpubits=mem_space/cpu_bits
final_cpubits=m.log(int(final_cpubits),2)
print(int(final_cpubits-address_pins)) #How many address pins are saved or required

print("--------------------------------------------")
print("              Question 5  Part-1 Type 2     ")
print("--------------------------------------------")

#part 2
def getmain_mem_space(mem_space_bits):
    if(mem_space_bits>30):
        mem_space_bits=mem_space_bits-30
        if(mem_space_type2=="byte"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"GB")
        elif(mem_space_type2=="nibble"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"GB")
        elif(mem_space_type2=="bit"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"GB")        

  
    if(mem_space_bits>20 and mem_space_bits<=30):
        mem_space_bits=mem_space_bits-30
        if(mem_space_type2=="byte"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"MB")
        elif(mem_space_type2=="nibble"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"MB")
        elif(mem_space_type2=="bit"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"MB")
    
    if(mem_space_bits>10 and mem_space_bits<=20):
        mem_space_bits=mem_space_bits-30
        if(mem_space_type2=="byte"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"kB")
        elif(mem_space_type2=="nibble"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"kB")
        elif(mem_space_type2=="bit"):
            mem_space_bits=mem_space_bits-3
            print("Main Memory Space - ",int(2**mem_space_bits),"kB")

def getmain_mem_word(main_memory):
    if(main_memory>33):
        main_memory=main_memory-33
        print("Main Memory Space - ",int(2**main_memory),"GB")

cpu_bits_part2=int(input("No. of bits in CPU: "))

address_pins_part2=int(input("No. of address pins: "))

mem_space_type2=input("Memory type : ")

if(mem_space_type2=="byte"):
    mem_space_bits=2**(address_pins_part2+3)
    mem_space_bits=(m.log(mem_space_bits,2))
    getmain_mem_space(mem_space_bits)

if(mem_space_type2=="bit"):
    mem_space_bits=2**(address_pins_part2)
    mem_space_bits=(m.log(mem_space_bits,2))
    getmain_mem_space(mem_space_bits)


if(mem_space_type2=="nibble"):
    mem_space_bits=2**(address_pins_part2+2)
    mem_space_bits=(m.log(mem_space_bits,2))
    getmain_mem_space(mem_space_bits)

if (mem_space_type2=="word"):
    main_memory=(2**(address_pins_part2))*cpu_bits_part2
    main_memory=(m.log(main_memory,2))
    getmain_mem_word(main_memory)
