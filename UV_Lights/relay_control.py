from common_config import create_device, create_client, clear_RS485, strong_clear_RS485, serial_lock
import time



class LED_Control:
    def __init__(self, slave_address:int, mqtt_topic="master/UV/uv_intensity", client = None):
        # create an object
        self.slave_address = slave_address
        self.device = None
        self.old_intensity = 0
        self.new_intensity = None
        self.lock = serial_lock

        # MQTT settings
        if client is None:
            self.client = create_client()
            self.client.loop_start()
        else:
            self.client = client

        self.topic = mqtt_topic
        self.client.message_callback_add(self.topic, self.on_message)
        self.client.subscribe(self.topic)


    def LED_initialzation(self):
        self.device = create_device(self.slave_address)
        self.device.serial.timeout = 1
        with self.lock:
            strong_clear_RS485(self.device)
            print("do some initialization")
            # self.device.write_bit(registeraddress=0x0000, value=0, functioncode=5)
        time.sleep(0.25)
        print("LED relay innitialized.")


    def on_message(self, client, userdata, msg):
        try:
            uv_intensity = int(float(msg.payload.decode()))
            self.new_intensity = uv_intensity
            print(f"[LED Control] Received new intensity {self.new_intensity}%")
        except Exception as e:
            print(f"Error: {e}")

    
    def LED_control(self):
        if self.device is None:
            print("[LED Control] LED relay not initialized.")
            return

        if self.new_intensity is not None and self.new_intensity != self.old_intensity:
            with self.lock:
                # clear_RS485(self.device)
                # self.new_pump_speed = int(2.55*self.new_pump_pwm) # 0%-100% -> 0-255
                # reg1 = (1 << 8) + 1
                # reg2 = (self.new_pump_speed << 8) + 10
                # self.device.write_registers(registeraddress=0x03e8, values = [reg1, reg2])
                print(f"doing something to make UV intensity {self.new_intensity}.")
                time.sleep(0.2)
                print(f"[LED Control] Set UV intensity to {self.new_intensity}%")
                self.old_intensity = self.new_intensity
    

    def LED_stop(self):
        with self.lock:
            # self.device.write_registers(registeraddress=0x03e8, values = [self.stop_reg1, self.stop_reg2])
            print(f" Do something to turn off LEDs.")
            self.client.loop_stop()
            self.client.disconnect()
            print("[LED Control] LEDs OFF. UV intensity = 0 ")