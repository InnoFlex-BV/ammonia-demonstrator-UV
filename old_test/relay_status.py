import minimalmodbus
import time



relay = minimalmodbus.Instrument('/dev/ttyRS485', 1)  # slave address = 1
relay.serial.baudrate = 9600
relay.serial.bytesize = 8
relay.serial.parity = minimalmodbus.serial.PARITY_NONE
relay.serial.stopbits = 1
relay.serial.timeout = 1
relay.mode = minimalmodbus.MODE_RTU


# read relay stauts
print("Relay status \n")
for reg in range(0,16):
    try:
        value = relay.read_bits(registeraddress=reg, number_of_bits=1, functioncode=1)
        print(f"Relay {reg+1}: {'ON' if value[0] else 'OFF'}")
    except Exception as e:
        print(f"Relay {reg+1} | Error -> {e}")
        break


uart_value = relay.read_register(registeraddress=0x2000, functioncode=3)
print(f"Raw UART register value: 0x{uart_value:04X}")

slave_address = relay.read_register(registeraddress=0x4000, functioncode=3)

# high 8 bits -> parity mode; low 8 bits -> baud rate mode
parity_mode = (uart_value >> 8) & 0xFF
baudrate_mode = uart_value & 0xFF

# baud rate correspondence
baudrate_dict = {0:4800,1:9600,2:19200,3:38400,4:57600,5:115200,6:128000,7:256000}
parity_dict = {0:'N',1:'O',2:'E'}

print(f"Baudrate: {baudrate_dict.get(baudrate_mode,'Unknown')}, Parity: {parity_dict.get(parity_mode,'Unknown')}, Slave Address: {slave_address}")
