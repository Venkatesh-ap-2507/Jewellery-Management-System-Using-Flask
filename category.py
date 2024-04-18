from flask import render_template,request,redirect,url_for
import mysql.connector

def addCategory():
    if request.method=="GET":
        return render_template('addCategory.html')
    else:
        cname = request.form['cname']
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "insert into Category (cname) values (%s)"
        val = (cname,)
        cursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('showAllcategory'))


def showAllcategory():
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "select * from category"
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("showAllcategory.html", cats=cats)

def deleteCategory(id):
    if request.method == "GET":
        return render_template("deleteConfirm.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
            cursor = mydb.cursor()
            sql = "delete from category where cid = %s"
            val = (id,)
            cursor.execute(sql,val)
            mydb.commit()
        return redirect(url_for("showAllcategory"))

def editCategory(id):
    if request.method == "GET":
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "select * from category where cid=%s"
        val = (id,)
        cursor.execute(sql,val)
        cat = cursor.fetchone()
        return render_template("editCategory.html",cat=cat)
    else:
        cname = request.form["cname"]
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "update category set cname=%s where cid=%s"
        val = (cname,id)
        cursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for("showAllcategory"))
