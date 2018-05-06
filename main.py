import connectWifi
import umqttClient
import micropython

from machine import Pin
from machine import Timer

micropython.alloc_emergency_exception_buf(100)

ssid = 'XT1580 9440'
password =  '51ad8166fa65'

PIN_OUT = const(2)
PIN_IN  = const(5)

pinOut = None
pinIn = None
newValue = None
command = None
timer = None

STATE_LAMP_TOPIC  = b'/lamp/state'
SWITCH_LAMP_TOPIC = b'/lamp/switch'

DICT_MSG_IN = {b'ON': 0, b'OFF' : 1}
DICT_MSG_OUT = {0: b'ON', 1 : b'OFF'}

def setupPins():
    global pinOut, pinIn
    if pinOut is not None or pinIn is not None:
       return
    print ('Setup Pins...')
    pinOut = Pin(PIN_OUT,Pin.OUT,value=1)
    pinIn = Pin(PIN_IN,Pin.IN)
    pinIn.irq(handler=pinInPressCallback)

def setupTimer():
    global timer
    if timer is None:
       timer = Timer(-1)
       timer.init(period=2000, mode=Timer.PERIODIC, callback=timerCallback)

def cleanCommand():
    global command
    command = 'pass'

def pinInPressCallback(pin):
    global command,newValue
    command = 'toggleByPress'
    newValue = int(not pinOut.value())

def timerCallback(timer):
    global command
    command = 'check'

def mqttSubcristionCallback(topic,msg):
    global command,newValue
    command = 'toggleByMQTT'
    newValue = DICT_MSG_IN[msg]

def checkAndSendMQTTMsg():
    umqttClient.getMQTT().check_msg()
    if (command == 'toggleByMQTT'):
       return
    sendState()

def sendState()
    print ('Enter sendMQTTStateLamp method, pinOUt state: ', DICT_MSG_OUT[pinOut.value()])
    umqttClient.getMQTT().publish(STATE_LAMP_TOPIC,DICT_MSG_OUT[pinOut.value()])
    cleanCommand()


def toggleSwitch():
    print ('Enter toogleSwitch method, newValue / pinOut.value(): ', DICT_MSG_OUT[newValue],' / ',DICT_MSG_OUT[pinOut.value()])
    if newValue!=pinOut.value():
       pinOut.value(newValue)
    sendState()

def setup():
    print ('Enter setup method...')
    setupPins()
    connectWifi.connect(ssid,password)
    umqttClient.getMQTT(callbackFunction=mqttSubcristionCallback).connect()
    umqttClient.getMQTT().subscribe(SWITCH_LAMP_TOPIC)
    setupTimer()
    cleanCommand()

def main():
    print ('Enter main method...')
    global command
    command = 'setup'
    try:
       while True:
          try:
              {'setup':setup, 'toggleByPress':toggleSwitch, 'toggleByMQTT':toggleSwitch, 'check':checkAndSendMQTTMsg, 'pass':lambda : None}[command]()
          except Exception as e:
              print ('Error: ',e)
              command = 'setup'
    finally:
       umqttClient.getMQTT().disconnect()
       connectWifi.disconnect()

if (__name__) == '__main__':
   main()
