from flask import Flask,jsonify, request, json
import os
apps=Flask(__name__)

@apps.route('/')
def test0():
    return "success"

@apps.route('/daftar',methods=["POST"])
def daftar():
    body= request.json
    body["class"]=[]
    body["classwork"]=[]
    
    response={}
    response["message"]="Create User Success"
    response["data"]={}

    userData=[]

    if os.path.exists ('./registrasi.json'):
        userFile= open('./registrasi.json','r')
        userData= json.load(userFile) 

    for userId in userData:
        if body["user id"]==userId["user id"] and userData!=[]:
            response["message"]="User ID {} is already exist".format(body["user id"])
            return jsonify(response)

    userData.append(body)

    userDict= open('./registrasi.json','w')
    userDict.write(json.dumps(userData))
    response["data"]=body
    return jsonify(response)

@apps.route('/daftar/<int:userid>',methods=["PUT"])
def updateUser(userid):
    body= request.json
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    for user in userData:
        if user["user id"]==userid:
            user["email"]=body["email"]
            user["fullname"]=body["fullname"]
            user["password"]=body["password"]
            user["username"]=body["username"]
   
    userDict= open('./registrasi.json','w')
    userDict.write(json.dumps(userData))
    
    return jsonify(userData)
            
@apps.route('/validasi',methods=["POST"])
def validasi():
    body=request.json
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)

    for i in userData:
        if body["username"]==i["username"] and body["password"]==i["password"]:
            return "LOGIN BERHASIL"
        else:
            pass
    return "LOGIN GAGAL, USERNAME/PASSWORD SALAH"
            
@apps.route('/getUser/<int:n>',methods=["GET"])
def getUser(n):
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    for user in userData:
        if user["user id"]==n:
            return jsonify(user)
    return "USER ID TIDAK TERDAFTAR"

@apps.route('/getUser/all',methods=["GET"])
def getUserAll():
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    return jsonify(userData)

@apps.route('/class',methods=["POST"])
def createClass():
    body= request.json
    body["student"]=[]
    body["classwork"]=[]

    response={}
    response["message"]="Create Class Success"
    response["data"]={}

    userData=[]
    
    if os.path.exists ('./kelas.json'):
        userFile= open('./kelas.json','r')
        userData= json.load(userFile) 
    
    for classId in userData:
        if body["classid"]==classId["classid"] and userData!=[]:
            response["message"]="Class ID {} is already exist".format(body["classid"])
            return jsonify(response)

    userData.append(body)

    userDict= open('./kelas.json','w')
    userDict.write(json.dumps(userData))
    
    #masukkin status ke user
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    
    for user in userData:
        if body["teachers"]==[user["user id"]]:
            kelas={
                    "classid":body["classid"],
                    "status":"teacher"
                }
            if kelas not in user["class"]:
                user["class"].append(kelas)
                
    userFile = open('./registrasi.json','w')
    userFile.write(json.dumps(userData))

    response["data"]=body
    return jsonify(response)

@apps.route('/class/<int:classid>',methods=["PUT"])
def updateClass(classid):
    body= request.json
    userFile = open('./kelas.json','r')
    userData = json.load(userFile)
    for kelas in userData:
        if kelas["classid"]==classid:
            kelas["classname"]=body["classname"]
           
    userDict= open('./kelas.json','w')
    userDict.write(json.dumps(userData))
    
    return jsonify(userData)

@apps.route('/getClass/<int:n>',methods=["GET"])
def getClass(n):
    userFile = open('./kelas.json','r')
    userData = json.load(userFile)
    for kelas in userData:
        if kelas["classid"]==n:
            for idnama in range(len(kelas["student"])):
                userFile2 = open('./registrasi.json','r')
                userData2 = json.load(userFile2)
                for nama in userData2:
                    if kelas["student"][idnama]==nama["user id"]:
                        kelas["student"][idnama]=(nama["username"])
                        break
            for idnama in range(len(kelas["teachers"])):
                userFile2 = open('./registrasi.json','r')
                userData2 = json.load(userFile2)
                for nama in userData2:
                    if kelas["teachers"][idnama]==nama["user id"]:
                        kelas["teachers"][idnama]=(nama["username"])
                        break
            return jsonify(kelas)
    return "CLASS ID TIDAK TERDAFTAR"

