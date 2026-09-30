/*
  AUTOAJUSTE PARA ANTENA LOOP MAGNÉTICA – condensador mariposa motorizado
  ESP32 + TMC2209 + NEMA17 con reductora 27:1 + sensor Hall A3144 + puente de ROE (tipo Bruene)

  Uso:
   - Selecciona banda (BANDA) -> el motor va a la posición aprendida (o al preset calculado).
   - Emite una PORTADORA de 5–10 W (modo AM/FM/CW o TUNE) y pulsa TUNE -> busca el mínimo de ROE.
   - ARRIBA/ABAJO: retoque fino manual (mantener pulsado = continuo).
   - TUNE mantenido 2 s -> busca home (Cmin).
   - Página web: conéctate a la WiFi "LoopTuner" y abre http://192.168.4.1
   - Puerto serie 115200: h (home) t (tune) u/d (paso) b<n> (banda) p<n> (posición) s (estado)

  Librerías (solo si USAR_OLED=1): Adafruit SSD1306 + Adafruit GFX.
  Placa: "ESP32 Dev Module" (paquete esp32 de Espressif para Arduino IDE).
*/
#include <Arduino.h>
#include <Preferences.h>
#include "config.h"
#include "bandas.h"
#if USAR_WIFI
#include <WiFi.h>
#include <WebServer.h>
WebServer web(80);
#endif
#if USAR_OLED
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
Adafruit_SSD1306 oled(128, 64, &Wire, -1);
bool oledOk = false;
#endif

Preferences prefs;
int32_t pos = 0;          // posición en micropasos (0 = home / Cmin)
bool homed = false;
int banda = 0;
float roe = 0;
String estado = "Inicio";

// ------------------------------------------------------------------ motor
bool driverOn = false;
void driver(bool on) {
  if (on == driverOn) return;
  digitalWrite(PIN_EN, on ? LOW : HIGH);
  driverOn = on;
  if (on) delay(5);
}

void moverRaw(int32_t destino, uint16_t us) {
  if (destino == pos) return;
  driver(true);
  int dir = destino > pos ? 1 : -1;
  digitalWrite(PIN_DIR, ((dir > 0) ^ INVERTIR_DIR) ? HIGH : LOW);
  delayMicroseconds(20);
  while (pos != destino) {
    digitalWrite(PIN_STEP, HIGH); delayMicroseconds(3);
    digitalWrite(PIN_STEP, LOW);  delayMicroseconds(us);
    pos += dir;
  }
}

// Movimiento con compensación de holgura: la aproximación final es SIEMPRE subiendo.
void moverA(int32_t destino, uint16_t us = US_RAPIDO) {
  destino = constrain(destino, 0, PASOS_MAX);
  if (destino < pos) moverRaw(destino - HOLGURA, us);
  moverRaw(destino, us);
}

bool hallActivo() { return digitalRead(PIN_HALL) == LOW; }

bool buscarHome() {
  estado = "Buscando home";
  driver(true);
  // si ya estamos sobre el imán, salir hacia arriba primero
  int32_t n = 0;
  pos = 0;
  while (hallActivo() && n++ < 4000) moverRaw(pos + 1, US_RAPIDO);
  // bajar hasta detectar el flanco (recorrido máx. = 1 vuelta de salida)
  int32_t limite = (int32_t)(370 * PASOS_GRADO);
  for (n = 0; n < limite && !hallActivo(); n++) moverRaw(pos - 1, n < limite - 2000 ? US_RAPIDO : US_LENTO);
  if (!hallActivo()) { estado = "ERROR: sin home"; driver(false); homed = false; return false; }
  pos = 0; homed = true;
  moverA(0);           // deja el rotor con la aproximación normalizada
  driver(false);
  estado = "Home OK";
  return true;
}

// ------------------------------------------------------------------ ROE
float mv(int pin) {
  uint32_t s = 0;
  for (int i = 0; i < MUESTRAS_ADC; i++) s += analogReadMilliVolts(pin);
  float v = (s / (float)MUESTRAS_ADC) * DIVISOR_ADC;
  return v > 20 ? v + CAIDA_DIODO_MV : 0;
}

// devuelve ROE, o -1 si no hay portadora
float medirRoe() {
  float f = mv(ADC_FWD), r = mv(ADC_REF);
  if (f < UMBRAL_FWD_MV) return -1;
  float g = constrain(r / f, 0.0f, 0.99f);
  return (1 + g) / (1 - g);
}

// ------------------------------------------------------------------ memoria
String clave(int b) { return String("b") + BANDAS[b].nombre; }
int32_t posBanda(int b) { return prefs.getInt(clave(b).c_str(), BANDAS[b].preset); }
void guardarBanda(int b, int32_t p) { prefs.putInt(clave(b).c_str(), p); }

