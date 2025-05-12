import pygame
import serial
import time

# Setup serial connection
arduino = serial.Serial('COM9', 115200)  # Adjust COM port as needed
time.sleep(2)  # Wait for Arduino to reset

# Initialize pygame joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

def send_motor_command(value):
    if value > 0.5:
        cmd = bytes([0, 1, 0])  # Forward
        print("reverse")
    elif value < -0.5:
        cmd = bytes([0, 1, 1])  # Reverse
        print("Forward")
    else:
        cmd = bytes([0, 0, 1])  # Stop
        print("Stop")
    arduino.write(cmd)

try:
    while True:
        pygame.event.pump()  # Process event queue
        y_axis = joystick.get_axis(1)  # Usually axis 1 is vertical
        send_motor_command(y_axis)
        time.sleep(0.1)  # Small delay for UART stability

except KeyboardInterrupt:
    print("Exiting...")
    send_motor_command(0)  # Stop on exit
    arduino.close()
    pygame.quit()
