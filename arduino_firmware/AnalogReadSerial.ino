/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/
int SLIDERS_USED = 8; // Use this to only transmit the values we care about
int SWITCHES_USED = 8;
int state[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}; // Declare up to 8 analog pins due to Arduino Nano analog pin restriction.
int pins[8] = {A0, A1, A2, A3, A4, A5, A6, A7};
// int dPins[8] = {D2, D3, D4, D5, D6, D7, D8, D9};
// int dPins[8] = {0, 1, 2, 3, 4, 5, 6, 7};
int dPins[8] = {2, 3, 4, 5, 6, 7, 8, 9};
String sliders_transmission = "";
int BAUDRATE = 9600;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(BAUDRATE);
  for (int pin = 0; pin < SWITCHES_USED; pin++){
      pinMode(dPins[pin], INPUT_PULLUP);
  }
}

// the loop routine runs over and over again forever:
void loop() {
    
    // read the input on analog pin 0:
    for (int index = 0; index < SLIDERS_USED; index++){
        state[index] = analogRead(pins[index]);
        
        sliders_transmission = sliders_transmission + String(state[index]);
        
        // Then we need to append a separator
        if (index != SLIDERS_USED - 1){
            sliders_transmission = sliders_transmission + ",";
        }
        
    }

    sliders_transmission = sliders_transmission + ",";

    // read the input on analog pin 0:
    for (int index = 0; index < SWITCHES_USED; index++){
        state[index + SLIDERS_USED] = int(digitalRead(dPins[index]));
        
        sliders_transmission = sliders_transmission + String(state[index + SLIDERS_USED]);
        
        // Then we need to append a separator
        if (index != SWITCHES_USED - 1){
            sliders_transmission = sliders_transmission + ",";
        }
        
    }
    
    // print out the value you read:
    Serial.println(sliders_transmission);
    sliders_transmission = "";
    
    //Delay 100ms between each transmission for stability
    delay(250);
}
