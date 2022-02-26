import json

spec = json.load(open("spec.json","r"))




def splitBinary(imm,s,e):
    ls =  [i for i in str(imm) if i != "b"]
    ls.reverse()     
    return "".join(ls[s:e+1])[::-1]

def regToaddr(inst,str):
    x_len = spec[spec[inst]["type"]]["x"]
    return format(int(str.strip(" ").strip("x")),x_len) 

def immExp(inst,str):
    imm_len =  spec[spec[inst]["type"]]["imm"]
    return  format(int(str.strip(" "),2),imm_len) 

def iType(inst,lst):
    bin_inst = spec[inst]["op"]
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = spec[inst]["func"] + bin_inst
    bin_inst = regToaddr(inst,lst[1]) + bin_inst
    bin_inst = immExp(inst,lst[2]) + bin_inst
    return bin_inst

def rType(inst,lst):
    bin_inst = spec[inst]["op"]
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = spec[inst]["func"] + bin_inst
    bin_inst = regToaddr(inst,lst[1]) + bin_inst
    bin_inst = regToaddr(inst,lst[2]) + bin_inst
    bin_inst = spec[inst]["func7"]
    return bin_inst

def sType(inst,lst):
    bin_inst = spec[inst]["op"]
    imm_full = immExp(inst,lst[2]) 
    bin_inst = splitBinary(imm_full,0,4) + bin_inst
    bin_inst = spec[inst]["func"] + bin_inst
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = regToaddr(inst,lst[1]) + bin_inst
    bin_inst = splitBinary(imm_full,5,11) + bin_inst
    return bin_inst

def bType(inst,lst):
    bin_inst = spec[inst]["op"]
    imm_full = immExp(inst,lst[2])
    bin_inst = splitBinary(imm_full,11,11) + bin_inst
    bin_inst = splitBinary(imm_full,1,4) + bin_inst
    bin_inst = spec[inst]["func"] + bin_inst
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = regToaddr(inst,lst[1]) + bin_inst
    bin_inst = splitBinary(imm_full,5,10) + bin_inst
    bin_inst = splitBinary(imm_full,12,12) + bin_inst
    return bin_inst

def uType(inst,lst):
    bin_inst = spec[inst]["op"]
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = immExp(inst,lst[1]) + bin_inst
    return bin_inst


def convertInst(inst,lst):
    if spec[inst]["type"] == "i" : return iType(inst,lst)
    elif spec[inst]["type"] == "r" : return rType(inst,lst)
    elif spec[inst]["type"] == "s" : return sType(inst,lst)
    elif spec[inst]["type"] == "b" : return bType(inst,lst)
    elif spec[inst]["type"] == "u" : return uType(inst,lst)
    else: print("Invalid Instruction")

def convertAssembly():
    w = open("output.txt","w")
    for i in open("one.S","r").readlines():
        inst = i.strip("\n").split(" ",1)
        inst[1] = inst[1].split(",")
        inst = convertInst(inst[0],inst[1])
        w.write(inst + "\n")

convertAssembly()