// ------------------------------------------------------------------ barridos
// barrido ascendente [desde, hasta] con paso 'salto'; devuelve la mejor posición
bool barrer(int32_t desde, int32_t hasta, int32_t salto, uint16_t us, int32_t &mejorPos, float &mejorRoe) {
  desde = constrain(desde, 0, PASOS_MAX); hasta = constrain(hasta, 0, PASOS_MAX);
  moverA(desde, US_RAPIDO);
  mejorRoe = 99; mejorPos = desde;
  int subidas = 0;
  for (int32_t p = desde; p <= hasta; p += salto) {
    moverRaw(p, us);
    delay(3);
    float s = medirRoe();
    if (s < 0) { estado = "Sin portadora"; return false; }
    if (s < mejorRoe) { mejorRoe = s; mejorPos = p; subidas = 0; }
    else if (mejorRoe < ROE_OBJETIVO && ++subidas > 6) break;   // ya pasamos el mínimo
  }
  return true;
}

bool autoajuste() {
  if (!homed && !buscarHome()) return false;
  if (medirRoe() < 0) { estado = "Sin portadora"; return false; }
  estado = "Ajustando " + String(BANDAS[banda].nombre);
  int32_t fino = BANDAS[banda].paso_fino, grueso = fino * 4;
  int32_t centro = posBanda(banda), ventana = (int32_t)(VENTANA_GRADOS * PASOS_GRADO);
  int32_t p1; float s1;
  if (!barrer(centro - ventana, centro + ventana, grueso, US_RAPIDO, p1, s1)) { driver(false); return false; }
  if (s1 > ROE_NO_ENCONTRADA) {                       // no está cerca: barrido completo
    estado = "Barrido completo";
    if (!barrer(0, PASOS_MAX, grueso, US_RAPIDO, p1, s1)) { driver(false); return false; }
  }
  int32_t p2; float s2;
  if (!barrer(p1 - 3 * grueso, p1 + 3 * grueso, fino, US_LENTO, p2, s2)) { driver(false); return false; }
  int32_t p3; float s3;                                // pasada final paso a paso
  if (barrer(p2 - fino, p2 + fino, 1, US_LENTO, p3, s3) && s3 <= s2) p2 = p3;
  moverA(p2, US_LENTO);
  delay(20);
  roe = medirRoe();
  driver(false);                                        // sin corriente: menos ruido y calor
  if (roe > 0 && roe < ROE_NO_ENCONTRADA) { guardarBanda(banda, p2); estado = "OK ROE " + String(roe, 2); return true; }
  estado = "ROE alta: revisa acoplo";
  return false;
}

void irABanda(int b) {
  banda = (b + N_BANDAS) % N_BANDAS;
  prefs.putInt("banda", banda);
  if (!homed && !buscarHome()) return;
  estado = String("Banda ") + BANDAS[banda].nombre;
  moverA(posBanda(banda)); driver(false);
}

void retocar(int dir) {
  moverA(pos + dir * BANDAS[banda].paso_fino, US_LENTO);
  driver(false);
  float s = medirRoe(); if (s > 0) roe = s;
}

// ------------------------------------------------------------------ interfaz
void pantalla() {
#if USAR_OLED
  if (!oledOk) return;
  oled.clearDisplay(); oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(2); oled.setCursor(0, 0); oled.print(BANDAS[banda].nombre);
  oled.setTextSize(1); oled.setCursor(64, 0); oled.print(BANDAS[banda].khz); oled.print(" kHz");
  oled.setCursor(64, 9); oled.print(homed ? "home OK" : "sin home");
  oled.setCursor(0, 22); oled.print("Pos "); oled.print(pos); oled.print("  "); oled.print(pos / PASOS_GRADO, 1); oled.print((char)247);
  oled.setTextSize(2); oled.setCursor(0, 34); oled.print("ROE "); if (roe > 0) oled.print(roe, 2); else oled.print("--");
  oled.setTextSize(1); oled.setCursor(0, 56); oled.print(estado.substring(0, 21));
  oled.display();
#endif
}

String json() {
  return String("{\"banda\":\"") + BANDAS[banda].nombre + "\",\"khz\":" + BANDAS[banda].khz + ",\"pos\":" + pos +
         ",\"grados\":" + String(pos / PASOS_GRADO, 2) + ",\"roe\":" + String(roe, 2) + ",\"home\":" + (homed ? "true" : "false") +
         ",\"estado\":\"" + estado + "\"}";
}

void comando(const String &c, long n) {
  if (c == "h") buscarHome();
  else if (c == "t") autoajuste();
  else if (c == "u") retocar(+1);
  else if (c == "d") retocar(-1);
  else if (c == "U") { moverA(pos + 10 * BANDAS[banda].paso_fino); driver(false); }
  else if (c == "D") { moverA(pos - 10 * BANDAS[banda].paso_fino); driver(false); }
  else if (c == "b") irABanda(n);
  else if (c == "n") irABanda(banda + 1);
  else if (c == "p") { moverA(n); driver(false); }
  else if (c == "g") { guardarBanda(banda, pos); estado = "Guardado"; }
}

