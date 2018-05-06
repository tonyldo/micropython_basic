import network

def isConnected():
    return network.WLAN(network.STA_IF).isconnected()

def connect(ssid,password):
    if isConnected():
       return
    network.WLAN(network.STA_IF).active(True)
    network.WLAN(network.STA_IF).connect(ssid, password)
    print('Trying to connect...')
    while not isConnected():
        pass
 
    network.WLAN(network.AP_IF).active(False)
    print('Connection successful!')
    print(network.WLAN(network.STA_IF).ifconfig())

def disconnect():
    network.WLAN(network.STA_IF).disconnect
    network.WLAN(network.STA_IF).active(False)
    network.WLAN(network.AP_IF).active(True)
