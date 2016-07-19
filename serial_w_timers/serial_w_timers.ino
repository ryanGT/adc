#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include <avr/io.h>
#include <avr/interrupt.h>
#include <math.h>

#define isrPin 5

int nISR=0;
int pinstate=0;
bool send_ser;
int inByte;

void setup(){
  Serial.begin(115200);

  pinMode(isrPin, OUTPUT);

  // initialize Timer1
  cli();          // disable global interrupts
  TCCR1A = 0;     // set entire TCCR1A register to 0
  TCCR1B = 0;     // same for TCCR1B

  // Set CS10 and CS12 bits for 1024 prescaler:
  TCCR1B |= (1 << CS10);
  TCCR1B |= (1 << CS12);

  // set compare match register to desired timer count:
  // f_ISR = 16,000,000Hz / (prescaler * (compare match register + 1))
  // compare match register = [16,000,000Hz/ (prescaler * f_ISR) ] - 1
  // OCR1A = compare match register
  OCR1A = 14;


  // turn on CTC mode:
  TCCR1B |= (1 << WGM12);
 
  // enable timer compare interrupt:
  TIMSK1 |= (1 << OCIE1A);

  sei();
}


void loop()
{
  if (Serial.available() > 0) {
    inByte = Serial.read();
    if (inByte == 1){
        Serial.print("serial with timers");
        Serial.print("\n");
    }
    else if (inByte == 2){
      // start new test
      send_ser = true;
      nISR = -1;
    }
    else if (inByte == 3){
      // stop test
      send_ser = false;
    }
  }
  //if ( nISR > 2000) {
  //  // hard coding a stop of serial streaming
  //  send_ser = false;
  //}
}
 
ISR(TIMER1_COMPA_vect)
{     
  nISR++;
  // This code toggles the voltage on isrPin to generate the square
  // wave.  If the pin was high (5V), send it low.  If it was low
  // (0V), send it high.
  digitalWrite(isrPin, HIGH);
  if (send_ser){ 
      Serial.write(nISR);
  }
  digitalWrite(isrPin, LOW);
}

