# HPMA115S0 Data Parser and logger for Python3 / Raspberry Pi
# MIT license; Copyright (c) 2019 Daniel Near (dan.e.near@gmail.com)
# Version 0.1 beta (2019/02/17)
#
# This python file reads data directly from the Honeywell HPMA115S0 Dust 
# particulate laser interferometer device, validates the data stream per
# Honeywell's published protocol and logs the values with a date/time stamp 
# to a CSV file
# This was designed for a friend to connect the HMPA sensor directly to
# the RPI GPIO header and log with minimal interaction.  

import serial
import time
port=serial.Serial("/dev/ttyAMA0",baudrate=9600, timeout=1.0)
firstwrite=False
while True:
    rcv=None
    gotData=False
    if port.inWaiting()>=32:
        rcv=port.read(port.inWaiting())
        #print(repr(rcv))
        
    if rcv is not None:
        if(len(rcv)>31):
            
            try:
                bytestream=rcv.split(b'BM')[1][0:31]
            except IndexError:
                print("IndexError")
                break
            if len(bytestream)==30:
                if bytestream[0:2]==b'\x00\x1c':
                    checksum=143
                    validated=0
                    for i in range(0,28):
                        checksum+=int(bytestream[i])
                    validated=int(bytestream[28])*256+int(bytestream[29])
                    if checksum==validated:
                        pm25=int(bytestream[4])*256+int(bytestream[5])
                        pm10=int(bytestream[6])*256+int(bytestream[7])
                        currentdatetime=time.strftime("%c")
                        print(currentdatetime,' pm2.5um:',pm25,' pm10um:',pm10,'\n')
                        gotData=True
                    else:
                        print('checksum failed')
                else:
                    print('invalid packet')
            else:
                print('incomplete packet')
        else:
            print('incomplete packet')
        if gotData==True:
            gotData=False
            f=open('/home/pi/Desktop/dustlog.csv','a+')
            if firstwrite==False:
                f.write('timestamp,pm2.5,pm10\n')
                firstwrite=True
            f.write(currentdatetime +',' + str(pm25) + ',' + str(pm10)+ '\n')
            f.close()
            print('sleeping 10s')
            time.sleep(10)
            
                    
        
            
