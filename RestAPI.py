import json, requests
from flask import Flask, render_template, redirect, url_for, request
import Database
import logging
import tkinter
from tkinter import messagebox
import os

app = Flask(__name__) #Make a WEB API server

#logging.basicConfig(filename="flaskLog", level= logging.DEBUG, format= '%(asctime)s''::''%(levelname)s''::''%(message)s')

Home_page_button = '<p></p><button><a href="http://127.0.0.1:5000/">Home Page</a></button>'
account_page_button = '<p></p><button><a href="http://127.0.0.1:5000/accountActions">Back to Account page</a></button>'
imgFolder = os.path.join('static','images')
app.config['UPLOAD_FOLDER'] = imgFolder

@app.route('/') #defin home page
@app.route('/home')
def homePage():
    homeImg = os.path.join(app.config['UPLOAD_FOLDER'],'airport.jpg')
    loginImg = os.path.join(app.config['UPLOAD_FOLDER'],'login.png')
    regImg = os.path.join(app.config['UPLOAD_FOLDER'],'reg.jpg')
    flightImg = os.path.join(app.config['UPLOAD_FOLDER'],'lidor.png')
    logging.info('User entered the HomePage!')
    return render_template('index.html', homeImg = homeImg, loginImg = loginImg, regImg = regImg,flightImg = flightImg)

@app.route('/registration')
@app.route('/register')
def register():
    return render_template('register.html')
2
@app.route('/storeUser', methods = ['POST'])
def storeUser():
    if request.method == 'POST':
        fullName = request.form['name']
        password = request.form['psw']
        id = request.form['id']
        try:
            Database.insertUser(fullName.lower(),password,id)
        except: return 'Value error - Id already register'
        logging.info(f'Username {fullName} has been added!')
    return f'{fullName} has been added successfully!' + Home_page_button + '<p></p><button><a href="http://127.0.0.1:5000/accountActions">Go to Account page</a></button>'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/userFound', methods= ['POST'])
def userFound():
    global loginId
    cheking = False
    if request.method == 'POST':
        loginId = request.form['id']
        password = request.form['psw']
        for i in Database.usersList:
            if i['realId'] == loginId and i['password'] == password:
                cheking = True
        if cheking == True:
            logging.info(f'Username {loginId} has logged in')
            return redirect(url_for('accountActions'))
        else:
            root = tkinter.Tk()
            #root.eval('tk::PlaceWindow . center' % tkinter.Toplevel(root))
            root.eval('tk::PlaceWindow . center')
            second_win = tkinter.Toplevel(root)
            root.eval(f'tk::PlaceWindow {str(second_win)} center')
            root.withdraw()
            messagebox.showerror('Error','Username or Passworde incorrect')
            root.deiconify
            root.destroy()
            root.quit
            root.mainloop()
            return render_template('login.html')

@app.route('/accountActions')
def accountActions():
    return render_template('accountActions.html')

@app.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        userData = []
        for user in Database.usersList:
            userInfo = user['id'], user['fullName'], user['password'], user['realId']
            userData.append(userInfo)
        userData = tuple(userData)  # converting the data to tuple for html
        return render_template('users.html', userData = userData)

    elif request.method == 'POST':
        newUser = request.get_json()
        fullName = newUser['fullName']
        password = newUser['password']
        realId = newUser['realId']
        Database.insertUser(fullName,password,realId)
        logging.info(f'user {fullName} with ID {realId} added')
        return json.dumps(Database.usersList)


@app.route('/users/<int:id>', methods=['GET','PUT','DELETE'])
def usersId(id):
    if request.method == 'GET':
        for i in Database.usersList:
            if i['id'] == id:
                logging.info('user reqested by POSTMAN')
                return json.dumps(i)
    try:
        if request.method == 'PUT':
            for i in Database.usersList:
                if i['id'] == id:
                    newUser = request.get_json()
                    i['fullName'] = newUser['fullName']
                    i['password'] = newUser['password']
                    i['realId'] = newUser['realId']
                    fullName = newUser['fullName']
                    password = newUser['password']
                    realId = newUser['realId']
                    Database.updateUser(id,fullName,password,realId)
                    logging.info(f'user {id} has been changed by POSTMAN')
                    return json.dumps(Database.usersList)
    except: logging.error('Unable to modify User')
    try:
        if request.method == 'DELETE':
            for i in Database.usersList:
                if i['id'] == id:
                    Database.deleteUser(id)
                    logging.info(f'User {id} deleted by POSTMAN')
                    return json.dumps(Database.usersList)
    except: logging.error('Unable to delete user')


@app.route('/flights',methods=['GET','POST'])
def flights():
    if request.method == 'GET':
        logging.info('User request flights')
        store = [] #to store all the flight data and afterward convert to tuple to shoe on html table
        for d in Database.flightList:
            flightInfo = d['flightId'],d['timeStamp'],d['reamainingSeats'],d['OriginCountryId'],d['destCountryId']
            store.append(flightInfo)
        tup = tuple(store) #convertinf the data to tuple for html
        return render_template('flightTable.html', tup = tup) + Home_page_button

    elif request.method == 'POST':
        newFlight = request.get_json()
        timeStamp = newFlight['timeStamp']
        reamainingSeats = newFlight['reamainingSeats']
        OriginCountryId = newFlight['OriginCountryId']
        destCountryId = newFlight['destCountryId']
        Database.insertFlights(timeStamp,reamainingSeats,OriginCountryId,destCountryId)
        logging.info(f'Flight {newFlight} added')
        return json.dumps(Database.flightList) + Home_page_button

