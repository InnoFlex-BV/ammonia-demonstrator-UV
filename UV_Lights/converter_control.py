from common_config import create_device, create_client, strong_clear_RS485, serial_lock
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
            init_values = [0]*8
            self.device.write_registers(registeraddress=0x0000, values=init_values)
        time.sleep(0.25)
        print("LED output innitialized.")


    def on_message(self, client, userdata, msg):
        try:
            uv_intensity = int(float(msg.payload.decode()))
            self.new_intensity = uv_intensity*100 # max analog voltage output: 10V = 10000mV (when uv_intensity=100%)
            print(f"[LED Control] Received new intensity {self.new_intensity}%")
        except Exception as e:
            print(f"Error: {e}")

    
    def LED_control(self):
        if self.device is None:
            print("[LED Control] LED relay not initialized.")
            return

        if self.new_intensity is not None and self.new_intensity != self.old_intensity:
            with self.lock:
                ao_values = [self.new_intensity]*8
                self.device.write_registers(registeraddress=0x0000, values=ao_values)
                time.sleep(0.1)
                print(f"[LED Control] Set UV intensity to {self.new_intensity} %")
                self.old_intensity = self.new_intensity
    

    def LED_stop(self):
        with self.lock:
            stop_values = [0]*8
            self.device.write_registers(registeraddress=0x0000, values=stop_values)
            self.client.loop_stop()
            self.client.disconnect()
            print("[LED Control] LEDs OFF. UV intensity = 0 ")