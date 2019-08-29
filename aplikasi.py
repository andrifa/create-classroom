from flask import Flask,jsonify, request, json
import os
from src.utils.crypt import encrypt,decrypt,readFile,writeFile
from src.utils.authorization import encode
from flask_cors import CORS
apps=Flask(__name__)
CORS(apps)

@apps.errorhandler(404)
def error404(e):
    message = {
        "message":"The requested URL {} was not found in this server".format(request.path)
    }
    return message, 404

#------------------------Function--------------------------#
userFileLoc='src/data/registrasi.json'
classFileLoc='src/data/kelas.json'
classworkFileLoc='src/data/classwork.json'
#----------------------------------------------------------#

@apps.route('/')
def test0():
    return "success"

@apps.route('/daftar',methods=["POST"])
def daftar():
    body= request.json
    body["class"]=[]
    body["classwork"]=[]
    statusCode=400

    body["password"]=encrypt(body["password"])
    
    response={}
    response["message"]="Create User Success"
    response["data"]={}

    userData=[]

    if os.path.exists (userFileLoc): 
        userData= readFile(userFileLoc)

    tempUserId=1
    if len(userData)==0:
        tempUserId = 1
    else:
        tempUserId=userData[-1]["user id"]+1
    body["user id"]=tempUserId

    for userId in userData:
        if body["user id"]==userId["user id"] and userData!=[]:
            response["message"]="User ID {} is already exist".format(body["user id"])
            return jsonify(response),statusCode
        elif body["username"]==userId["username"]:
            response["message"]="Username is already exist"
            return jsonify(response),statusCode
        elif body["email"]==userId["email"]:
            response["message"]="Email is already exist"
            return jsonify(response),statusCode
    
    userData.append(body)

    writeFile(userFileLoc,userData)

    response["data"]=body
    return jsonify(response)

@apps.route('/daftar/<int:userid>',methods=["PUT"])
def updateUser(userid):
    body= request.json

    body["password"]=encrypt(body["password"])
    
    response={}
    response["message"]="Update User Success"
    response["data"]={}

    userData = readFile(userFileLoc)
    count=0
    for user in userData:
        if user["user id"]==userid:
            count+=1
            user["email"]=body["email"]
            user["fullname"]=body["fullname"]
            user["password"]=body["password"]
            user["username"]=body["username"]
    if count!=1:
        response["message"]="User ID {} is not registered".format(userid)
        return jsonify(response)
    
    writeFile(userFileLoc,userData)

    response["data"]=body
    return jsonify(response)
            
@apps.route('/validasi',methods=["POST"])
def validasi():
    body=request.json
    
    response={}
    response["message"]="Login User Failed"
    response["data"]={}
    statusCode=400

    userData = readFile(userFileLoc)

    for user in userData:        
        user["password"]=decrypt(user["password"])
        if body["username"]==user["username"] and body["password"]==user["password"]:
            response["message"]="Login User Success"
            user["password"]="*"*len(user["password"])
            response["data"]=user
            response["token"]=encode(body["username"])
            return jsonify(response)
        else:
            pass
    return jsonify(response), statusCode
            
@apps.route('/getUser/<int:n>',methods=["GET"])
def getUser(n):
    
    response={}
    response["message"]="Get User Failed, user id {} is not registered".format(n)
    response["data"]={}

    userData = readFile(userFileLoc)
    classData = readFile(classFileLoc)

    for user in userData:
        if user["user id"]==n:
            for kelas in user["class"]:
                for classid in classData:
                    if classid["classid"]==kelas["classid"]:
                        kelas["classid"]=classid["classname"]
                        kelas["kelasid"]=classid["classid"]
            response["message"]="Get User {} Success".format(n)
            response["data"]=user
            return jsonify(response)
    return jsonify(response)

@apps.route('/getUser/all',methods=["GET"])
def getUserAll():
    userData = readFile(userFileLoc)
    return jsonify(userData)

