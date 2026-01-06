import random
import time
import paho.mqtt.client as mqtt

broker_ip = "192.168.0.89" 
topic = "slave/uv/test"
client_id = "UV_Pi_manager"

client = mqtt.Client(client_id=client_id)

try:
    client.connect(broker_ip, 1883, 60)
    client.loop_start()
    while True:
        test_value = random.randint(0, 5)
        client.publish(topic, payload=test_value)
        # print(f"[Test] Published: {test_value}")
        time.sleep(3)

except KeyboardInterrupt:
    print("\n Exiting programm due to keyboard interrupt...")
except Exception as e:
    print(f"Error: {e}")
finally:
    client.loop_stop()
    client.disconnect()
    print("Disconnected.")