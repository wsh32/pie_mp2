#include "scanner.h"
#include <Servo.h>

char input_buff[READ_LEN];
char output_buff[WRITE_LEN];

CommInput input;
CommOutput output;

void setup() {
  pinMode(3, OUTPUT);
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(100);
  while (!Serial.available());

  servoYaw.attach(SERVO_YAW);
  servoPitch.attach(SERVO_PITCH);
}
bool led = false;
void loop() {
  if (Serial.available()) {
    size_t bytes_read = Serial.readBytes(input_buff, READ_LEN);
    if (parseInput(input_buff, &input)) {
      output.out_int = input.in_int + 1;
      if (encodeOutput(output, output_buff, WRITE_LEN)) {
        Serial.write(output_buff, WRITE_LEN);
      }
    }
    led = led ^ true;
    digitalWrite(3, led);
    digitalWrite(13, led);
  }
}

bool parseInput(char* input, CommInput* buff) {
  buff->in_int = *input;
  return true;
}

bool encodeOutput(const CommOutput &output, char* buff, uint8_t len) {
  buff[0] = output.out_int;
  return true;
}