@apps.route('/class',methods=["POST"])
def createClass():
    body= request.json
    body["student"]=[]
    body["classwork"]=[]

    response={}
    response["message"]="Create Class Success"
    response["data"]={}

    cekTeacher = readFile(userFileLoc)
    count=False
    for cek in cekTeacher:
        if [cek["user id"]]==body["teachers"]:
            count=True
            break
    if not count:
        response["message"]="Teacher id {} is not recognized".format(body["teachers"][0])
        return jsonify(response)

    userData=[]
    
    if os.path.exists (classFileLoc):
        userData= readFile(classFileLoc)
    
    tempUserId=1
    if len(userData)==0:
        tempUserId = 1
    else:
        tempUserId=userData[-1]["classid"]+1
    body["classid"]=tempUserId
    
    for classId in userData:
        if body["classid"]==classId["classid"] and userData!=[]:
            response["message"]="Class ID {} is already exist".format(body["classid"])
            return jsonify(response)

    userData.append(body)

    writeFile(classFileLoc,userData)
    
    #masukkin status ke user
    userData = readFile(userFileLoc)
    
    for user in userData:
        if body["teachers"]==[user["user id"]]:
            kelas={
                    "classid":body["classid"],
                    "status":"teacher"
                }
            if kelas not in user["class"]:
                user["class"].append(kelas)
                
    writeFile(userFileLoc,userData)

    response["data"]=body
    return jsonify(response)

@apps.route('/class/<int:classid>',methods=["PUT"])
def updateClass(classid):
    body= request.json
    
    response={}
    response["message"]="Update Class Success"
    response["data"]={}

    userData = readFile(classFileLoc)
    count=0
    for kelas in userData:
        if kelas["classid"]==classid:
            count+=1
            kelas["classname"]=body["classname"]
            break

    if count!=1:
        response["message"]="Update Class Failed, Class id {} is not registered".format(classid)
        return jsonify(response)

    writeFile(classFileLoc,userData)
    
    response["data"]=kelas

    return jsonify(response)

@apps.route('/getClass/<int:n>',methods=["GET"])
def getClass(n):
    
    response={}
    response["message"]="Class {} is not registered".format(n)
    response["data"]={}

    userData = readFile(classFileLoc)
    userData2 = readFile(userFileLoc)
    for kelas in userData:
        if kelas["classid"]==n:
            for idnama in range(len(kelas["student"])):
                for nama in userData2:
                    if kelas["student"][idnama]==nama["user id"]:
                        kelas["student"][idnama]=(nama["username"])
                        break
            for idnama in range(len(kelas["teachers"])):
                for nama in userData2:
                    if kelas["teachers"][idnama]==nama["user id"]:
                        kelas["teachers"][idnama]=(nama["username"])
                        break
            response["message"]="Get class {} success".format(n)
            response["data"]=kelas
            return jsonify(response)
    return jsonify (response)

@apps.route('/getClass/all',methods=["GET"])
def getClassAll():
    userData = readFile(classFileLoc)
    userData2 = readFile(classworkFileLoc)

    for kelas in userData:
        for kelasid in range(len(kelas["classwork"])):
            for kelasid2 in userData2:
                if kelasid2["classworkid"]==kelas["classwork"][kelasid]["classworkid"]:
                    kelas["classwork"][kelasid]=kelasid2
    return jsonify(userData)
    
@apps.route('/class/<int:classid>',methods=["DELETE"])
def removeClass(classid):
    response={}
    response["message"]="Delete success, class {} is deleted".format(classid)
    response["data"]={}

    cekData = readFile(classFileLoc)
    
    count=0
    for cek in cekData:
        if classid==cek["classid"]:
            count+=1
    if count!=1:
        response["message"]="Delete failed, class {} is not registered".format(classid)
        return jsonify(response)

    
    #delete class di user
    userData = readFile(userFileLoc)
    userData2 = readFile(classFileLoc)

    for kelas in userData:
        for kelas2 in kelas["class"]:
            if kelas2["classid"]==classid:
                kelas["class"].remove(kelas2)                
                break
        for work in userData2:
            if work["classid"]==classid:
                for work2 in work["classwork"]:
                    for kelas3 in kelas["classwork"]:
                        if work2["classworkid"]==kelas3["classworkid"]:
                            kelas["classwork"].remove(kelas3)
    
    #delete class di classwork
    kelasData = readFile(classFileLoc)
    classWorkData = readFile(classworkFileLoc)
    for classworks in kelasData:
        if classworks["classid"]==classid:
            for classworks2 in classworks["classwork"]:
                for tugas in classWorkData:
                    if tugas["classworkid"]==classworks2["classworkid"]:
                        classWorkData.remove(tugas)

    #delete class di class
    for kelasid in kelasData:
        if kelasid["classid"]==classid:
            kelasData.remove(kelasid)

    writeFile(userFileLoc,userData)
    writeFile(classworkFileLoc,classWorkData)
    writeFile(classFileLoc,kelasData)

    response["data"]=kelasData
    return jsonify(response)

