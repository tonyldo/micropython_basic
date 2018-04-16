import connectWifi
import umqttClient
import micropython

from machine import Pin
from machine import Timer

micropython.alloc_emergency_exception_buf(100)

PIN_OUT = const(2)
PIN_IN  = const(0)

pinOut = None
pinIn = None
newValue = None
command = None
timer = None

STATE_LAMP_TOPIC  = b'/lamp/state'
SWITCH_LAMP_TOPIC = b'/lamp/switch'

DICT_MSG_IN = {b'ON': 0, b'OFF' : 1}
DICT_MSG_OUT = {0: b'ON', 1 : b'OFF'}

def cleanCommand():
    global command
    command = 'check'
    print ('Wait commands...')

def setupPins():
    global pinOut, pinIn
    if pinOut is not None or pinIn is not None:
       return

    print ('Setup Pins...')
    pinOut = Pin(PIN_OUT,Pin.OUT)
    pinIn = Pin(PIN_IN,Pin.IN)
    pinIn.irq(handler=pinInPressCallback)

def setupTimer():
    global timer
    if timer is None:
       timer = Timer(-1)
       timer.init(period=2000, mode=Timer.PERIODIC, callback=timerSenderStateCallback)

def pinInPressCallback(pin):
    global command,newValue
    command = 'toggle'
    newValue = int(not pinOut.value())

def mqttSubcristionCallback(topic,msg):
    global command,newValue
    command = 'toggle'
    newValue = DICT_MSG_IN[msg]

def timerSenderStateCallback(timer):
    global command
    command = 'send'

def sendMQTTStateLamp():
    print ('Enter sendMQTTStateLamp method, pinOUt state: ', DICT_MSG_OUT[pinOut.value()])
    umqttClient.getMQTT().publish(STATE_LAMP_TOPIC,DICT_MSG_OUT[pinOut.value()])

    cleanCommand()


def checkMQTTMsg():
    umqttClient.getMQTT().check_msg()


def toggleSwitch():
    print ('Enter toogleSwitch method, newValue / pinOut.value(): ',newValue,' / ',pinOut.value())
    if newValue!=pinOut.value():
       pinOut.value(newValue)

    cleanCommand()

def setup():
    print ('Enter setup method...')
    setupPins()
    connectWifi.connect()
    umqttClient.getMQTT(callbackFunction=mqttSubcristionCallback).connect()
    umqttClient.getMQTT().subscribe(SWITCH_LAMP_TOPIC)
    setupTimer()

    cleanCommand()


def main():
    print ('Enter main method...')
    global command
    command = 'setup'

    while True:
        try:
           {'setup':setup, 'toggle':toggleSwitch, 'check':checkMQTTMsg, 'send':sendMQTTStateLamp}[command]()
        except Exception as e:
           print ('Error: ',e)
           command = 'setup'


if (__name__) == '__main__':
   main()
