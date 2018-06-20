// Quick 'n Dirty serial emulator running on Arduino UNO to 
// Generate a serial bitstream for project Python GUI Debugging


int sample_number; 
float v1; 
float v2; 
float a1; 
float a2; 
float t1; 
float t2; 

void setup() {
  // Start the serial port 
  Serial.begin(115200);

  Serial.println("Hello World! and Cici :D"); 

  // Init the values
  sample_number = 0; 
  v1 = 12;
  v2 = v1+0.1;
  a1 = 8;
  a2 = a1 + 1; 
  t1 = 25.1; 
  t2 = t1 - 1; 
  
}

void loop() {
  // Send the serial string

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

  // Inc the values

  sample_number++;
  v1 = v1+0.1;
  v2 = v2+0.1;
  a1 = a1+0.1;
  a2 = a2+0.1;
  t1 = t1+0.1;
  t2 = t2+0.1;
  
  // Error checking: 

  if (sample_number > 999) sample_number = 0; 
  if (v1 > 12.6) v1 = 11.5;
  if (v2 > 12.6) v2 = 11.5;
  if (a1 > 19.9) a1 = 8;
  if (a2 > 19.9) a2 = 8;
  if (t1 > 30) t1 = 12;
  if (t2 > 30) t2 = 12;

  // flow control / delay
  delay(2);
  
  

}
