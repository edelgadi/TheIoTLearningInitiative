import mraa
import time

class TH02:
    x = None

    def __init__(self,pin):
        self.x = mraa.I2c(pin)
        self.x.address(0x40)

    def readTemperature(self):
        self.x.writeReg(0x03,0x11)
        while self.x.readReg(0x00) & 0x01:
             pass
        a = self.x.readBytesReg(0x01,2)
        #Accord with data sheet the last 2 bits are trash
        b = ((a[0]<<8)|a[1])>>2
        return (b/32.0)-50.0

    def readHumidity(self):
        self.x.writeReg(0x03,0x01)
        while self.x.readReg(0x00) & 0x01:
             pass
        a = self.x.readBytesReg(0x01,2)
        #Accord with data sheet the last 4 bits are trash
        b = ((a[0]<<8)|a[1])>>4
        return (b/16.0)-24.0

'''
a=TH02(1)
while True:
    print "T %d" %a.readTemperature()
    print "H %d" %a.readHumidity()
    time.sleep(1)
'''
