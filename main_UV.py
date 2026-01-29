import signal
import sys
import time

from common_config import create_client
from UV_Lights.converter_control import LED_Control


# Global flag for graceful shutdown
running = True


def signal_handler(signum, _frame):
    """Handle shutdown signals gracefully."""
    global running
    signal_name = signal.Signals(signum).name
    print(f"\nReceived {signal_name}, shutting down...")
    running = False


def main():
    global running

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    mqtt_client = create_client()
    mqtt_client.loop_start()

    led_converter = None

    try:
        # Initialize devices
        led_converter = LED_Control(
            slave_address=2,
            mqtt_topic="master/uv/uv_intensity",
            client=mqtt_client
        )
        led_converter.LED_initialization()
        time.sleep(1)

        # Task scheduler
        tasks = [
            {"name": "LED Control", "func": led_converter.LED_control, "interval": 4.0, "next_run": 0.0},
        ]

        print("Main loop started. Press Ctrl+C to exit.")

        while running:
            now = time.time()
            for task in tasks:
                if now >= task["next_run"]:
                    try:
                        task["func"]()
                    except Exception as e:
                        print(f"Error in [{task['name']}]: {e}")
                    task["next_run"] = now + task["interval"]
            time.sleep(0.01)

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

    finally:
        print("Cleaning up...")

        if led_converter is not None:
            try:
                led_converter.LED_stop()
            except Exception as e:
                print(f"Error stopping LED converter: {e}")

        try:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        except Exception as e:
            print(f"Error disconnecting MQTT client: {e}")

        print("All devices cleaned up.")


if __name__ == "__main__":
    main()