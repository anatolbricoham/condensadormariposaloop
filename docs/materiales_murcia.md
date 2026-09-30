# Dónde conseguir los materiales en Murcia

> Direcciones, horarios y precios cambian: llama antes. Los precios son orientativos (2026).
> Las cantidades exactas por versión están en [`resultados/lista_materiales.md`](../resultados/lista_materiales.md).

## 1. Placas de aluminio cortadas por láser (lo más importante)

Lleva en un pendrive (o manda por email) los ficheros **`cad/salida/rotor.dxf`** y
**`cad/salida/estator.dxf`**. Pide:

- **Aluminio 1 mm**, aleación EN AW-1050 o 5754 (vale cualquiera que tengan en stock; 5754 es más rígida).
- Cantidades: ver lista de materiales (+10 % de repuesto).
- **Desbarbado** (vibrado/lijado) de los cantos: en alta tensión cualquier rebaba es un punto de arco.
- Que **no** doblen ni marquen las placas: tienen que quedar planas.
- Orientativo: 1–2 € por pieza en series de 50–100; muchos talleres ponen el material.

| Taller | Zona | Web |
|---|---|---|
| Corte Láser García | Murcia | https://lasergarcia.es/ |
| Corte Láser JM (también metacrilato) | Murcia | https://cortelaserjm.com/ |
| GME Lasercut (corte y grabado) | Murcia | https://gmelasercut.es/ |
| Cortyple – corte de chapa a medida | Murcia | https://cortyple.com/ |
| Láser Molina | Molina de Segura | https://www.lasermolina.com/ |
| Plegados Nicolás – corte láser | Murcia | https://www.plegadosnicolas.es/corte-laser |
| Moralsa (almacén propio de chapa) | Región de Murcia | https://www.moralsa.com/ |
| TCI Cutting / Sidemur (aluminio y férricos) | Murcia | http://sidemur.es/productos/corte-de-chapa-en-laser/ |
| **Alternativa online**: LaserBoost (subes el DXF, te lo envían) | envío | https://www.laserboost.com/es/corte-laser-murcia/ |

Si solo consigues **acero inoxidable 1 mm**, también sirve (TA2WK lo ofrece), pero pesa ~3× y
tiene más resistencia; en la mariposa la corriente por placa es baja, así que las pérdidas son aceptables.

## 2. Tapas (placas finales) aislantes

Fichero **`cad/salida/tapa.dxf`**, 2 unidades, **policarbonato o metacrilato de 8–10 mm**
(el policarbonato aguanta mejor el sol y los golpes; si la antena va en exterior, mejor
policarbonato o PTFE). Alternativa: imprimir en **PETG/ASA** con 100 % de relleno.

- Corte Láser JM – taller de metacrilato: https://cortelaserjm.com/taller-metacrilato/
- Diseñato (metacrilato y policarbonato en Murcia): https://www.disenato.com/content/13-metacrilato-en-murcia
- GME Lasercut: https://gmelasercut.es/
- Impresión 3D: pregunta en el Radio Club Región de Murcia o en makerspaces locales.

## 3. Tornillería inoxidable M5

Varilla roscada **M5 inox A2 (DIN 975)** en barras de 1 m, **tuercas DIN 934 M5** (altura 4 mm) y
**arandelas DIN 125 M5** (espesor 1 mm), **siempre inox** (no zincado: se oxida y el óxido provoca arcos).

- Obramat Murcia (ex-Bricomart): https://www.obramat.es/almacenes/obramat-murcia.html
- Leroy Merlin Murcia y ferreterías / suministros industriales de la zona (compra por cajas de 100: sale mucho más barato).
- Suministro industrial online con base en Murcia: https://todoparalaindustria.com/collections/suministro-industrial

**Receta de separadores** (evita tener que cortar tubo con precisión):

| Hueco | Separador | Montaje |
|---|---|---|
| 3 mm | 7 mm | 1 tuerca + 3 arandelas |
| 4 mm | 9 mm | 2 tuercas + 1 arandela |
| 5 mm | 11 mm | 2 tuercas + 3 arandelas |
| 6 mm | 13 mm | 3 tuercas + 1 arandela |

Mide un lote de tuercas con el calibre: si salen de 3,8 mm en vez de 4,0 compensa con arandelas.
Alternativa más limpia: **tubo de aluminio 8×1 mm** cortado a medida (tornero o taller de aluminio).

## 4. Tubo de cobre para el loop

- **Tubo de cobre 22 mm** (barra 2,5 m, rígido) + **7 codos de 45°** de soldar para hacer un octógono de 1 m:
  Obramat Murcia (barra 22 mm 2,5 m: https://www.obramat.es/barra-cobre-o22mm-2-5m-10424911.html),
  Leroy Merlin, BigMat, almacenes de fontanería.
- Para el octógono de Ø 1 m necesitas **3,14 m** de perímetro → 8 tramos de ≈ 39 cm → **2 barras de 2,5 m**.
- Alternativa: **tubo de cobre recocido** en rollo (se curva a mano en círculo), en almacenes de climatización.
- Soldadura: **estaño-plata (soldadura blanda de fontanería) o mejor soldadura fuerte (plata 15–40 %)**
  con soplete. Las uniones son la principal fuente de pérdidas.

## 5. Electrónica / RF

- **Electrónica Llorga** (Murcia): https://electronicallorga.com/ — conectores PL-259/SO-239 o N, coaxial RG-213/RG-58,
  terminales, termorretráctil, núcleos de ferrita (choke), motorreductor 12 V.
- Murcia Electrónica – tienda de componentes: https://www.murciaelectronica.com/category/tienda-de-componentes-electronicos/
- Listados de tiendas: https://murcia10.es/tienda-componentes-electronicos-murcia/
- **Reductora planetaria 6:1 / dial vernier**: no es habitual en tiendas físicas; se compra online
  (eBay, AliExpress, Oren Elliott Products, MGS4U, enlaces del artículo de TA2WK) o de segunda mano
  en el **Merca Radio Región de Murcia**.

## 6. Comunidad local (muy recomendable)

- **Radio Club Región de Murcia – EA5RCZ**: https://ea5rcz.es/ (organizan el Merca Radio, donde se
  encuentran condensadores de vacío, reductoras, analizadores de antena…).
- URE – Secciones: https://www.ure.es/secciones/

Con ellos puedes conseguir prestado un **medidor LCR** (para medir Cmin/Cmax) y un
**analizador de antenas** (NanoVNA, RigExpert) para ajustar el loop.
