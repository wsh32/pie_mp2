#ifndef SCANNER_H
#define SCANNER_H

#define SERVO_YAW 5
#define SERVO_PITCH 6
#define IR PIN_A0

#define READ_LEN 8
#define WRITE_LEN 8

#define TIME_DELAY 1

#define NUM_AVERAGE 10

#include <Servo.h>

Servo servo_yaw;
Servo servo_pitch;

struct CommInput {
  uint8_t cmd;
  uint8_t echo;
  uint8_t yaw_cmd;
  uint8_t pitch_cmd;
};

struct CommOutput {
  uint8_t echo;
  uint8_t led_status;
  uint16_t distance_measurement;
};

bool parseInput(char* input, CommInput* buff);
bool encodeOutput(const CommOutput &output, char* buff, uint8_t len);

uint16_t read_ir_sensor();

#endif
