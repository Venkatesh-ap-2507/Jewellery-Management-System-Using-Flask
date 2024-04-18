import mysql.connector
from flask import render_template, request, redirect, url_for,session,make_response
from werkzeug.utils import secure_filename
from datetime import datetime

def homepage():
    mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="jewelleryflaskdb")
    cursor = mydb.cursor()
    sql = '''SELECT product_id,product_name,price,description, image_url,cname 
                FROM product AS p
                INNER JOIN category AS cat
                ON p.cid = cat.cid;
                '''
    cursor.execute(sql)
    product = cursor.fetchall()
    sql1 = "select * from category"
    cursor.execute(sql1)
    cats = cursor.fetchall()
    return render_template('homepage.html',product=product,cats=cats)

def showproduct(product_id):
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="jewelleryflaskdb")
    cursor = mydb.cursor()
    sql = '''SELECT * FROM product_vw WHERE cat_id=%s'''  # Using correct column name `cat_id`
    val = (product_id,)
    cursor.execute(sql, val)
    product = cursor.fetchall() 
    sql1 = "SELECT * FROM category"
    cursor.execute(sql1)
    cats = cursor.fetchall()
    return render_template("homepage.html", product=product, cats=cats)

def Login():
    if request.method == "GET":
        if "message" in request.cookies:
            message = request.cookies.get("message")
        else:
            message = None
        return render_template("Login.html",message=message)
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        sql = '''select count(*) from  user where username=%s and password=%s'''
        mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="jewelleryflaskdb")
        cursor = mydb.cursor()
        val = (uname,pwd)
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if int(count[0]) == 1:
            session["uname"] = uname
            return redirect('/')
        else:
            return redirect(url_for('Login'))

def Register():
    if request.method == "GET":
        return render_template("Register.html")
    else:
        uname = request.form['uname']
        pwd = request.form['pwd']
        email = request.form['email']
        mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = '''insert into user(username,password,email_id) values(%s,%s,%s)'''
        val = (uname,pwd,email)
        try:
            cursor.execute(sql,val)
        except:
            message = "User Already Exists Please select Different Username"
            return render_template("Register.html",message=message)
        else:
            mydb.commit()
        
        return redirect('/Login')

def Logout():
    session.clear()
    return redirect('/')

def ViewDetails(product_id):
    if request.method == "GET":
        mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = 'SELECT * FROM product_vw where product_id = %s'
        val = (product_id,)
        cursor.execute(sql,val)
        product = cursor.fetchone()
        return render_template( 'ViewDetails.html', product = product )
    else:
        mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="jewelleryflaskdb")
        cursor = mydb.cursor()
        uname = session["uname"]
        qty = request.form["qty"]
        if "uname" in session:
            sql = "select count(*) from mycart where username=%s and product_id=%s"
            val = (session["uname"],product_id)
            cursor.execute(sql,val)
            count = cursor.fetchone()
            if(int(count[0])==1):
                message = "Item already in cart"
            else:
                sql = "insert into mycart (username,product_id,qty) values(%s,%s,%s)"
                val = (uname,product_id,qty)
                cursor.execute(sql,val)
                mydb.commit()
                message = "Item add to cart Successfully"
            return redirect(url_for("showCartItems",message=message))
        else:
            return redirect("/Login")

def showCartItems():
    if request.method == "GET":
        if "uname" in session :
            if "message" in request.args:
                message = request.args["message"]
            else:
                message=""
            uname = session["uname"]
            sql = "select * from Cart_vw where username=%s and order_id is NULL"
            val = (uname,)
            mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="jewelleryflaskdb")
            cursor = mydb.cursor()
            cursor.execute(sql,val)
            items = cursor.fetchall()

            sql = "select sum(Sub_Total) from cart_vw where username=%s and order_id is NULL"
            val = (session["uname"],)
            cursor.execute(sql,val)
            total = cursor.fetchone()[0]
            print(total)
            session["total"] = total


            return render_template('ShowCart.html',items=items,message=message)
        else:
            return redirect("/Login")
    else:
        action = request.form["action"]
        mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="jewelleryflaskdb")
        cursor = mydb.cursor() 
        if action == "update":
            qty = request.form["qty"]
            sql = "update mycart set qty=%s where username=%s and product_id=%s"
            val = (qty,session["uname"],request.form["product_id"])
            cursor.execute(sql,val)
            mydb.commit()
        else:
             sql = "delete from mycart where username=%s and product_id = %s"
             val = (session["uname"],request.form["product_id"])
             cursor.execute(sql,val)
             mydb.commit()
        return redirect('/ShowCart')

