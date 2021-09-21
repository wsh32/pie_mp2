#ifndef SCANNER_H
#define SCANNER_H

#define SERVO_YAW 5
#define SERVO_PITCH 6
#define IR PIN_A0

#define READ_LEN 80
#define WRITE_LEN 2

#include <Servo.h>

Servo servoYaw;
Servo servoPitch;

struct CommInput {
  uint8_t in_int;
};

struct CommOutput {
  uint8_t out_int;
};

bool parseInput(char* input, CommInput* buff);
bool encodeOutput(const CommOutput &output, char* buff, uint8_t len);

uint16_t readIrSensor();

#endif
