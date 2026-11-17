from config import SERVO_CHANNELS, SERVO_LIMITS

class SafetySystem: #i dont want to be unsafe. im a good obedient boi
    
    def __init__(self):
        self.emergency_stopped = False
    
    def validate_command(self, channel, angle):
        
        if self.emergency_stopped:
            raise RuntimeError("Emergency stop is active. Cannot execute command.")
        
        if type(channel) is not int:
            raise ValueError("Channel must be an integer.")
        
        if channel not in range(SERVO_CHANNELS):
            raise ValueError("Invalid Servo channel.")
        
        if isinstance(angle, bool) or not isinstance(angle, (int, float)):
            raise ValueError("Angle must be a number.")
        
        minimum, maximum = SERVO_LIMITS[channel]
        
        if not minimum <= angle <= maximum:
            raise ValueError(f"Angle {angle} is out of bounds for channel {channel}. Must be between {minimum} and {maximum}.")
        
        return True
    
    def emergency_stopper(self):
        self.emergency_stopped = True
    def reset(self):
        self.emergency_stopped = False
    def is_stopped(self):
        return self.emergency_stopped