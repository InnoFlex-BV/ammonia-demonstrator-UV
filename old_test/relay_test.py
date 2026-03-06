import serial
import sys
sys.path.append('/home/innoflex/ammonia-demonstrator-UV')
from calculate_CRC import calc_crc
import time


ser = serial.Serial(port='/dev/ttyRS485',
                    baudrate=9600,
                    bytesize=8,
                    parity='N',
                    stopbits=1,
                    timeout=1)

slave_address = 0x01
functioncode = 0x05
relay_channel = 0x0201
delay_time = 3 # [s]

frame = bytearray()
string2 = "01 05 00 00 00 00"

try:
    frame.append(slave_address)
    frame.append(functioncode)
    frame += relay_channel.to_bytes(2, 'big')
    value_time = int(delay_time*10)
    frame += value_time.to_bytes(2, 'big')
    frame += calc_crc(frame)


    frame2 = bytearray.fromhex(string2)
    frame2 += calc_crc(frame2)

    ser.write(frame)
    print("Sent.")
    response = ser.read(8)
    print("Response:", response.hex())


except Exception as e:
    print(f"{type(e).__name__}: {e}")

print("\n Done.")

