from set_point import SetPointMQTT
from read_rs485 import read_HG803
from heater_control import HeaterController
import time


class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0
        self.prev_error = 0
        self.prev_time = time.time()


    def compute(self, setpoint, measurement):
        current_time = time.time()
        dt = current_time-self.prev_time
        if dt<0:
            dt = 1
        error = setpoint - measurement
        self.integral = self.integral + error*dt
        derivative = (error - self.prev_error)/dt

        output = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
        output = max(0, min(100, output))
        self.prev_error = error
        self.prev_time = current_time()
        return output


if __name__ == "__main__":
    PID = PIDController(Kp = 2, Ki = 0.1, Kd = 0.5)
    uv_heater = HeaterController()
    set_point_source = SetPointMQTT("192.168.0.68", "master/UV/UV_temp")

    try:
        while True:
            setpoint = set_point_source.get_set_point
            sensor_temp, humidity = read_HG803()
            output = PID.compute(setpoint, sensor_temp)
            uv_heater.set_new_output(output)
            time.sleep(60)

    except KeyboardInterrupt:
        print("Stopping ...")
        uv_heater.stop_heater()
