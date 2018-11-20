
#-----------------------FUNCTION-----------------------

def bindigits(n, bits): #-----Convert Decimal to Binary n bits------
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)
def sign_bit(imm): #-----Convert 1 & 0 bits Function-----
    result = ''
    imm = str(imm)
    for i in imm :
        if i == '1':
            result = result + "0"
        else :
            result = result + "1"            
    return result
def add_binary_nums(x, y) : #-----Add binary n bit-----
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

#------------------Read Decimal Machine Code form text------------------
decimalCode = []
with open('D:/CPE/ComArch/MachineCode.txt') as f:
    lines = f.readlines()
    for i in lines:
        memory = i.split(' ')
        decimalCode.append(memory[0])

#------------------Select only Machine Code------------------
memDecimal = []
for i in decimalCode:
    Soi = i.split('\n')
    memDecimal.append(Soi[0])
print(memDecimal)

#------------------Prepare Binarry Machinne Code in Memory for Processing------------------
mem = []
reg = [0,0,0,0,0,0,0,0]
strLines = 0
while (strLines < len(memDecimal)):
    Binary = bindigits(int(memDecimal[strLines]),32)
    mem.append(Binary)
    strLines = strLines + 1

#------------------Processing follow ------------------
memline = 0
while(memline < len(mem)):
    opcode = mem[int(memline)][7:10]
    #-----Print Simulator Result-----
    print("@@@")
    print("state :")
    print("     PC : " + str(memline))
    #-----Print Memory-----
    print("     memory :")
    i = 0
    while i < (len(mem)):
        if(mem[i][0:1] == "1"):
            memPrint = int(add_binary_nums(sign_bit(mem[i]),'1'),2)*(-1)
        else:
            memPrint = int(mem[i],2)
        print("     mem[ " + str(i) +  " ] " + str(memPrint))
        i = i + 1
    #-----Print Register-----
    print("register :")
    j = 0
    while j < (len(reg)):
        print("     reg[ " + str(j) +  " ] " + str(reg[j]))
        j = j + 1
    #ADD
    if (opcode == "000"):
        rs = int(mem[int(memline)][10:13],2) 
        rt = int(mem[int(memline)][13:16],2) 
        destReg = int(mem[int(memline)][29:32],2) 
        addResult = int(reg[rt]) + int(reg[rs]) 
        reg[destReg] = addResult
    #NAND
    if (opcode == "001"):
        rs = int(mem[int(memline)][10:13],2) 
        rt = int(mem[int(memline)][13:16],2) 
        destReg = int(mem[int(memline)][29:32],2) 
        reg[destReg] = ( ~( int(reg[rt],2) & int(reg[rs],2) ) )  
    #LW
    if (opcode == "010"):
        rs = int(mem[int(memline)][10:13],2) 
        rt = int(mem[int(memline)][13:16],2) 
        offset = int(mem[int(memline)][16:32],2) 
        addrValue = offset + int(reg[rs])
        if(mem[addrValue][0:1] == "1"):
            reg[rt] = int(add_binary_nums(sign_bit(mem[addrValue]),'1'),2)*(-1)
        else:
            reg[rt] = int(mem[addrValue],2)
    #SW
    if (opcode == "011"):
        rs = int(mem[int(memline)][10:13],2) 
        rt = int(mem[int(memline)][13:16],2) 
        offset = int(mem[int(memline)][16:32],2) 
        addrValue = offset + int(reg[rs])
        mem[addrValue] = int(reg[rt],2)
    #BEQ
    if (opcode == "100"): 
        rs = int(mem[int(memline)][10:13],2) 
        rt = int(mem[int(memline)][13:16],2) 
        offset = mem[int(memline)][16:32]
        if( reg[rt] == reg[rs]):
            if(mem[memline][16:17] == "1"):
                offsetJamp = int(add_binary_nums(sign_bit(offset),"1"),2)*(-1)
            else:
                offsetJamp = int(offset,2)
            jampAddr = memline + offsetJamp
            memline = jampAddr
    #JALR
    if (opcode == "101"):
        rs = int(mem[int(memline)][10:13],2) 
        rd = int(mem[int(memline)][13:16],2) 
        if(rs == rd): #Have yet to Verify 
            reg[rt] = memline
            memline = reg[rs]
        else: #if and else have the same process
            reg[rt] = memline
            memline = reg[rs]
    #HALT
    if (opcode == "110"):
        print("Machine halted")
        break
    #NOOP
    if (opcode == "111"):
        continue
    memline = memline + 1

    