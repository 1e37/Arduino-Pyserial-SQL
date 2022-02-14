from sqlite3 import connect
import serial
import time
import mariadb
import sys
import datetime


try: con = mariadb.connect(
      user="serial_user",
      password="xxx",
      host="localhost",
      port=3306,
      database="connDB"
      )
# Print error when DB not reachable
except mariadb.Error as e:
    print(f"Error on DB: {e}") 
    sys.exit(1) 

#Get cursor
cur = con.cursor()

# Read the highest ID we do own
MariasCMD = "SELECT MAX(id) FROM sensor_data;"
cur.execute(MariasCMD)
result = (cur.fetchone()[0])
print("result = " + str(result))
newresult = result +1
MariasCMD = "INSERT INTO sensor_data (timeresults, id) VALUES ('55551'," + str(newresult) + ");"
cur.execute(MariasCMD)
con.commit()

print(str(newresult) + " was created.")
