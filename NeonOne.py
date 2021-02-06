import os
import sys
import time
import datetime
import threading
from System.IO.Ports import SerialPort

try:
    port = raw_input ( 'input serial port name, for example COM1 : ' )
    ser = SerialPort(PortName=port, BaudRate=115200)
except:
    print ( 'something wrong, used COM15' )
    ser = SerialPort(PortName='COM15',BaudRate=115200)

ser.Open()

outfile = 'temperature.log'
command = [] # command to sends 

def fn_in():   
    while 1:
        # waits for a string
        in_len = 0;
        while in_len < 1:
            in_st = ser.ReadLine()
            in_len = len ( in_st )

        fileOut = open ( outfile, 'a' )
        now = datetime.datetime.now(); 
        dt =  now.strftime("%d-%m-%Y %H:%M:%S ")
        try:
            celsius = float( in_st )
            fileOut.write( dt + "{:+2.1f}".format (celsius) + ' C\n' )
        except:
            fileOut.write( dt + in_st + '\n' )
        fileOut.close()

        
        
def fn_out():   
    while 1:
        global command
        if len( command ) > 0:
            cmd = command.pop(0)
            # print ('\r>>> sending to the device: ' + cmd )
            cmd = cmd + '\r'
            ser.Write( cmd )

        
# run to thread 
tr_in = threading.Thread( target = fn_in)
tr_in.daemon = True
tr_in.start() 

# run to thread 
tr_out = threading.Thread( target = fn_out)
tr_out.daemon = True
tr_out.start()

print ('enter help - for commands list')

while 1:    
    str = raw_input(">>> ")

    if str == 'exit': 
        sys.exit(0)
    elif str == 'help': 
        print ('\n ENTER ONE OF THE FOLLOWING:\n    start - start pereodic temperature measurement\n    stop - stop measurement process\n    period <S> - change measurement period <S> - time in seconds, ranging from 1 to 5,\n    exit - exit the program')   
    elif str == 'start' or str == 'stop' or ( str >= 'period 1' and str <= 'period 5' ):
        command.append (str)
        print ('\r>>> sending to the device: ' + str )
    else:
        print ('wrong command')

