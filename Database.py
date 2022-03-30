import sqlite3

conn = sqlite3.connect(r'C:\\Users\\lidor\\Desktop\\SQL\\SERI-AIR Project.db', check_same_thread = False) #Make connection to the database

#store the data in lists-

countriesList = []
flightList = []
ticketList = []
usersList = []

#defin function to extract info from the data base and append to the lists above-

#---------USERS---------

def getUsers():
    users = conn.execute('select * from Users')
    for i in users:
        dic = {"id": i[0], "fullName": i[1], "password": i[2], "realId": i[3]}
        usersList.append(dic)

def insertUser(name,password,id):
    conn.execute(f'INSERT INTO Users(fullName,password,realId) VALUES(\'{name}\',\'{password}\',\'{id}\')')
    conn.commit()
    usersList.clear()
    getUsers()

def updateUser(id,fullName,password,realId):
    conn.execute(f'UPDATE Users SET fullName =\'{fullName}\' WHERE id ={id}')
    conn.execute(f'UPDATE Users SET password = {password} WHERE id ={id}')
    conn.execute(f'UPDATE Users SET realId ={realId} WHERE id ={id}')
    conn.commit()
    usersList.clear()
    getUsers()

def deleteUser(id):
    conn.execute(f'DELETE FROM Users WHERE id = {id}')
    conn.commit()
    usersList.clear()
    getUsers()

def findId(loginId):
    userId = conn.execute(f'SELECT id FROM Users WHERE realId = {loginId}')
    for i in userId:
        return i[0]

#---------FLIGHTS---------

def getFlights():
    flights = conn.execute('select * from Flights')
    for i in flights:
        dic = {"flightId": i[0], "timeStamp": i[1], "reamainingSeats": i[2], "OriginCountryId": i[3], "destCountryId": i[4]}
        flightList.append(dic)

def insertFlights(timeStamp,reamainingSeats,OriginCountryId,destCountryId):
    conn.execute(f'INSERT INTO Flights(timeStamp,reamainingSeats,OriginCountryId,destCountryId)\
    VALUES(\'{timeStamp}\',{reamainingSeats},{OriginCountryId},{destCountryId})')
    conn.commit()
    flightList.clear()
    getFlights()

def updateFlights(flightId,timeStamp,reamainingSeats,OriginCountryId,destCountryId):
    conn.execute(f'UPDATE Flights SET timeStamp =\'{timeStamp}\' WHERE flightId ={flightId}')
    conn.execute(f'UPDATE Flights SET reamainingSeats ={reamainingSeats} WHERE flightId ={flightId}')
    conn.execute(f'UPDATE Flights SET OriginCountryId ={OriginCountryId} WHERE flightId ={flightId}')
    conn.execute(f'UPDATE Flights SET destCountryId ={destCountryId} WHERE flightId ={flightId}')
    conn.commit()
    flightList.clear()
    getFlights()

def deleteFlightNum(flightId):
    conn.execute(f'DELETE FROM Flights WHERE flightId = {flightId}')
    conn.commit()
    flightList.clear()
    getFlights()

def deleteFlightSits(amount,flightId):
    conn.execute(f'UPDATE Flights SET reamainingSeats = reamainingSeats - {amount} WHERE flightId = {flightId}')
    conn.commit()
    getTickets()

def appendFlightSits(flightId):
    conn.execute(f'UPDATE Flights SET reamainingSeats = reamainingSeats + 1 WHERE flightId = {flightId}')
    conn.commit()
    getTickets()

#---------TICKETS---------

def getTickets():
    tickts = conn.execute('select * from Tickets')
    for i in tickts:
        dic = {"ticketId": i[0], "userId": i[1], "flightId": i[2]}
        ticketList.append(dic)

def connectUserToTicket(userId,flightId,amount):
    for times in range(amount):
        conn.execute(f'INSERT INTO Tickets(userId,flightId) VALUES({userId},{flightId})')
        conn.commit()
    ticketList.clear()
    getTickets()

def myTickets(id):
    tickts = conn.execute(f'select * from Tickets WHERE userId = {id}')
    personTickets = []
    for i in tickts:
        rows = i[0], i[2]
        personTickets.append(rows)
    return personTickets

def deleteTicket(ticketId):
    delete = conn.execute(f'DELETE FROM Tickets WHERE ticketId = {ticketId}')
    conn.commit()
    ticketList.clear()
    getTickets()

def insertTicket(userId,flightId):
    ticket = conn.execute(f'INSERT INTO Tickets(userId,flightId) VALUES({userId},{flightId})')
    conn.commit()
    ticketList.clear()
    getTickets()

#---------COUNTRIES---------

def getCountries():
    countries = conn.execute('select * from Countries')
    for i in countries:
        dic = {"code":i[0], "name":i[1]}
        countriesList.append(dic)

def insertCountry(name):
    country = conn.execute(f'INSERT INTO Countries(name) VALUES(\'{name}\')')
    conn.commit()
    countriesList.clear()
    getCountries()

getCountries()
getFlights()
getTickets()
getUsers()