import mysql.connector

myconn = mysql.connector.connect(
host ="localhost",
user ="root",
passwd ="" 
)

cursorObject = myconn.cursor()
print(myconn)

cursorObject.execute("CREATE DATABASE my_miniproj_db")

dbs = cursorObject.execute("show databases")

for x in cursorObject:
    print(x)

