#ifndef __DUMMY_HARDWARE__
#define __DUMMY_HARDWARE__

#include <Arduino.h>
#include <Adafruit_NeoPixel.h>


float getCurrent();

float getPressure();


/*
void setMotorSpeed(int speed, int max, Adafruit_NeoPixel NeoPixel){
    int mySpeed = (speed/max)*255;
    NeoPixel.setPixelColor(0, NeoPixel.Color(mySpeed, 0, mySpeed));
}
*/

#endif