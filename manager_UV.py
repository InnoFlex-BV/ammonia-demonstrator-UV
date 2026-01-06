import paho.mqtt.client as mqtt
import subprocess
import signal
import socket
import time


broker_ip = "192.168.0.89" # rev_Pi has no mDNS support, so name with ".local" cannot work. SO it need to use number IP such as "192.168.x.x"
topic_control = "master/uv/control"
topic_status = "slave/uv/status"
main_script_path  = "/home/innoflex/ammonia-demonstrator-UV/main_test.py"
UV_process = None


def on_message(client, userdata, msg):
    global UV_process
    command = msg.payload.decode().upper()

    if command == "START":
        if UV_process is None or UV_process.poll() is not None:
            print("Starting main_UV.py ...")
            UV_process = subprocess.Popen(["python3", main_script_path])
            client.publish(topic_status, "RUNNING", retain=True)

    elif command == "STOP":
        if UV_process and UV_process.poll() is None:
            print("Stopping main_UV.py ...")
            UV_process.send_signal(signal.SIGINT)
            UV_process.wait()
            UV_process = None
            client.publish(topic_status, "STOPPED", retain=True)
            print("UV Module Stopped")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic_control)
    client.publish(topic_status, "STOPPED", retain=True)


"""initialize MQTT"""
client = mqtt.Client(client_id="UVPi_manager")
client.on_connect = on_connect
client.on_message = on_message
client.will_set(topic_status, "OFFLINE", retain=True) # in case of that UV_pi is not working


"""Re-do if DNS or MQTT went wrong"""
while True:
    try:
        print("Trying to connect to MQTT broker...")
        client.connect(broker_ip, 1883, 60)
        print("MQTT Connected")
        break
    except socket.gaierror:
        print("DNS not ready.")
    except Exception as e:
        print(f"Connection Failed: {e}")

    time.sleep(5)

client.loop_forever()
