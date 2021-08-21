import m3
l1=[]
pc_list=[]
memory=[]
registers=[]                   
#registers=['0000000000000000', '0000000000000000', '0000000000000101', '0000000000000010', '0000000000000000', '0000000000000000', '0000000000000000']
while True:
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

def reg_no(string,register):
    k=-1
    register_keys = list(register.keys())
    register_values = list(register.values())

    if string in register_values:
        k=int(register_keys[register_values.index(string)][1:])
    return k




def Execute(opcode,string,register,registers):
    global halted
    global pc
    global FLAGS
    tempflag=FLAGS
    reset()
    max_int=65535
    if string[:5]==opcode["add"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b+c
        if a>max_int:
            a=a-max_int
            changeflag('v')

        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["sub"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        if c>b:
            a=0
            changeflag('v')
        else:
            a=b-c
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["mul"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b*c
        if a>max_int:
            a=a-max_int
            changeflag('v')
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["xor"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b^c
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["or"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b|c
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["and"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b&c
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]=="00010":
        registers[reg_no(string[5:8],register)]="00000000"+string[8:]
    
    elif string[:5]==opcode["rs"][0]:
        a=int(registers[reg_no(string[5:8],register)],2)
        a=a>>int(string[8:],2)
        registers[reg_no(string[5:8],register)]=format(a,'016b')

    elif string[:5]==opcode["ls"][0]:
        a=int(registers[reg_no(string[5:8],register)],2)
        a=a<<int(string[8:],2)
        registers[reg_no(string[5:8],register)]=format(a,'016b')

    elif string[:5]==opcode["div"][0]:
        a=int(registers[reg_no(string[10:13],register)],2)
        b=int(registers[reg_no(string[13:16],register)],2)
        q=a//b
        r=a%b
        registers[0]=format(q,'016b')
        registers[1]=format(r,'016b')

    elif string[:5]==opcode["mov"][0]:
        if string[13:16]=="111":
            registers[reg_no(string[10:13],register)]=tempflag
        else:    
            a=int(registers[reg_no(string[13:16],register)],2)
            registers[reg_no(string[10:13],register)]=format(a,'016b')

    elif string[:5]==opcode["not"][0]:
        a=int(registers[reg_no(string[13:16],register)],2)
        b=~a
        registers[reg_no(string[10:13],register)]=format(b,'016b')

    elif string[:5]==opcode["cmp"][0]:
        a=int(registers[reg_no(string[10:13],register)],2)
        b=int(registers[reg_no(string[13:16],register)],2)
        reset()
        if a>b:
            changeflag('g')
        elif a<b:
            changeflag('l')
        elif a==b:
            changeflag('e')

    elif string[:5]==opcode["st"][0]:
        a=int(registers[reg_no(string[5:8],register)],2)
        b=format(a,'016b')
        location=int(string[8:],2)
        M1.addtomemory(b,location) 

    elif string[:5]==opcode["ld"][0]:
        location=int(string[8:],2)
        a=int(M1.getData(location),2)
        registers[reg_no(string[5:8],register)]=format(a,'016b')

    elif string[:5]==opcode["jmp"][0]:
        location=int(string[8:],2)
        pc=location-1

    elif string[:5]==opcode["jgt"][0]:
        if tempflag=="0000000000000010":
            location=int(string[8:],2)
            pc=location-1

    elif string[:5]==opcode["jlt"][0]:
        if tempflag=="0000000000000100":
            location=int(string[8:],2)
            pc=location-1
    
    elif string[:5]==opcode["je"][0]:
        if tempflag=="0000000000000001":
            location=int(string[8:],2)
            pc=location-1

    elif string[:5]==opcode["hlt"][0]:
        halted= True
               
    return registers

def reset():
    global FLAGS
    FLAGS="0000000000000000"


def changeflag(string):
    global FLAGS
    if string=="v":
        FLAGS="0000000000001000"
    elif string=="l":
        FLAGS="0000000000000100"
    elif string=="g":
        FLAGS="0000000000000010" 
    elif string=="e":
        FLAGS="0000000000000001"
        

pc=0
halted = False
M1= mem(l1)
FLAGS="0000000000000000"
RF(registers,m3.register)
while not halted:
    instruction=M1.getData(pc)
    Execute(m3.opcode,instruction,m3.register,registers)
    print(format(pc,'08b'),*registers,FLAGS)
    pc+=1

M1.dump()
