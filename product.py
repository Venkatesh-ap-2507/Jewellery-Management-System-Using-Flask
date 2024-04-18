import mysql.connector
from flask import render_template,request,redirect,url_for
from werkzeug.utils import secure_filename

def addProduct():
    if request.method == "GET":
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "SELECT * FROM category"
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("addproduct.html", cats=cats)
    else:
        pname = request.form["pname"]
        price = request.form["price"]
        description = request.form["description"]
        f = request.files['image_url']
        filename = secure_filename(f.filename)
        filename = "static/productimages/" +f.filename
        f.save(filename)
        filename = "productimages/"+f.filename
        cat_id = request.form["cat"]
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "insert into product (product_name,price,description,image_url,cid) values (%s,%s,%s,%s,%s)"
        val = (pname,price,description,filename,cat_id)
        cursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for("showAllproduct"))

def showAllproduct():
    mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
    cursor = mydb.cursor()
    sql = '''SELECT p.product_id, p.product_name, p.price, p.description, p.image_url, c.cname 
                FROM product AS p 
                INNER JOIN category AS c 
                ON p.cid = c.cid;
                '''
    cursor.execute(sql)
    product = cursor.fetchall()
    return render_template("showAllproduct.html", products=product)

def deleteproduct(product_id):
    if request.method == "GET":
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "select * from product where product_id = %s"
        val = (product_id,)
        cursor.execute(sql,val)
        product = cursor.fetchone()
        return render_template("deleteproduct.html", product=product)
    else:
        action = request.form["action"]
        if action == "Yes":
            mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
            cursor = mydb.cursor()
            sql = "delete from product where product_id = %s"
            val = (product_id,)
            cursor.execute(sql,val)
            mydb.commit()
        return redirect(url_for('showAllproduct'))


def editproduct(product_id):
    if request.method == "GET":
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "select * from product where product_id = %s"
        val = (product_id,)
        cursor.execute(sql,val)
        product = cursor.fetchone()

        sql = "SELECT * FROM category"
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("editproduct.html", product=product, cats=cats)
    else:
        pname = request.form["pname"]
        price = request.form["price"]
        description = request.form["description"]
        f = request.files['image_url']
        filename = secure_filename(f.filename)
        filename = "static/productimages/" +f.filename
        f.save(filename)
        filename = "productimages/"+f.filename
        cat_id = request.form["cat"]

        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "update product set product_name=%s, price=%s, description=%s, image_url=%s, cid=%s where product_id=%s"
        val = (pname,price,description,filename,cat_id,product_id)
        cursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for("showAllproduct"))