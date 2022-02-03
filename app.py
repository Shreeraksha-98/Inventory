from datetime import date
from flask import Flask,redirect,url_for,render_template,request
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import pyodbc

app = Flask(__name__, instance_relative_config=True)

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/add_customer")
@cross_origin()
def add_customer():
    return render_template("Customer_info.html")

@app.route('/add_cust_form', methods = ["GET", "POST"])
@cross_origin()
def add_cust_form():
    if request.method == "POST":
        # Customer details
        Name = (request.form["Customer_Name"])
        Phone = (request.form["Phone_no"])
        Email = (request.form["Email"])

        conn = pyodbc.connect(
                "Driver={SQL Server Native Client 11.0};"
                "Server=SHREERAKSHA\SQLEXPRESS;"
                "Database=Inventory;"
                "Trusted_Connection=yes;"
            )

        cursor = conn.cursor()
        cursor.execute(
                'insert into Customer_details(Cust_Name,Phone_no,Email) values(?,?,?);',
                (Name, Phone, Email)
            )
        conn.commit()
    return(render_template("Customer_info.html"))

@app.route("/add_rental")
@cross_origin()
def add_rental():
    namelist = []
    conn = pyodbc.connect(
                        "Driver={SQL Server Native Client 11.0};"
                        "Server=SHREERAKSHA\SQLEXPRESS;"
                        "Database=Inventory;"
                        "Trusted_Connection=yes;"
                    )
    cursor = conn.cursor()
    cursor.execute(
                    "select Cust_Name from Customer_details"
                    )
    for each in cursor:
            namelist.append(each)
    return render_template("Add_rental.html",namelist=namelist)

@app.route('/add_rent_form', methods = ["GET", "POST"])
@cross_origin()
def add_rent_form():
    if request.method == "POST":
        
         # Rental details
        Cust_name = (request.form["Customer_Name"])
        Rental_date = (request.form["Rental_date"])
        Return_date = (request.form["Return_date"])
        Vehilce = str(request.form["Vehicle_type"]) 

        conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=SHREERAKSHA\SQLEXPRESS;"
            "Database=Inventory;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute(
            'select NO_VEHICLES from Veh_Inv where VEHICLE = ?;',
            (Vehilce)
        )
        #v_no = []
        #for each in cursor:
            #v_no.append(each)

        if cursor != 0 :
            cursor.execute(
                'update Veh_Inv set NO_VEHICLES = NO_VEHICLES-1 where VEHICLE= ?;',
                (Vehilce)
            )
            conn.commit()
            if Return_date:
                cursor.execute(
                'insert into Rental_details(Customer_name,Rental_date,Return_date,Vehicle_type) values(?,?,?,?);',
                (Cust_name, Rental_date, Return_date, Vehilce)
                )
                conn.commit()

            else:
                cursor.execute(
                'insert into Rental_details(Customer_name,Return_date,Vehicle_type) values(?,?,?);',
                (Cust_name, Return_date, Vehilce)
                )
                conn.commit()                   
                    
        else:
            p_text = 'Sorry, Vehicle not avilable at the moment'
            render_template("Add_rental.html", p_text=p_text)        

        

    return render_template("Add_rental.html")        

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Adding Customer
        if request.form['submit_button'] == 'Add Customer':
            return(redirect(url_for('add_customer')))
        
        # Adding rental details
        elif request.form['submit_button'] == 'Add Rental Booking':    
            
            return redirect(url_for("add_rental"))

        elif request.form['submit_button'] == 'See Customer List':
            conn = pyodbc.connect(
                        "Driver={SQL Server Native Client 11.0};"
                        "Server=SHREERAKSHA\SQLEXPRESS;"
                        "Database=Inventory;"
                        "Trusted_Connection=yes;"
                    )
            cursor = conn.cursor()
            cursor.execute('select * from Customer_details')
            ghi = []
            for each in cursor:
                ghi.append(each)
            return render_template("See_cust_details.html", ghi=ghi)            

        elif request.form['submit_button'] == 'See Rental Booking List':
            conn = pyodbc.connect(
                        "Driver={SQL Server Native Client 11.0};"
                        "Server=SHREERAKSHA\SQLEXPRESS;"
                        "Database=Inventory;"
                        "Trusted_Connection=yes;"
                    )
            cursor = conn.cursor()
            cursor.execute('select * from Rental_details')
            cde = []
            for each in cursor:
                cde.append(each)
            return render_template("See_rental_details.html", cde=cde)            

        else:
            conn = pyodbc.connect(
                        "Driver={SQL Server Native Client 11.0};"
                        "Server=SHREERAKSHA\SQLEXPRESS;"
                        "Database=Inventory;"
                        "Trusted_Connection=yes;"
                    )
            cursor = conn.cursor()
            cursor.execute('select * from Veh_Inv')
            abc=[]
            for each in cursor:
                abc.append(each)
            return render_template("Vehicles_list.html", abc=abc)
            
    
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
