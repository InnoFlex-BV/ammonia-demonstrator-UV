import threading
import time

import minimalmodbus
import paho.mqtt.client as mqtt


# Thread lock for RS485 serial communication
serial_lock = threading.Lock()

# MQTT configuration
BROKER_IP = "192.168.0.89"  # mDNS is not working on RevPi_4
BROKER_PORT = 1883
KEEPALIVE = 60

# RS485 configuration
PORT = "/dev/ttyRS485"

# Initialize MQTT client
common_client = mqtt.Client(client_id="UV_Pi")
common_client.connect(BROKER_IP, BROKER_PORT, KEEPALIVE)

# Device cache
devices: dict[int, minimalmodbus.Instrument] = {}


def create_device(slave_address: int) -> minimalmodbus.Instrument:
    """Create or return a cached Modbus device for the given slave address."""
    if slave_address in devices:
        return devices[slave_address]

    device = minimalmodbus.Instrument(PORT, slave_address)
    device.serial.baudrate = 9600
    device.serial.bytesize = 8
    device.serial.parity = minimalmodbus.serial.PARITY_NONE
    device.serial.stopbits = 1
    device.serial.timeout = 0.5
    device.mode = minimalmodbus.MODE_RTU

    devices[slave_address] = device
    return device


def create_client() -> mqtt.Client:
    """Return the shared MQTT client instance."""
    return common_client


def clear_RS485(device: minimalmodbus.Instrument) -> None:
    """Clear the RS485 serial buffers."""
    try:
        device.serial.reset_input_buffer()
        device.serial.reset_output_buffer()
    except Exception as e:
        print(f"[RS485] Clear warning: {e}")


def strong_clear_RS485(device: minimalmodbus.Instrument) -> None:
    """Perform a strong clear of RS485 buffers with sync bytes."""
    try:
        device.serial.reset_input_buffer()
        device.serial.reset_output_buffer()
        device.serial.write(b'\xFF' * 4)
        time.sleep(0.05)
    except Exception as e:
        print(f"[RS485] Strong clear warning: {e}")