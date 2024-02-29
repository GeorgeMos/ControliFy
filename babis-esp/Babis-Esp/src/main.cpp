#include <Arduino.h>
#include "cli.h"
#include "network.h"
#include "stdlib.h"
#include "string.h"
#include "stdio.h"
#include <Adafruit_NeoPixel.h>


//#define _updateInterval 10 //ms

unsigned long time_now = 0;


Cli menu;
Connection server;

/*
void updateVals(){
    char message[50];
    char current[10];
    char pressure[10];

    snprintf(message, sizeof(message), "vals,%f,%f", getCurrent(), getPressure());
    server.writePacket(message); //Send data with code:vals and delimiter ,
}
*/

void setup() {
  menu = Cli(9600);
  menu.cli_init();
  server = Connection("Matina", "2273023626", 2390);
  server.init();   
  server.setUpdateTime(10); 
}

void loop() {
    menu.runMenu();     //Run the cli 
    server.monitor();   //Monitor trafic and perform state changes

}
