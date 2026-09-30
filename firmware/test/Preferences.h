#pragma once
#include "Arduino.h"
struct Preferences{ bool begin(const char*,bool){return true;} int getInt(const char*,int d){return d;} void putInt(const char*,int){} };
