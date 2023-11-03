import json
from flask import Flask, redirect, url_for, render_template, send_file,request, session, jsonify
from datetime import datetime ,date,timedelta
import sqlite3
app = Flask(__name__)
app.secret_key = "SecretSecret"
app.permanent_session_lifetime = timedelta(minutes=31)


@app.route('/')  
def home():
    con = sqlite3.connect("data_store.db")                   
    cur = con.cursor()
    con.execute("create table if not exists organization  (id INTEGER PRIMARY KEY AUTOINCREMENT, organizationName TEXT NOT NULL, sector TEXT NOT NULL, department TEXT NOT NULL, unit TEXT NOT NULL)")
    
    con.execute("create table if not exists knowledgDomain  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgDomainName TEXT NOT NULL, degree TEXT NOT NULL, ageRange TEXT NOT NULL, organization TEXT NOT NULL, department TEXT NOT NULL , sector TEXT NOT NULL , unit TEXT NOT NULL , jop TEXT NOT NULL , jopLevel TEXT NOT NULL , preRecuiset TEXT NOT NULL)")
    
    org = cur.execute("select DISTINCT organizationName  from organization  ;").fetchall()
    know = cur.execute("select *  from knowledgDomain  ;").fetchall()
    print(org)
    return render_template("main.html" , org=org,know=know)
    # session.pop("TA",None)
    # session.pop("stu_affairs",None)
    
    # return redirect('/')
@app.route('/genrate',methods=["POST","GET"])  
def genrate():
    if request.method == 'POST':
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists organization  (id INTEGER PRIMARY KEY AUTOINCREMENT, organizationName TEXT NOT NULL, sector TEXT NOT NULL, department TEXT NOT NULL, unit TEXT NOT NULL)")
        
        con.execute("create table if not exists knowledgDomain  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgDomainName TEXT NOT NULL, degree TEXT NOT NULL, ageRange TEXT NOT NULL, organization TEXT NOT NULL, department TEXT NOT NULL , sector TEXT NOT NULL , unit TEXT NOT NULL , jop TEXT NOT NULL , jopLevel TEXT NOT NULL , preRecuiset TEXT NOT NULL)")
        
        org = cur.execute("select DISTINCT organizationName  from organization  ;").fetchall()
        know = cur.execute("select *  from knowledgDomain  ;").fetchall()
        print(org)
        degree=request.form['degree']
        ageStart=int(request.form['start']) 
        end = int(request.form['end'])
        organization=request.form['organization']
        department=request.form['department']
        sector=request.form['sector']
        unit=request.form['unit']
        jop=request.form['jopName']
        jopLevel=request.form['jopLevel']
        preRecuiset=request.form['prerequisite']
        knowledgDomain = []
        for k in know:   
            if (organization in k[4] or 'any'in k[4]) and (degree in k[2] or 'any'in k[2]) and (department in k[5] or 'any'in k[5]) and (sector in k[6] or 'any'in k[6]) and (unit in k[7] or 'any'in k[7])  and (jop in k[8] or 'any'in k[8]) and (jopLevel in k[9] or 'any'in k[9]) and ( ageStart>= int(k[3].split('->')[0]) and end <= int(k[3].split('->')[1]) ) and ((set(preRecuiset.split('-')).issubset(set(k[10].split('-')))) or 'any'in k[10]):
                knowledgDomain.append(k[1]) 
        print(knowledgDomain)
        data = []
        for k in knowledgDomain:
             
            datasersch  = cur.execute("select *  from subjects where knowledg = ? ;" ,[str(k)]).fetchall()
            if datasersch:
                data = data + (datasersch)
        print((data))   
        return render_template("main.html" , org=org,know=know ,data=data )

@app.route('/genrate/getData',methods=["POST","GET"])  
def genrateGetData():
    if request.method == 'POST':
        # cour=request.data.decode("utf-8")
        organizatin = request.data
        organizatin=json.loads(organizatin)
        
        conn = sqlite3.connect("data_store.db")
        c = conn.cursor()
        org = c.execute("select *  from subjects where knowledg = ? ;",([organizatin['knowledg']])).fetchall()
        conn.commit()
        c.close()
        conn.close()
        print(org)

        return jsonify(org)


