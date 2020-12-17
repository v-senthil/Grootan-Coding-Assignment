from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import random
import string
import time
named_tuple = time.localtime()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/todb", methods=['GET', 'POST'])
def db():
    starttime = time.strftime("%S", named_tuple)
    conn = sqlite3.connect('csvdata.db', check_same_thread=False)
    cursor = conn.cursor()
    if request.method == 'POST':
        file = request.files['csv']
        file=file.filename
        data = pd.read_csv(file)
        col_value = data.columns
        col = len(data.columns)
        rows = len(data.index)

        #if header name in "Password", it encrypts the data in the column
        for i in range(0,col):
            if col_value[i] == 'password' or col_value[i] == 'Password' or col_value[i] == 'PASSWORD':
                data['broken'] = msg.encode()
                f=Fernet(key)
                data['broken']=f.encrypt(encoded)

        #Dynamic table creation
        #it creates a table with the corresponding file name
        #for one unique file, it create a table
        letters = string.ascii_lowercase
        filename =  ''.join(random.choice(letters) for i in range(4))
        sql1 ='''CREATE TABLE '''+ filename +'''('''+ col_value[0] +''' VARCHAR(255))'''
        cursor.execute(sql1)
        for i in range (1,col):
            sql ='''ALTER TABLE '''+ filename +''' ADD COLUMN '''+ col_value[i] +''' varchar(255)'''
            cursor.execute(sql)
            continue

        #Insert into the dynamic generated table
        valueinsert = (col-1) * "?,"
        with open(file,'r') as file:
            record = 1
            for row in file:
                success = cursor.execute("INSERT INTO "+ filename +" Values ("+ valueinsert +"?)", row.split(","))
                conn.commit()
                record+=1

        #Total TIme
        endtime =time.strftime("%S", named_tuple)
        totaltime = int(endtime) - int(starttime)
        if success:
            success = "CSV data Successfully uploaded to Database as "+filename+" in "+ str(totaltime) +" seconds for "+ str(rows) +" rows"
            return render_template("index.html", success=success)
        else:
            error = "Failure"
            return render_template("index.html", error= error)
    else:
        return render_template("index.html", error= error)



# Error Handling
@app.errorhandler(404)
def error(error):
    error = "Failure"
    return render_template('index.html',error=error), 404


if __name__ == "__main__":
    app.run(port=1002, debug=True)
