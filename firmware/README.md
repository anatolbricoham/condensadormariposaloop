# Firmware de autoajuste (ESP32)

| Fichero | Qué es |
|---|---|
| `autotune_loop/autotune_loop.ino` | Programa principal: motor, home, medida de ROE, autoajuste, pulsadores, OLED, web |
| `autotune_loop/config.h` | Pines y parámetros (holgura, velocidades, umbrales, WiFi) |
| `autotune_loop/bandas.h` | **Generado** por `cad/generar_3d.py`: posiciones calculadas de cada banda |
| `test/simular.sh` | Compila el firmware en el PC (g++) con cabeceras simuladas y simula un autoajuste |

## Algoritmo

1. **Home**: baja hasta el flanco del sensor Hall → posición 0 = Cmin.
2. **Barrido grueso** ascendente de ±8° alrededor de la posición aprendida (o del preset) con saltos de ¼ del ancho de banda.
3. Si la ROE no baja de 4, **barrido completo** de 0 a 95°.
4. **Barrido fino** alrededor del mejor punto y **pasada final paso a paso**.
5. **Aproximación final siempre subiendo**: si hay que retroceder, se baja `HOLGURA` pasos de más y se vuelve a subir, para que la holgura de la reductora no afecte.
6. Se **desactiva el driver** (sin ruido ni consumo) y la posición se **guarda** en la memoria flash del ESP32 para esa banda.

Simulación incluida (resonancia de 32 pasos de ancho y 300 pasos de holgura): el autoajuste acaba en la resonancia exacta.

## Compilar

Arduino IDE 2 → placa **ESP32 Dev Module** (paquete *esp32* de Espressif) → librerías *Adafruit SSD1306* y *Adafruit GFX*.
Con PlatformIO: `platform = espressif32`, `board = esp32dev`, `framework = arduino`.
Pon `USAR_OLED 0` o `USAR_WIFI 0` en `config.h` si no usas esas funciones.
