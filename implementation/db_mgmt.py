import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="nlp_cities"
)

def storedata(query):
  mycursor = mydb.cursor()
  mycursor.execute(query)
  mydb.commit()

def readdata(query):
  mycursor = mydb.cursor()
  mycursor.execute(query)
  myresult = mycursor.fetchall()
  return myresult