#if USAR_WIFI
const char PAGINA[] PROGMEM = R"HTML(<!doctype html><html lang=es><meta name=viewport content="width=device-width">
<title>Loop Tuner</title><style>body{font-family:sans-serif;max-width:420px;margin:auto;padding:12px;background:#111;color:#eee}
button{font-size:1.1em;margin:4px;padding:12px;min-width:88px;border-radius:8px;border:0;background:#e39a3b}
#r{font-size:2.4em}select{font-size:1.1em;padding:8px}</style>
<h2>Loop Tuner</h2><div id=r>ROE --</div><div id=i></div>
<p><select id=b onchange="c('b',this.value)"></select></p>
<p><button onclick="c('D')">&laquo;&laquo;</button><button onclick="c('d')">&laquo;</button><button onclick="c('u')">&raquo;</button><button onclick="c('U')">&raquo;&raquo;</button></p>
<p><button onclick="c('t')">AUTO TUNE</button><button onclick="c('g')">Guardar</button><button onclick="c('h')">Home</button></p>
<p style="color:#aaa">Para TUNE emite una portadora de 5–10 W.</p>
<script>const B=%BANDAS%;b.innerHTML=B.map((x,i)=>`<option value=${i}>${x}</option>`).join('');
function c(k,n=0){fetch(`/cmd?c=${k}&n=${n}`).then(e=>e.json()).then(v)}
function v(j){r.textContent='ROE '+(j.roe>0?j.roe.toFixed(2):'--');i.textContent=`${j.banda} · pos ${j.pos} (${j.grados}°) · ${j.estado}`;b.value=B.indexOf(j.banda)}
setInterval(()=>fetch('/estado').then(e=>e.json()).then(v),1500);</script></html>)HTML";
void iniciarWeb() {
  WiFi.softAP(WIFI_SSID, WIFI_PASS);
  web.on("/", [] {
    String s = FPSTR(PAGINA), l = "[";
    for (int i = 0; i < N_BANDAS; i++) l += String(i ? "," : "") + "\"" + BANDAS[i].nombre + "\"";
    s.replace("%BANDAS%", l + "]");
    web.send(200, "text/html", s);
  });
  web.on("/estado", [] { float s = medirRoe(); if (s > 0) roe = s; web.send(200, "application/json", json()); });
  web.on("/cmd", [] { comando(web.arg("c"), web.arg("n").toInt()); web.send(200, "application/json", json()); });
  web.begin();
}
#endif

struct Boton { uint8_t pin; bool antes; uint32_t t0; bool largo; };
Boton bt[4] = {{BTN_ARRIBA, 1, 0, 0}, {BTN_ABAJO, 1, 0, 0}, {BTN_TUNE, 1, 0, 0}, {BTN_BANDA, 1, 0, 0}};

void leerBotones() {
  for (int i = 0; i < 4; i++) {
    bool ahora = digitalRead(bt[i].pin);
    uint32_t t = millis();
    if (!ahora && bt[i].antes) { bt[i].t0 = t; bt[i].largo = false; }             // pulsado
    if (!ahora && !bt[i].largo && t - bt[i].t0 > 600) {                          // mantenido
      if (i == 0) retocar(+1);
      else if (i == 1) retocar(-1);
      else if (i == 2 && t - bt[i].t0 > 2000) { bt[i].largo = true; buscarHome(); }
      if (i < 2) { pantalla(); continue; }
    }
    if (ahora && !bt[i].antes && t - bt[i].t0 > 30 && t - bt[i].t0 < 600) {       // soltado (corta)
      if (i == 0) retocar(+1); else if (i == 1) retocar(-1);
      else if (i == 2) autoajuste(); else irABanda(banda + 1);
    }
    bt[i].antes = ahora;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_STEP, OUTPUT); pinMode(PIN_DIR, OUTPUT); pinMode(PIN_EN, OUTPUT);
  digitalWrite(PIN_EN, HIGH);
  pinMode(PIN_HALL, INPUT_PULLUP);
  for (auto &b : bt) pinMode(b.pin, INPUT_PULLUP);
  analogSetAttenuation(ADC_11db);
  prefs.begin("looptuner", false);
  banda = constrain(prefs.getInt("banda", 0), 0, N_BANDAS - 1);
#if USAR_OLED
  oledOk = oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
#endif
#if USAR_WIFI
  iniciarWeb();
#endif
  pantalla();
  if (HOMING_AL_ARRANCAR && buscarHome()) irABanda(banda);
  Serial.println(F("Loop Tuner listo. Comandos: h t u d U D b<n> n p<n> g s"));
}

void loop() {
  static uint32_t tp = 0;
  leerBotones();
#if USAR_WIFI
  web.handleClient();
#endif
  if (Serial.available()) {
    String l = Serial.readStringUntil('\n'); l.trim();
    if (l.length()) { if (l[0] != 's') comando(l.substring(0, 1), l.substring(1).toInt()); Serial.println(json()); }
  }
  if (millis() - tp > 500) { tp = millis(); float s = medirRoe(); if (s > 0) roe = s; pantalla(); }
}
