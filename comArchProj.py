def instuction(instr):
    #R-type
    if(instr == "add"):
        return "000"
    if(instr == "nand"):
        return "001"
    #I-Type
    if(instr == "lw"):
        return "010"
    if(instr == "sw"):
        return "011"
    if(instr == "beq"):
        return "100"
    #J-type
    if(instr =="jalr"):
        return "101"
    #O-type
    if(instr =="halt"):
        return "110"
    if(instr =="noop"):
        return "111"
    

def toBinary(i):
    if i == 0:
        return "0".zfill(3)
    s = ''
    while i:
        if i & 1 == 1:
            s = "1" + s
        else:
            s = "0" + s
        i //= 2
    return s.zfill(3)

with open('D:/CPE/ComArch/test.txt') as f:
    lines = f.readlines()
    line = -1
    line_label = []
    for i in lines:
       # print(i)
#user_input = input("Enter instruction , field0 , field1 and field2 : ")
        instr = i.split(' ')
        #print(len(instr))
        line = line + 1
        line_label.append(instr[0])
        #print(line_label[0])
       
        if(instr[1] == "add" or instr[1] == "nand"): #R-Type
            x = int(instr[2][1:])
            y = int(instr[3][1:])
            z = int(instr[4][1:])
            print(int("0000000" + instuction(instr[1]) + toBinary(x) + toBinary(y) +"0000000000000"+ toBinary(z),2)) 

        elif(instr[1] == "lw" or instr[1] == "sw" or instr[1] == "beq"): #I-Type
            x = int(instr[2][1:])
            y = int(instr[3][1:])
            #z = int(instr[4])
            # for count in line_label:
            #     if(instr[4] == line_label[count]):
            #         break
            # z = int(count) 
            print(int("0000000" + instuction(instr[1]) +toBinary(x) +toBinary(y) +toBinary(z).zfill(16),2))
                
        elif(instr[1] == "jalr"): #J-Type
            x = int(instr[2][1:])
            print(int("0000000" + instuction(instr[1]) +toBinary(x) +toBinary(y)+"0000000000000000",2))

        elif(instr[0] == "halt" or instr[1] == "noop"): #O-Type
            print(int("0000000" + instuction(instr[1]) +"0000000000000000000000",2))
       
            