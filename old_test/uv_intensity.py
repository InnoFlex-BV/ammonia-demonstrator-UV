import minimalmodbus
import paho.mqtt.client as mqtt
from relay_control import RelayControl
import time

relay = minimalmodbus.Instrument('/dev/ttyRS485', 1)  # slave address = 1
relay.serial.baudrate = 9600
relay.serial.bytesize = 8
relay.serial.parity = minimalmodbus.serial.PARITY_NONE
relay.serial.stopbits = 1
relay.serial.timeout = 1
relay.mode = minimalmodbus.MODE_RTU


relay_ctrl = RelayControl(relay_instrument=relay)

old_intensity = 0
new_intensity = None


broker_ip = "192.168.0.207"  # IP of Master
topic = "master/uv/uv_intensity"


def on_message(client, userdata, msg):
    global new_intensity
    new_intensity = int(float(msg.payload.decode()))


client = mqtt.Client("SlaveClient")
client.on_message = on_message
client.connect(broker_ip, 1883, 60)
client.subscribe(topic)
client.loop_start()


## set new intensity of uv lights
try:
    while True:
        if new_intensity is not None and new_intensity != old_intensity:
            relay_ctrl.close_all_relay()
            relay_ctrl.open_certain_relay(16, new_intensity)
            print(f"Set UV lights intensity to {new_intensity}/16")
            old_intensity = new_intensity
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program...")
    relay.write_bit(registeraddress=0x00FF,value=0x0000,functioncode=5) #close all relays

finally:
    client.loop_stop()
    client.disconnect()
