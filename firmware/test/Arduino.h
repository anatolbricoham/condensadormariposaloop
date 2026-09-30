#pragma once
#include <string>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#define HIGH 1
#define LOW 0
#define OUTPUT 1
#define INPUT_PULLUP 2
#define ADC_11db 3
#define F(x) x
#define PROGMEM
#define FPSTR(x) String(x)
template<class T> T constrain(T v, T a, T b){ return v<a?a:(v>b?b:v); }
inline long constrain(long v,int a,long b){return v<a?a:(v>b?b:v);}
class String { public: std::string s;
  String(){} String(const char*c):s(c){} String(const std::string&x):s(x){}
  String(int v){s=std::to_string(v);} String(long v){s=std::to_string(v);} String(unsigned v){s=std::to_string(v);}
  String(float v,int d){char b[32];snprintf(b,32,"%.*f",d,v);s=b;}
  String operator+(const String&o)const{return String(s+o.s);} String operator+(const char*o)const{return String(s+o);}
  String operator+(int v)const{return String(s+std::to_string(v));} String operator+(unsigned v)const{return String(s+std::to_string(v));}
  String operator+(long v)const{return String(s+std::to_string(v));}
  friend String operator+(const char*a,const String&b){return String(std::string(a)+b.s);}
  String& operator+=(const String&o){s+=o.s;return *this;}
  bool operator==(const char*o)const{return s==o;} char operator[](int i)const{return s[i];}
  int length()const{return s.size();} const char* c_str()const{return s.c_str();}
  String substring(int a,int b=-1)const{ if(a>(int)s.size())return String(); return String(b<0?s.substr(a):s.substr(a,std::max(0,b-a)));}
  long toInt()const{return atol(s.c_str());} void trim(){} void replace(const char*,const String&){}
};
struct SerialC{void begin(int){} int available(){return 0;} String readStringUntil(char){return String();} void println(const String&){} void println(const char*){} };
extern SerialC Serial;
void pinMode(int,int); void digitalWrite(int,int); int digitalRead(int); void delay(int); void delayMicroseconds(int);
uint32_t millis(); uint32_t analogReadMilliVolts(int); void analogSetAttenuation(int);