@apps.route('/getClass/all',methods=["GET"])
def getClassAll():
    userFile = open('./kelas.json','r')
    userData = json.load(userFile)
    for kelas in userData:
        for kelasid in kelas["classwork"]:
            userFile2 = open('./classwork.json','r')
            userData2 = json.load(userFile2)
            for kelasid2 in userData2:
                if kelasid2["classworkid"]==kelasid["classworkid"]:
                    kelas["classwork"]=kelasid2
    return jsonify(userData)
    
@apps.route('/class/<int:classid>',methods=["DELETE"])
def removeClass(classid):
    #delete class di user
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)

    for kelas in userData:
        for kelas2 in kelas["class"]:
            if kelas2["classid"]==classid:
                kelas["class"].remove(kelas2)                
                break
        for kelas3 in kelas["classwork"]:
            userFile2 = open('./kelas.json','r')
            userData2 = json.load(userFile2) 
            for work in userData2:
                if work["classid"]==classid:
                    for work2 in work["classwork"]:
                        if work2["classworkid"]==kelas3["classworkid"]:
                            kelas["classwork"].remove(kelas3)
    
    #delete class di classwork
    kelasFile = open('./kelas.json','r')
    kelasData = json.load(kelasFile)

    for classworks in kelasData:
        if classworks["classid"]==classid:
            classWorkFile = open('./classwork.json','r')
            classWorkData = json.load(classWorkFile)
            for tugas in classWorkData:
                for classworks2 in classworks["classwork"]:
                    if tugas["classworkid"]==classworks2["classworkid"]:
                        classWorkData.remove(tugas)

    #delete class di class
    for kelasid in kelasData:
        if kelasid["classid"]==classid:
            kelasData.remove(kelasid)

    user=open('./registrasi.json','w')
    classwork=open('./classwork.json','w')
    kelas=open('./kelas.json','w')
    
    user.write(json.dumps(userData))
    classwork.write(json.dumps(classWorkData))
    kelas.write(json.dumps(kelasData))
    return "BERHASIL DI HAPUS"

@apps.route('/removeId',methods=["GET"])
def removeId():
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    
    userData.pop()
    
    userFile = open('./registrasi.json','w')
    userFile.write(json.dumps(userData))

    return jsonify(userData)

@apps.route('/joinClass',methods=["POST"])
def joinClass():
    body = request.json

    #masukin user ke class

    userFile = open('./kelas.json','r')
    userData = json.load(userFile)

    for kelas in userData:
        if body["classid"]==kelas["classid"]:
            if body["user id"] not in kelas["student"] and body["user id"] not in kelas["teachers"]:
                kelas["student"].append(body["user id"])
    userFile = open('./kelas.json','w')
    userFile.write(json.dumps(userData))

    #masukin class ke user

    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    
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
                
    userFile = open('./registrasi.json','w')
    userFile.write(json.dumps(userData))

    return jsonify(userData)

@apps.route('/outclass',methods=["DELETE"])
def outclass():
    body = request.json
    
    #remove user dari class

    userFile = open('./kelas.json','r')
    userData = json.load(userFile)

    for kelas in userData:
        if body["classid"]==kelas["classid"]:
            if body["user id"] in kelas["student"]:
                kelas["student"].remove(body["user id"])
    userFile2 = open('./kelas.json','w')
    userFile2.write(json.dumps(userData))
    userFile2.close()

    CWFile = open('./registrasi.json','r')
    CWData = json.load(CWFile)
    
    #remove classwork dari user
    userCWFile = open('./kelas.json','r')
    userCWData = json.load(userCWFile) 

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

    userFile = open('./registrasi.json','w')
    userFile.write(json.dumps(CWData))
    
    return jsonify(CWData)

@apps.route('/class/<int:classid>',methods=["POST"])
def classwork(classid):
    body = request.json
    if os.path.exists ('./classwork.json'):
        userFile= open('./classwork.json','r')
        userData= json.load(userFile)
        for idtugas in userData:
            if body["classworkid"]==idtugas["classworkid"]:
                return "ID TUGAS SUDAH ADA PILIH ID LAIN"
    
    #masukin tugas ke class

    userFile = open('./kelas.json','r')
    userData = json.load(userFile)

    check=0
    for cek in userData:
        if classid==cek["classid"]:
            check+=1
            if cek["student"]==[]:
                return 'TIDAK ADA MURID'
    if check==1:
        pass
    else:
        return "CLASS ID TIDAK TERDAFTAR"


    for kelas in userData:
        if classid==kelas["classid"]:
            kelas["classwork"].append(body)
    userFile = open('./kelas.json','w')
    userFile.write(json.dumps(userData))

    #masukin class ke user

    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    
    for user in userData:
        kelas={
        "classid": classid,
        "status": "students"
        }
        if kelas in user["class"]:
            user["classwork"].append(body)
                
    userFile = open('./registrasi.json','w')
    userFile.write(json.dumps(userData))

    #masukin tugas ke file baru
    userData=[]
    body["answers"]=[]
    if os.path.exists ('./classwork.json'):
        userFile= open('./classwork.json','r')
        userData= json.load(userFile) 

    userData.append(body)

    userDict= open('./classwork.json','w')
    userDict.write(json.dumps(userData))

    return jsonify(userData)

