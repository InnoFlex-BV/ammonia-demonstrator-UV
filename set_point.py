## this code reads the goal from master_pi and set it as target set-point in (low level logic) PID control loop of temperature
import paho.mqtt.client as mqtt
import time


class SetPointMQTT:
    def __init__(self, broker_ip, topic):
        self.broker_ip = "192.168.0.68"  # IP of Master
        self.topic = "master/UV/UV_temp"
        self.old_temp = 0
        self.new_temp = None

        self.client = mqtt.Client("SlaveClient")
        self.client.on_message = self.on_message

        self.client.connect(self.broker_ip, 1883, 60)
        self.client.subscribe(self.topic)
        self.client.loop_start()


    def on_message(self, client, userdata, msg):
        self.new_temp = float(msg.payload.decode())


    def get_set_point(self):
        return self.new_temp


    def run(self):
        try:
            while True:
                if new_temp is not None and new_temp != old_temp:
                    print(f"Set setpoint to {new_temp}%")
                    old_temp = new_temp
                time.sleep(60)

        except KeyboardInterrupt:
            print("Exiting program...")

        finally:
            client.loop_stop()
            client.disconnect()



## just run set_point.py
if __name__ == "__main__":
    controller = SetPointController("192.168.0.68", "master/UV/UV_temp")
    controller.run()
