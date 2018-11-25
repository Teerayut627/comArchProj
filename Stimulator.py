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
with open('D:/CPE/ComArch/MachineCode.txt') as f: # open file machine code take in each line in decimal code array
    lines = f.readlines()
    for i in lines:
        memory = i.split(' ')
        decimalCode.append(memory[0])

#------------------Select only Machine Code------------------
memDecimal = []
for i in decimalCode: # เอา array decimal code ออกมา เอาส่วนที่ตัดออก มาใส่ใน mem array of decimal
    Soi = i.split('\n')
    memDecimal.append(Soi[0])
print(memDecimal)

#------------------Prepare Binarry Machinne Code in Memory for Processing------------------
mem = []
reg = [0,0,0,0,0,0,0,0]
strLines = 0
while (strLines < len(memDecimal)):
    Binary = bindigits(int(memDecimal[strLines]),32) # เอาแต่ละบรรทัดของ memdecimal มาแปลงเป็น binary 32bit เก็บไว้ใน mem array
    mem.append(Binary)
    strLines = strLines + 1

#------------------Processing follow ------------------

PC = 0
ExecutedInstr = 1 # ใช้นับว่าทำกี่ครั้ง
while(PC < len(mem)):
    opcode = mem[int(PC)][7:10] # แยกเอาเฉพาะ opcode มาจาก ใน memmory array
    #-----Print Simulator Result-----
    print("@@@")
    print("state :")
    print("     PC : " + str(PC))
    #-----Print Memory-----
    print("     memory :")
    i = 0
    while i < (len(mem)):
        if(mem[i][0:1] == "1"): # ปริ้นค่า mem ทุกตัว
            memPrint = int(add_binary_nums(sign_bit(mem[i]),'1'),2)*(-1)  # กรณีที่ค่าใน mem ติดลบ เลขฐาน 10 โดยที่กลับ bit บวก1 คูณกับ -1 
        else:  
            memPrint = int(mem[i],2)
        print("     mem[ " + str(i) +  " ] " + str(memPrint)) 
        i = i + 1
    #-----Print Register-----
    print("register :")
    j = 0
    while j < (len(reg)):
        print("     reg[ " + str(j) +  " ] " + str(reg[j])) # show ค่า register ทุกตัว
        j = j + 1
    print("end state")
    #ADD
    if (opcode == "000"): # ฟังก์ชัน add 
        rs = int(mem[int(PC)][10:13],2) 
        rt = int(mem[int(PC)][13:16],2) 
        destReg = int(mem[int(PC)][29:32],2) 

        addABinary = bindigits(reg[rs],33)[-32:] # จำกัด bit ของ rs,rt ให้เหลือแค่ 32 bit 
        addBBinary = bindigits(reg[rt],33)[-32:]

        if ( int(reg[rs]) < 0): # ค่าใน register rs ติดลบ กลับ bit บวก 1 จะได้เลขฐาน 10 ที่ติดลบ
            valueA = int(add_binary_nums(sign_bit(addABinary),"1"),2)*(-1)
        else:
            valueA = int(addABinary,2) # เก็บค่าใน register rs เป็นเลขฐาน 10

        if ( int(reg[rt]) < 0):# ค่าใน register rt ติดลบ กลับ bit บวก 1 จะได้เลขฐาน 10 ที่ติดลบ
            valueB = int(add_binary_nums(sign_bit(addBBinary),"1"),2)*(-1)
        else:
            valueB = int(addBBinary,2) # เก็บค่าใน register rt เป็นเลขฐาน 10

        
        addResult = valueA + valueB  # เอาค่า rs กับ rt บวกกัน
        print(str(addResult) + " = " + str(valueA)+"+"+str(valueB))
        addResultBinary = bindigits(addResult,33)[-32:] # เอาค่าผลบวกที่ได้มาตัดเหลือ 32bit 
        if ( addResult < 0): # ค่าผลบวก น้อยกว่า 0 ก็เปลี่ยน 32 bit มาเป็น ฐาน10 ในรูปติดลบ
            addResult10 = int(add_binary_nums(sign_bit(addResultBinary),"1"),2)*(-1)
        else:
            addResult10 = int(addResultBinary,2)
        
        reg[destReg] = addResult10


    #NAND
    if (opcode == "001"):
        rs = int(mem[int(PC)][10:13],2) 
        rt = int(mem[int(PC)][13:16],2) 
        destReg = int(mem[int(PC)][29:32],2) 

        print(bindigits(reg[rs],33)[-32:])
        print(bindigits(reg[rt],33)[-32:])

        nandABinary = bindigits(reg[rs],33)[-32:]
        nandBBinary = bindigits(reg[rt],33)[-32:]

        if( reg[rs] < 0 ):
            nandA = int(add_binary_nums(sign_bit(nandABinary),"1"),2)*(-1)
        else:
            nandA = int(nandABinary,2)

        if( reg[rt] < 0  ):
            nandB = int(add_binary_nums(sign_bit(nandBBinary),"1"),2)*(-1)
        else:
            nandB = int(nandBBinary,2)
        

        reg[destReg] = ~(nandA & nandB)

    #LW
    if (opcode == "010"):
        rs = int(mem[int(PC)][10:13],2) 
        rt = int(mem[int(PC)][13:16],2) 
        offset = int(mem[int(PC)][16:32],2) 
        addrValue = offset + int(reg[rs])
        if(mem[addrValue][0:1] == "1"):
            reg[rt] = int(add_binary_nums(sign_bit(mem[addrValue]),'1'),2)*(-1)
        else:
            reg[rt] = int(mem[addrValue],2)

    #SW
    if (opcode == "011"):
        rs = int(mem[int(PC)][10:13],2) 
        rt = int(mem[int(PC)][13:16],2) 
        offset = int(mem[int(PC)][16:32],2) 
        addrValue = offset + int(reg[rs])
        print(str(reg[rs]) +" in " +str(rs) +" , " +str(reg[rt]) +" in "  +str(rt) +" " +str(offset))
        print(addrValue)
        mem[addrValue] =  bindigits(reg[rt],32)
        print(bindigits(reg[rt],32))

    #BEQ
    if (opcode == "100"): 
        rs = int(mem[int(PC)][10:13],2) 
        rt = int(mem[int(PC)][13:16],2) 
        offset = mem[int(PC)][16:32]

        beqABinary = bindigits(reg[rs],33)[-32:] #Limits bits
        beqBBinary = bindigits(reg[rt],33)[-32:]

        if ( int(reg[rs]) < 0):
            valueA = int(add_binary_nums(sign_bit(beqABinary),"1"),2)*(-1)
        else:
            valueA = int(beqABinary,2)

        if ( int(reg[rt]) < 0):
            valueB = int(add_binary_nums(sign_bit(beqBBinary),"1"),2)*(-1)
        else:
            valueB = int(beqBBinary,2)


        if( valueA == valueB):
            if(mem[PC][16:17] == "1"):
                offsetJamp = int(add_binary_nums(sign_bit(offset),"1"),2)*(-1)
            else:
                offsetJamp = int(offset,2)
            jampAddr = PC + offsetJamp
            PC = jampAddr
    #JALR
    if (opcode == "101"):
        
        rs = int(mem[int(PC)][10:13],2) 
        rd = int(mem[int(PC)][13:16],2) 
        print(mem[int(PC)][13:16])
        print("yut")
        print("Jump to " +str(reg[rs]))
        reg[rd] = PC + 1
        print("stored " +str(PC) +" in " + str(rd))
        PC = int(reg[rs])
        continue

    #HALT
    if (opcode == "110"):
        print("Machine halted")
        break
    #NOOP
    if (opcode == "111"):
        continue
    PC = PC + 1
    ExecutedInstr = ExecutedInstr + 1

#-----Final Print Simulator Result-----
print("Total of " +str(ExecutedInstr) +" instructions executed")
print("Final State of Machine :")
print("@@@")
print("state :")
print("     PC : " + str(PC + 1))
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
print("end state")   