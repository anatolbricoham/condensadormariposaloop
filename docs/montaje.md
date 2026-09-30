# Montaje paso a paso

Basado en el procedimiento de TA2WK, adaptado a las piezas de este repositorio.
Ejemplo con la **versión B (hueco 4 mm, 22 juegos, separador 9 mm)**; para otra versión
cambia solo el separador y el número de placas.

## Herramientas

Calibre (pie de rey), llaves de 8 mm (M5) ×2, llave de tubo de 8 mm, taladro de columna
(si hay que repasar agujeros), broca 5,5 mm, lima fina y lija 400–600, sierra para metal o
cortatubos (loop), soplete + soldadura (loop), medidor LCR, analizador de antena o NanoVNA,
guantes (los cantos del aluminio cortan).

## 1. Preparar las placas

1. Comprueba que todas las placas están **planas** (apóyalas sobre un cristal).
2. **Desbarba** los cantos: lija 400 → 600 hasta que al pasar el dedo no notes nada. Redondea las esquinas.
3. Repasa los agujeros con broca 5,5 mm si el M5 entra justo.
4. Limpia con alcohol isopropílico. No toques más las caras con los dedos.

## 2. Montar los dos grupos de estátor

1. Corta **4 varillas M5** a la longitud de la lista de materiales.
2. En cada varilla pon una tuerca de tope + arandela a la altura de la primera tapa.
3. Monta **dos varillas por lado** (A = derecha, B = izquierda) atravesando la tapa trasera.
4. Apila: *placa de estátor → separador (2 tuercas + 1 arandela = 9 mm) → placa de estátor →…*
   hasta tener **22 placas por lado**. Aprieta cada separador ligeramente para que la placa quede
   perpendicular. Comprueba con el calibre que la distancia entre placas es **9,0 mm ± 0,2**.
5. El estátor B es la **misma pieza girada 180°**.

## 3. Montar el rotor

1. En el eje central (varilla M5 o eje de 8 mm) coloca un collarín, la primera placa de rotor y
   separadores de 9 mm entre placas de rotor (**21 placas**).
2. Cierra con otro collarín/doble tuerca. Todas las placas de rotor deben quedar **alineadas
   angularmente** (usa una regla apoyada en los lóbulos antes de apretar).
3. Introduce el rotor entre los estátores con el rotor girado 90° (posición de Cmin) y desliza el eje
   por los rodamientos/casquillos de las tapas.

## 4. Centrado (el paso crítico)

1. Gira el rotor a Cmax: **cada placa de rotor tiene que quedar justo en medio de dos placas de estátor**
   (4 mm a cada lado). Ajusta la posición axial del rotor con las tuercas del eje.
2. Si un extremo toca y el otro no, las placas no son paralelas: corrige con arandelas.
3. Gira 360° a mano: no debe rozar en ningún punto. Mira contra una luz: se debe ver una ranura
   uniforme.
4. Coloca los 4 tirantes aislantes (M6 nylon o fibra) entre tapas y aprieta.

## 5. Pruebas eléctricas

1. **Continuidad**: entre A y B **no** debe haber continuidad en ninguna posición; entre rotor y A/B tampoco.
2. **LCR** entre A y B: anota Cmin (rotor a 90°) y Cmax (0°). Compara con `resultados/variantes.md`.
3. Si tienes acceso a un medidor de aislamiento (megger 1–5 kV) pruébalo; si no, empieza transmitiendo
   con **5–10 W** y sube poco a poco escuchando si hay chisporroteo.

## 6. Accionamiento

- El rotor está **a potencial de RF** (unos kV respecto a tierra en el peor caso): el eje debe unirse a la
  reductora/motor mediante un **acoplamiento aislante** (tramo de varilla de fibra de vidrio o nylon de
  10 cm mínimo).
- Manual: **reductora planetaria 6:1** o **dial vernier** (180° de recorrido, suficiente porque la
  mariposa va de Cmax a Cmin en 90°).
- Remoto con autoajuste (recomendado): NEMA17 + reductora 27:1 + ESP32, piezas impresas y firmware de este
  repositorio. Ver [guía paso a paso](guia_paso_a_paso.md).

## 7. Conexión al loop

- Une cada grupo de estátor a un extremo del loop con **pletina de cobre de 20–25 mm** o malla ancha,
  lo **más corta posible** (cada mΩ cuenta: con 100 W circulan 25–50 A).
- Terminales de ojal M5 atornillados en las varillas del estátor con arandela y tuerca inox, o mejor
  soldar una lengüeta de cobre al tubo.
- El condensador va en la **parte de arriba** del loop; el lazo de acoplo (Ø D/5) en la de abajo, en el
  plano del loop.

## 8. Ajuste

1. Conecta NanoVNA/analizador al lazo de acoplo.
2. Gira el condensador hasta ver el "pico" de resonancia en la banda.
3. Deforma ligeramente el lazo de acoplo (más ovalado / más redondo, o acércalo/aléjalo del tubo)
   hasta conseguir **ROE < 1,5**.
4. Recuerda: el ancho de banda es estrechísimo (ver tabla del loop); cada cambio de más de unos kHz
   exige retocar el condensador.

## Seguridad

- **Alta tensión RF**: 3–6 kV con 100 W. Quemaduras de RF graves. Nunca toques loop ni condensador
  transmitiendo.
- Campo magnético intenso cerca del loop: mantén **≥ 3 m** de distancia de personas en transmisión a 100 W
  (consulta la normativa de exposición de radioaficionados en España, Orden CTE/23/2002 y RD 1066/2001).
- Protege el condensador de la lluvia y el polvo (caja de PVC/policarbonato): la humedad reduce
  la tensión de ruptura.
