#include "network.h"

//DEBUG
void setMotorSpeed(int val, Adafruit_NeoPixel &NeoPixel){
    NeoPixel.setPixelColor(0, NeoPixel.Color(val, val, 0));
    NeoPixel.show();
}

Adafruit_NeoPixel NeoPixel(NUM_PIXELS, PIN_NEO_PIXEL, NEO_GRB + NEO_KHZ800);
Connection::Connection()
{

}

Connection::Connection(char *ssid, char *passw, int port)
{
    strcpy(this->_ssid, ssid);
    strcpy(this->_passw, passw);
    this->_port = port;
    this->_state = NET_STATES::BEGIN;
    this->_data = DataManager();
    NeoPixel.begin();
    this->_updateTime = 50; //Default update time 50ms
    this->_timeNow = 0;
}

void Connection::init()
{
    WiFi.mode(WIFI_STA);
    WiFi.begin(this->_ssid, this->_passw);
    Serial.println("\nConnecting");

    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
    }
    this->_udp.begin(WiFi.localIP(), this->_port);

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
}

int Connection::readPacket()
{
    int packetSize = this->_udp.parsePacket();
    //If there is a udp packet available
    if(packetSize){
        // read the packet into packetBufffer
        int len = this->_udp.read(packetBuffer, 255);
        if (len > 0) {
        packetBuffer[len] = 0;
        }
        return 0; //Packet available
    }
    return 1; //Packet not available
}

void Connection::writePacket(const char *replyBuffer)
{ 
    this->_udp.beginPacket(this->_udp.remoteIP(), this->_udp.remotePort());
    int size = strlen(replyBuffer);
    for(int i = 0; i < size; i++){
        this->_udp.write(replyBuffer[i]);
    }
    this->_udp.endPacket();
}

void Connection::fsm()
{
    switch (this->_state)
    {
    case NET_STATES::BEGIN: //Set next state to connect or test
        NeoPixel.setPixelColor(0, NeoPixel.Color(0, 0, 255)); //Led blue
        Serial.println("BEGIN");    //DEBUG
        if(!strcmp(this->packetBuffer, "test")){
            this->_state = NET_STATES::TEST;
        }
        else if(!strcmp(this->packetBuffer, "connect")){
            this->_state = NET_STATES::CONNECT;
        }
        break;

    case NET_STATES::TEST: //Test connection. Dont set client ip yet
        Serial.println("TEST"); //DEBUG
        if(!strcmp(this->packetBuffer, this->_name)){ //Expecting to recieve the name of the device
            char replyBuffer[] = "confirm";
            writePacket(replyBuffer);
        }
        this->_state = NET_STATES::BEGIN;
        break;
    
    case NET_STATES::CONNECT:
        Serial.println("CONNECT");
        NeoPixel.setPixelColor(0, NeoPixel.Color(255, 0, 0)); //DEBUG
        if(!strcmp(this->packetBuffer, this->_name)){ //Expecting to recieve the name of the device
            char replyBuffer[] = "confirm";
            writePacket(replyBuffer);
            this->_state = NET_STATES::IDLE;
            Serial.println("IDLE"); //DEBUG
            this->_clientIp = this->_udp.remoteIP(); //Seting the connected client's ip
        }else this->_state = NET_STATES::BEGIN;
        break;
    
    case NET_STATES::IDLE:  //On IDLE Start updating the client on values from hardware
        //Set RGB Led to green (Only for devkit)
        NeoPixel.setPixelColor(0, NeoPixel.Color(255, 0, 0)); //DEBUG
        if(!strcmp(this->packetBuffer, "disconnect")){
            Serial.println("DISCONNECT");   //DEBUG
            NeoPixel.setPixelColor(0, NeoPixel.Color(0, 255, 0)); //DEBUG
            this->_state = NET_STATES::BEGIN;
        }
        else if(!strcmp(this->packetBuffer, "GRAPH")){
            Serial.println("GRAPH");    //DEBUG
            this->_state = NET_STATES::GRAPH_IN;
            this->_data.clearGraph();
        }
        else if(!strcmp(this->packetBuffer, "RUN")){
            Serial.println("RUN");    //DEBUG
            this->_state = NET_STATES::RUN;
        }

        break;
    case NET_STATES::GRAPH_IN:
        NeoPixel.setPixelColor(0, NeoPixel.Color(0, 255, 255));
        if(!strcmp(this->packetBuffer, "END")){
            NeoPixel.setPixelColor(0, NeoPixel.Color(255, 0, 0));   //DEBUG
            Serial.println("END");  //DEBUG
            this->_state = NET_STATES::IDLE;
        }
        else{
            //this->_data.clearGraph();
            
            //Parsing input and saving to data manager
            std::string s = this->packetBuffer;
            
            std::string delimiter = ",";
            std::vector<std::string> parsedInput;
            size_t pos = 0;
            std::string token;
            
            while ((pos = s.find(delimiter)) != std::string::npos) {
                token = s.substr(0, pos);
                parsedInput.push_back(token);
                s.erase(0, pos + delimiter.length());
            }
            parsedInput.push_back(s);
            
            if(!parsedInput.at(0).compare("vals")){
                int x = atoi(parsedInput.at(1).c_str());
                int y = atoi(parsedInput.at(2).c_str());
                this->_data.appendGraph(x, y);
            }
            
        }
        break;

    case NET_STATES::RUN:
        int size = this->_data.size();
        unsigned int startTime = millis();
        unsigned int currentTime;
        int valX;
        int valY;
        int dataSize = this->_data.size();
        int index = 0;
        while(index < size){
            valX = this->_data.getX(index);
            valY = this->_data.getY(index);
            currentTime = millis();
            if(currentTime - startTime >= valX){
                setMotorSpeed(valY, NeoPixel);  //Send rpm to motor control here
                index++;
                
                //Updating client on hardware state change
                if(timer()){
                    sendData();
                }
            }


        }
        this->_state = NET_STATES::IDLE;

    
        NeoPixel.setPixelColor(0, NeoPixel.Color(255, 0, 0));   //DEBUG
        Serial.println("IDLE");  //DEBUG
        this->_state = NET_STATES::IDLE;
        break;

    //default:
        //break;
    }
}

void Connection::monitor()
{
    //NeoPixel.clear();
    if(!readPacket()){
        fsm();
    }
    NeoPixel.show();
}

NET_STATES Connection::getState(){
    return this->_state;
}

void Connection::setUpdateTime(unsigned int milliseconds)
{
    this->_updateTime = milliseconds;
}


/**
 * @brief Send data from hardware to the client
 * 
 */
void Connection::sendData()
{
    char message[50];
    char current[10];
    char pressure[10];

    snprintf(message, sizeof(message), "vals,%f,%f", getCurrent(), getPressure());
    writePacket(message); //Send data with code:vals and delimiter ,
}

/**
 * @brief Returns 1 every set time interval
 * 
 * @return int 
 */
int Connection::timer()
{
    if(millis() >= this->_timeNow + this->_updateTime && getState() == NET_STATES::RUN){
        this->_timeNow += this->_updateTime;
        return 1;
    }
    else return 0;
}