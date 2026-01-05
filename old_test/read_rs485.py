## assume using HG803 sensor, all the settings should be verified/changed
import minimalmodbus
from time import sleep


##settings for sensor reading
#sensor_level = minimalmodbus.Instrument('/dev/ttyUSB1',1) #port name, slave's modbus address
sensor_level = minimalmodbus.Instrument('/dev/ttyACM0',3) # in case of using USB flash disk, number = slave address
sensor_level.serial.baudrate = 9600                             # BaudRate
sensor_level.serial.bytesize = 8                                        # Number of data bits to be requested
sensor_level.serial.parity = minimalmodbus.serial.PARITY_NONE   # Parity Setting here is NONE but can be ODD or EVEN
sensor_level.serial.stopbits = 1                                        # Number of stop bits
sensor_level.serial.timeout  = 0.5                                      # Timeout time in seconds
sensor_level.mode = minimalmodbus.MODE_RTU                              # Mode to be used (RTU or ascii mode)


## encapsulation
def read_HG803():

    data =sensor_level.read_registers(0, 2, 3) # Starting Address, Quantity of Registers, Function code
    temperature = data[0]/100 # sensor data type = magnified 100 times
    humidity = data[1]/100
    return temperature, humidity


## if just run read_rs485.py
if __name__=="__main__":
    try:
        while True:
            temperature, humidity = read_HG803()
            print(f"Temperature: {temperature} degree, Humidity: {humidity} %")
            sleep(1)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
