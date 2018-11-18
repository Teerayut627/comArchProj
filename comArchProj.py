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
    machine = ""
    fi = open("D:/CPE/ComArch/machineCode.txt","w")
#collect Label(instr[0])    
    for i in lines:
        instr = i.split(' ')
        line_label.append(instr[0])

#collect Label(instr[0]) and fill_value
    for i in lines:
        instr = i.split(' ')
        if(instr[1] == ".fill"):
            fill_list.append(instr[0])
            fill_value.append(instr[2])
    
    # print(fill_list)
    # print(fill_value)
    current_address = 0
    for i in lines:
        #print(i)
        instr = i.split(' ')
        #print(len(instr))
    #R-Type
        if(instr[1] == "add" or instr[1] == "nand"): 
            x = int(instr[2])
            y = int(instr[3])
            z = int(instr[4])
            print(int(bindigits(0,7) + instuction(instr[1]) + bindigits(x,3) + bindigits(y,3) +bindigits(0,13)+ bindigits(z,3),2)) 
            machine = bindigits(0,7) + instuction(instr[1]) + bindigits(x,3) + bindigits(y,3) +bindigits(0,13)+ bindigits(z,3)
    #I-Type
        elif(instr[1] == "lw" or instr[1] == "sw"): 
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
            machine = bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(int(z),16)
       
    #.fill
        elif(instr[1] == ".fill"):
            x = instr[2]
            find = False
            count = 0
            while(count < len(line_label)):
                if(line_label[count] == instr[2]):
                    find = True
                    break
                count = count + 1
            if(find == True):
                z = count
                print(int(z))
                machine = bindigits(int(z),32)
                
            else:
                print(int(x))
                machine = bindigits(int(x),32)
              
    #beq
        elif(instr[1] == "beq"):
            x = int(instr[2])
            y = int(instr[3])
            z = instr[4]
            find = False
            count = 0
            while(count < len(line_label)):
                # print(line_label[count])
                if(line_label[count] == instr[4]):
                    find = True
                    break
                count = count + 1
            if(find == True): 
                z = (count - current_address) - 1
            print(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(int(z),16),2))
            machine = bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(int(z),16)
           
    #J-Type       
        elif(instr[1] == "jalr"):
            x = int(instr[2])
            print(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3)+bindigits(0,16),2))
            machine = bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3)+bindigits(0,16)
           
        elif(instr[1] == "halt" or instr[1] == "noop"): #O-Type
            print(int(bindigits(0,7) + instuction(instr[1]) +bindigits(0,22),2))
            machine = bindigits(0,7) + instuction(instr[1]) +bindigits(0,22)  
        
        current_address = current_address + 1 
        
        fi.write(machine + " \n")
    fi.close()  

mem = []
reg = [0,0,0,0,0,0,0,0]
with open('D:/CPE/ComArch/machineCode.txt') as f:
    lines = f.readlines()
    for i in lines:
        memory = i.split(' ')
        mem.append(memory[0])



memline = 0
while(memline < 2):
    opcode = mem[int(memline)][7:10]

    if (opcode == "010"):
        rs = mem[int(memline)][10:13]
        rt = mem[int(memline)][13:16]
        offset = mem[int(memline)][16:32]
        print("opcode = "+opcode +" "+"rs = " +rs +" "+ "rt = " +rt +" "+ "offset = " +offset)
        
        # addr = int(mem[int(offset,2)],2) 
        addr = int(offset,2)
        valueInRs = reg[int(rs,2)]
        rtAddr = int(rt,2)
        addrValue = addr + int(valueInRs)
        reg[rtAddr] = int(mem[addrValue],2)


    memline = memline + 1
    print("valueInRs = "+str(valueInRs) + " rtAddr = " +str(rtAddr) +" IMM = " +str(addr))
    i = 0
    while i < (len(mem)):
        print("mem[ " + str(i) +  " ] " + mem[i])
        i = i + 1

    j = 0
    while j < (len(reg)):
        print("reg[ " + str(j) +  " ] " + str(reg[j]))
        j = j + 1





    























    