@app.route('/flights/<int:id>', methods=['GET','PUT','DELETE'])
def flightsId(id):
    if request.method == 'GET':
        for i in Database.flightList:
            if i['flightId'] == id:
                return json.dumps(i)
    try:
        if request.method == 'PUT':
            for i in Database.flightList:
                if i['flightId'] == id:
                    newFlight = request.get_json()
                    i['timeStamp'] = newFlight['timeStamp']
                    i['reamainingSeats'] = newFlight['reamainingSeats']
                    i['OriginCountryId'] = newFlight['OriginCountryId']
                    i['destCountryId'] = newFlight['destCountryId']
                    timeStamp = newFlight['timeStamp']
                    reamainingSeats = newFlight['reamainingSeats']
                    OriginCountryId = newFlight['OriginCountryId']
                    destCountryId = newFlight['destCountryId']
                    Database.updateFlights(id,timeStamp,reamainingSeats,OriginCountryId,destCountryId)
                    logging.info(f'Flight {newFlight} has changed')
                    return json.dumps(Database.flightList)
    except: logging.error('Unable to modify flight')
    try:
        if request.method == 'DELETE':
            for i in Database.flightList:
                if i['flightId'] == id:
                    Database.deleteFlightNum(id)
                    return json.dumps(Database.flightList)
    except: logging.error('Unable to delete flight')

@app.route('/tickets', methods=['GET','POST'])
def tickets():
    if request.method == 'GET':
        return json.dumps(Database.ticketList) + Home_page_button
    elif request.method == 'POST':
        newTicket = request.get_json()
        ticketId = newTicket['ticketId']
        userId = newTicket['userId']
        flightId = newTicket['flightId']
        Database.insertTicket(ticketId,userId)
        Database.deleteFlightSits(1,flightId)
        logging.info(f'Ticket {ticketId} has been related to {userId}')
        return json.dumps(Database.ticketList) + Home_page_button

@app.route('/tickets/<int:id>', methods=['GET','DELETE'])
def ticketsId(id):
    if request.method == 'GET':
        for i in Database.ticketList:
            if i['ticketId'] == id:
                return json.dumps(i)
    try:
        if request.method == 'DELETE':
            for i in Database.ticketList:
                if i['ticketId'] == id:
                    flightId = i['flightId']
                    Database.deleteTicket(id)
                    Database.appendFlightSits(flightId)
                    logging.info(f'Ticket {id} deleted')
                    return json.dumps(Database.ticketList)
    except: logging.error('Unable to delete ticket')

@app.route('/buyTickets')
def buyTickets():
    return render_template('buyTickets.html')

@app.route('/buyTicket', methods= ['POST'])
def buyTicket():
    if request.method == 'POST':
        flightId = request.form['id']
        realId = request.form['realid']
        ticketAmount = request.form['number']
        crusor = Database.conn.execute(f'SELECT * FROM Users WHERE realId = "{realId}"')
        for id in crusor:
            numID = id[0]
        Database.connectUserToTicket(numID,flightId,int(ticketAmount))
        Database.deleteFlightSits(ticketAmount,flightId)
        logging.info(f'{ticketAmount} Ticket - {numID} has reserved for user {realId}')
        return f'{ticketAmount} tickets reserved for User {realId} flight number: {flightId}' + Home_page_button + account_page_button
    
@app.route('/myTickets')
def myTickets():
    userId = Database.findId(loginId)
    logging.info('User request to see tickets')
    userTicket = Database.myTickets(userId)
    return  render_template('myTickets.html', userTicket = userTicket) + Home_page_button + account_page_button

@app.route('/deleteTicket')
def deleteTicket():
    return render_template('deleteTicket.html')

@app.route('/deleteTheTicket', methods= ['POST'])
def deleteTheTicket():
    try:
        if request.method == 'POST':
            ticketId = request.form['id']
            flightId = Database.conn.execute(f'SELECT flightId FROM Tickets WHERE ticketId = {ticketId}')
            for i in flightId:
                flighNum = i[0]
            Database.deleteTicket(ticketId)
            Database.appendFlightSits(flighNum)
            logging.info(f'Ticket {ticketId} deleted')
            return f'Ticket number {ticketId} has been deleted!'
    except: logging.error(f'Unable to delete ticket {ticketId}')

@app.route('/countries',methods=['GET','POST'])
def countries():
    if request.method == 'GET':
        return json.dumps(Database.countriesList) + homePage
    elif request.method == 'POST':
        newCountry = request.get_json()
        name = newCountry['name']
        Database.insertCountry(name)
        logging.info(f'Flight {name} has been added by POSTMAN')
        return json.dumps(Database.countriesList)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/adminPage', methods = ['POST'])
def adminPage():
    if request.method == 'POST':
        adminPass = request.form['psw']
        defPass = 'example1234'
        if adminPass == defPass:
            return render_template('adminPage.html')



app.run()
