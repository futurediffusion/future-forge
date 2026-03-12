# UI Development Notes

## Guía de validación manual: modo Classic vs Future

> Objetivo: validar que la experiencia y los resultados de UI en **Future** no regresan frente a **Classic** en los flujos de generación más usados.

### Preparación previa

1. Inicia una instancia de **Classic** y otra de **Future** con el mismo modelo/checkpoint y extensiones comparables.
2. Usa el mismo navegador, resolución de ventana y tema UI en ambas instancias.
3. Limpia estado previo antes de cada bloque:
   - refresca la página,
   - fija semilla conocida,
   - vacía/normaliza prompt y parámetros.
4. Registra evidencia (capturas y/o notas) por cada caso con timestamp.

---

### 1) Generación básica (prompt + negative + styles)

**Pasos manuales**

1. En `txt2img`, escribe un prompt corto y uno negativo (por ejemplo, 15-30 tokens cada uno).
2. Aplica un estilo desde el selector de styles (y luego quítalo para verificar ida/vuelta).
3. Ejecuta `Generate` en Classic y en Future con los mismos parámetros base (steps, sampler, seed, size).

**Criterios de aceptación observables**

- Los campos de prompt/negative aceptan edición normal sin lag visible ni pérdida de texto.
- Aplicar/quitar styles modifica el contenido esperado (combinación o restauración) de forma consistente en ambos modos.
- `Generate` produce imagen sin errores UI (sin bloqueos, sin botones atascados).
- La metadata de parámetros mostrada/guardada refleja prompt, negative y style aplicado correctamente.

---

### 2) Hires fix / dimensiones / CFG / batch / scripts

**Pasos manuales**

1. Activa `Hires fix` y configura upscale + second pass steps.
2. Cambia `Width/Height`, `CFG Scale`, `Batch count` y `Batch size`.
3. Ejecuta al menos un script común (por ejemplo, X/Y/Z Plot o script interno disponible en ambos modos).
4. Lanza generación y compara comportamiento entre Classic y Future.

**Criterios de aceptación observables**

- `Hires fix` aparece/habilita los controles relacionados y estos responden al cambio de estado.
- Width/Height/CFG/Batch mantienen el valor al generar (sin reset inesperado).
- El script seleccionado muestra su panel y aplica sus parámetros al job.
- El conteo de imágenes y resolución final coincide con la configuración solicitada.

---

### 3) Paste params, token counters, restore progress, upscale

**Pasos manuales**

1. Copia parámetros de una imagen previa (`Paste params`) y aplícalos en una sesión limpia.
2. Verifica actualización de `token counters` al editar prompt/negative.
3. Inicia una generación, recarga la UI (si aplica) y valida `restore progress`.
4. Ejecuta upscale sobre una imagen generada y revisa parámetros derivados.

**Criterios de aceptación observables**

- `Paste params` rellena los campos esperados (prompt, sampler, steps, seed, tamaño, etc.).
- Los token counters cambian en tiempo real y no quedan desincronizados tras pegar parámetros.
- `Restore progress` recupera estado de cola/progreso sin duplicar ni perder el job visible.
- El flujo de upscale inicia y finaliza con salida visible, sin errores de estado en la galería.

---

### 4) Extra networks y cambio entre tabs

**Pasos manuales**

1. Abre panel de `Extra networks` (LoRA/embeddings/u otros disponibles).
2. Inserta al menos un recurso en prompt desde el panel.
3. Cambia entre tabs (`txt2img`, `img2img`, `Extras`, etc.) repetidamente durante edición.
4. Vuelve al tab inicial y confirma persistencia de estado.

**Criterios de aceptación observables**

- El panel carga elementos y permite búsqueda/selección sin congelamientos.
- Insertar un recurso en prompt produce el token/formato esperado.
- El cambio de tabs no limpia campos críticos ni rompe componentes colapsables.
- Al volver al tab original, los valores principales se mantienen (salvo los que deban resetearse explícitamente).

---

### 5) Menú de Generate forever, interrupt/skip y estados de botones

**Pasos manuales**

1. Abre el menú asociado a `Generate` y activa/desactiva `Generate forever`.
2. Inicia generación y usa `Interrupt` en una corrida.
3. Inicia otra corrida y usa `Skip` (cuando haya más de una iteración/paso aplicable).
4. Observa el estado visual de botones durante: idle, running, interrupted, finished.

**Criterios de aceptación observables**

- `Generate forever` alterna estado de forma clara y persistente según diseño esperado.
- `Interrupt` detiene el trabajo activo en tiempo razonable y devuelve botones a estado coherente.
- `Skip` avanza/cancela la unidad en curso sin dejar la UI bloqueada.
- Los botones no muestran estados contradictorios (por ejemplo, `Generate` habilitado mientras sigue running real).

---

## Plantilla breve de reporte (recomendada)

- Entorno: commit, navegador, GPU, flags de arranque.
- Caso validado: sección y paso.
- Resultado: ✅ OK / ⚠️ Parcial / ❌ Falla.
- Evidencia: captura/log breve.
- Diferencia Classic vs Future: ninguna / menor / crítica.
- Acción sugerida: bug, ajuste UX, o no aplica.
