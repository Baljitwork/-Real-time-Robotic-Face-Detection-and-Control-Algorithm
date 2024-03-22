#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;



void setup() {
servo1.attach(4);
servo2.attach(5);
servo3.attach(6); // Connect servo to pin 9
Serial.begin(9600);
}

void loop() {
if (Serial.available()) {
char receivedData = Serial.read();
if (receivedData == '1') {
servo1.write(33); // Set servo angle to 160 degrees
}
else if (receivedData == '2')
{
servo1.write(167); // Set servo angle to 45 degrees
}
else if(receivedData == '3')
{
servo2.write(70); // Set servo angle to 75 degrees
}
else if(receivedData == '4')
{
servo2.write(100); // Set servo angle to 110 degrees
}
else if(receivedData == '5')
{
servo1.write(90); // Set servo angle to 90 degrees
}
