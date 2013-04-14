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
 *  - 127: Unknown error (not implemented ;)
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

#ifndef DS18B20P_LIB
#define DS18B20P_LIB

// #define DS18B20P_LIB_DEBUG

// Include arduino base library
#include <Arduino.h>

// Load the OneWire library
#define ONEWIRE_SEARCH 0 // We don't need search, might save a few precious bytes by excluding it
#include "OneWire.h"

// Start class definition
class DS18B20P
{
	public:
		/**
		 * Dummy constructor, does nothing, initialize later with .begin(pin)
		 */
		DS18B20P();
		
		/**
		 * Constructor with pin given
		 * param[in] The data pin a DS18B20-PAR is connected to
		 */
		DS18B20P(unsigned int pin);

		/**
		 * Initialize object for use if created with dummy constructor
		 * param[in] The data pin a DS18B20-PAR is connected to
		 */
		void begin(unsigned int pin);

		/**
		 * Execute the full read procedure and return the current temperature, will last 800+msec
		 */
		double read();

		// Define error codes for readability
		enum errorCodes {
			firstPresenceError = 124,
			secondPresenceError = 125,
			crcError = 126,
			unknownError = 127
		};

	private:
		// Container for an instance of OneWire class
		OneWire onewire;

		/**
		 * Convert byte data received from sensor into actual celsius value
		 * param[in] The 9 bytes read from sensor's scratchpad
		 */
		double getValue( byte data[9] );
};

#endif
