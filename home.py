import os
from datetime import timedelta, datetime
from werkzeug.utils import secure_filename
from datetime import date
import ar_master
from flask import Flask, render_template, flash, request, session, current_app, send_from_directory, redirect
import os
from datetime import timedelta, date
from io import BytesIO
from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, session, send_file, redirect
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import ar_master

import os
from datetime import timedelta, date
from io import BytesIO
from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, session, send_file, redirect
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pymysql
import ar_master

import os
from datetime import date
from io import BytesIO
from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, session, send_file, redirect
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import pymysql
import ar_master
import io

app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
mm = ar_master.master_flask_code()


app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
mm = ar_master.master_flask_code()


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/user_home")
def user_home():
    return render_template('user_home.html')

@app.route("/admin_home")
def admin_home():
    return render_template('admin_home.html')
@app.route("/owner_home")
def owner_home():
    return render_template('owner_home.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    error = ("invalid user")

    if request.method == 'POST':
        un = request.form['uname']
        pa = request.form['pass']
        print(un)
        print(pa)
        pa = pa.strip()
        un = un.strip()
        if un == "admin" and pa == "admin":
            return render_template('admin_home.html', error=error)
        else:
            return render_template('admin.html', error=error)
    return render_template('admin.html')




@app.route("/user", methods=['GET', 'POST'])
def user():
    error = ("invalid user")
    if request.method == 'POST':
        un = request.form['uname']
        pa = request.form['pass']
        usern = mm.select_direct_query(
            "select username from user_details where username='" + str(un) + "' and password='" + str(pa) + "'")


        if usern:
            today = date.today()
            today=str(today)
            session['username'] = usern
            usern=usern[0][0]
            datax = mm.select_direct_query("select * from user_details where username='" + str(usern) + "'")
            user_name = datax[0][1]
            try:

                data = mm.select_direct_query("select id,end_date from rental_request where user_name='" + str(user_name) + "'")


                for da in data:
                    id=da[0]
                    enddate=da[1]
                    x = enddate.split("-")
                    year=int(x[0])
                    month=int(x[1])
                    day=int(x[2])
                    y=today.split("-")
                    year1=int(y[0])
                    month1=int(y[1])
                    day1=int(y[2])

                    f_date = date(year1, month1, day1)
                    l_date = date(year, month, day)
                    print(f_date,l_date)

                    delta =    f_date-l_date
                    print(delta)
                    fine_amount=delta.days*1000
                    print(fine_amount)
                    qq="update rental_request set fine_amount='" + str(fine_amount) + "' where id='" + str(id) + "'"
                    print(qq)
                    d = mm.insert_query(qq)
                return render_template('user_home.html', error=error)
            except:

                return render_template('user_home.html', error=error)
        else:
            return render_template('user.html', error=error)
    return render_template('user.html')

@app.route("/user_register", methods = ['GET', 'POST'])
def user_register():
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
    return render_template('user_register.html')

@app.route("/owner", methods=['GET', 'POST'])
def owner():
    error = None
    if request.method == 'POST':
        un = request.form['uname']
        pa = request.form['pass']
        usern = mm.select_direct_query(
            "select username from owner_details where username='" + str(un) + "' and password='" + str(pa) + "'")
        print(usern)

        if usern:
            session['username'] = usern
            return render_template('owner_home.html', error=error)
        else:
            return render_template('owner.html', error=error)
    return render_template('owner.html')
@app.route("/owner_register", methods = ['GET', 'POST'])
def owner_register():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        gender = request.form['gender']
        username = request.form['username']
        password = request.form['password']
        maxin = mm.find_max_id("owner_details")
        qry = ("insert into owner_details values('" + str(maxin) + "','" + str(name) + "','" + str(
            contact) + "','" + str(email) + "','" + str(address) + "','" + str(gender) + "','" + str(username) + "','" + str(password) + "')")
        result = mm.insert_query(qry)
        print(result)
        return render_template('owner.html',flash_message=True,data="Success")
    return render_template('owner_register.html')


@app.route("/owner_add_machine", methods = ['GET', 'POST'])
def owner_add_machine():
    if request.method == 'POST':
        machine_name = request.form['machine_name']
        type = request.form['type']
        description = request.form['description']
        days = request.form['days']
        rental = request.form['rental']
        f = request.files['file']
        f.save(os.path.join("static/uploads/", secure_filename(f.filename)))

        maxin = mm.find_max_id("machine_details")
        qry = ("insert into machine_details values('" + str(maxin) + "','" + str(machine_name) + "','" + str(
            type) + "','" + str(description) + "','" + str(days) + "','" + str(rental) + "','" + str(f.filename) + "')")
        result = mm.insert_query(qry)
        print(result)
        return render_template('owner_add_machine.html',flash_message=True,data="Success")
    return render_template('owner_add_machine.html')



@app.route("/admin_view_user")
def admin_view_user():
    data = mm.select_direct_query("select name,contact,email,address,gender,username from user_details")
    return render_template('admin_view_user.html',items=data)

@app.route("/user_search", methods = ['GET', 'POST'])
def user_search():

    if request.method == 'POST':
        search = request.form['search']
        data = mm.select_direct_query("select * from machine_details where machine_name='"+str(search)+"'")
        return render_template('user_search.html', items=data)
    return render_template('user_search.html')

@app.route("/user_click/<id>",methods = ['GET', 'POST'])
def user_click(id):
      usern=session['username']
      usern=usern[0][0]
      datax = mm.select_direct_query("select * from user_details where username='" + str(usern) + "'")
      user_name=datax[0][1]
      user_contact = datax[0][2]
      user_email = datax[0][3]
      user_address = datax[0][4]
      session['id'] = id
      data = mm.select_direct_query("select * from machine_details where id='" + str(id) + "'")
      machine_name=data[0][1]
      type=data[0][2]
      description = data[0][3]
      days = data[0][4]
      rental = data[0][5]

      maxin = mm.find_max_id("rental_request")
      qry = ("insert into rental_request values('" + str(maxin) + "','" + str(machine_name) + "','" + str(
          type) + "','" + str(description) + "','" + str(days) + "','" + str(rental) + "','"+ str(user_name) +"','"+ str(user_contact) +"','"+ str(user_email) +"','"+ str(user_address) +"','Booking','0','','','')")
      result = mm.insert_query(qry)
      print(result)
      return redirect('/user_search')





@app.route("/user_view_rental")
def user_view_rental():
    usern = session['username']
    usern = usern[0][0]
    datax = mm.select_direct_query("select * from user_details where username='" + str(usern) + "'")
    user_name = datax[0][1]
    data = mm.select_direct_query("select * from rental_request where user_name='"+ str(user_name) +"'")
    return render_template('user_view_rental.html',items=data)


@app.route("/user_view_pay")
def user_view_pay():
    usern = session['username']
    usern = usern[0][0]
    datax = mm.select_direct_query("select * from user_details where username='" + str(usern) + "'")
    user_name = datax[0][1]
    data = mm.select_direct_query("select * from rental_request where status='Accept' and user_name='"+ str(user_name) +"'")
    return render_template('user_view_pay.html',items=data)



@app.route("/payment", methods = ['GET', 'POST'])
def payment():


    usern = session['username']
    usern = usern[0][0]
    datax = mm.select_direct_query("select * from user_details where username='" + str(usern) + "'")
    user_name = datax[0][1]
    user_contact = datax[0][2]
    id=session['id']
    data = mm.select_direct_query("select amount,machine_name,days from rental_request where id='"+ str(id) +"'")
    amount=data[0][0]
    pname=data[0][1]
    day=data[0][2]
    print(day)
    day=int(day)
    today = date.today()

    Enddate = today + timedelta(days=day)
    if request.method == 'POST':
        amount = request.form['amount']
        cardno = request.form['cardno']
        holder_name = request.form['holder_name']
        cvv = request.form['cvv']


        maxin = mm.find_max_id("payment_details")
        qry = ("insert into payment_details values('" + str(maxin) + "','" + str(user_name) + "','" + str(
            user_contact) + "','" + str(amount) + "','" + str(cardno) + "','" + str(holder_name) + "','" + str(cvv) + "','"+ str(pname) +"')")
        result = mm.insert_query(qry)
        print(result)
        d = mm.insert_query("update rental_request set status='Paid',date='"+ str(today) +"',end_date='"+ str(Enddate) +"' where id='" + str(id) + "'")
        return redirect('/user_view_rental')
    return render_template('payment.html',amount=amount)


@app.route("/pay/<id>",methods = ['GET', 'POST'])
def pay(id):

      session['id'] = id
      return redirect('/payment')




@app.route("/owner_user_pay")
def owner_user_pay():
    data = mm.select_direct_query("select * from rental_request where status='Booking'")
    return render_template('owner_user_pay.html',items=data)
@app.route("/owner_accept/<id>" )
def owner_accept(id):

      session['id'] = id
      d = mm.insert_query("update rental_request set status='Accept' where id='" + str(id) + "'")
      return redirect('/owner_user_pay')
@app.route("/owner_reject/<id>" )
def owner_reject(id):

      session['id'] = id
      d = mm.insert_query("update rental_request set status='Reject' where id='" + str(id) + "'")
      return redirect('/owner_user_pay')

@app.route("/user_fine_pay")
def user_fine_pay():
    data = mm.select_direct_query("select * from rental_request where fine_amount!=''")
    return render_template('user_fine_pay.html',items=data)



@app.route("/user_emp_request", methods = ['GET', 'POST'])
def user_emp_request():
    if request.method == 'POST':
        usern = session['username']
        usern = usern[0][0]
        datax = mm.select_direct_query("select * from user_details where username='" + str(usern) + "'")
        user_name = datax[0][1]
        user_contact = datax[0][2]
        employee_no = request.form['employee_no']
        work_details = request.form['work_details']
        date = request.form['date']
        salary = request.form['salary']



        maxin = mm.find_max_id("reqeust_employee")
        qry = ("insert into reqeust_employee values('" + str(maxin) + "','" + str(employee_no) + "','" + str(
            work_details) + "','" + str(date) + "','" + str(salary) + "','"+ str(user_name) +"','"+ str(user_contact) +"')")
        result = mm.insert_query(qry)
        print(result)
        return render_template('user_emp_request.html',flash_message=True,data="Success")
    return render_template('user_emp_request.html')


@app.route("/owner_accepted_details")
def owner_accepted_details():
    data = mm.select_direct_query("select * from rental_request")
    return render_template('owner_accepted_details.html',items=data)

@app.route("/owner_fine_pay")
def owner_fine_pay():
    data = mm.select_direct_query("select * from rental_request where fine_amount!=''")
    return render_template('owner_fine_pay.html',items=data)

@app.route("/owner_supply_emp")
def owner_supply_emp():
    data = mm.select_direct_query("select * from reqeust_employee")
    return render_template('owner_supply_emp.html',items=data)
@app.route("/admin_view_machine")
def admin_view_machine():
    data = mm.select_direct_query("select * from machine_details")
    return render_template('admin_view_machine.html',items=data)

@app.route("/admin_emp_details")
def admin_emp_details():
    data = mm.select_direct_query("select name,contact,email,address,gender,username from owner_details")
    return render_template('admin_emp_details.html',items=data)


@app.route("/admin_view_fine")
def admin_view_fine():
    data = mm.select_direct_query("select * from rental_request where fine_amount!=''")
    return render_template('admin_view_fine.html',items=data)

@app.route("/admin_accepted_details")
def admin_accepted_details():
    data = mm.select_direct_query("select * from rental_request")
    return render_template('admin_accepted_details.html',items=data)


@app.route("/generate_paid_rentals_pdf")
def generate_paid_rentals_pdf():
    usern = session['username'][0][0]
    datax = mm.select_direct_query(f"SELECT * FROM user_details WHERE username='{usern}'")
    user_name = datax[0][1]
    data = mm.select_direct_query(f"SELECT * FROM rental_request WHERE user_name='{user_name}' AND status='Paid'")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    current_date = date.today().strftime("%B %d, %Y")
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(name='Title', fontSize=18, spaceAfter=10)
    date_style = ParagraphStyle(name='Date', fontSize=12, spaceAfter=10)

    elements.append(Paragraph('Paid Rental Report', title_style))
    elements.append(Paragraph(f"Date: {current_date}", date_style))
    elements.append(Paragraph(f"Farmer Name: {user_name}", date_style))  # Include username in the report

    table_data = [['ID', 'Machine Name', 'Type', 'Description', 'Days', 'Rental', 'Status']]
    for record in data:
        table_data.append([record[0], record[1], record[2], record[3], record[4], record[5], record[10]])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="paid_rental_report.pdf", mimetype='application/pdf')