@apps.route('/removeId',methods=["GET"])
def removeId():

    userData = readFile(userFileLoc)
    
    userData.pop()
    
    writeFile(userFileLoc,userData)

    return jsonify(userData)

@apps.route('/joinClass',methods=["POST"])
def joinClass():
    body = request.json
    response={}
    response["message"]="Join class success, user id {} join class {}".format(body["user id"],body["classid"])
    response["data"]={}

    cekData = readFile(userFileLoc)
    check=0
    for cek in cekData:
        if cek["user id"]==body["user id"]:
            check+=1
    if check!=1:
        response["message"]="Join class failed, user id {} is not registered".format(body["user id"])
        return jsonify(response)


    #masukin user ke class

    userData = readFile(classFileLoc)

    count=0
    for kelas in userData:
        if body["classid"]==kelas["classid"]:
            count+=1
            if body["user id"] not in kelas["student"] and body["user id"] not in kelas["teachers"]:
                kelas["student"].append(body["user id"])
                count+=1
                break
    
    if count==2:
        pass
    elif count==1:
        response["message"]="Join class failed, user id {} already in class {}".format(body["user id"],body["classid"])
        return jsonify(response)
    else:
        response["message"]="Join class failed, class id {} is not registered".format(body["classid"])
        return jsonify(response)
    
    writeFile(classFileLoc,userData)

    #masukin class ke user

    userData = readFile(userFileLoc)
    
    for user in userData:
        if body["user id"]==user["user id"]:
            kelas={
                    "classid":body["classid"],
                    "status":"students"
                }
            kelas2={
                    "classid":body["classid"],
                    "status":"teacher"
                }
            if kelas not in user["class"] and kelas2 not in user["class"]:
                user["class"].append(kelas)
                break
                
    writeFile(userFileLoc,userData)
    
    response["data"]=user
    return jsonify(response)

@apps.route('/outclass',methods=["DELETE"])
def outclass():
    body = request.json
    response={}
    response["message"]="leave class success, user id {} left class {}".format(body["user id"],body["classid"])
    response["data"]={}

    cekData = readFile(userFileLoc)
    check=0
    for cek in cekData:
        if cek["user id"]==body["user id"]:
            check+=1
    if check!=1:
        response["message"]="Leave class failed, user id {} is not registered".format(body["user id"])
        return jsonify(response)
    #remove user dari class

    userData = readFile(classFileLoc)

    count=0
    for kelas in userData:
        if body["classid"]==kelas["classid"]:
            count+=1
            if body["user id"] in kelas["student"]:
                kelas["student"].remove(body["user id"])
                count+=1
                break
    if count==2:
        pass
    elif count==1:
        response["message"]="Leave class failed, user id {} not in class {}".format(body["user id"],body["classid"])
        return jsonify(response)
    else:
        response["message"]="Leave class failed, class id {} is not registered".format(body["classid"])
        return jsonify(response)
    
    CWData = readFile(userFileLoc)
    
    #remove classwork dari user
    userCWData = readFile(classFileLoc) 

    for userCW in userCWData:
        if body["classid"]==userCW["classid"]:
            for userCW2 in userCW["classwork"]:
                for CW in CWData:
                    if body["user id"]==CW["user id"]:
                        for CW2 in CW["classwork"]:
                            if userCW2["classworkid"]==CW2["classworkid"]:
                                CW["classwork"].remove(CW2)
    #remove class dari user
    for user in CWData:
        if body["user id"]==user["user id"]:
            kelas={
                    "classid":body["classid"],
                    "status":"students"
                }
            if kelas in user["class"]:
                user["class"].remove(kelas)
                break

    writeFile(classFileLoc,userData)
    writeFile(userFileLoc,CWData)
    
    response["data"]=user
    return jsonify(response)
