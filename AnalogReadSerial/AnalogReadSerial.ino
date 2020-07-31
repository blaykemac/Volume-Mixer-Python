/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/
int SLIDERS_USED = 8; // Use this to only transmit the values we care about
int sliders[8] = {0,0,0,0,0,0,0,0}; // Declare up to 8 analog pins due to Arduino Nano analog pin restriction.
int pins[8] = {A0, A1, A2, A3, A4, A5, A6, A7};
String sliders_transmission = "";
int BAUDRATE = 9600;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(BAUDRATE);
}

// the loop routine runs over and over again forever:
void loop() {
    
    // read the input on analog pin 0:
    for (int index = 0; index < SLIDERS_USED; index++){
        sliders[index] = analogRead(pins[index]);
        
        sliders_transmission = sliders_transmission + String(sliders[index]);
        
        // Then we need to append a separator
        if (index != SLIDERS_USED - 1){
            sliders_transmission = sliders_transmission + ",";
        }
        
    }
    
    // print out the value you read:
    Serial.println(sliders_transmission);
    sliders_transmission = "";
    
    //Delay 100ms between each transmission for stability
    delay(250);
}
