#include "scanner.h"
#include <Servo.h>

char input_buff[READ_LEN];
char output_buff[WRITE_LEN];

CommInput input;
CommOutput output;

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(1);

  servoYaw.attach(SERVO_YAW);
  servoPitch.attach(SERVO_PITCH);
}
bool led = false;
void loop() {
  if (Serial.available()) {
//    size_t bytes_read = Serial.readBytes(input_buff, READ_LEN);
//    //Serial.write(100);
//    if (bytes_read > 0) {
//      digitalWrite(13, HIGH);
//      delay(100);
//      Serial.write(101);
//      if (parseInput(input_buff, &input)) {
//        output.out_int = input.in_int + 1;
//        if (encodeOutput(output, output_buff, WRITE_LEN)) {
//          //Serial.write(output_buff, WRITE_LEN);
//        }
//      }
//    } else {
//      digitalWrite(13, LOW);
//    }
    led = led ^ true;
    digitalWrite(13, led);
    Serial.println(Serial.read());
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
