import m3   
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
l1=[]
pc_list=[]
memory=[]
registers=[]                   
#registers=['0000000000000000', '0000000000000000', '0000000000000101', '0000000000000010', '0000000000000000', '0000000000000000', '0000000000000000']
while True:    #appending the input in list l1
    try :
        line = input()
        if line!="":
            l1.append(line)

    except EOFError:
        break
class mem:

    def __init__(self,list):
        self.memory=list
        self.length=len(list)
        self.memdec()
    
    def getData(self,pc):
        return self.memory[pc]
        
    def memdec(self):
        for i in range(256-self.length):
            self.memory.append("0000000000000000")

        return self.memory

    def addtomemory(self,string,location):
        self.memory[location]=string
        

        return self.memory

    def dump(self):
        for i in self.memory:
            print(i)

def RF(registers,register):
    for i in range(len(register)-1):
        registers.append("0000000000000000")

    return registers
#appending keys and values present in dictionary(register) in two seperate lists
def reg_no(string,register):
    k=-1
    register_keys = list(register.keys())
    register_values = list(register.values())

    if string in register_values:
        k=int(register_keys[register_values.index(string)][1:])
    return k



#main function
def Execute(opcode,string,register,registers):
    global halted
    global pc
    global FLAGS
    global x
    global y
    global cycle
    tempflag=FLAGS
    reset()
    max_int=65535
    #addition instruction
    if string[:5]==opcode["add"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b+c
        #overflow flag is set if computation overflows
        if a>max_int:
            a=a-max_int
            changeflag('v')

        registers[reg_no(string[7:10],register)]=format(a,'016b')
    #subtraction instruction
    elif string[:5]==opcode["sub"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        #overflow flag is set if below condition fulfills and 0 is assigned to 'a'
        if c>b:
            a=0
            changeflag('v')
        else:
            a=b-c
        registers[reg_no(string[7:10],register)]=format(a,'016b')
    #multiply instruction
    elif string[:5]==opcode["mul"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b*c
        #overflow flag is set if computation overflows
        if a>max_int:
            a=a-max_int
            changeflag('v')
        registers[reg_no(string[7:10],register)]=format(a,'016b')
    #xor instruction
    elif string[:5]==opcode["xor"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b^c
        registers[reg_no(string[7:10],register)]=format(a,'016b')
    #or instruction
    elif string[:5]==opcode["or"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b|c
        registers[reg_no(string[7:10],register)]=format(a,'016b')
    #and instruction
    elif string[:5]==opcode["and"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b&c
        registers[reg_no(string[7:10],register)]=format(a,'016b')
    #move immediate instruction
    elif string[:5]=="00010":
        registers[reg_no(string[5:8],register)]="00000000"+string[8:]
    #right shift instruction
    elif string[:5]==opcode["rs"][0]:
        a=int(registers[reg_no(string[5:8],register)],2)
        a=a>>int(string[8:],2)
        registers[reg_no(string[5:8],register)]=format(a,'016b')
    #left shift instruction
    elif string[:5]==opcode["ls"][0]:
        a=int(registers[reg_no(string[5:8],register)],2)
        a=a<<int(string[8:],2)
        registers[reg_no(string[5:8],register)]=format(a,'016b')
    #divide instruction
    elif string[:5]==opcode["div"][0]:
        a=int(registers[reg_no(string[10:13],register)],2)
        b=int(registers[reg_no(string[13:16],register)],2)
        q=a//b
        r=a%b
        registers[0]=format(q,'016b')
        registers[1]=format(r,'016b')
    #move register instruction
    elif string[:5]==opcode["mov"][0]:
        if string[13:16]=="111":
            registers[reg_no(string[10:13],register)]=tempflag
        else:    
            a=int(registers[reg_no(string[13:16],register)],2)
            registers[reg_no(string[10:13],register)]=format(a,'016b')
    #not instruction
    elif string[:5]==opcode["not"][0]:
        a=int(registers[reg_no(string[13:16],register)],2)
        b=~a
        registers[reg_no(string[10:13],register)]=format(b,'016b')
    #compare instruction
    elif string[:5]==opcode["cmp"][0]:
        a=int(registers[reg_no(string[10:13],register)],2)
        b=int(registers[reg_no(string[13:16],register)],2)
        reset()
        #sets greater than,less than,equal flag depending upon the input given
        if a>b:
            changeflag('g')
        elif a<b:
            changeflag('l')
        elif a==b:
            changeflag('e')
    #store instruction
    elif string[:5]==opcode["st"][0]:
        a=int(registers[reg_no(string[5:8],register)],2)
        b=format(a,'016b')
        location=int(string[8:],2)
        y.append(location) #y is a list containing memory address
        x.append(cycle) #x is a list containing cycle no
        M1.addtomemory(b,location) 
    #load instruction
    elif string[:5]==opcode["ld"][0]:
        location=int(string[8:],2)
        a=int(M1.getData(location),2)
        registers[reg_no(string[5:8],register)]=format(a,'016b')
    #unconditional jump instruction
    elif string[:5]==opcode["jmp"][0]:
        location=int(string[8:],2)
        pc=location-1

    #Jump If Greater Than instruction
    elif string[:5]==opcode["jgt"][0]:
        if tempflag=="0000000000000010":
            location=int(string[8:],2)
            pc=location-1
    #Jump If less Than instruction
    elif string[:5]==opcode["jlt"][0]:
        if tempflag=="0000000000000100":
            location=int(string[8:],2)
            pc=location-1
    #Jump If equal instruction
    elif string[:5]==opcode["je"][0]:
        if tempflag=="0000000000000001":
            location=int(string[8:],2)
            pc=location-1
    #hlt instruction
    elif string[:5]==opcode["hlt"][0]:
        halted= True #this will stop the code from executing
               
    return registers

def reset():  #resetting the flags value
    global FLAGS
    FLAGS="0000000000000000"


def changeflag(string):   #setting the value for flags register
    global FLAGS
    if string=="v":  #overflow
        FLAGS="0000000000001000"
    elif string=="l": #less-than
        FLAGS="0000000000000100"
    elif string=="g": #greater-than
        FLAGS="0000000000000010" 
    elif string=="e":  #equal
        FLAGS="0000000000000001"
        

pc=0
halted = False
M1= mem(l1)
FLAGS="0000000000000000"
RF(registers,m3.register)
cycle=0
x=[]
y=[]
while not halted:
    instruction=M1.getData(pc)
    Execute(m3.opcode,instruction,m3.register,registers)
    print(format(pc,'08b'),*registers,FLAGS)
    y.append(pc)
    pc+=1
    #y.append(pc)
    x.append(cycle)
    cycle+=1
    #x.append(cycle)
M1.dump()
#for plotting graph
plt.scatter(x,y)
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()

