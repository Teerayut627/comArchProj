def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

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
    

def bindigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

def sign_bit (imm) : 
    result = ''
    imm = str(imm)
    for i in imm :
        if i == '1':
            result = result + "0"
        else :
            result = result + "1"            
    return add_binary_nums(result[0:-1], bin(1))
    
def add_binary_nums(x, y) :
        max_len = max(len(x), len(y))

        x = x.zfill(max_len)
        y = y.zfill(max_len)

        result = ''
        carry = 0

        for i in range(max_len-1, -1, -1) :
            r = carry
            r += 1 if x[i] == '1' else 0
            r += 1 if y[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result
            carry = 0 if r < 2 else 1       

        if carry !=0 : result = '1' + result
        return result.zfill(max_len)


decMem = []
with open('D:/CPE/ComArch/assemblyCom.txt') as f:
    lines = f.readlines()
    line_label = []
    fill_list = []
    fill_value = []
    machine = ""
    fi = open("D:/CPE/ComArch/MachineCode.txt","w")

# collect Label(instr[0])    
    for i in lines:
        instr = i.split(' ')
        j = 0
        while(j < len(line_label)):
            if(line_label[j] == instr[0] and line_label[j] != ""):
                print("error : label repeatedly")
                break
            j = j + 1
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
            decMem.append(int(bindigits(0,7) + instuction(instr[1]) + bindigits(x,3) + bindigits(y,3) +bindigits(0,13)+ bindigits(z,3),2)) 
            machine = str(int(bindigits(0,7) + instuction(instr[1]) + bindigits(x,3) + bindigits(y,3) +bindigits(0,13)+ bindigits(z,3),2))
    #I-Type
        elif(instr[1] == "lw" or instr[1] == "sw"): 
            x = int(instr[2])
            y = int(instr[3])
            z = instr[4]
            find = False
            count = 0
            if(RepresentsInt(z) == False):
                while(count < len(line_label)):
                    if(line_label[count] == instr[4]):
                        find = True
                        break
                    count = count + 1
                if(find == True):
                    z = count
                else:
                    print("error : undefind labels at lw/sw")
                    break
            decMem.append(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(int(z),16),2))
            machine = str(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(int(z),16),2))
    #.fill
        elif(instr[1] == ".fill"):
            if(RepresentsInt(instr[2]) == True):
                if(int(instr[2]) > 32767 or int(instr[2]) < -32768):
                    print("error : offsetField more than 16 bits")
                    break
            x = instr[2]
            find = False
            count = 0
            while(count < len(line_label)):
                if(line_label[count] == instr[2]):
                    find = True
                    break
                count = count + 1
            if(RepresentsInt(instr[2]) == False):
                if(find == True):
                    z = count
                    decMem.append(int(z))
                    machine = str(int(z))
                else:
                    print("error : undefind labels at .fill")
            else:
                decMem.append(int(x))
                machine = str(int(x))
              
    #beq
        elif(instr[1] == "beq"):
            x = int(instr[2])
            y = int(instr[3])
            z = instr[4]
            find = False
            count = 0
            if(RepresentsInt(z) == False):
                while(count < len(line_label)):
                # print(line_label[count])
                    if(line_label[count] == instr[4]):
                        find = True
                        break
                    count = count + 1
                if(find == True): 
                    z = (count - current_address) - 1
                else:
                    print("error : undefind labels at beq")
                    break
            decMem.append(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(int(z),16),2))
            machine = str(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3) + bindigits(int(z),16),2))
           
    #J-Type       
        elif(instr[1] == "jalr"):
            x = int(instr[2])
            y = int(instr[3])
            decMem.append(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3)+bindigits(0,16),2))
            machine = str(int(bindigits(0,7) + instuction(instr[1]) +bindigits(x,3) +bindigits(y,3)+bindigits(0,16),2))
           
        elif(instr[1] == "halt" or instr[1] == "noop"): #O-Type
            decMem.append(int(bindigits(0,7) + instuction(instr[1]) +bindigits(0,22),2))
            machine = str(int(bindigits(0,7) + instuction(instr[1]) +bindigits(0,22),2))
            
        else:
            print("error : instruction error")
            break
        
        current_address = current_address + 1 
        
        fi.write(machine + " \n")
    fi.close()  

