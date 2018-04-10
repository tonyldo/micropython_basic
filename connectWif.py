import network
ssid = 'XT1580 9440'
password =  '51ad8166fa65'

def isConnected():
    return network.WLAN(network.STA_IF).isconnected()

def connect():
    if isConnected():
       return
    network.WLAN(network.STA_IF).active(True)
    network.WLAN(network.STA_IF).connect(ssid, password)
    print('Trying to connect...')
    while not isConnected():
        pass
 
    print('Connection successful!')
    print(network.WLAN(network.STA_IF).ifconfig())
