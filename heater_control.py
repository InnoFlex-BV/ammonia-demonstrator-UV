import minimalmodbus
from time import sleep



class HeaterController:
    def __init__(self):
        # setting for heater controller MVSS1 Modbus
        self.uv_heater = minimalmodbus.Instrument('/dev/ttyACM0', 4) #termianl & slave address
        self.uv_heater.serial.baudrate = 9600
        self.uv_heater.serial.bytesize = 8
        self.uv_heater.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.uv_heater.serial.stopbits = 1
        self.uv_heater.serial.timeout = 0.5
        self.uv_heater.mode = minimalmodbus.MODE_RTU
        self.old_output = 0
        self.new_output = None


    def set_new_output(self, new_value):
        # set output of heater
        if new_output is not None and new_output != old_output:
            self.uv_heater.write_register(registeraddress=30, value=new_output,functioncode=6) # set output
            print(f"Set UV_heater to {new_output}%")
            self.old_output = new_output


    def stop_heater(self):
        # stop the heater, output->0%
        print("Stop Heating ...")
        uv_heater.write_register(registeraddress=30,value=0,functioncode=6)
