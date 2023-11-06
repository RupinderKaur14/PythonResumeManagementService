from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import sqlite3
import pandas as pd


app = Flask(__name__)
CORS(app)


#get emails out of csv
@app.route('/users',methods=['GET'])
def getUsers():

    #get emails from csv file to json
    csv_file_path = "file path"
    df = pd.read_csv(csv_file_path)
    column_to_send = df.iloc[:, 1]
    print(column_to_send)
    json_data = column_to_send.to_json(orient='values')

    return json_data


#send email
@app.route('/sendEmail',methods=['POST'])
def postEmailid():
    request_data = request.get_json()
    emailId = request_data.get('email')
    response = sendemail(emailId)
    response_data = {"status": "OK", "message": response}
    
    return jsonify(response_data)


# get email sent history
@app.route("/getEmailHistory", methods=['GET'])
def getEmailHistory():
    emailId = request.args.get("email")
    if emailId is None:
        return "Email parameter is missing or invalid", 400  # Return an error response

    print("emailId:" + str(emailId))
    
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()
    query = "SELECT * FROM RUN_HISTORY WHERE Receiver = ? ORDER BY Date DESC"
    cursor.execute(query, (str(emailId),))
    data = cursor.fetchall()
    print("data:"+ str(data))
    connection.close()

    json_data= {
        "history": [
            {"id": id, "time":time, "receiver": receiver}
            for id, time, receiver in data
        ]
    }
    print("json data:"+ str(json_data))

    return jsonify(json_data)


def sendemail(emailId):
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    sender_email = 'SenderEmail@outlook.com'
    password = '****'

    server = smtplib.SMTP(smtp_server,smtp_port)
    server.starttls()
    server.login(sender_email,password)

    subject = 'subject'
    body = "body"

    #attachment file path get from json
    with open('input.json','r') as json_file:
        data = json.load(json_file)


    with open(data['file_location'], 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name='fileName.pdf')
    part['Content-Disposition'] = f'attachment; filename=fileName.pdf'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = emailId
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))
    message.attach(part)
    server.sendmail(sender_email, emailId, message.as_string())

    server.quit()

    saveData(emailId)
    return 'Email sent successfully!'



def saveData(emailId):
    connection = sqlite3.connect('mydatabase.db')
    cursor = connection.cursor()

    # Create a table
    cursor.execute('CREATE TABLE IF NOT EXISTS RUN_HISTORY (id INTEGER PRIMARY KEY, Date datetime, Receiver VARCHAR(100))')

    cursor.execute("INSERT INTO RUN_HISTORY (Date, Receiver) VALUES (CURRENT_TIMESTAMP, '{0}')".format(emailId))
    connection.commit()
    connection.close()


app.run()
