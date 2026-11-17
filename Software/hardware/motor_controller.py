from config import BACKEND
from hardware.simulation import ServoSimulation
from hardware.safety import SafetySystem


class MotorController:
    def __init__(self, backend=None):
        self.backend_name = backend or BACKEND
        self.safety = SafetySystem()

        if self.backend_name == "simulation":
            self.controller = ServoSimulation()
        elif self.backend_name == "steven":
            from hardware.pca9685_controller import PCA9685Controller
            self.controller = PCA9685Controller()
        else:
            raise ValueError(f"Unsupported backend: {self.backend_name}.")

    def set_angle(self, channel, angle):
        self.safety.validate_command(channel, angle)
        return self.controller.set_angle(channel, angle)

    def get_positions(self):
        return self.controller.get_positions()

    def emergency_stop(self):
        self.safety.emergency_stopper()

        if hasattr(self.controller, "emergency_stop"):
            return self.controller.emergency_stop()

        if hasattr(self.controller, "emergency_stopper"):
            return self.controller.emergency_stopper()

        raise AttributeError("Controller does not support emergency stopping.")

    def emergency_stopper(self):
        return self.emergency_stop()

    def reset_emergency_stop(self):
        self.safety.reset()

        if hasattr(self.controller, "reset_emergency_stop"):
            return self.controller.reset_emergency_stop()

        raise AttributeError("Controller does not support resetting the emergency stop.")

    def get_status(self):
        status = self.controller.get_status()
        status["controller"] = "MotorController"
        status["backend"] = self.backend_name
        status["emergency_stopped"] = self.safety.is_stopped()
        return status