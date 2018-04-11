import connectWifi
import umqttClient
import time
from machine import Pin

PIN_OUT = const(2)
PIN_IN  = const(0)

pinOut = None
pinIn = None
pinInValue = None

STATE_LAMP_TOPIC  = b'/lamp/state'
SWITCH_LAMP_TOPIC = b'/lamp/switch'

DICT_MSG_IN = {b'ON': 0, b'OFF' : 1}
DICT_MSG_OUT = {0: b'ON', 1 : b'OFF'}
mqttMsg = None

mqttCommand = None
pressButtonCommand = None
setupCommand = None

def cleanCommands():
    print ('Clean Commands!')
    global mqttCommand, pressButtonCommand, setupCommand, mqttMsg
    mqttCommand = False
    pressButtonCommand = False
    setupCommand = False
    mqttMsg = b'NONE'
    print ('Waiting for new commands...')

def setupPins():
    global pinOut, pinIn
    if pinOut is not None or pinIn is not None:
       return

    print ('Setup Pins...')
    pinOut = Pin(PIN_OUT,Pin.OUT)
    pinIn = Pin(PIN_IN,Pin.IN)
    pinIn.irq(handler=pinInPressCallback)
    pinOut.value(pinIn.value())

def pinInPressCallback(pin):
    global pressButtonCommand,pinInValue
    pressButtonCommand = True
    #pinInValue = pin.value()
    pinInValue = int(not pinOut.value())

def mqttSubcristionCallback(topic,msg):
    global mqttCommand,mqttMsg
    mqttCommand = True
    mqttMsg = msg

def sendMQTTStateLamp():
     print ('Enter sendMQTTStateLamp method, pinOUt state: ', DICT_MSG_OUT[pinOut.value()])
     umqttClient.getMQTT().publish(STATE_LAMP_TOPIC,DICT_MSG_OUT[pinOut.value()])

def toogleSwitch(newValue):
    print ('Enter toogleSwitch method, newValue / pinOut.value(): ',newValue,' / ',pinOut.value())
    if newValue!=pinOut.value():
       pinOut.value(newValue)
       sendMQTTStateLamp()
    cleanCommands()

def setup():
    print ('Enter setup method...')
    setupPins()
    connectWifi.connect()
    umqttClient.getMQTT(callbackFunction=mqttSubcristionCallback).connect()
    umqttClient.getMQTT().subscribe(SWITCH_LAMP_TOPIC)
    sendMQTTStateLamp()
    cleanCommands()

def main():
    print ('Enter main method...')
    global setupCommand
    setupCommand = True

    while True:
          try:
             if setupCommand:
                setup()
             elif mqttCommand and mqttMsg in DICT_MSG_IN:
                print ('Executing MQTT command!')
                toogleSwitch(DICT_MSG_IN[mqttMsg])
             elif pressButtonCommand:
                print ('Executing Button command!')
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
