from machine import Pin

Pins={}

def setupPin(pin,mode,callbackIRQ=None,triggerIRQ=Pin.IRQ_RISING|Pin.IRQ_FALLING):
    p = Pin(pin,mode)
    if callbackIRQ is not None:
       p.irq(trigger=triggerIRQ,handler=callbackIRQ)
    return p

def addPin(id='default',pin=2,mode=Pin.OUT,callbackIRQ=None,triggerIRQ=Pin.IRQ_RISING|Pin.IRQ_FALLING):
    global Pins
    Pins[id] = setupPin(pin,mode,callbackIRQ,triggerIRQ)
    return Pins[id]

def getPin(id):
    return Pins[id]