@app.route('/view')  
def view():
    con = sqlite3.connect("data_store.db")                   
    cur = con.cursor()
    con = sqlite3.connect("data_store.db")                   
    cur = con.cursor()
    con.execute("create table if not exists knowledgDomain  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgDomainName TEXT NOT NULL, degree TEXT NOT NULL, ageRange TEXT NOT NULL, organization TEXT NOT NULL, department TEXT NOT NULL , sector TEXT NOT NULL , unit TEXT NOT NULL , jop TEXT NOT NULL , jopLevel TEXT NOT NULL , preRecuiset TEXT NOT NULL)")
    know = cur.execute("select *  from knowledgDomain  ;").fetchall()  
    con.execute("create table if not exists subjects  (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT NOT NULL, knowledg TEXT NOT NULL, study TEXT NOT NULL, startend TEXT NOT NULL, degree TEXT NOT NULL , joblevel TEXT NOT NULL , courseHoure TEXT NOT NULL , prerequisite TEXT NOT NULL)")
    sub = cur.execute("select *  from subjects  ;").fetchall()
    print(sub)

    return render_template("viewStore.html", sub=sub,know=know )   
    
    
    
@app.route('/setting',methods=["POST","GET"])  
def setting():
    if request.method == 'GET':
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists organization  (id INTEGER PRIMARY KEY AUTOINCREMENT, organizationName TEXT NOT NULL, sector TEXT NOT NULL, department TEXT NOT NULL, unit TEXT NOT NULL)")
        
        con.execute("create table if not exists knowledgDomain  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgDomainName TEXT NOT NULL, degree TEXT NOT NULL, ageRange TEXT NOT NULL, organization TEXT NOT NULL, department TEXT NOT NULL , sector TEXT NOT NULL , unit TEXT NOT NULL , jop TEXT NOT NULL , jopLevel TEXT NOT NULL , preRecuiset TEXT NOT NULL)")
        
        org = cur.execute("select DISTINCT organizationName  from organization  ;").fetchall()
        know = cur.execute("select *  from knowledgDomain  ;").fetchall()
        print(org)
        
        return render_template("setting.html", org=org,know=know )
    elif request.method == 'POST':
        print(request.form)
        knowledgDomainName=request.form['knowledgeName']
        degree=request.form['degree']
        ageRange=str(request.form['start']) +'->' +str(request.form['end'])
        organization=request.form['organization']
        department=request.form['department']
        sector=request.form['sector']
        unit=request.form['unit']
        jop=request.form['jopName']
        jopLevel=request.form['jopLevel']
        preRecuiset=request.form['prerequisite']
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists knowledgDomain  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgDomainName TEXT NOT NULL, degree TEXT NOT NULL, ageRange TEXT NOT NULL, organization TEXT NOT NULL, department TEXT NOT NULL , sector TEXT NOT NULL , unit TEXT NOT NULL , jop TEXT NOT NULL , jopLevel TEXT NOT NULL , preRecuiset TEXT NOT NULL)")
        with sqlite3.connect("data_store.db") as con:  
            cur = con.cursor()  
            cur.execute("INSERT into knowledgDomain (knowledgDomainName,degree,ageRange,organization,department,sector,unit,jop,jopLevel,preRecuiset) values (?,?,?,?,?,?,?,?,?,?)",
                        (knowledgDomainName,degree,ageRange,organization,department,sector,unit,jop,jopLevel,preRecuiset))  
            
        con.commit()
        return  redirect('/setting') 
@app.route('/knowledgDomain/delete/<x>')  
def knowledgDomainDelete(x):
    print(x)
    database = sqlite3.connect("data_store.db")
    cursor = database.cursor()
    cursor.execute("DELETE FROM knowledgDomain WHERE id = ?", [str(x)])
    database.commit()
    cursor.close()
    database.close()
    return  redirect('/setting')     
@app.route('/knowledgDomain/edit/<x>',methods=["POST","GET"])  
def knowledgDomainEdit(x):
    
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists knowledgDomain  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgDomainName TEXT NOT NULL, degree TEXT NOT NULL, ageRange TEXT NOT NULL, organization TEXT NOT NULL, department TEXT NOT NULL , sector TEXT NOT NULL , unit TEXT NOT NULL , jop TEXT NOT NULL , jopLevel TEXT NOT NULL , preRecuiset TEXT NOT NULL)")
        
        know = cur.execute("select *  from knowledgDomain where id = ? ;" ,[str(x)]).fetchall()
        org = cur.execute("select DISTINCT organizationName  from organization  ;").fetchall()
        print(know)
        return render_template("editKnowlgeDomain.html" , know=know[0],org=org  ) 


