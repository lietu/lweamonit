#ifndef __LWEAMONIT_H
#define __LWEAMONIT_H

// Include arduino base library
#include <Arduino.h>

// Include the configuration
#include "config.h"

// Library for DS18B20P parasite powered 1-wire temperature sensor
#include "ds18b20p.h"

class lweamonit {
public:
	void setup(void);
	void loop(void);

protected:
	DS18B20P ds18b20p_1;

};

#endif
