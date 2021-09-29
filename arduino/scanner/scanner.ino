#include "scanner.h"
#include <Servo.h>

char input_buff[READ_LEN];
char output_buff[WRITE_LEN];

uint16_t sample_buffer[BUFF_SIZE];
size_t buffer_index = 0;  // Current buffer index (buffer_index - 1 = index of last inserted value)

bool led = false;
bool enabled = false;
uint16_t current_reading = 0;

CommInput input;
CommOutput output;

unsigned long last_read_timestamp_ms = 0;
bool waiting_send = false;

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
  enabled = (input.cmd == 1);
  led = enabled;
  digitalWrite(13, led);

  if (Serial.available()) {
    if (!waiting_send) {
      last_read_timestamp_ms = millis();
      waiting_send = true;
    }

    size_t bytes_read = Serial.readBytes(input_buff, READ_LEN);
    if (!parseInput(input_buff, &input)) {
      // No errors currently reported
    }
  }

  if (((millis() - last_read_timestamp_ms) > TIME_DELAY) && waiting_send) {
    current_reading = 0;
    for (int i = 0; i < BUFF_SIZE; i++) {
      current_reading += float(analogRead(IR)) / BUFF_SIZE;
    }

    output.echo = input.echo;
    output.led_status = led;
    output.distance_measurement = current_reading;
    if (encodeOutput(output, output_buff, WRITE_LEN)) {
      Serial.write(output_buff, WRITE_LEN);
    }

    waiting_send = false;
  }

  if (enabled) {
    servo_yaw.write(input.yaw_cmd);
    servo_pitch.write(input.pitch_cmd);
  }
}

bool parseInput(char* input, CommInput* buff) {
  buff->cmd = input[0];
  buff->echo = input[1];
  buff->yaw_cmd = input[2];
  buff->pitch_cmd = input[3];
  return true;
}

bool encodeOutput(const CommOutput &output, char* buff, uint8_t len) {
  buff[0] = output.echo;
  buff[1] = output.led_status;
  buff[2] = (output.distance_measurement & 0xff00) >> 8;
  buff[3] = (output.distance_measurement & 0x00ff);
  return true;
}