#remove user id in classwork setelah outclass
@apps.route('/class/<int:classid>',methods=["POST"])
def classwork(classid):
    body = request.json

    response={}
    response["message"]="create classwork success"
    response["data"]={}

    Data=readFile(classworkFileLoc)
    tempUserId=1
    if len(Data)==0:
        tempUserId = 1
    else:
        tempUserId=Data[-1]["classworkid"]+1
    body["classworkid"]=tempUserId

    if os.path.exists (classworkFileLoc):
        userData= readFile(classworkFileLoc)
        for idtugas in userData:
            if body["classworkid"]==idtugas["classworkid"]:
                response["message"]="create classwork failed, classwork id {} already exists, try another one".format(body["classworkid"])
                return jsonify(response)
    
    #masukin tugas ke class

    userData = readFile(classFileLoc)

    check=0
    for cek in userData:
        if classid==cek["classid"]:
            check+=1
            if cek["student"]==[]:
                response["message"]="create classwork failed, no students"
                return jsonify(response)
    if check==1:
        pass
    else:
        response["message"]="create classwork failed, class id {} is not registered".format(classid)
        return jsonify(response)

    for kelas in userData:
        if classid==kelas["classid"]:
            kelas["classwork"].append(body)
    
    writeFile(classFileLoc,userData)

    #masukin tugas ke file baru
    userData=[]
    body["answers"]=[]
    if os.path.exists (classworkFileLoc):
        userData= readFile(classworkFileLoc) 

    userData.append(body)

    writeFile(classworkFileLoc,userData)

    #masukin class ke user

    userData = readFile(userFileLoc)
    
    for user in userData:
        kelas={
        "classid": classid,
        "status": "students"
        }
        if kelas in user["class"]:
            user["classwork"].append(body)
            body["status"]="unfinished"
                
    writeFile(userFileLoc,userData)

    response["data"]=body
    return jsonify(response)

@apps.route('/classwork/<int:classworkid>',methods=["POST"])
def assignClasswork(classworkid):
    body= request.json
    
    response={}
    response["message"]="assign classwork success"
    response["data"]={}

    #cek keberadaan id
    userData = readFile(userFileLoc)
    count=0
    for user in userData:
        if body["user id"] == user["user id"]:
           count+=1
    if count==1:
        pass
    else:
        response["message"]="assign classwork failed, user id {} is not registered".format(body["user id"])
        return jsonify(response)
    #sudah ada id memasukkan status ke user
    cobacek=0
    for user in userData:
        if body["user id"] == user["user id"]:
            if user["classwork"]!=[]:
                for work in user["classwork"]:
                    if classworkid==work["classworkid"]:
                        work["status"]="done"
                        cobacek+=1
                        break
            else:
                response["message"]="assign classwork failed, no classwork classwork id {}".format(classworkid)
                return jsonify(response)
               
    writeFile(userFileLoc,userData) 
    
    if cobacek==1:
        pass
    else:
        response["message"]="assign classwork failed, classwork id {} is not matched with user id {}".format(classworkid,body["user id"])
        return jsonify(response)

    #memasukkan tugas ke classwork
    userData = readFile(classworkFileLoc)

    for cek in userData:
        if cek["classworkid"]==classworkid:
            for cekid in cek["answers"]:
                if cekid["user id"]==body["user id"]:
                    response["message"]="assign classwork failed, classwork id {} already submitted".format(classworkid)
                    return jsonify(response)

    for tugas in userData:
        if tugas["classworkid"]==classworkid:
            tugas["answers"].append(body)
            break
           
    writeFile(classworkFileLoc,userData)
    
    #masukin answer ke user id
    userx = readFile(userFileLoc)
    for user in userx:
        if body["user id"] == user["user id"]:
            if user["classwork"]!=[]:
                for work in user["classwork"]:
                    if classworkid==work["classworkid"]:
                        work["answers"]=body["answer"]
                        break
               
    writeFile(userFileLoc,userx)

    response["data"]=tugas
    return jsonify(response)

