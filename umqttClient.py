from simple import MQTTClient
import machine
import ubinascii

broker = 'm14.cloudmqtt.com'
brokerPort = 17769
clientID = b'esp_'+ubinascii.hexlify(machine.unique_id())
user = 'albjxxal'
password = 'nCNxNNZNlsWP'
mqttClient = None

def getMQTT(callbackFunction=None):
    global mqttClient 
    if mqttClient is None:
       mqttClient = MQTTClient(clientID,broker,port=brokerPort,user=user,password=password)
       if callbackFunction is not None:
          mqttClient.set_callback(callbackFunction)
    return mqttClient
