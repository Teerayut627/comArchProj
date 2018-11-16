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
    

# def toBinary(i):
#     if i == 0:
#         return "0".zfill(3)
#     s = ''
#     while i:
#         if i & 1 == 1:
#             s = "1" + s
#         else:
#             s = "0" + s
#         i //= 2
#     return s.zfill(3)

def bindigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

with open('D:/CPE/ComArch/test.txt') as f:
    lines = f.readlines()
    line_label = []
    fill_list = []
    fill_value = []
    

    for i in lines:
        instr = i.split(' ')
        line_label.append(instr[0])

    for i in lines:
        instr = i.split(' ')
        if(instr[1] == ".fill"):
            fill_list.append(instr[0])
            fill_value.append(instr[2])
    
    # print(fill_list)
    # print(fill_value)
    
    for i in lines:
        current_address = 0
        #print(i)

        instr = i.split(' ')
        #print(len(instr))

        if(instr[1] == "add" or instr[1] == "nand"): #R-Type
            x = int(instr[2])
            y = int(instr[3])
            z = int(instr[4])
            print(int(bindigits(0,7) + instuction(instr[1]) + bindigits(x,3) + bindigits(y,3) +"0000000000000"+ bindigits(z,3),2)) 

        elif(instr[1] == "lw" or instr[1] == "sw"): #I-Type
            x = int(instr[2])
            y = int(instr[3])
            z = instr[4]
            find = False
            count = 0
            while(count < len(line_label)):
                if(line_label[count] == instr[4]):
                    find = True
                    break
                count = count + 1
            if(find == True):
                z = (count - current_address) 
            print(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(int(z),16),2))

        elif(instr[1] == ".fill"):
            x = int(instr[2])
            print(int(x))


        elif(instr[1] == "beq"):
            x = int(instr[2])
            y = int(instr[3])
        
            count = 0
            while(count < len(line_label)):
                # print(line_label[count])
                if(line_label[count] == instr[4]):
                    break
                count = count + 1
                # print(count)
            go_to = (count - current_address) - 1
            print(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(go_to,16),2))
       
        elif(instr[1] == "jalr"): #J-Type
            x = int(instr[2])
            print(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3)+bindigits(0,16),2))

        elif(instr[0] == "halt" or instr[1] == "noop"): #O-Type
            print(int(bindigits(0,7) + instuction(instr[1]) +bindigits(0,22),2))
        current_address = current_address + 1 