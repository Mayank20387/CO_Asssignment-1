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
        #for i in range(256):
        #    self.memory[i]=="0000000000000000"
        self.memory[location]=string
        #        self.memory[i]=string

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
#for i in range(len(l1)):
 #   l2.append(l1[i].split()
#pc=0
#M1= mem(l1)
#RF(registers,m3.register)
s="0010101000000011"
t="1001100000000000"
#print(M1.getData(pc))
#M1.memdec()
#M1.dump()
#for i in mem.memory:
#       print(i)
halted = 0
def Execute(opcode,string,register,registers):
    global halted
    #print(M1.getData(1))
    if string[:5]==opcode["add"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b+c
        #print(a)
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["sub"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b-c
        #print(a)
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["mul"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b*c
        #print(a)
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["xor"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b^c
        #print(a)
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["or"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b|c
        #print(a)
        registers[reg_no(string[7:10],register)]=format(a,'016b')

    elif string[:5]==opcode["and"][0]:
        b=int(registers[reg_no(string[10:13],register)],2)
        c=int(registers[reg_no(string[13:16],register)],2)
        a=b&c
        #print(a)
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
        a=int(registers[reg_no(string[13:16],register)],2)
        registers[reg_no(string[10:13],register)]=format(a,'016b')

    elif string[:5]==opcode["not"][0]:
        a=int(registers[reg_no(string[13:16],register)],2)
        b=~a
        registers[reg_no(string[10:13],register)]=format(b,'016b')

    elif string[:5]==opcode["cmp"][0]:
        a=int(registers[reg_no(string[10:13],register)],2)
        b=int(registers[reg_no(string[13:16],register)],2)
        if a>b:
            print(1)
        else:
            print(0)

    elif string[:5]==opcode["st"][0]:
        a=int(registers[reg_no(string[5:8],register)],2)
        b=format(a,'016b')
        location=int(string[8:],2)
        M1.addtomemory(b,location) 

    elif string[:5]==opcode["ld"][0]:
        location=int(string[8:],2)
        a=int(M1.getData(location),2)
        registers[reg_no(string[5:8],register)]=format(a,'016b')

    elif string[:5]==opcode["hlt"][0]:
        halted=1
        
         
        
    return registers,halted

#print(registers)
#Execute(m3.opcode,M1.getData(pc),m3.register,registers)
#Execute(m3.opcode,s,m3.register,registers)
#Execute(m3.opcode,t,m3.register,registers)
#print(registers)
#M1.dump()
def PC(pc,list):
    if pc<256:
        list.append(format(pc,'08b'))

#def completedump(pc,list2):
 #   for i in range():


pc=0
M1= mem(l1)
RF(registers,m3.register)
while(halted!=1):
    instruction=M1.getData(pc)
    #print(instruction)
    Execute(m3.opcode,instruction,m3.register,registers)
#Execute(m3.opcode,s,m3.register,registers)
#print(halted)
    print(format(pc,'08b'),*registers,"0000000000000000")
    pc+=1
#M1= mem(l1)
#RF(registers,m3.register)
#s="0010101000000011"
#t="0010000000000011"
#print(M1.getData(pc))
#M1.memdec()
M1.dump()
#print(*registers,sep=" ")