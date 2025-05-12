#include "TLE9879_Group.h"

TLE9879_Group *shields;

void setup() {
  shields = new TLE9879_Group(1);
  Serial.begin(115200);
}

void loop() {
  while (Serial.available() > 3){
    Serial.read();
  }

  if (Serial.available() >= 3) {
    Serial.read();                    // Skip steering
    int speed_flag = Serial.read();  // 1 = run, 0 = stop
    int direction = Serial.read();   // 1 = forward, 0 = reverse

    if (speed_flag == 1) {
      // Motor ON
      shields->setMode(FOC, BOARD1);

      if (direction == 1) {
        shields->setLedColor(COLOR_GREEN, BOARD1);   // Forward
        shields->setMotorSpeed(2000, BOARD1);
        shields->setMotorMode(START_MOTOR, BOARD1);
      } else {
        shields->setLedColor(COLOR_YELLOW, BOARD1);
        shields->setMotorSpeed(-2000, BOARD1);
        shields->setMotorMode(START_MOTOR, BOARD1);  // Reverse
      }

    } else {
      // Motor OFF (neutral)
      shields->setMotorMode(STOP_MOTOR, BOARD1);
      shields->setLedColor(COLOR_RED, BOARD1);       // Neutral
    }
  }
}
