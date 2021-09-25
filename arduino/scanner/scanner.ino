#include "scanner.h"
#include <Servo.h>

char input_buff[READ_LEN];
char output_buff[WRITE_LEN];

uint16_t sample_buffer[BUFF_SIZE];
size_t buffer_index = 0;  // Current buffer index (buffer_index - 1 = index of last inserted value)

bool led = false;
uint16_t current_reading = 0;

CommInput input;
CommOutput output;

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(115200);
  Serial.setTimeout(100);
  while (!Serial.available());

  servo_yaw.attach(SERVO_YAW);
  servo_pitch.attach(SERVO_PITCH);

  // clear sample buffer
  for (int i = 0; i < BUFF_SIZE; i++) {
    sample_buffer[i] = 0;
  }
}
void loop() {
  if (Serial.available()) {
    size_t bytes_read = Serial.readBytes(input_buff, READ_LEN);
    if (!parseInput(input_buff, &input)) {
      // No errors currently reported
    }

    led ^= 1;
    digitalWrite(13, led);
    
    output.echo = input.echo + 1;
    output.led_status = led;
    output.distance_measurement = 3855;
    if (encodeOutput(output, output_buff, WRITE_LEN)) {
      Serial.write(output_buff, WRITE_LEN);
    }
  }

  servo_yaw.write(input.yaw_cmd);
  servo_pitch.write(input.pitch_cmd);

  // TODO: wait for servo to reach position
  
  // Collect sample
  uint16_t ir_sample = analogRead(IR);
  // Add to ring buffer
  sample_buffer[buffer_index] = ir_sample;

  // Rolling average ring buffer
  uint16_t average = 0;
  for (int i = 0; i < BUFF_SIZE; i++) {
    average += sample_buffer[i] / BUFF_SIZE;
  }

  current_reading = average;
}

bool parseInput(char* input, CommInput* buff) {
  buff->cmd = input[0];
  buff->echo = input[1];
  buff->yaw_cmd = (input[2] << 8) + input[3];
  buff->pitch_cmd = (input[4] << 8) + input[5];
  return true;
}

bool encodeOutput(const CommOutput &output, char* buff, uint8_t len) {
  buff[0] = output.echo;
  buff[1] = output.led_status;
  buff[2] = (output.distance_measurement & 0xff00) >> 8;
  buff[3] = (output.distance_measurement & 0x00ff);
  return true;
}
