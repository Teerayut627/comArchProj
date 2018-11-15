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


user_input = input("Enter instruction , field0 , field1 and field2 : ")
instr,field0,field1,field2 = user_input.split(' ')
if(instr == "add" or "nand"): #R-Type
    x = int(field0[1:])
    y = int(field1[1:])
    z = int(field2[1:])
    print("0000000 " + instuction(instr) +" "+ toBinary(x) +" "+ toBinary(y) +" 0000000000000 "+ toBinary(z))

if(instr == "lw" or "sw" or "beq"): #I-Type
    x = int(field0[1:])
    y = int(field1[1:])
    