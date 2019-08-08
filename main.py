import connectWifi
import umqttClient
import machine
import time

ssid = 'wifiSSID'
password =  'WifiPass'

LWT  = b'/ringbell/gosleep'
ring_bell_topic = b'/ringbell/status'

DICT_MSG_OUT = {0: b'ON', 1 : b'OFF'}

def ring_bell():
    print ('Enter sendRingBellStatus method: ', DICT_MSG_OUT[0])
    umqttClient.getMQTT().publish(ring_bell_topic,DICT_MSG_OUT[0], retain=False, qos=1)

def setup():
    print ('Enter setup method...')
    connectWifi.connect(ssid,password)
    umqttClient.getMQTT().connect()

def main():
    print ('Enter main method...')
    try:
      setup()
      ring_bell()
      time.sleep(3) 
      machine.deepsleep()
    finally:
       if not umqttClient.getMQTT(): 
          umqttClient.getMQTT().disconnect()
       connectWifi.disconnect()

if (__name__) == '__main__':
   main()
