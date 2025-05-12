import pygame
import serial
import time
#this setup works with controller V1 and V2
# Serial Port 
arduino = serial.Serial('COM9', 115200)  
time.sleep(2) 

#Pygame Joystick Config 
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

#-1 to 1 → 0 to 180 
def map_steering(x_value):

    if abs(x_value) < 0.05:
        x_value = 0
    return int((x_value + 1) * 90)  # -1..1 --> 0..180

#Sending to Arduino
def send_motor_command(y_axis, x_axis):
    steering = map_steering(x_axis)

    if y_axis < 0:
        cmd = bytes([steering, 1, 1])  # Forward
        print(f"Forward       | Steering: {steering}")
    elif y_axis > 0:
        cmd = bytes([steering, 1, 0])  # Reverse
        print(f"Reverse       | Steering: {steering}")
    else:
        cmd = bytes([steering, 0, 0])  # Stop + update steering
        print(f"Steering Only | Steering: {steering}")
    
    arduino.write(cmd)

#Main Loop
try:
    print("Joystick control active. ZUKUMO Calibrating ..........")
    arduino.write(bytes([90, 0, 1]))
    while True:
        pygame.event.pump() 

        y_axis = joystick.get_axis(1)  # Y axis
        x_axis = joystick.get_axis(3)  # X axis

        send_motor_command(y_axis, x_axis)
        time.sleep(0.1)  #responsiveness

except KeyboardInterrupt:
    print("Exiting...")
    arduino.write(bytes([90, 0, 1])) # Stop on exit
    arduino.close()
    pygame.quit()
