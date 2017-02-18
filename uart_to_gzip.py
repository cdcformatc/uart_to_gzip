import serial
import sys
from datetime import datetime
import struct
import time
import gzip

time_format = "{0:%Y}{0:%m}{0:%d}{0:%H}{0:%M}"
    
def open_files(outpath,time):
    time_s = time_format.format(time)
    fnall = outpath + time_s + '_all.bin.gz'
    
    fall = gzip.open(fnall, 'wb')
    return fall
    
def open_port(port,baud):
    ser = None
    while ser==None:
        try:
            ser = serial.Serial(port, baudrate=baud, timeout=1.1)  # open first serial port
        except serial.serialutil.SerialException:
            print "Can not open port, trying again in 5 second"
            ser = None
            time.sleep(5)
    print "Connected to",ser.portstr  # check which port is used
    return ser
    
def main(outpath,port,baud):
    line = ''
    ser = open_port(port,baud)
    start = datetime.utcnow().replace(second=0, microsecond=0)
    fall = open_files(outpath,start)
    
    while 1:
        dt = datetime.utcnow()
        if (dt - start).total_seconds() > 60:
            start = dt
            fall.close()
            fall = open_files(outpath,start)
            
        line = ser.read(32)
        if line != "":
            fall.write(line)
            
    ser.close() # close port
    fall.close()
    
if __name__== '__main__':
    outpath = sys.argv[1]
    port = sys.argv[2]
    baud = int(sys.argv[3])
    main(outpath,port,baud)
