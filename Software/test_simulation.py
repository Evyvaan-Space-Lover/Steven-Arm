# from hardware.simulation import ServoSimulation
from hardware.motor_controller import MotorController

FAKEsteven = MotorController()

print("Initial state.")
print(FAKEsteven.get_status())

print("\nMoving servo 1 to 120 degrees.")
FAKEsteven.set_angle(0, 120)

print(f"\nCurrent state.\n{FAKEsteven.get_status()}")

print("\nEmergency Stop")
FAKEsteven.emergency_stopper()

try:
    print("\nAttempting to move servo 2 to 90 degrees.")
    FAKEsteven.set_angle(1, 90)
except RuntimeError as e:
    print(f"Correctly blocked yay| Error btw: {e}")

print("\n TEST COMPLETED HELL YEAH")