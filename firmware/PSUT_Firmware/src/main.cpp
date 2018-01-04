#include <Arduino.h>

#define PIN_VCH1  A0
#define PIN_ACH1  A2
#define PIN_VCH2  A1
#define PIN_ACH2  A3

int sample_number;
float v1;
float v2;
float a1;
float a2;
float t1;
float t2;

//****************************************************************************//
// Function Prototypes
void readAnalogueCh1();
void readAnalogueCh2();
void printVars();

//****************************************************************************//
// Main program execution

void setup() {
  // Setup the analogue reference
  analogReference(EXTERNAL);

  // Setup the pin inputs
  pinMode(PIN_VCH1, INPUT);
  pinMode(PIN_ACH1, INPUT);
  pinMode(PIN_VCH2, INPUT);
  pinMode(PIN_ACH2, INPUT);

  // Start the serial port
  Serial.begin(115200);

  Serial.println("Hello World! and Cici :D");
  Serial.println("Firmware V0.1");
  Serial.println();

  // Init the values
  sample_number = 0;
  v1 = 0;
  v2 = 0;
  a1 = 0;
  a2 = 0;
  t1 = 25;
  t2 = 26;
}

void loop() {
  // Send the serial string

  readAnalogueCh1();
  readAnalogueCh2();
  printVars();

  // Inc the values
  sample_number++;


  // Error checking:
  if (sample_number > 999) sample_number = 0;


  // flow control / delay
  delay(2);
}

//routine to read channel 1 values
void readAnalogueCh1(){
  v1  = analogRead(PIN_VCH1);
  a1  = analogRead(PIN_ACH1);

  // scale values :
  // voltage: 1/4 divider, and 4096mV reference < 1023 = 4096mV
  // or ~4mV / bit => *4 = 16mV / bit
  v1  = (v1 * 16) / 1000; // convert to volts
  // current: 100mV / A, and 4mV / Bit
  // => 25 Bits / A
  // 40mA / Bit
  // also offset of 2.5ish V, so ~625 bit offset
  a1  = ((a1 - 625) * 40) / 1000; // convert to amps

}

//routine to read channel 2 values
void readAnalogueCh2(){
  v2  = analogRead(PIN_VCH2);
  a2  = analogRead(PIN_ACH2);

  // scale values :
  // voltage: 1/4 divider, and 4096mV reference < 1023 = 4096mV
  // or ~4mV / bit => *4 = 16mV / bit
  v2  = (v2 * 16) / 1000; // convert to volts
  // current: 100mV / A, and 4mV / Bit
  // => 25 Bits / A
  // 40mA / Bit
  // also offset of 2.5ish V, so ~625 bit offset
  a2  = ((a2 - 625) * 40) / 1000; // convert to amps
}

// Serial print routine
void printVars(){
  Serial.print("1");
  Serial.print(sample_number);
  Serial.print(",");
  Serial.print(v1);
  Serial.print(",");
  Serial.print(a1);
  Serial.print(",");
  Serial.print(t1);
  Serial.println(";");

  Serial.print("2");
  Serial.print(sample_number);
  Serial.print(",");
  Serial.print(v2);
  Serial.print(",");
  Serial.print(a2);
  Serial.print(",");
  Serial.print(t2);
  Serial.println(";");
}
