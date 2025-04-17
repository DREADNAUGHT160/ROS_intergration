import pygame
import serial
import time

# === CONFIG ===
COM_PORT = 'COM7'  # Change this to match your board
BAUD_RATE = 115200

# === SETUP SERIAL ===
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)

# === INIT CONTROLLER ===
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ No controller connected.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"🎮 Controller connected: {joystick.get_name()}")

# === MAIN LOOP ===
recording = False

def get_direction(y, threshold=0.5):
    if y < -threshold:
        return "FORWARD"
    elif y > threshold:
        return "BACKWARD"
    return "NEUTRAL"

def get_steering(x, threshold=0.3):
    if x < -threshold:
        return "LEFT"
    elif x > threshold:
        return "RIGHT"
    return "STRAIGHT"

def get_speed(val):
    return int(((val + 1) / 2) * 100)  # -1 → 1 becomes 0 → 100

print("🟢 Controller-to-UART bridge running. Press Ctrl+C to stop.")

try:
    while True:
        pygame.event.pump()

        # Read axes
        left_x = joystick.get_axis(0)  # Steering
        right_y = joystick.get_axis(4)  # FWD/BWD
        rpm_axis = joystick.get_axis(6)  # RPM slider
        brake = joystick.get_axis(5)     # Brake trigger (optional)

        # Read buttons
        button_a = joystick.get_button(0)  # A = start recording
        button_b = joystick.get_button(1)  # B = stop recording

        if button_a:
            recording = True
        if button_b:
            recording = False

        direction = get_direction(right_y)
        steering = get_steering(left_x)
        rpm = get_speed(rpm_axis)
        rec_flag = 1 if recording else 0

        # Format command string
        cmd = f"{direction}:{steering}:{rpm}:{rec_flag}\n"
        ser.write(cmd.encode())

        # Read and print MCU response
        response = ser.readline().decode().strip()
        if response:
            print(f"<< MCU: {response}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n🔴 Exiting...")
finally:
    pygame.quit()
    ser.close()
    print("🔌 Serial closed.")
