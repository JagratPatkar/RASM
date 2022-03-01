import json
from pickletools import bytes4
import sys
spec = json.load(open("spec.json","r"))


def error(): print("Invalid Instruction")

def splitBinary(imm):
    ls =  [i for i in str(imm) if i != "b"]
    ls.reverse()     
    return ls

def getSecs(ls,s,e):
    return "".join(ls[s:e+1])[::-1]

def regToaddr(inst,str):
    x_len = spec[spec[inst]["type"]]["x"]
    return format(int(str.strip(" ").strip("x").strip("r")),x_len) 

def immExp(inst,str):
    imm_len =  spec[spec[inst]["type"]]["imm"]
    if spec[inst]["type"] == "j":
        return format(int(str.strip(" "),2),imm_len) + "0"
    return  format(int(str.strip(" "),2),imm_len) 

def iType(inst,lst):
    bin_inst = spec[inst]["op"]
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = spec[inst]["func"] + bin_inst
    imm_full = splitBinary(immExp(inst,lst[2]))
    if spec[inst]["func7"]: imm_full[10] = '1'
    bin_inst = regToaddr(inst,lst[1]) + bin_inst
    bin_inst = getSecs(imm_full,0,11) + bin_inst
    return bin_inst

def rType(inst,lst):
    bin_inst = spec[spec[inst]["type"]]["op"]
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = spec[inst]["func"] + bin_inst
    bin_inst = regToaddr(inst,lst[1]) + bin_inst
    bin_inst = regToaddr(inst,lst[2]) + bin_inst
    bin_inst = spec[inst]["func7"] + bin_inst
    return bin_inst

def sType(inst,lst):
    bin_inst = spec[spec[inst]["type"]]["op"]
    imm_full = splitBinary(immExp(inst,lst[2]))
    bin_inst = getSecs(imm_full,0,4) + bin_inst
    bin_inst = spec[inst]["func"] + bin_inst
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = regToaddr(inst,lst[1]) + bin_inst
    bin_inst = getSecs(imm_full,5,11) + bin_inst
    return bin_inst

def bType(inst,lst):
    bin_inst = spec[spec[inst]["type"]]["op"]
    imm_full = splitBinary(immExp(inst,lst[2]))
    bin_inst = getSecs(imm_full,11,11) + bin_inst
    bin_inst = getSecs(imm_full,1,4) + bin_inst
    bin_inst = spec[inst]["func"] + bin_inst
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = regToaddr(inst,lst[1]) + bin_inst
    bin_inst = getSecs(imm_full,5,10) + bin_inst
    bin_inst = getSecs(imm_full,12,12) + bin_inst
    return bin_inst

def uType(inst,lst):
    bin_inst = spec[inst]["op"]
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    bin_inst = immExp(inst,lst[1]) + bin_inst
    return bin_inst


def jType(inst,lst):
    bin_inst = spec[inst]["op"]
    bin_inst = regToaddr(inst,lst[0]) + bin_inst
    imm_full = splitBinary(immExp(inst,lst[1]))
    bin_inst = getSecs(imm_full,12,19) + bin_inst
    bin_inst = getSecs(imm_full,11,11) + bin_inst
    bin_inst = getSecs(imm_full,1,10) + bin_inst
    bin_inst = getSecs(imm_full,20,20) + bin_inst
    return bin_inst


def convertInst(inst,lst):
    if spec[inst]["type"] == "i" : return iType(inst,lst)
    elif spec[inst]["type"] == "r" : return rType(inst,lst)
    elif spec[inst]["type"] == "s" : return sType(inst,lst)
    elif spec[inst]["type"] == "b" : return bType(inst,lst)
    elif spec[inst]["type"] == "u" : return uType(inst,lst)
    elif spec[inst]["type"] == "j" : return jType(inst,lst)
    else: error()

def convertAssembly():
    w = open("output.bin","wb")
    for i in open(sys.argv[1],"r").readlines():
        inst = i.strip("\n").split(" ",1)
        if len(inst) > 1 and '' not in inst:
            inst[1] = inst[1].strip(" ").split(",")
            inst = convertInst(inst[0],inst[1])
            w.write(int(inst,2).to_bytes(4,'big'))
        else: error()
    w.close()

convertAssembly()