@app.route("/download_accepted_requests")
def download_accepted_requests():
    try:
        # Example SQL query to fetch accepted rental requests
        query = "SELECT * FROM rental_request WHERE status = 'Paid'"
        data = mm.select_direct_query(query)

        # Get username from session (assuming it's stored there after login)
        username = session.get('username', 'Guest')

        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Generate PDF buffer
        pdf_buffer = create_accepted_requests_pdf(data, username, current_datetime)

        # Offer PDF as a downloadable response
        return send_file(
            io.BytesIO(pdf_buffer),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='accepted_rental_requests.pdf'
        )
    except Exception as e:
        return str(e)

def create_accepted_requests_pdf(data, username, current_datetime):
    buffer = io.BytesIO()  # Create a BytesIO buffer
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set up styles
    title_style = "Helvetica-Bold"
    subtitle_style = "Helvetica"
    data_style = "Helvetica"

    # Write header to the PDF
    pdf.setFont(title_style, 16)
    pdf.drawCentredString(300, 750, "Accepted Rental Requests")
    
    # Write username and datetime
    pdf.setFont(subtitle_style, 12)
    pdf.drawString(50, 730, f"Machine Owner: {username}")
    pdf.drawString(50, 710, f"Date and Time: {current_datetime}")

    # Set up table headers
    pdf.setFont(subtitle_style, 12)
    pdf.drawString(50, 660, "Request ID")
    pdf.drawString(50, 640, "Farmer Name")
    pdf.drawString(50, 620, "Start Date")
    pdf.drawString(50, 600, "End Date")
    pdf.drawString(50, 580, "Machine Name")
    pdf.drawString(50, 560, "Machine Type")
    pdf.drawString(50, 540, "Days")
    pdf.drawString(50, 520, "Amount")
    pdf.drawString(50, 500, "Fine Amount")
    pdf.drawString(50, 480, "Farmer Contact")

    # Write data to the PDF
    y = 660  # Start position for data rows
    pdf.setFont(data_style, 10)
    for item in data:
        # Write each item's data in a row-wise format
        pdf.drawString(150, y, f"{item[0]}")         # Request ID
        pdf.drawString(150, 640, f"{item[6]}")        # Farmer Name
        pdf.drawString(150,620, f"{item[12]}")       # Start Date
        pdf.drawString(150, 600, f"{item[13]}")       # End Date
        pdf.drawString(150, 580, f"{item[1]}")        # Machine Name
        pdf.drawString(150, 560, f"{item[2]}")        # Machine Type
        pdf.drawString(150, 540, f"{item[4]}")        # Days
        pdf.drawString(150, 520, f"{item[5]}")        # Amount
        pdf.drawString(150, 500, f"{item[14]}")       # Fine Amount
        pdf.drawString(150, 480, f"{item[7]}")        # Farmer Contact
        y -= 20  # Move to the next row

    pdf.save()
    buffer.seek(0)  # Reset the buffer position to start
    return buffer.getvalue()


######################################
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)