import minimalmodbus
import time

relay = minimalmodbus.Instrument('/dev/ttyRS485', 1)  # slave address = 1
relay.serial.baudrate = 9600
relay.serial.bytesize = 8
relay.serial.parity = minimalmodbus.serial.PARITY_NONE
relay.serial.stopbits = 1
relay.serial.timeout = 1
relay.mode = minimalmodbus.MODE_RTU


old_intensity = 0
new_intensity = None


broker_ip = "192.168.0.68"  # IP of Master
topic = "master/uv/uv_intensity"


def on_message(client, userdata, msg):
    global new_intensity
    new_intensity = int(float(msg.payload.decode()))


client = mqtt.Client("SlaveClient")
client.on_message = on_message

client.connect(broker_ip, 1883, 60)
client.subscribe(topic)

client.loop_start()


# set new intensity of uv lights
try:
    while True:
        if new_intensity is not None and new_intensity != old_intensity:
            # [ ___________________________________________________________ ] # <--- set intensity, using a function in another py
            print(f"Set UV lights intensity to {new_intensity}%")
            old_intensity = new_intensity
        sleep(1)

except KeyboardInterrupt:
    print("Exiting program...")
    relay.write_bits(registeraddress=0x00FF,value=0x0000,functioncode=5) #close all relays

finally:
    client.loop_stop()
    client.disconnect()
