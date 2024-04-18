import mysql.connector
from flask import render_template, request, redirect, url_for, session

def login():
    if request.method=="GET":
        return render_template("adminLogin.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        # Connect to the database
        sql = '''SELECT count(*) FROM admin WHERE username=%s AND password=%s'''
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        val = (uname, pwd)
        cursor.execute(sql,val)
        result=cursor.fetchone()
        if int(result[0])==1 :
            session['uname'] = uname
            mydb.commit()
            return redirect("/adminHome")
        else:
            return redirect(url_for('login'))
        
def adminHome():
    if 'uname' in session:
        return render_template('adminHome.html')
    else:
        return redirect(url_for("login"))

def Logout():
    session.clear()
    return redirect('/')