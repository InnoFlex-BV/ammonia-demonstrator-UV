import time
from common_config import create_device, create_client
from UV_Lights.converter_control import LED_Control



mqtt_client = create_client()
mqtt_client.loop_start()

""" create objects """
LED_converter = None



try:

    """  initializations of devices """
    LED_converter = LED_Control(slave_address=2, mqtt_topic="master/uv/uv_intensity", client = mqtt_client)
    LED_converter.LED_initialzation()
    time.sleep(1)

    """  start multi thread """
    tasks = [
        {"name": "LED Relay", "func": LED_converter.LED_control, "interval": 4, "next_run": 0},    
    ]


    while True:
        now = time.time()
        for t in tasks:
            if now  >= t["next_run"]:
                try:
                    t["func"]()
                except Exception as e:
                    print(f"Error in [{t['name']}]. Task {t['func'].__name__} error: {e}")
                t["next_run"] = now + t["interval"]
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n Exiting programm due to keyboard interrupt...")

except Exception as e:
    print(f"\nExiting program due to error: {e}")

finally:
    # cleanup all devices in RS485
       
    if LED_converter is not None:
        try:
            LED_converter.LED_stop()
        except Exception as e:
            print(f"Error stopping converter: {e}")


    print("All devices cleaned up.")