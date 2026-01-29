from common_config import create_device, create_client, strong_clear_RS485, serial_lock
import time


MIN_INTENSITY = 0
MAX_INTENSITY = 100
MV_PER_PERCENT = 100  # 100% = 10000mV (10V max analog output)


class LED_Control:
    def __init__(self, slave_address: int, mqtt_topic="master/UV/uv_intensity", client=None):
        self.slave_address = slave_address
        self.device = None
        self.old_intensity_mv = 0
        self.new_intensity_mv = None
        self.lock = serial_lock

        # MQTT settings
        if client is None:
            self.client = create_client()
            self.client.loop_start()
        else:
            self.client = client

        self.topic = mqtt_topic
        self.client.message_callback_add(self.topic, self._on_message)
        self.client.subscribe(self.topic)

    def LED_initialization(self):
        """Initialize the LED converter with all outputs set to 0."""
        self.device = create_device(self.slave_address)
        self.device.serial.timeout = 1
        with self.lock:
            strong_clear_RS485(self.device)
            init_values = [0] * 8
            self.device.write_registers(registeraddress=0x0000, values=init_values)
        time.sleep(0.25)
        print("[LED Control] LED output initialized.")


    def _on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages for UV intensity control."""
        try:
            payload = msg.payload.decode().strip()
            uv_intensity = int(float(payload))

            if uv_intensity < MIN_INTENSITY or uv_intensity > MAX_INTENSITY:
                print(f"[LED Control] Invalid intensity {uv_intensity}%, must be {MIN_INTENSITY}-{MAX_INTENSITY}")
                return

            self.new_intensity_mv = uv_intensity * MV_PER_PERCENT
            print(f"[LED Control] Received intensity: {uv_intensity}% ({self.new_intensity_mv}mV)")
        except ValueError as e:
            print(f"[LED Control] Invalid payload '{msg.payload}': {e}")
        except Exception as e:
            print(f"[LED Control] Error processing message: {e}")

    def LED_control(self):
        """Apply new intensity if changed. Called periodically from main loop."""
        if self.device is None:
            print("[LED Control] Device not initialized.")
            return

        if self.new_intensity_mv is not None and self.new_intensity_mv != self.old_intensity_mv:
            try:
                with self.lock:
                    ao_values = [self.new_intensity_mv] * 8
                    self.device.write_registers(registeraddress=0x0000, values=ao_values)
                    time.sleep(0.1)
                intensity_percent = self.new_intensity_mv // MV_PER_PERCENT
                print(f"[LED Control] Set UV intensity to {intensity_percent}% ({self.new_intensity_mv}mV)")
                self.old_intensity_mv = self.new_intensity_mv
            except Exception as e:
                print(f"[LED Control] Failed to set intensity: {e}")

    def LED_stop(self):
        """Stop LED output and clean up resources."""
        if self.device is None:
            print("[LED Control] Device not initialized, skipping stop.")
            return

        try:
            with self.lock:
                stop_values = [0] * 8
                self.device.write_registers(registeraddress=0x0000, values=stop_values)
            print("[LED Control] LEDs OFF. UV intensity = 0")
        except Exception as e:
            print(f"[LED Control] Error stopping LEDs: {e}")