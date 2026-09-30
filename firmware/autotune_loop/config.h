// ===================== CONFIGURACIÓN DEL CONTROLADOR =====================
#pragma once

// --- Pines ESP32 DevKit v1 ---
#define PIN_STEP     25   // TMC2209 STEP
#define PIN_DIR      26   // TMC2209 DIR
#define PIN_EN       27   // TMC2209 EN (activo a nivel bajo)
#define PIN_HALL     23   // salida A3144 (colector abierto, pull-up 10k a 3,3 V en el controlador)
#define BTN_ARRIBA   32   // pulsadores a GND (pull-up interno)
#define BTN_ABAJO    33
#define BTN_TUNE     18   // pulsación corta = autoajuste · larga (2 s) = buscar home
#define BTN_BANDA    19
#define ADC_FWD      36   // VP: tensión directa del puente de ROE (tras divisor 1:2)
#define ADC_REF      39   // VN: tensión reflejada
// OLED SSD1306 0,96" I2C: SDA 21, SCL 22

#define USAR_OLED    1    // 0 si no montas pantalla
#define USAR_WIFI    1    // punto de acceso con página de control
#define WIFI_SSID    "LoopTuner"
#define WIFI_PASS    "73loop73"      // mínimo 8 caracteres

// --- Mecánica ---
#define INVERTIR_DIR     0      // pon 1 si "arriba" hace bajar la capacidad
#define HOLGURA          400    // pasos (>= holgura de la reductora, ~1,5°); aproximación final siempre subiendo
#define US_RAPIDO        150    // µs por micropaso en movimientos
#define US_LENTO         600    // µs por micropaso en el barrido fino
#define HOMING_AL_ARRANCAR 1

// --- Medida de ROE ---
#define DIVISOR_ADC      2.0f   // divisor 10k/10k en cada salida del puente (+ zener 3,3 V de protección)
#define CAIDA_DIODO_MV   200    // 1N5711 / BAT41 a baja corriente
#define UMBRAL_FWD_MV    300    // por debajo = no hay portadora
#define MUESTRAS_ADC     16
#define ROE_OBJETIVO     1.5f   // se da por buena
#define ROE_NO_ENCONTRADA 4.0f  // si el barrido local no baja de aquí, barrido completo
#define VENTANA_GRADOS   8.0f   // ± alrededor del preset/posición aprendida
