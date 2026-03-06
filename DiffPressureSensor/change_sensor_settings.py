import minimalmodbus
from time import sleep


device = minimalmodbus.Instrument('/dev/ttyRS485', 39)
device.serial.baudrate = 9600
device.serial.bytesize = 8
device.serial.parity = minimalmodbus.serial.PARITY_NONE
device.serial.stopbits = 1
device.serial.timeout = 1
device.mode = minimalmodbus.MODE_RTU



# change settings
try:
    # device.write_register(registeraddress=0x0000, value=39, functioncode=6) # change slave address to 39
    device.write_register(registeraddress=0x0002, value=4, functioncode=6) # always Pa
    device.write_register(registeraddress=0x0003, value=0, functioncode=6) # 0-4 decimal points

    sleep(0.1)
except Exception as e:
    print(f"{type(e).__name__}: {e}")

print("\n Done.")