@apps.route('/classwork/<int:classworkid>',methods=["POST"])
def assignClasswork(classworkid):
    body= request.json
    #cek keberadaan id
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    count=0
    for user in userData:
        if body["user id"] == user["user id"]:
           count+=1
    if count==1:
        pass
    else:
        return "ID TIDAK DITEMUKAN" 
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
                return "CLASSWORKID TIDAK ADA"                 
    userDict= open('./registrasi.json','w')
    userDict.write(json.dumps(userData)) 
    
    if cobacek==1:
        pass
    else:
        return "USER ID TIDAK COCOK DENGAN CLASSWORK"

    #memasukkan tugas ke classwork
    userFile = open('./classwork.json','r')
    userData = json.load(userFile)

    for cek in userData:
        if cek["classworkid"]==classworkid:
            for cekid in cek["answers"]:
                if cekid["user id"]==body["user id"]:
                    return "ASSIGNMENT SUDAH DIKUMPULKAN"

    for tugas in userData:
        if tugas["classworkid"]==classworkid:
            tugas["answers"].append(body)
           
    userDict= open('./classwork.json','w')
    userDict.write(json.dumps(userData))
    
    return jsonify(userData)

@apps.route('/getClassWork/<int:n>',methods=["GET"])
def getClassWork(n):
    userFile = open('./classwork.json','r')
    userData = json.load(userFile)
    for tugasKelas in userData:
        if tugasKelas["classworkid"]==n:
            return jsonify(tugasKelas)
    return "CLASSWORK ID TIDAK TERDAFTAR"

@apps.route('/classwork/<int:classworkid>',methods=["PUT"])
def updateClasswork(classworkid):
    body= request.json
    #update in user
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    for cwUser in userData:
        for cwUser2 in cwUser["classwork"]:
            if classworkid==cwUser2["classworkid"]:
                cwUser2["question"]=body["question"]
                break
    #update in class
    kelasFile = open('./kelas.json','r')
    kelasData = json.load(kelasFile)
    for cwKelas in kelasData:
        for cwKelas2 in cwKelas["classwork"]:
            if classworkid==cwKelas2["classworkid"]:
                cwKelas2["question"]=body["question"]
                break
    #update in classwork
    tugasFile = open('./classwork.json','r')
    tugasData = json.load(tugasFile)
    for cwTugas in tugasData:
        if classworkid==cwTugas["classworkid"]:
            cwTugas["question"]=body["question"]
            break
    user = open('./registrasi.json','w')
    kelas = open('./kelas.json','w')
    tugas = open('./classwork.json','w') 
    user.write(json.dumps(userData))
    kelas.write(json.dumps(kelasData))
    tugas.write(json.dumps(tugasData))   
    return jsonify(tugasData)

@apps.route('/classwork/<int:classworkid>',methods=["DELETE"])
def removeClasswork(classworkid):
    body= request.json
    #update in user
    userFile = open('./registrasi.json','r')
    userData = json.load(userFile)
    for cwUser in userData:
        for cwUser2 in cwUser["classwork"]:
            if classworkid==cwUser2["classworkid"]:
                cwUser["classwork"].remove(cwUser2)
                break
    #update in class
    kelasFile = open('./kelas.json','r')
    kelasData = json.load(kelasFile)
    for cwKelas in kelasData:
        for cwKelas2 in cwKelas["classwork"]:
            if classworkid==cwKelas2["classworkid"]:
                cwKelas["classwork"].remove(cwKelas2)
                break
    #update in classwork
    tugasFile = open('./classwork.json','r')
    tugasData = json.load(tugasFile)
    for cwTugas in tugasData:
        if classworkid==cwTugas["classworkid"]:
            tugasData.remove(cwTugas)
            break
    user = open('./registrasi.json','w')
    kelas = open('./kelas.json','w')
    tugas = open('./classwork.json','w') 
    user.write(json.dumps(userData))
    kelas.write(json.dumps(kelasData))
    tugas.write(json.dumps(tugasData))   
    return jsonify(userData)
