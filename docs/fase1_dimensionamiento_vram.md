# Fase 1: Dimensionamiento Matemático y Requisitos de Memoria (LLM Local)

**Proyecto:** `H_LLM_IA_BBB`  
**Fecha de corte:** Septiembre 2026  
**Herramienta de cálculo utilizada:** [`tools/calculador_vram_llm.py`](file:///c:/Users/Juan%20Carlos/Documents/Antigravity%20projects/H_LLM_IA_BBB/tools/calculador_vram_llm.py)

---

## 1. El Concepto Clave: ¿Por qué la VRAM es el factor crítico?

En la ejecución local de modelos de lenguaje (LLM), el rendimiento está determinado principalmente por el **ancho de banda de memoria** (*Memory Bandwidth*) y la **capacidad de memoria de vídeo (VRAM)**, no por la potencia de cálculo bruto (TFLOPS).

- **Inferencia Autorregresiva (Token a Token):** Para generar un único token, la GPU debe leer la totalidad de los pesos del modelo desde la memoria a los núcleos de cómputo.
- **Caída drástica de velocidad por desborde a RAM:**
  - VRAM GDDR6 / GDDR6X: **~288 a 1.000 GB/s** $\rightarrow$ Rendimiento típico: **25 a 120 tokens/segundo**.
  - RAM del sistema (DDR4 / DDR5 Dual Channel): **~40 a 90 GB/s** $\rightarrow$ Rendimiento en offload mixto: **~1 a 3 tokens/segundo**.
  - Si un modelo no cabe por completo en la VRAM, desbordar incluso 500 MB hacia la memoria RAM reduce la velocidad a un ritmo demasiado lento para una conversación interactiva.

---

## 2. Anatomía del Consumo de VRAM

El espacio total ocupado en la GPU se divide en tres componentes ineludibles:

$$\text{VRAM Total Requerida} = \text{Peso de los Pesos Cuantizados} + \text{KV Cache (Contexto)} + \text{Sobrecarga del Runtime / Sistema}$$

1. **Pesos del Modelo:** Dependen de la cantidad de parámetros (en miles de millones, B) y los bits por peso (BPW) de la cuantización:
   - FP16 (Sin cuantizar): 16.0 bits/peso (~2.0 GB por cada 1B de parámetros).
   - Q8_0: 8.5 bits/peso (~1.05 GB por 1B).
   - Q4_K_M (Estándar de oro equilibrio calidad/peso): ~4.5 bits/peso (~0.55 GB por 1B).
   - IQ4_XS / Q3_K_M: ~3.4 a 4.25 bits/peso (~0.42 a 0.52 GB por 1B).
2. **KV Cache (Memoria de Contexto):** Almacena las representaciones clave-valor de los tokens ya procesados en la conversación. Crece linealmente con la cantidad de tokens activos (4k, 8k, 16k, 32k). En modelos modernos con GQA (*Grouped Query Attention*), el consumo se ha optimizado enormemente pero sigue siendo significativo en contextos largos.
3. **Sobrecarga de Framework (Runtime Overhead):** Entre 400 MB y 800 MB reservados por CUDA, ROCm, DirectML o Vulkan para buffers de activación de tensores y contexto del sistema operativo (en Windows, el compositor DWM consume aproximadamente 300-500 MB adicionales de la GPU principal si tiene pantalla conectada).

---

## 3. Matriz de Requisitos de VRAM por Modelo y Cuantización

Valores exactos calculados para los modelos más populares de 2025/2026:

| Familia de Modelo | Parámetros Reales | Cuantización | Ventana Contexto | Pesos (GiB) | KV Cache (GiB) | VRAM Total Mínima | Categoría de Hardware Requerida |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Llama 3.2 / Qwen 2.5** | 3.2B | `Q4_K_M` | 4.096 | 1.74 | 0.44 | **2.83 GiB** | GPU 4GB / 6GB o iGPU básica |
| **Llama 3.2 / Qwen 2.5** | 3.2B | `Q8_0` | 8.192 | 3.29 | 0.88 | **4.82 GiB** | GPU 6GB / 8GB |
| **Llama 3.1 / Qwen 2.5** | 8.0B | `Q4_K_M` | 4.096 | 4.36 | 0.50 | **5.51 GiB** | GPU 8GB (RX 6600, RTX 3050/4060) |
| **Llama 3.1 / Qwen 2.5** | 8.0B | `Q4_K_M` | 8.192 | 4.36 | 1.00 | **6.01 GiB** | GPU 8GB con margen ajustado |
| **Llama 3.1 / Qwen 2.5** | 8.0B | `Q4_K_M` | 16.384 | 4.36 | 2.00 | **7.01 GiB** | GPU 8GB (límite absoluto) / 12GB |
| **Llama 3.1 / Qwen 2.5** | 8.0B | `Q5_K_M` | 8.192 | 5.33 | 1.00 | **6.98 GiB** | GPU 8GB / 12GB |
| **Llama 3.1 / Qwen 2.5** | 8.0B | `Q8_0` | 8.192 | 8.23 | 1.00 | **9.88 GiB** | GPU 12GB (RTX 3060 12GB) |
| **Qwen 2.5 / DeepSeek R1** | 14.7B | `Q4_K_M` | 4.096 | 8.01 | 0.75 | **9.41 GiB** | GPU 12GB (RTX 3060 12GB) |
| **Qwen 2.5 / DeepSeek R1** | 14.7B | `Q4_K_M` | 8.192 | 8.01 | 1.50 | **10.16 GiB** | GPU 12GB (Holgado) / 16GB |
| **Qwen 2.5 / DeepSeek R1** | 14.7B | `Q5_K_M` | 8.192 | 9.79 | 1.50 | **11.94 GiB** | GPU 16GB (Arc A770 / RX 7600 XT) |
| **Qwen 2.5 / Coder 32B** | 32.5B | `IQ4_XS` | 4.096 | 16.72 | 1.00 | **18.37 GiB** | GPU 24GB (Tesla P40 / Dual 3060) |
| **Qwen 2.5 / Coder 32B** | 32.5B | `Q4_K_M` | 4.096 | 17.71 | 1.00 | **19.36 GiB** | GPU 24GB |
| **Qwen 2.5 / Coder 32B** | 32.5B | `Q4_K_M` | 8.192 | 17.71 | 2.00 | **20.36 GiB** | GPU 24GB |
| **Llama 3.3 / Qwen 72B** | 70.0B | `Q3_K_M` | 4.096 | 29.15 | 1.25 | **31.05 GiB** | Setup Dual 24GB (48GB) o APU 64GB |
| **Llama 3.3 / Qwen 72B** | 70.0B | `Q4_K_M` | 4.096 | 38.14 | 1.25 | **40.04 GiB** | Setup Dual 24GB (48GB) o APU 64GB |

---

## 4. Conclusiones Matemáticas de la Fase 1

1. **El umbral de los 8 GB:** Permite ejecutar modelos de 7B/8B en cuantización `Q4_K_M` con soltura (hasta 8k de contexto), pero queda completamente excluido de modelos 14B.
2. **El punto dulce económico (12 GB):** Con 12 GB de VRAM se desbloquea el acceso a modelos de 14B (como Qwen 2.5 14B), que ofrecen un salto de calidad y razonamiento sustancial respecto a los modelos 8B.
3. **El salto a los 24 GB:** Necesario para abordar modelos de 32B (Qwen 2.5 32B o modelos de razonamiento avanzado). Se puede alcanzar de forma ultra-económica mediante tarjetas de servidor recicladas (Tesla P40) o configuraciones multi-GPU dual (2x RTX 3060).
