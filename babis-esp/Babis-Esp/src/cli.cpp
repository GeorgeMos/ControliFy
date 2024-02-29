#include "cli.h"

Cli::Cli()
{

}

Cli::Cli(int baud)
{
    this->_baud = baud;
    Serial.begin(this->_baud);
}

void Cli::cli_init()
{
    this->_state = CLI_STATES::MAIN_MENU;
    Serial.setTimeout(1);
}

/**
 * @brief Runs the state machcine and waits for input
 * 
 */
void Cli::runMenu()
{
    fsm();
    readInput();
    inputParser();
    //Serial.println(this->_input);
}

void Cli::flushInputBuffer()
{
    this->_input.erase();
}

void Cli::readInput()
{
    int i = 0;
    while(Serial.available()){
        this->_input[i] = Serial.read();
        delay(2);
        i++;
    }
    //Serial.print((this->_input).c_str());
    if(this->_input.size() > 0){
        this->_input.erase(this->_input.end()-1);  //Remove '\n' character
    }
    Serial.print(this->_input.c_str());
}

/**
 * @brief Reads the input string and sets the command value
 * 
 * @param input 
 */

void Cli::inputParser()
{
    if(this->_input.compare("help")){
        this->_command = CLI_COMMAND::HELP;
    }
    
}

void Cli::mainMenu()
{
    Serial.println("Babis O Kenos Cli configuration menu");
    Serial.println("Get started with 'help'");
    Serial.print("#>");
    
}

void Cli::helpMenu()
{
    Serial.println("Help menu");
    Serial.print("#>");
}

void Cli::fsm()
{
    switch (this->_state)
    {
    case CLI_STATES::WAIT:
        if(this->_command == CLI_COMMAND::HELP){
            this->_state = CLI_STATES::HELP_MENU;
        }

        
        flushInputBuffer();
        break;
    case CLI_STATES::MAIN_MENU:
        mainMenu();
        this->_state = CLI_STATES::WAIT;
        break;

    case CLI_STATES::HELP_MENU:

        break;
    
    default:
        break;
    }
}


