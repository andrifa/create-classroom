from flask import json

huruf="abcdefghijklmnopqrstuvwxyz0123456789"

def encrypt(bodyPassword):    
    password=bodyPassword
    bodyPassword=""
    for i in password:
        x=huruf.index(i)+3
        if x>len(huruf)-1:
            bodyPassword+=huruf[x-len(huruf)]
        else:
            bodyPassword+=huruf[x]
    return bodyPassword

def decrypt(bodyPassword):    
    password=bodyPassword
    bodyPassword=""
    for i in password:
        x=huruf.index(i)-3
        if x<0:
            bodyPassword+=huruf[x+len(huruf)]
        else:
            bodyPassword+=huruf[x]
    return bodyPassword

###----------------------fungsi manggil-------------------------###

def readFile(fileLoc):
    fileRead = json.load(open(fileLoc,'r')) 
    return fileRead

def writeFile(fileLoc,fileData):
    open(fileLoc,'w').write(json.dumps(fileData)) 