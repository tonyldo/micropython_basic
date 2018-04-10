import connectWifi
import umqttClient
import time
from machine import Pin

PIN_OUT = const(2)
PIN_IN  = const(5)

pinOut = None
pinIn = None
pinInValue

STATE_LAMP_TOPIC  = const(b'/lamp/state')
SWITCH_LAMP_TOPIC = const(b'/lamp/switch')

DICT_MSG_IN = {b'ON': 1, b'OFF' : 0}
DICT_MSG_OUT = {1: b'ON', 0 : b'OFF'}
mqttMsg

mqttCommand
pressButtonCommand
setupCommand

def cleanCommands():
    global mqttCommand, pressButtonCommand, setupCommand, mqttMsg
    mqttCommand = False
    pressButtonCommand = False
    setupCommand = False
    mqttMsg = b'NONE'

def setupPins():
    global pinOut, pinIn
    if pinOut is None:
       pinOut = Pin(PIN_OUT,Pin.OUT)
    if pinIn is None:
       pinIn = Pin(PIN_IN,Pin.IN)
       pinIn.irq(handler=pinInPressCallback)

def pinInPressCallback(pin):
    global pressButtonCommand,pinInValue
    pressButtonCommand = True
    pinInValue = not pin.value()
        
def mqttSubcristionCallback(topic,msg):
    global mqttCommand,mqttMsg
    mqttCommand = True
    mqttMsg = msg

def sendMQTTStateLamp():
     print ('Enter sendMQTTStateLamp method, pinOUt state: ',pinOut.value())
     umqttClient.getMQTT().publish(STATE_LAMP_TOPIC,DICT_MSG_OUT[pinOut.value()])

def toogleSwitch(newValue):
    print ('Enter toogleSwitch method, newValue /pinOut.value(): ',newValue,' / ',pinOut.value())
    if newValue!=pinOut.value():
       pinOut.value(newValue)
       sendMQTTStateLamp()
       cleanCommands()
    
    
def setup():
    print 'Enter setup method...'
    setupPins()
    connectWifi.connect()
    umqttClient.getMQTT(callbackFunction=mqttSubcristionCallback).connect()
    umqttClient.getMQTT().subscribe(SWITCH_LAMP_TOPIC)
    sendMQTTStateLamp()
    cleanCommands()

def main():
    print 'Enter main method...'
    global setupCommand
    setupCommand = True

    while True:
          try:
             if setupCommand:
                setup()
             elif mqttCommand and mqttMsg in DICT_MSG_IN: 
                toogleSwitch(DICT_MSG_IN[mqttMsg])
             elif pressButtonCommand:
                toogleSwitch(pinInValue)
             else:
                pass

             umqttClient.getMQTT().check_msg()
          except Exception as e:
             print ('Error: ',e)
             setupCommand = True

          time.sleep(1)
         
if (__name__) == '__main__':
   main()
