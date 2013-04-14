#include "lweamonit.h"

void lweamonit::setup(void)
{
	// Initialize serial port for output at 9600 baud
	Serial.begin(9600);
	
	// Set pin 13 (on-board LED) to expect output
	pinMode(13, OUTPUT);

	// Initialize DS18B20P instance
	this->ds18b20p_1.begin(DS18B20P_PIN_1);
}

void lweamonit::loop(void)
{
	// Ask to read from ds18b20p_1
	double d_temp_1 = this->ds18b20p_1.read();

	// Output data
	Serial.print("S1: ");
	Serial.print(d_temp_1);

	// End output line
	Serial.println("");

	// Wait for a while before new iteration
	delay(ITERATION_DELAY); 
}