def MakePayment():
    if request.method == "GET":
        return render_template("MakePayment.html")
    else:
        cardno = request.form["cardno"]
        cvv = request.form["cvv"]
        expiry = request.form["expiry"]
        mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="jewelleryflaskdb")
        cursor = mydb.cursor()
        sql = "select count(*) from payment where cardno=%s and cvv=%s and expiry=%s"
        val = (cardno,cvv,expiry)
        cursor.execute(sql,val)
        count = int(cursor.fetchone()[0])
        if count == 1:
            total = session["total"]
            #Perform transaction
            sql1 = "update payment set balance = balance - %s where cardno=%s and cvv=%s and expiry=%s"
            val1 = (total,cardno,cvv,expiry)
            sql2 = "update payment set balance = balance + %s where cardno=%s and cvv=%s and expiry=%s"
            val2 = (total,'2222','222','2030-12-01')
            cursor.execute(sql1,val1)
            cursor.execute(sql2,val2)
            mydb.commit()

            dd = datetime.today().strftime('%Y-%m-%d')
            sql3 = "insert into order_master (username,date_of_order,amount) values (%s,%s,%s)"
            val3 = (session["uname"],dd,total)
            cursor.execute(sql3,val3)
            mydb.commit()
            
            print("Done till ordermaster")
            sql4 = "select id from order_master where username=%s and date_of_order=%s and amount=%s limit 1"
            val4 = (session["uname"],dd,total)
            print(val4)
            cursor.execute(sql4,val4)
            oid = cursor.fetchone()[0]
            
            sql5 = "update mycart set order_id = %s where username=%s and order_id is null"
            val5 = (oid,session["uname"])
            cursor.execute(sql5,val5)
            mydb.commit()
            return redirect("/")
        else:
            return redirect(url_for("MakePayment"))


def my_orders():
    if request.method == "GET":
        if "uname" in session:
            if "message" in request.args:
                message = request.args['message']
            else:
                message = ""
            uname = session["uname"]
            mydb = mysql.connector.connect(
                host="localhost", user="root", password="root", database="jewelleryflaskdb")
            cursor = mydb.cursor()

            sql = "SELECT * FROM order_master WHERE username = %s"
            val = (uname,)
            cursor.execute(sql, val)
            order_ids = cursor.fetchall()

            orders = []
            for o_id in order_ids:
                sql = """SELECT m.order_id, m.username, m.id, p.product_name, p.price, p.image_url, m.qty, o.date_of_order, p.price * m.qty AS subtotal
                    FROM product p
                    INNER JOIN mycart m ON p.product_id = m.product_id
                    INNER JOIN order_master o ON m.order_id = o.id
                    WHERE m.order_id = %s;
                    """
                val = (o_id[0],)
                cursor.execute(sql, val)
                orders += cursor.fetchall()

            cursor.close()
            mydb.close()

            return render_template("myorder.html", orders=orders, message=message)
        else:
            return redirect('/Login')


def about_us():
    return render_template('about.html')


def contact_us():
    return render_template('contact.html')


def addToWishlist(product_id):
    if request.method == "GET":
        if "uname" in session:
            uname = session["uname"]
            mydb = mysql.connector.connect(
                host="localhost", user="root", password="root", database="jewelleryflaskdb")
            cursor = mydb.cursor()
            sql = "INSERT INTO wishlist (username, product_id) VALUES (%s, %s)"
            val = (uname, product_id)
            cursor.execute(sql, val)
            mydb.commit()
            return redirect("/showproduct/{}".format(product_id))
        else:
            return redirect("/Login")


def viewWishlist():
    if request.method == "GET":
        if "uname" in session:
            uname = session["uname"]
            mydb = mysql.connector.connect(
                host="localhost", user="root", password="root", database="jewelleryflaskdb")
            cursor = mydb.cursor()
            sql = "SELECT p.product_id, p.product_name, p.price, p.description, p.image_url, c.cname FROM product p INNER JOIN category c ON p.cid = c.cid WHERE p.product_id IN (SELECT product_id FROM wishlist WHERE username = %s)"
            val = (uname,)
            cursor.execute(sql, val)
            wishlist_items = cursor.fetchall()
            print("Wishlist Items:", wishlist_items)  # Debugging statement
            return render_template("wishlist.html", wishlist=wishlist_items)
        else:
            return redirect("/Login")



