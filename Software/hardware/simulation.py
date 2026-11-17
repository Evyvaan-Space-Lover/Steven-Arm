from config import (SERVO_CHANNELS, SERVO_LIMITS, INITIAL_POSITIONS)


class ServoSimulation:
    def __init__(self):
        self.positions = INITIAL_POSITIONS.copy()
        self.emergency_stopped = False

    def set_angle(self, channel, angle):
        if type(channel) is not int:
            raise TypeError("Channel must be an integer.")

        if channel not in range(SERVO_CHANNELS):
            raise ValueError("Invalid servo channel.")

        if isinstance(angle, bool) or not isinstance(angle, (int, float)):
            raise ValueError("Angle must be a number.")

        if self.emergency_stopped:
            raise RuntimeError("Steven is stopped :(")

        minimum, maximum = SERVO_LIMITS[channel]

        if not minimum <= angle <= maximum:
            raise ValueError(
                f"Angle {angle} is out of bounds for channel {channel}. "
                f"Must be between {minimum} and {maximum}."
            )

        self.positions[channel] = float(angle)
        print(f"Simulated servo channel {channel} set to angle {angle}.")
        return self.positions[channel]

    def get_positions(self):
        return self.positions.copy()

    def emergency_stop(self):
        self.emergency_stopped = True
        return True

    def emergency_stopper(self):
        return self.emergency_stop()

    def reset_emergency_stop(self):
        self.emergency_stopped = False
        return False

    def get_status(self):
        return {
            "backend": "simulation",
            "emergency_stop": self.emergency_stopped,
            "positions": self.positions.copy()
        }

