# LLM Hardware & VRAM Dimensioning Calculator

Herramienta técnica para modelado cuantitativo de recursos computacionales requeridos por modelos de lenguaje en ejecución local. Calcula con precisión el consumo de VRAM, requerimientos de contexto (KV Cache), sobrecarga del sistema operativo y tasa de transferencia de tokens.

---

## Arquitectura y Componentes

- **Calculador central:** `calculador_vram_llm.py` con modelado de cuantizaciones (FP16, Q8_0, Q4_K_M).
- **Métricas:** Estimación de tokens por segundo según ancho de banda de memoria de la GPU (GB/s).
- **Prevención de cuellos de botella:** Alerta ante desbordes a memoria RAM del sistema.

---

## Instrucciones de Uso

```bash
# Cálculo de requisitos para modelo de 8B parámetros en contexto de 8k
python tools/calculador_vram_llm.py --params 8 --quant Q4_K_M --ctx 8192
```

---

## Consideraciones de Seguridad

- Este repositorio almacena código fuente, utilitarios de prueba y documentación técnica de ingeniería.
- Todas las credenciales, llaves privadas y variables de entorno deben suministrarse de forma local mediante archivos no versionados.
- Las herramientas de auditoría contenidas deben utilizarse exclusivamente en entornos autorizados y laboratorios de prueba.

---

**Autor:** Juan Carlos Araneda M.  
**Licencia:** MIT License (consulte [LICENSE](LICENSE))
