# Checklist de validación manual: `txt2img_future`

> Objetivo: validar que la pestaña **Future** en txt2img es funcionalmente equivalente (o superior) a **Generation** antes de planificar su sustitución.

## Reglas de avance (gate)

- [ ] **No** planificar sustitución de `Generation` hasta completar todos los checks de este documento.
- [ ] Cada caso debe registrarse con estado: `PASS` / `FAIL` / `N/A`.
- [ ] Todo `FAIL` debe incluir evidencia y ticket de seguimiento.

---

## 0) Preparación

- [ ] Arrancar WebUI con build actual.
- [ ] Activar feature flag `txt2img_show_future_tab`.
- [ ] Confirmar que están visibles ambas pestañas: `Future` y `Generation`.
- [ ] Usar mismo modelo/checkpoint, sampler y seed base para comparar resultados entre tabs.

Evidencia sugerida:
- Captura de UI con ambas pestañas.
- Log de arranque mostrando configuración aplicada.

---

## 1) Disparo de generación (Enter + botón)

### Caso 1.1 — Enter en prompt
- [ ] En `Future`, escribir prompt válido.
- [ ] Presionar **Enter** en el cuadro de prompt.
- [ ] Verificar que inicia generación sin clic en botón.
- [ ] Verificar que no dispara doble job.

### Caso 1.2 — Botón Generate
- [ ] En `Future`, ejecutar con botón **Generate**.
- [ ] Verificar que inicia generación una sola vez.
- [ ] Verificar comportamiento consistente con Enter (estado, progreso y resultado).

Criterio de aceptación:
- [ ] Enter y botón generan exactamente un job por acción, sin diferencias funcionales relevantes.

---

## 2) Actualización correcta de `gallery`, `infotext` y `html_log`

### Caso 2.1 — `gallery`
- [ ] Tras generar, `gallery` muestra imagen(s) nuevas.
- [ ] Orden y cantidad de imágenes coincide con parámetros (`batch size`, etc.).

### Caso 2.2 — `infotext`
- [ ] `infotext` se actualiza para la última imagen.
- [ ] Incluye parámetros esperados (prompt, seed, sampler, steps, cfg, tamaño, etc.).

### Caso 2.3 — `html_log`
- [ ] `html_log` se actualiza en cada ejecución.
- [ ] No contiene errores JS/Python ni placeholders vacíos inesperados.

Criterio de aceptación:
- [ ] Los tres outputs se refrescan en cada corrida y permanecen sincronizados.

---

## 3) Cobertura de parámetros clave

Ejecutar una corrida por cada bloque y verificar impacto en salida + `infotext`.

### Caso 3.1 — Negative prompt
- [ ] Cambiar negative prompt y confirmar efecto/registro.

### Caso 3.2 — Tamaño
- [ ] Probar al menos 2 resoluciones diferentes.
- [ ] Confirmar dimensiones finales en metadata/resultado.

### Caso 3.3 — CFG
- [ ] Probar mínimo dos valores de CFG (bajo/alto).
- [ ] Confirmar que se refleja en `infotext`.

### Caso 3.4 — Batch
- [ ] Probar variación de `batch size` y/o `batch count`.
- [ ] Verificar cantidad total de imágenes y navegación en `gallery`.

### Caso 3.5 — Hires fix
- [ ] Activar `hires fix` y ejecutar.
- [ ] Validar segunda etapa/upscale y parámetros asociados en `infotext`.

Criterio de aceptación:
- [ ] Todos los parámetros se aplican correctamente y quedan trazables en outputs.

---

## 4) Compatibilidad con `custom_inputs` y scripts

### Caso 4.1 — `custom_inputs`
- [ ] Probar al menos un flujo que use `custom_inputs`.
- [ ] Confirmar que UI/valores se leen y afectan generación.

### Caso 4.2 — Scripts
- [ ] Probar scripts representativos habilitados para txt2img (al menos 2).
- [ ] Verificar que se ejecutan sin errores y que sus parámetros se respetan.

Criterio de aceptación:
- [ ] `Future` mantiene compatibilidad operativa con extensibilidad existente.

---

## 5) No regresiones en `Generation` clásica

### Caso 5.1 — Smoke test básico
- [ ] Ejecutar flujo estándar en tab `Generation`.
- [ ] Verificar outputs (`gallery`, `infotext`, `html_log`) y controles básicos.

### Caso 5.2 — Paridad mínima
- [ ] Repetir set corto de pruebas clave (Enter/botón, CFG, batch, hires fix) en `Generation`.
- [ ] Confirmar que no aparece degradación tras cambios relacionados con `Future`.

Criterio de aceptación:
- [ ] `Generation` sigue estable mientras coexistencia esté activa.

---

## 6) Cierre y decisión

### Resumen de ejecución
- Fecha:
- Responsable:
- Commit/branch validado:
- Entorno (GPU/CPU, SO, navegador):

### Resultado por bloque
- 1) Enter + botón: `PASS/FAIL`
- 2) gallery/infotext/html_log: `PASS/FAIL`
- 3) parámetros clave: `PASS/FAIL`
- 4) custom_inputs/scripts: `PASS/FAIL`
- 5) regresión Generation: `PASS/FAIL`

### Gate final
- [ ] **Checklist completo en PASS**.
- [ ] **Solo entonces** abrir tarea de planificación para sustituir `Generation`.

## 7) Planificación de sustitución de `Generation` (habilitar únicamente al pasar gate)

> Completar esta sección **solo** cuando el gate final esté en verde.

- [ ] Definir estrategia de migración (feature flag, rollout gradual o switch directo).
- [ ] Inventariar dependencias de UI/API/scripts afectadas por `Generation`.
- [ ] Definir plan de comunicación de cambio para usuarios/extensiones.
- [ ] Preparar plan de rollback.
- [ ] Acordar criterios de “done” para retirar `Generation`.
