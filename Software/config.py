
# ==========================================
# STEVEN - CENTRAL CONFIGURATION
# ==========================================

# BACKEND
BACKEND = "simulation"



HOST = "127.0.0.1"
PORT = 8000


SERVO_CHANNELS = 6


SERVO_MAPPING = {
    0: "base",
    1: "shoulder",
    2: "elbow",
    3: "wrist",
    4: "shoulder2",
    5: "gripper"
}

#shot in the dark these nos. are for limits and shi. need to be callibrated with hardware

SERVO_LIMITS = {
    0: (0, 180),
    1: (0, 180),
    2: (0, 180),
    3: (0, 180),
    4: (0, 180),
    5: (0, 180)
}


PWM_FREQUENCY = 50

#these pulse widths are the best guesses i could make

SERVO_CALIBRATION = {
    0: {
        "min_pulse": 500,
        "max_pulse": 2500
    },
    1: {
        "min_pulse": 500,
        "max_pulse": 2500
    },
    2: {
        "min_pulse": 500,
        "max_pulse": 2500
    },
    3: {
        "min_pulse": 500,
        "max_pulse": 2500
    },
    4: {
        "min_pulse": 500,
        "max_pulse": 2500
    },
    5: {
        "min_pulse": 500,
        "max_pulse": 2500
    }
}


INITIAL_POSITIONS = {
    0: 90,
    1: 90,
    2: 90,
    3: 90,
    4: 90,
    5: 90
}


I2C_ADDRESS = 0x40

# Raspberry Pi GPIO4 controls PCA9685 OE.
OE_GPIO = 4
