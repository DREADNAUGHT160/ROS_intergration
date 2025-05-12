#include "TLE9879_Group.h"
#include <Servo.h>

TLE9879_Group *shields;
Servo steeringServo;  // Create servo object

void setup() {
  shields = new TLE9879_Group(1);
  Serial.begin(115200);
  steeringServo.attach(9);  // Attach to pin 9
}

void loop() {
  while (Serial.available() > 3) {
    Serial.read();  // Flush excess
  }

  if (Serial.available() >= 3) {
    int steering = Serial.read();     // 0–180 degrees
    int speed_flag = Serial.read();   // 1 = run, 0 = stop
    int direction = Serial.read();    // 1 = forward, 0 = reverse

    // Set steering angle via servo
    if (steering != 90){
          steeringServo.write(steering);
          shields->setLedColor(COLOR_BLUE, BOARD1);
    }

    if (speed_flag == 1) {
      shields->setMode(FOC, BOARD1);

      if (direction == 1) {
        shields->setLedColor(COLOR_GREEN, BOARD1);    // Forward
        shields->setMotorSpeed(2000, BOARD1);
        shields->setMotorMode(START_MOTOR, BOARD1);
      } else {
        shields->setLedColor(COLOR_YELLOW, BOARD1);   // Reverse
        shields->setMotorSpeed(-2000, BOARD1);
        shields->setMotorMode(START_MOTOR, BOARD1);
      }

    } else {
      shields->setMotorMode(STOP_MOTOR, BOARD1);
      shields->setLedColor(COLOR_RED, BOARD1);        // Neutral
    }
  }
}
