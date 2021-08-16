import network #network library to wirelessly access things
import ubinascii #to decode the mac address
print("start1v2")
#my wifi
station = network.WLAN(network.STA_IF)#declare station interface
station.active(True) #activate the interface
#your wifi name,        ,   wifi password
#station.scan()
station.connect("Sssml1", "deadbeef0123456789abcdef01")#only connects to 2.4GHz
#print("nearby stations", station.scan())
print("start2")
if(station.isconnected()):
    print("Station connected!")
    print('network config:', station.ifconfig()) # Print IP address
    # ifconfig is linux eqvt to ipconfig for windows
    print('MAC address:', station.config('mac')) #original form
    mac = ubinascii.hexlify(station.config('mac'),':').decode()
    print('MAC address (decoded):', mac)

# The last two lines are used to print out the mac address

print("end")


