# importing required library
import mysql.connector
#Create the connection object
myconn = mysql.connector.connect(
    host = "localhost",
    username = "root",
    passwd =""
    )
#printing the connection object
print(myconn)