#!/usr/bin/python

import paho.mqtt.client as paho
import psutil
import pywapi
import dweepy
import signal
import sys
import time
import pyupm_grove as grove

from TH02 import *
from flask import Flask
from flask_restful import Api, Resource
from threading import Thread

DeviceID = "90b68610b05b"

#RESTFull support class
app = Flask(__name__)
api = Api(app)

class DataSensorRestApi(Resource):
    def get(self):
        data = 'Temperature: %d *C     '%sensTH.readTemperature()
        data = data + 'Humidity: %d%%     '%sensTH.readHumidity()
        data = data + 'Light: %d Lux'%sensL.value()
        return data
#End RESTFull support

sensTH = TH02(1)
sensL = grove.GroveLight(0)

def functionApiWeather():
    data = pywapi.get_weather_from_weather_com('MXJO0043', 'metric')
    message = data['location']['name']
    message = message + ", Temperature " + \
data['current_conditions']['temperature']
    message = message + ", Atmospheric Pressure " + \
data['current_conditions']['temperature']
    return message

def functionDataActuator(status):
    print "Data Actuator Status %s" % status

def functionDataActuatorMqttOnMessage(mosq, obj, msg):
    print "Data Sensor Mqtt Subscribe Message!"
    functionDataActuator(msg.payload)

def functionDataActuatorMqttSubscribe():
    mqttclient = paho.Client()
    mqttclient.on_message = functionDataActuatorMqttOnMessage
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/"+DeviceID+"/DataActuator", 0)
    while mqttclient.loop() == 0:
        pass

def functionDataSensor():
#    netdata = psutil.net_io_counters()
#    data = netdata.packets_sent + netdata.packets_recv
    temp = sensTH.readTemperature()
    hum = sensTH.readHumidity()
    lig = sensL.value()
    dweepy.dweet_for('IoT'+DeviceID, {'Temp':str(temp), \
'Hum':str(hum),'Lig':str(lig)})
    print dweepy.get_latest_dweet_for('IoT'+DeviceID)

def functionDataSensorMqttOnPublish(mosq, obj, msg):
    print "Data Sensor Mqtt Published!"

def functionDataSensorMqttPublish():
    mqttclient = paho.Client()
    mqttclient.on_publish = functionDataSensorMqttOnPublish
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    while True:
        data = functionDataSensor()
        topic = "IoT101/"+DeviceID+"DataSensor"
        mqttclient.publish(topic, data)
        time.sleep(1)

def functionSignalHandler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, functionSignalHandler)
    
    threadmqttpublish = Thread(target=functionDataSensorMqttPublish)
    threadmqttpublish.start()

    threadmqttsubscribe = Thread(target=functionDataActuatorMqttSubscribe)
    threadmqttsubscribe.start()

    api.add_resource(DataSensorRestApi, '/sensor')
    app.run(host='0.0.0.0', debug=True)

    while True:
        print "Hello Internet of Things 101"
        print "Data Sensor: %s " % functionDataSensor()
        print "API Weather: %s " % functionApiWeather()
        time.sleep(2)

# End of File
