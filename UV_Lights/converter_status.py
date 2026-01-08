import minimalmodbus
from time import sleep


device = minimalmodbus.Instrument('/dev/ttyRS485', 2)
device.serial.baudrate = 9600
device.serial.bytesize = 8
device.serial.parity = minimalmodbus.serial.PARITY_NONE
device.serial.stopbits = 1
device.serial.timeout = 1
device.mode = minimalmodbus.MODE_RTU



# change settings
try:
    for addr in range(0, 8):
        value = device.read_register(addr)
        print(f"4x{str(addr).zfill(4)} = {value}")
        sleep(0.1)

except Exception as e:
    print(f"{type(e).__name__}: {e}")

print("\n Done.")