import serial
import time
import mariadb
import sys
import datetime

#First run of this code will bring the state 'Motion Detected' to true due to Arduino initialize.

#Connection string for remote DB 
try: conn = mariadb.connect(
      user="serial_user",
      password="Eisenbahn123",
      host="mmgalaxy.ddns.net",
      port=3306,
      database="connDB"
      )

#Print error when DB not reachable
except mariadb.Error as e:
    print(f"Error on DB: {e}") 

#Grant database access 
cur = conn.cursor()

#Connect to Serial
ser = serial.Serial('COM4', baudrate = 9600, timeout=1)

#Function to read-out Arduino PIR-value
def getPIRvalue():
    ser.write(b'g')
    arduinoData = ser.readline().decode('utf-8')
    return arduinoData

try:
    #1 = Serial conected
    while(1):
        
        #Send Command to Arduino and get the current state
        msgbytes = bytes(getPIRvalue(), encoding='utf-8')
        targetbyte_end = bytes("Motion End\r\n", encoding='utf-8')
        targetbyte_start = bytes("Motion Detected\r\n", encoding='utf-8')

        if msgbytes in targetbyte_start:
            print("[Info] Targetbytes do equal to Motion detected!")
            time.sleep(1)

            #Start a timer to know how long the job was active
            timestart = datetime.datetime.now()

            #Check if table is already exists, if not create one
            tablename = 'sensor_data' 
            cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'sensor_data';")

            #Grab the last fetch and check if the return is equal to tablename
            nameresult = (str(cur.fetchone()[0]))
            if nameresult == tablename:
                time.sleep(1)
                print("[Info] Table " + tablename + " exists")
                print("[Info] Fetchnote is equal.")

                #Get the newest INT from tabledata
                MariasCMD = "SELECT MAX(id) FROM sensor_data;"
                cur.execute(MariasCMD)
                result = str((cur.fetchone()[0]))
                resultint = int(result)
                time.sleep(3)
                print("[Info] result = " + str(result))
                newresult = resultint +1
                timeend = datetime.datetime.now()
                timeresult = (timeend-timestart).microseconds
                MariasCMD = "INSERT INTO sensor_data (timeresults, id) VALUES (" +str(timeresult) +"," + str(newresult) + ");"
                cur.execute(MariasCMD)
                conn.commit()
                print("[Info] " + str(newresult) + " was created.")
            
            else:
                #Check if table exists
                if nameresult != tablename:
                    print("[Error] Table " + tablename + " do not exists \n Creating one.")

                    #Create all required tables and fill with basic data
                    print("[Error] Fetchnote was not equal!" + cur.fetchone()[0])
                    print("[Info] Please Wait 2 Seconds for table creation..")
                    cur.execute("CREATE TABLE "+ tablename + "(timeresults int);")
                    cur.execute("ALTER TABLE `sensor_data` ADD `ID` INT NOT NULL")
                    cur.execute("ALTER TABLE `sensor_data` ADD PRIMARY KEY(`ID`);")
                    cur.execute("INSERT INTO sensor_data (timeresults, id) VALUES ('0', '0');")
                    time.sleep(2)
                    print("[Info] Table" + tablename + " created")
                    time.sleep(2)
                    break
        else:
            if msgbytes in targetbyte_end:
                print("[Info] No work to do.")

except Exception as ex:
        print(ex)