import os
from urllib import request

from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename

import ar_master

app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
user='root'
password=''
host='localhost'
database='ration_shop'
mm = ar_master.master_flask_code()
@app.route("/")
def homepage():
    return render_template('index.html')
@app.route("/admin")
def admin():
    return render_template('admin.html')
@app.route("/admin_log", methods = ['GET', 'POST'])
def admin_log():
    error = None
    if request.method == 'POST':
        un=request.form['uname']
        pa=request.form['pass']
        print(un)
        print(pa)
        pa=pa.strip()
        un=un.strip()
        if un == "admin" and pa == "admin":

            return render_template('adminhome.html',error=error)
        else:
            return render_template('admin_log.html', error=error)
@app.route("/adminhome")
def adminhome():
            return render_template('adminhome.html')
@app.route("/add_product", methods = ['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        productname = request.form['productname']
        brand = request.form['brand']
        price = request.form['price']
        quantity=request.form['quantity']
        f = request.files['file']
        f.save(os.path.join("static/uploads/", secure_filename(f.filename)))

        maxin=mm.find_max_id("product_details")
        qry=("insert into product_details values('" + str(maxin) + "','" + str(productname) + "','" + str(
            brand) + "','" + str(price) + "','" + str(quantity) + "','" + str(f.filename) + "')")
        result=mm.insert_query(qry)
        print(result)
        return render_template('add_product.html',flash_message=True,data="Success")
    return render_template('add_product.html')
@app.route("/add_user", methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        gender = request.form['gender']
        username = request.form['username']
        password = request.form['password']
        maxin = mm.find_max_id("user_details")
        qry = ("insert into user_details values('" + str(maxin) + "','" + str(name) + "','" + str(
            contact) + "','" + str(email) + "','" + str(address) + "','" + str(gender) + "','" + str(username) + "','" + str(password) + "')")
        result = mm.insert_query(qry)
        print(result)
        return render_template('user.html',flash_message=True,data="Success")
    return render_template('add_user.html')

@app.route("/view_user")
def view_user():
    data = mm.select_direct_query("select name,contact,email,address,gender,username from user_details")
    return render_template('view_user.html',items=data)

@app.route("/user",methods = ['GET', 'POST'])
def user():
    msg=None
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['pass']

        n1=str(n)
        g1=str(g)

        q=("SELECT * from user_details where username='" + str(n1) + "' and password='" + str(g1) + "'")
        data=mm.select_direct_query(q)
        data=len(data)
        if data==0:
            return render_template('user.html',flash_message=True,data="Failed")
        else:
            msg='Success'
            session['user'] =n
            return render_template('user_home.html',sid=n)
    return render_template('user.html',error=msg)




@app.route("/user_home")
def user_home():
            return render_template('user_home.html')

@app.route("/search",methods = ['GET', 'POST'])
def search():
   if request.method=='POST':
     searchbar = request.form['searchbar']
     qry = "select id,productname,brand,price,quantity,file from product_details where productname= '" + str(searchbar) + "'"
     data = mm.select_direct_query(qry)
     return render_template('search.html', items=data)
   return render_template('search.html')
@app.route("/buy_page/<id>",methods = ['GET', 'POST'])
def buy_page(id):
      data = mm.select_direct_query("select * from product_details where  id='" + str(id) + "'")
      session['id'] = id
      return render_template('buy_page.html',items=data)

@app.route("/buy_details")
def buy_details():
    data = mm.select_direct_query("select amount,holdername,accno,cvv,username from account_details")
    return render_template('buy_details.html',items=data)
@app.route("/buy_1",methods = ['GET', 'POST'])
def buy_1():
    n=session['user']
    id=session['id']
    if request.method == 'POST':
        contact = mm.select_direct_query("select contact from user_details where username='" + str(n) + "'")
        contact1=contact[0][0]

        print(contact1)
        email = mm.select_direct_query("select email from user_details where username='" + str(n) + "'")
        email1 = email[0][0]
        address = mm.select_direct_query("select address from user_details where username='" + str(n) + "'")
        address1 = address[0][0]
        gender = mm.select_direct_query("select gender from user_details where username='" + str(n) + "'")
        gender1 = gender[0][0]
        pr = mm.select_direct_query("select quantity from product_details where id='" + str(id) + "'")
        qu=pr[0][0]
        a=int(qu)-1
        pname = mm.select_direct_query("select productname from product_details where id='" + str(id) + "'")
        prname = pname[0][0]
        d=mm.insert_query("update product_details set quantity='" + str(a) + "' where id='" + str(id) + "'")
        print(d)
        amount = request.form['amount']
        cvv = request.form['cvv']
        name = request.form['name']
        accno = request.form['accno']
        maxin = mm.find_max_id("account_details")
        qry = ("insert into account_details values('" + str(maxin) + "','" + str(amount) + "','" + str(
            cvv) + "','" + str(
            name) + "','" + str(accno) + "','" + str(n) + "','" + str(contact1) + "','" + str(email1) + "','" + str(address1) + "','" + str(gender1) + "','" + str(prname) + "')")
        result = mm.insert_query(qry)
        print(result)
        return render_template('search.html', flash_message=True, data="Success")

    return render_template('user.html')
@app.route("/stock")
def stock():
    data = mm.select_direct_query("select productname,brand,price,quantity,file from product_details")

    return render_template('stock.html',items=data)
@app.route("/admin_buy_details")
def admin_buy_details():
    data = mm.select_direct_query("select productname,amount,username,holdername,email,contact from account_details")
    return render_template('admin_buy_details.html', items=data)

@app.route("/contact")
def contact():
      return render_template('contact.html')
#####################################
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)