import board
import busio
import digitalio

from adafruit_pca9685 import PCA9685

from config import (
    SERVO_CHANNELS,
    SERVO_LIMITS,
    SERVO_CALIBRATION,
    INITIAL_POSITIONS,
    PWM_FREQUENCY,
    I2C_ADDRESS,
)


class PCA9685Controller:

    def __init__(self):

        self.positions = INITIAL_POSITIONS.copy()
        self.emergency_stopped = True
        self.closed = False

        # Configure OE first.
        # OE is active LOW, so HIGH disables outputs.
        self.oe = digitalio.DigitalInOut(board.D4)
        self.oe.direction = digitalio.Direction.OUTPUT
        self.oe.value = True

        # Initialise I2C and PCA9685.
        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.pca = PCA9685(
            self.i2c,
            address=I2C_ADDRESS
        )

        self.pca.frequency = PWM_FREQUENCY


        for channel in range(SERVO_CHANNELS):

            self._validate_calibration(channel)

            self.pca.channels[channel].duty_cycle = 0

    

    def _validate_calibration(self, channel):

        if channel not in SERVO_LIMITS:
            raise ValueError(
                f"Missing angle limits for channel {channel}."
            )

        if channel not in SERVO_CALIBRATION:
            raise ValueError(
                f"Missing PWM calibration for channel {channel}."
            )

        min_angle, max_angle = SERVO_LIMITS[channel]

        min_pulse = SERVO_CALIBRATION[channel]["min_pulse"]
        max_pulse = SERVO_CALIBRATION[channel]["max_pulse"]

        period_us = 1_000_000 / PWM_FREQUENCY

        if min_angle >= max_angle:
            raise ValueError("Invalid servo angle limits.")

        if not 0 < min_pulse < max_pulse < period_us:
            raise ValueError(
                f"Invalid PWM calibration for channel {channel}."
            )

    def _angle_to_duty_cycle(self, channel, angle):

        min_angle, max_angle = SERVO_LIMITS[channel]

        calibration = SERVO_CALIBRATION[channel]

        min_pulse = calibration["min_pulse"]
        max_pulse = calibration["max_pulse"]

        angle_ratio = (
            (angle - min_angle) /
            (max_angle - min_angle)
        )

        pulse_width = (
            min_pulse +
            angle_ratio * (max_pulse - min_pulse)
        )

        period_us = 1_000_000 / PWM_FREQUENCY

        duty_cycle = round(
            (pulse_width / period_us) * 65535
        )

        return max(0, min(65535, duty_cycle))



    def set_angle(self, channel, angle):

        if self.closed:
            raise RuntimeError("Controller is closed.")

        if self.emergency_stopped:
            raise RuntimeError(
                "Emergency stop is active."
            )

        if type(channel) is not int:
            raise ValueError("Channel must be an integer.")

        if channel not in range(SERVO_CHANNELS):
            raise ValueError("Invalid servo channel.")

        if isinstance(angle, bool) or not isinstance(angle, (int, float)):
            raise ValueError("Angle must be numeric.")

        min_angle, max_angle = SERVO_LIMITS[channel]

        if not min_angle <= angle <= max_angle:
            raise ValueError(
                "Angle exceeds configured servo limits."
            )

        duty_cycle = self._angle_to_duty_cycle(
            channel,
            angle
        )

        self.pca.channels[channel].duty_cycle = duty_cycle

        self.positions[channel] = float(angle)

        return self.positions[channel]


    def get_positions(self):

        return self.positions.copy()

    def emergency_stop(self):

        if self.closed:
            return

        # Disable all PCA9685 outputs.
        self.oe.value = True

        self.emergency_stopped = True

        for channel in range(SERVO_CHANNELS):
            self.pca.channels[channel].duty_cycle = 0

    def reset_emergency_stop(self):

        if self.closed:
            raise RuntimeError("Controller is closed.")

        # Clear all PWM commands before enabling outputs.
        for channel in range(SERVO_CHANNELS):
            self.pca.channels[channel].duty_cycle = 0

        # Enable PCA9685 outputs.
        self.oe.value = False

        self.emergency_stopped = False


    def get_status(self):

        return {
            "backend": "steven",
            "emergency_stopped": self.emergency_stopped,
            "positions": self.get_positions(),
            "hardware_ready": False
        }


    def close(self):

        if self.closed:
            return

        self.emergency_stop()

        self.oe.deinit()
        self.pca.deinit()
        self.i2c.deinit()

        self.closed = True
