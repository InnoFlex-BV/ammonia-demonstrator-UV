# ammonia-demonstrator-UV
UV module codes

This folder contains codes for:

- Control of UV lights (driver/relay/actuator)

## Files

- `main_UV.py` - Main entry point with task scheduler and signal handling
- `common_config.py` - Shared MQTT client and RS485/Modbus configuration
- `UV_Lights/converter_control.py` - LED converter control via Modbus

## Configuration

Hardcoded values in `common_config.py`:
- MQTT Broker: `192.168.0.89:1883`
- RS485 Port: `/dev/ttyRS485`
- Modbus slave address: `2` (in main_UV.py)

## Usage

```bash
python main_UV.py
```

The program subscribes to MQTT topic `master/uv/uv_intensity` and accepts intensity values 0-100 (%).

Graceful shutdown: `Ctrl+C` or `SIGTERM`

## Recent Changes

- Added signal handling (SIGINT/SIGTERM) for graceful shutdown
- Fixed typo: `LED_initialzation` -> `LED_initialization`
- Added input validation for intensity values (0-100%)
- Fixed misleading log messages (now shows both % and mV)
- Added type hints and docstrings
- Improved error handling throughout
