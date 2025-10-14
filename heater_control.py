import minimalmodbus
from time import sleep

# setting for heater controller MVSS1
uv_heater = minimalmodbus.Instrument('/dev/ttyACM0', 4)
uv_heater.serial.baudrate = 9600
uv_heater.serial.bytesize = 8
uv_heater.serial.parity = minimalmodbus.serial.PARITY_NONE
uv_heater.serial.stopbits = 1
uv_heater.serial.timeout = 0.5
uv_heater.mode = minimalmodbus.MODE_RTU


old_output = 0
new_output = None

# set output of heater
try:
    while True:
        if new_output is not None and new_output != out_output:
            uv_heater.write_register(registeraddress=30, value=new_speed,functioncode=6) # set output
            print(f"Set fan speed to {new_speed}%")
            old_output = new_output
        sleep(60)

except KeyboardInterrupt:
    print("Exiting program...")
    uv_heater.write_register(registeraddress=30,value=0,functioncode=6)
