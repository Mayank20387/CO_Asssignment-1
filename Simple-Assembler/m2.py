import m1
l1=[]  #contains input
l2=[]  #Splitted input
l3=[]  #splitted input
symbols={}  #variable and labels with their line number
binary=[]   #contains the binary encoded value
lerror=[]   #contains all the errors
while True:
    try :
        line = input()
        if line!="":
            l1.append(line)

    except EOFError:
        break

for i in range(len(l1)):    #splitting the input and appending it in l2 and l3
    l2.append(l1[i].split())
    l3.append(l1[i].split())

varloc=len(l2)-1
variable = 0

def pass1(list,symbols,varloc):                  #function for appending variable and label with their line number in a dictionary
    global variable
    for i in range(len(list)):
        if list[i][0]=="var" and len(list[i])==2:
            varloc+=1
            variable+=1
            symbols.update({list[i][1] : ["variable",varloc]})

        elif ":" in list[i][0]:
            symbols.update({list[i][0][:-1] : ["label",i+1]})

    return symbols,variable                      #return dictionary i.e symbols and variable(total count)


def pass2(opcode,list,register,binary):         #function to append binary encoded value of the input in a list and then print it later
    global variable
    for i in range(len(list)):
        if list[i][0][:-1] in symbols:
                list[i].pop(0)
        if list[i][0] in opcode :
            #binary encoding for TYPE-A functions
            if len(list[i])==4:
                n=opcode[list[i][0]][0]+"00"+register[list[i][1]]+register[list[i][2]]+register[list[i][3]]
                binary.append(n)

            elif len(list[i])==3:
                #binary encoding for TYPE-B functions
                if "$" in list[i][2]:
                    k=int(list[i][2][1:])
                    l=opcode[list[i][0]][0]
                    if (l=="00011"):
                        l="00010"
                    n=l+register[list[i][1]]+format(k,'08b')
                    binary.append(n)
                #binary encoding for TYPE-C functions
                elif list[i][1] and list[i][2] in register:
                     n=opcode[list[i][0]][0]+"00000"+register[list[i][1]]+register[list[i][2]]
                     binary.append(n)
                #binary encoding for TYPE-D functions
                elif  list[i][2] in symbols:
                    p=symbols[list[i][2]][1]-variable
                    n=opcode[list[i][0]][0]+register[list[i][1]]+format(p,'08b')
                    binary.append(n)

            elif len(list[i])==2:
                #binary encoding for TYPE-E functions
                if list[i][1] in symbols:
                    if symbols[list[i][1]][0]=="label":
                        r=int(symbols[list[i][1]][1])-1-variable
                        n=opcode[list[i][0]][0]+"000"+format(r,'08b')
                        binary.append(n)
            #binary encoding for TYPE-F function (hlt)
            elif len(list[i])==1:
                n=opcode[list[i][0]][0]+"00000000000"
                binary.append(n)
    return binary

def ec(opcode,symbols,list,lerror,register):  #function for error checking
    a1=[]
    a2=[] #list containing instructions and register not present in opcode/register
    a3=[]
    k=0
    c=0
    v=0
    for i in range(len(list)):
        if len(list[i])>=1 and list[i]!="hlt":
            a3.append(list[i])
        else:
            lerror.append("General Syntax Error")

    for i in a3:
        if 'hlt' in i:
            k+=1
    if k==0:
        lerror.append("hlt is missing")
            
    if "hlt" not in a3[len(a3)-1] or k!=1:
        
        lerror.append("hlt not being used as the last instruction")
    
    
    for i in range (len(a3)):
        for j in a3[i]:
            if j not in register:
                a2.append(j)
            if j in symbols:
                a2.remove(j)
            if j=="var" :
                a2.remove(j)
            if j in opcode:
                a2.remove(j)
            if ":" in j and j[:-1] in symbols:
                a2.remove(j)
            if "$" in j:
                if j[1:].isdigit():
                    k=int(j[1:])
                    a2.remove(j)
                    if k<0 or k>255:
                        lerror.append("Illegal Immediate values (less than 0 or more than 255)")

    if len(a2)!=0:            
        lerror.append(("Typos in instruction name or register name"))
              
    for i in range (len(a3)):
        if a3[i][0] == "var":
            c+=1

    for i in range(c):
        if a3[i][0] != "var":
            v=1   
    if v==1:
        lerror.append("Variables not declared at the beginning")

    for i in range (len(a3)):
        if "FLAGS" in a3[i]:
            if a3[i][0]!="mov" or a3[i][2]!="FLAGS" or a3[i][1] not in register or a3[i][1]=="FLAGS":
                lerror.append("Illegal use of FLAGS register")
        if a3[i][0]=="jmp" or a3[i][0]=="je" or a3[i][0]=="jlt" or a3[i][0]=="jgt":
            if a3[i][1] not in symbols:
                lerror.append("Use of undefined labels")
            elif symbols[a3[i][1]][0]!="label":
                lerror.append("Misuse of labels as variables or vice-versa")

        if a3[i][0]=="ld" or a3[i][0]=="st":
            if a3[i][2] not in symbols:
                lerror.append("Use of undefined variables")
            elif  symbols[a3[i][2]][0]!="variable":
                lerror.append("Misuse of labels as variables or vice-versa")

    for i in range (len(a3)):
        if a3[i][0] in opcode:
            if opcode[a3[i][0]][1] =="A":
                if len(a3[i])!=4: 
                    lerror.append("Wrong syntax used for instructions")
                elif a3[i][1] and a3[i][2] and a3[i][3] not in register:
                    lerror.append("Wrong syntax used for instructions")

            elif opcode[a3[i][0]][1] =="B" or (a3[i][0] =="mov" and "$" in a3[i][2]) :
                if len(a3[i])!=3: 
                    lerror.append("Wrong syntax used for instructions")
                elif a3[i][1] not in register:
                    lerror.append("Wrong syntax used for instructions")
                elif "$" not in a3[i][2]:
                    lerror.append("Wrong syntax used for instructions") 

            elif opcode[a3[i][0]][1] =="C":
                if len(a3[i])!=3: 
                    lerror.append("Wrong syntax used for instructions")
                elif a3[i][1] and a3[i][2] not in register:
                    lerror.append("Wrong syntax used for instructions")

            elif opcode[a3[i][0]][1] =="D":
                if len(a3[i])!=3: 
                    lerror.append("Wrong syntax used for instructions")
                elif a3[i][1] not in register:
                    lerror.append("Wrong syntax used for instructions")
                elif a3[i][2] not in symbols:
                    lerror.append("Wrong syntax used for instructions")

            elif opcode[a3[i][0]][1] =="E":
                if len(a3[i])!=2: 
                    lerror.append("Wrong syntax used for instructions")
                elif a3[i][1] not in symbols:
                    lerror.append("Wrong syntax used for instructions")

            elif opcode[a3[i][0]][1] =="F":
                if len(a3[i])!=1: 
                    lerror.append("Wrong syntax used for instructions")
    
    return lerror , a3
       
pass1(l2,symbols,varloc)
for i in range(len(l3)):         #to remove labels
        if l3[i][0][:-1] in symbols:
                l3[i].pop(0)

ec(m1.opcode,symbols,l3,lerror,m1.register)

if (lerror==[]):
    pass2(m1.opcode,l2,m1.register,binary)  #printing the binary values (when input given is error free)
    for i in binary:
        print(i)
else:
    lerror=set(lerror)                    #printing errors
    for i in lerror:
        print(i)

    