@apps.route('/getClassWork/<int:n>',methods=["GET"])
def getClassWork(n):
    userData = readFile(classworkFileLoc)
    userNama = readFile(userFileLoc)

    response={}
    response["message"]="get classwork failed, no id classwork"
    response["data"]={}
    
    for tugasKelas in userData:
        if tugasKelas["classworkid"]==n:
            for userid in tugasKelas["answers"]:
                for nama in userNama:
                    if nama["user id"]==userid["user id"]:
                        userid["user id"]=nama["username"]
            response["message"]="get classwork success"
            response["data"]=tugasKelas
            return jsonify(response)
    return jsonify(response)

@apps.route('/getClassWork/all',methods=["GET"])
def getClassWorkAll():
    userData = readFile(classworkFileLoc)
    return jsonify(userData)

@apps.route('/classwork/<int:classworkid>',methods=["PUT"])
def updateClasswork(classworkid):
    body= request.json

    response={}
    response["message"]="Update classwork success"
    response["data"]={}

    cekData = readFile(classworkFileLoc)
    count=0
    for cek in cekData:
        if cek["classworkid"]==classworkid:
            count+=1
    if count!=1:
        response["message"]="Update classwork failed, classwork id {} is not registered".format(classworkid)
        return jsonify(response)

    #update in user
    userData = readFile(userFileLoc)
    for cwUser in userData:
        for cwUser2 in cwUser["classwork"]:
            if classworkid==cwUser2["classworkid"]:
                cwUser2["question"]=body["question"]
                break
    #update in class
    kelasData = readFile(classFileLoc)
    for cwKelas in kelasData:
        for cwKelas2 in cwKelas["classwork"]:
            if classworkid==cwKelas2["classworkid"]:
                cwKelas2["question"]=body["question"]
                break
    #update in classwork
    tugasData = readFile(classworkFileLoc)
    for cwTugas in tugasData:
        if classworkid==cwTugas["classworkid"]:
            cwTugas["question"]=body["question"]
            break
    
    writeFile(userFileLoc,userData)
    writeFile(classFileLoc,kelasData)
    writeFile(classworkFileLoc,tugasData)   
    
    response["data"]=tugasData
    return jsonify(response)

@apps.route('/classwork/<int:classworkid>',methods=["DELETE"])
def removeClasswork(classworkid):
    body= request.json

    response={}
    response["message"]="Remove classwork success"
    response["data"]={}

    cekData = readFile(classworkFileLoc)
    count=0
    for cek in cekData:
        if cek["classworkid"]==classworkid:
            count+=1
    if count!=1:
        response["message"]="Remove classwork failed, classwork id {} is not registered".format(classworkid)
        return jsonify(response)

    #update in user
    userData = readFile(userFileLoc)
    for cwUser in userData:
        for cwUser2 in cwUser["classwork"]:
            if classworkid==cwUser2["classworkid"]:
                cwUser["classwork"].remove(cwUser2)
                break
    #update in class
    kelasData = readFile(classFileLoc)
    for cwKelas in kelasData:
        for cwKelas2 in cwKelas["classwork"]:
            if classworkid==cwKelas2["classworkid"]:
                cwKelas["classwork"].remove(cwKelas2)
                break
    #update in classwork
    tugasData = readFile(classworkFileLoc)
    for cwTugas in tugasData:
        if classworkid==cwTugas["classworkid"]:
            tugasData.remove(cwTugas)
            break
    
    writeFile(userFileLoc,userData) 
    writeFile(classFileLoc,kelasData)
    writeFile(classworkFileLoc,tugasData)  
    
    response["data"]=tugasData
    return jsonify(response)
