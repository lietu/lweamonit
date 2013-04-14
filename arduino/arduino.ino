/*
 * Lweamonit - Lightweight weather monitoring station tools
 * Copyright (C) 2013  Janne Enberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


/**
 * lweamonit-arduino
 *
 * Arduino application for providing data to lweamonit
 *
 * This file starts the application, no need to touch this code
 *
 * Configuration in config.h
 */


#include "lweamonit.h"
lweamonit application;

void setup(void)
{
	application.setup();
}

void loop()
{
	application.loop();
}

