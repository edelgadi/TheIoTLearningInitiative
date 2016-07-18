import mraa
import time

class TH02:
    x = None

    def __init__(self,pin):
        self.x = mraa.I2c(pin)
        self.x.address(0x40)

    def readTemperature(self):
        self.x.writeReg(0x03,0x11)
        while self.x.readReg(0x00) and 0x01:
             pass
        a = self.x.readBytesReg(0x01,2)
        return ((a[0]<<8)|a[1])/128.0-50.0

    def readHumidity(self):
        self.x.writeReg(0x03,0x01)
        while self.x.readReg(0x00) and 0x01:
             pass
        a = self.x.readBytesReg(0x01,2)
        return ((a[0]<<8)|a[1])/512.0-24.0

#a=TH02(1)
#while True:
#     print a.readTemperature()
#     print a.readHumidity()