@app.route('/knowledgDomain/editSave',methods=["POST","GET"])  
def knowledgDomainSave():
    if request.method == 'POST':
        knowledgDomainName=request.form['knowledgeName']
        degree=request.form['degree']
        ageRange=str(request.form['start']) +'->' +str(request.form['end'])
        organization=request.form['organization']
        department=request.form['department']
        sector=request.form['sector']
        unit=request.form['unit']
        jop=request.form['jopName']
        jopLevel=request.form['jopLevel']
        preRecuiset=request.form['prerequisite']
        code = request.form['code']
        conn = sqlite3.connect("data_store.db")
        c = conn.cursor()
        sql = "UPDATE knowledgDomain SET knowledgDomainName= ? ,degree = ?,ageRange = ?,organization = ? ,department = ?,sector = ?,unit = ?,jop = ?,jopLevel = ?,preRecuiset = ? WHERE id = ?"
        c.execute(sql, (knowledgDomainName,degree,ageRange,organization,department,sector,unit,jop,jopLevel,preRecuiset,int(code)))
        conn.commit()
        c.close()
        conn.close()

        return redirect('/setting')




        
@app.route('/subject',methods=["POST","GET"])  
def subject():
    if request.method == 'GET':
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists knowledgDomain  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgDomainName TEXT NOT NULL, degree TEXT NOT NULL, ageRange TEXT NOT NULL, organization TEXT NOT NULL, department TEXT NOT NULL , sector TEXT NOT NULL , unit TEXT NOT NULL , jop TEXT NOT NULL , jopLevel TEXT NOT NULL , preRecuiset TEXT NOT NULL)")
        know = cur.execute("select *  from knowledgDomain  ;").fetchall()  
        con.execute("create table if not exists subjects  (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT NOT NULL, knowledg TEXT NOT NULL, study TEXT NOT NULL, startend TEXT NOT NULL, degree TEXT NOT NULL , joblevel TEXT NOT NULL , courseHoure TEXT NOT NULL , prerequisite TEXT NOT NULL)")
        sub = cur.execute("select *  from subjects  ;").fetchall()
        print(sub)
        return render_template("subject.html",know=know,sub=sub ) 
    if request.method == 'POST':
        
        subject =request.form['subject']
        knowledg = request.form['knowledg']
        study = request.form['study']
        startend = str(request.form['start'])+"->"+str(request.form['end'])
        degree = request.form['degree']
        joblevel = request.form['joblevel']
        courseHoure =  request.form['courseHoure']
        prerequisite = request.form['prerequisite']
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists subjects  (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT NOT NULL, knowledg TEXT NOT NULL, study TEXT NOT NULL, startend TEXT NOT NULL, degree TEXT NOT NULL , joblevel TEXT NOT NULL , courseHoure TEXT NOT NULL , prerequisite TEXT NOT NULL)")
        with sqlite3.connect("data_store.db") as con:  
            cur = con.cursor()  
            cur.execute("INSERT into subjects (subject,knowledg,study,startend,degree,joblevel,courseHoure,prerequisite) values (?,?,?,?,?,?,?,?)",
                        (subject,knowledg,study,startend,degree,joblevel,courseHoure,prerequisite))  
            
        con.commit()
        
        
        return redirect('/subject')

@app.route('/organization/delete/<x>')  
def organizationDel(x):
    print(x)
    database = sqlite3.connect("data_store.db")
    cursor = database.cursor()
    cursor.execute("DELETE FROM organization WHERE id = ?", [str(x)])
    database.commit()
    cursor.close()
    database.close()
    return  redirect('/organization') 
@app.route('/subject/delete/<x>')  
def subjectDel(x):
    print(x)
    database = sqlite3.connect("data_store.db")
    cursor = database.cursor()
    cursor.execute("DELETE FROM subjects WHERE id = ?", [str(x)])
    database.commit()
    cursor.close()
    database.close()
    return  redirect('/subject') 
