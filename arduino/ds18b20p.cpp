/**
 * DS18B20-PAR (aka. DS18B20P) interface library
 *
 * Created by Janne Enberg aka. Lietu
 * http://lietu.net/
 *
 * Requires slightly modified version of OneWire class in it's folder, which should be fully
 * compatible with original, just adds ability to run empty constructor and initialize with .begin()
 *
 * Uncomment DS18B20P_LIB_DEBUG to write read data to serial port (if we get that far).
 * Return codes -55 to 100 are good, 124-127 are errors.
 *  - 124: First presence check failed, device not present(?)
 *  - 125: Presence check after temperature conversion failed, device not compatible(?)
 *  - 126: CRC check after read failed repeatedly, device broken or not compatible(?)
 *  - 127: Unknown error
 *
 * This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
 *
 * This allows you to share and modify the work, including for commercial uses, as long as:
 *  - You credit me on the original code 
 *  - Any altered code will be released under the exact same license
 *
 * http://creativecommons.org/licenses/by-sa/3.0/
 *
 * This license does not apply to the OneWire libraries distributed with this code, 
 * its license is mentioned in the OneWire.cpp file.
 */

#include "ds18b20p.h"

// Empty constructor, for "good arduino library style", can initialize with .begin(pin)
DS18B20P::DS18B20P() {}

// Constructor with pin given
DS18B20P::DS18B20P( unsigned int pin )
{
	// Just call begin(), no need to duplicate code here
	this->begin( pin );
}

// Initialize the object
void DS18B20P::begin( unsigned int pin )
{
	// Initialize our onewire instance with the pin
	// This line is basically what we needed to modify OneWire for...
	this->onewire.begin( pin );
}

// Read temperature in C from sensor
double DS18B20P::read()
{
	// Container for the 9 data bytes we will read from the sensor
	byte data[9];

	// Send reset pulse, check for presence
	if( this->onewire.reset() )
	{
		// Issue Skip ROM command (we don't want to search for a specific sensor)
		this->onewire.skip();
		// Issue temperature conversion command, enable strong parasite power
		this->onewire.write( 0x44, 1 );

		// TODO: Return here, rename function to startRead() and move rest to a continueRead() function that checks it's been 800msec since the above line was run
		// Implement new function: double DS18B20P::read() { startRead(); return continueRead(); }
		// ... we could probably do quite a lot of things during this 800msec ....

		// Wait for conversion to complete
		delay( 800 ); // 750ms is enough according to datasheet, just in case we give it 800ms

		// Issue reset
		if( this->onewire.reset() )
		{
			// Skip ROM and issue read scratchpad command, to read temperature data and CRC
			this->onewire.skip();
			this->onewire.write( 0xBE );

			#ifdef DS18B20P_LIB_DEBUG
				Serial.println("DS18B20P .. reading 9 bytes:");
			#endif

			// Read 9 bytes
			for( unsigned int i = 0; i < 9; ++i )
			{
				data[i] = this->onewire.read();

				#ifdef DS18B20P_LIB_DEBUG
					Serial.print( data[i], HEX );
					Serial.print(" ");
				#endif
			}

			#ifdef DS18B20P_LIB_DEBUG
				Serial.println("");
				
				Serial.print( "Calculated CRC: " );
				Serial.print( OneWire::crc8( data, 8 ), HEX );
				Serial.println( "" );
			#endif

			// Check CRC, calculate CRC from first 8 bytes, should match against last byte
			if( OneWire::crc8( data, 8 )!=data[8] )
				return DS18B20P::crcError;

			// Convert to celsius with double precision and return
			return this->getValue( data );
		}
		else
		{
			return DS18B20P::secondPresenceError;
		}
	}
	else
	{
		return DS18B20P::firstPresenceError;
	}
}

double DS18B20P::getValue( byte data[9] )
{
	// Define result variable
	double value;

	// The other variables we will be using..
	int reading, signedBit;

	// Use them to build the full reading
	reading = (data[1] /* high byte */ << 8) + data[0] /* low byte */;

	// Check if the signed bit is set by testing most significant bit
	signedBit = reading & 0x8000; 

	// If it is set, the reading is negative and actual numbers need adjusting to be readable
	if( signedBit==true )
		reading = (reading ^ 0xffff) + 1; // Toggle bits, add 1

	// The data is still in a bit odd format, a little multiplication will fix that..
	// I assume this is to give a better range with the two bytes of data..
	value = (double)( reading ) * 0.0625; // * 6.25 / 100;
	// In case you want speed, this might be slightly faster
	// value = (double)((6 * reading) + (reading / 4)) / 100;

	return value;
}
