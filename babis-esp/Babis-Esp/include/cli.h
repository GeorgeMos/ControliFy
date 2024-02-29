#ifndef __CLI__
#define __CLI__
#include <Arduino.h>
#include <string>
#define RX_BUFF_SIZE 256
enum CLI_STATES
{
    WAIT,        //Wait for user input
    MAIN_MENU,   //Main menu state
    HELP_MENU,   //Help menu state
};

enum CLI_COMMAND
{
    HELP,
    WIFI_SETUP
};

class Cli
{
private:
    int _baud;
    int _state;
    int _command;

    std::string _input;

    void fsm();
    void readInput();
    void inputParser();
    void flushInputBuffer();
    void mainMenu();
    void helpMenu();
    void wifiSetupMenu();
public:
    Cli();
    Cli(int baud);
    void cli_init();
    void runMenu();
};

#endif
