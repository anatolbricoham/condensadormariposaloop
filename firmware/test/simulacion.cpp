#include "Arduino.h"
#include <cmath>
extern int32_t pos; extern int banda; extern float roe; extern String estado; bool autoajuste(); bool buscarHome();
SerialC Serial; int dirPin=1; const double HOLG=300;
double motor=12345, rotor=12345, RES=20100, BWP=32;
void pinMode(int,int){}
void digitalWrite(int p,int v){ if(p==26) dirPin=v; if(p==25 && v==1){ motor += dirPin?1:-1;
  if(motor>rotor+HOLG/2) rotor=motor-HOLG/2; if(motor<rotor-HOLG/2) rotor=motor+HOLG/2; } }
int digitalRead(int p){ if(p==23) return (rotor>-2000 && rotor<200)?0:1; return 1; }
void delay(int){} void delayMicroseconds(int){} uint32_t millis(){return 0;}
uint32_t analogReadMilliVolts(int p){ double x=(rotor-RES)/(BWP/2); double g=std::sqrt(x*x/(1+x*x));
  return p==36 ? 750 : (uint32_t)(1500*g/2); }
void analogSetAttenuation(int){}
int main(){
  buscarHome(); printf("home: %s pos=%d rotor=%.0f\n", estado.c_str(), pos, rotor);
  banda=0;
  for(int k=0;k<3;k++){ bool ok=autoajuste(); printf("tune%d ok=%d roe=%.2f pos=%d rotor=%.0f (res %.0f) %s\n",k,ok,roe,pos,rotor,RES,estado.c_str()); RES+=150; }
  RES=5000; bool ok=autoajuste(); printf("lejos: ok=%d roe=%.2f rotor=%.0f res=%.0f %s\n",ok,roe,rotor,RES,estado.c_str());
}