@app.route('/subject/edit/<x>')  
def subjectEdit(x):
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists subjects  (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT NOT NULL, knowledg TEXT NOT NULL, study TEXT NOT NULL, startend TEXT NOT NULL, degree TEXT NOT NULL , joblevel TEXT NOT NULL , courseHoure TEXT NOT NULL , prerequisite TEXT NOT NULL)")
        sub = cur.execute("select *  from subjects where id = ? ;" ,[str(x)]).fetchall()
        print(sub)
        know = cur.execute("select *  from knowledgDomain  ;").fetchall()
        return render_template("editSubject.html" , sub=sub[0],know=know  )
@app.route('/organization/edit/<x>')  
def organizationEdit(x):
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists organization  (id INTEGER PRIMARY KEY AUTOINCREMENT, organizationName TEXT NOT NULL, sector TEXT NOT NULL, department TEXT NOT NULL, unit TEXT NOT NULL)")
        
        org = cur.execute("select *  from organization where id = ? ;" ,[str(x)]).fetchall()
        print(org)
        return render_template("editOrg.html" , org=org[0]  )
    # if request.method == 'POST':
        
    #     return redirect('/organization')
    

@app.route('/subject/editSave',methods=["POST","GET"])  
def subjectSave():
    if request.method == 'POST':
        code =request.form['code']
        subject =request.form['subject']
        knowledg = request.form['knowledg']
        study = request.form['study']
        startend = str(request.form['start'])+"->"+str(request.form['end'])
        degree = request.form['degree']
        joblevel = request.form['joblevel']
        courseHoure =  request.form['courseHoure']
        prerequisite = request.form['prerequisite']
        
        conn = sqlite3.connect("data_store.db")
        c = conn.cursor()
        sql = "UPDATE subjects SET subject  = ?,knowledg = ?,study = ?,startend = ?,degree = ?,joblevel = ?,courseHoure = ?,prerequisite = ? WHERE id = ?"
        c.execute(sql, (subject,knowledg,study,startend,degree,joblevel,courseHoure,prerequisite,int(code)))
        conn.commit()
        c.close()
        conn.close()

        return redirect('/subject') 




@app.route('/organization/editSave',methods=["POST","GET"])  
def organizationSave():
    if request.method == 'POST':
        organizatin = request.form['organizatin']
        department = request.form['department']
        sector = request.form['sector']
        unit = request.form['unit']
        code = request.form['code']
        
        conn = sqlite3.connect("data_store.db")
        c = conn.cursor()
        sql = "UPDATE organization SET organizationName = ?, sector = ?,department = ?,unit = ? WHERE id = ?"
        c.execute(sql, (organizatin,sector,department,unit,int(code)))
        conn.commit()
        c.close()
        conn.close()

        return redirect('/organization')
           



@app.route('/organization/getData',methods=["POST","GET"])  
def organizationGetData():
    if request.method == 'POST':
        # cour=request.data.decode("utf-8")
        organizatin = request.data
        organizatin=json.loads(organizatin)
        
        conn = sqlite3.connect("data_store.db")
        c = conn.cursor()
        org = c.execute("select *  from organization where organizationName = ? ;",([organizatin['cours']])).fetchall()
        conn.commit()
        c.close()
        conn.close()
        print(org)

        return jsonify(org)



    

@app.route('/organization',methods=["POST","GET"])  
def organization():
    if request.method == 'GET':
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists organization  (id INTEGER PRIMARY KEY AUTOINCREMENT, organizationName TEXT NOT NULL, sector TEXT NOT NULL, department TEXT NOT NULL, unit TEXT NOT NULL)")
        
        org = cur.execute("select  *  from organization  ;").fetchall()
        
        return render_template("organization.html" , org=org  ) 
    elif request.method == 'POST':
        
        
        organizatin = request.form['organizatin']
        department = request.form['department']
        sector = request.form['sector']
        unit = request.form['unit']
        
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists organization  (id INTEGER PRIMARY KEY AUTOINCREMENT, organizationName TEXT NOT NULL, sector TEXT NOT NULL, department TEXT NOT NULL, unit TEXT NOT NULL)")
        with sqlite3.connect("data_store.db") as con:  
            cur = con.cursor()  
            cur.execute("INSERT into organization (organizationName,sector,department,unit) values (?,?,?,?)",(organizatin,sector,department,unit))  
            con.commit()
        return redirect('/organization')
        
if __name__ == '__main__':
    app.run(debug= True)
    