# Fase 2: Investigación de Hardware, Valores de Mercado y Compatibilidad de SO

**Proyecto:** `H_LLM_IA_BBB` (Bueno, Bonito y Barato)  
**Fecha de corte:** Septiembre 2026  
**Fuentes analizadas:** Mercado secundario (eBay, AliExpress, plataformas locales), retail (Amazon, Newegg), repositorios y foros de la comunidad de IA local (*r/LocalLLaMA*, Ollama, llama.cpp).

---

## 1. Catálogo de Opciones de Hardware Económico (Tier BBB)

Hemos categorizado las mejores alternativas del mercado ordenadas por su filosofía de coste y viabilidad práctica:

### Categoría A: GPUs Dedicadas de Consumo (Máxima compatibilidad y facilidad)

#### 1. NVIDIA GeForce RTX 3060 12GB (La "Reina Indiscutible" del Hardware BBB)
- **Especificaciones:** 12 GB GDDR6, bus de 192-bit, ancho de banda: **360 GB/s** (versión original) / **288 GB/s** (revisión estándar). CUDA Compute Capability 8.6 (Ampere).
- **Precio de Mercado:** ~$190 – $240 USD (Usada) | ~$270 – $310 USD (Nueva).
- **Ratio Coste por GB VRAM:** ~$16.6 – $20.0 USD / GB.
- **Modelos que corre 100% en VRAM:** Llama 3.1 8B (Q8 o Q4 a 16k contexto), Qwen 2.5 14B (Q4_K_M a 8k contexto).
- **Ventajas:** Compatibilidad absoluta "plug-and-play" con cualquier software (Ollama, LM Studio, vLLM, llama.cpp). Consumo contenido (170W).
- **Desventajas:** No puede con modelos de 32B sin recurrir a offload lento a RAM.

#### 2. NVIDIA GeForce RTX 2060 12GB (La alternativa Turing ultra-económica)
- **Especificaciones:** 12 GB GDDR6, bus de 192-bit, ancho de banda: **336 GB/s**. Compute Capability 7.5 (Turing).
- **Precio de Mercado:** ~$150 – $190 USD (Usada).
- **Ratio Coste por GB VRAM:** ~$12.5 – $15.8 USD / GB.
- **Evaluación:** Excelente opción si el presupuesto no alcanza para la RTX 3060. Misma capacidad de 12GB para correr modelos de 14B.

#### 3. Intel Arc A770 16GB (La campeona del ancho de banda y 16GB)
- **Especificaciones:** 16 GB GDDR6, bus de 256-bit, ancho de banda masivo: **512 GB/s**.
- **Precio de Mercado:** ~$270 – $330 USD (Usada / Ofertas retail).
- **Ratio Coste por GB VRAM:** ~$16.8 – $20.6 USD / GB.
- **Modelos que corre 100% en VRAM:** 14B en Q5_K_M / Q8_0 y 32B en cuantizaciones muy compactas (IQ3/IQ4 con contexto moderado).
- **Ventajas:** 16 GB reales con un ancho de banda altísimo (512 GB/s se traduce en hasta ~45-50 tokens/s en modelos de 14B).
- **Desventajas:** Requiere placa base con soporte estricto de **Resizable BAR (ReBAR)**. No tiene CUDA nativo; depende de Intel oneAPI / IPEX-LLM o backends Vulkan/SYCL en llama.cpp. Mayor fricción de instalación inicial.

#### 4. AMD Radeon RX 7600 XT 16GB
- **Especificaciones:** 16 GB GDDR6, bus de 128-bit, ancho de banda: **288 GB/s** (+ 32MB Infinity Cache). RDNA 3.
- **Precio de Mercado:** ~$320 – $380 USD.
- **Ratio Coste por GB VRAM:** ~$20.0 – $23.7 USD / GB.
- **Evaluación:** 16GB de VRAM modernos con bajo consumo. Excelente en Linux vía ROCm; en Windows requiere LM Studio con backend HIP/ROCm o DirectML.

---

### Categoría B: Hardware de Servidor Reciclado (Máxima VRAM por Dólar)

#### 5. NVIDIA Tesla P40 24GB (El "Caballo de Batalla" de 24 GB)
- **Especificaciones:** 24 GB GDDR5, bus de 384-bit, ancho de banda: **346 GB/s**. Arquitectura Pascal (2016).
- **Precio de Mercado:** ~$160 – $230 USD (AliExpress / eBay).
- **Ratio Coste por GB VRAM:** **~$7.0 – $9.5 USD / GB** (La métrica más barata del mercado).
- **Modelos que corre 100% en VRAM:** Modelos de 32B (Qwen 2.5 32B en Q4_K_M) con total fluidez (~14-16 t/s).
- **Requisitos Críticos y Retos:**
  - **Refrigeración:** Es una tarjeta pasiva para servidores. Requiere adaptador de ventilador (impreso en 3D o comprado por ~$15 USD) con un ventilador blower de 12V ruidoso o potente.
  - **Alimentación:** Conector CPU EPS de 8 pines (no PCIe estándar; requiere cable adaptador).
  - **Sin salidas de vídeo:** Opera como acelerador secundario (la pantalla va a la iGPU de la CPU o a otra gráfica básica).
  - **Arquitectura Pascal:** No tiene núcleos Tensor modernos ni aceleración FP16 rápida. Sin embargo, en inferencia cuantizada INT4/INT8 con llama.cpp y GGUF rinde con gran solvencia.

---

### Categoría C: Mini PCs y APUs con Memoria Unificada (Silencio, Bajo Consumo y Flexibilidad)

#### 6. Mini PC AMD Ryzen 7 7840HS / 8845HS con 32GB o 64GB DDR5
- **Especificaciones:** 8 núcleos Zen 4, gráfica integrada Radeon 780M (RDNA 3), soporte para 32 GB o 64 GB DDR5-5600 en Dual Channel (ancho de banda compartido: **~85-90 GB/s**).
- **Precio de Mercado:** Mini PC barebone (~$320 – $380 USD) + Kit 64GB RAM DDR5 (~$130 – $160 USD) + SSD NVMe 1TB (~$65 USD). **Total: ~$515 – $600 USD**.
- **Cómo funciona para IA:** En la BIOS se asigna ("VRAM fija" o asignación dinámica) hasta **16 GB** (en sistema de 32 GB) o hasta **48 GB** (en sistema de 64 GB) para la iGPU.
- **Rendimiento:**
  - Modelos 8B (Q4_K_M): **~15 – 20 tokens/segundo** (ideal para lectura humana).
  - Modelos 14B (Q4_K_M): **~8 – 10 tokens/segundo**.
  - Modelos 32B / 70B: Posible cargarlos íntegros con 64GB de RAM (~3.5 t/s para 32B, ~1.5 t/s para 70B).
- **Ventajas:** Consumo eléctrico mínimo (25W - 54W), silencioso, sirve como mini servidor casero 24/7 (Nextcloud, Home Assistant, servidor API de LLM).
- **Regla Inquebrantable:** Debe ser **Dual Channel** obligatorio (dos módulos de RAM). Un solo módulo (Single Channel) reduce el ancho de banda a la mitad (~45 GB/s) y hace la inferencia insoportablemente lenta.

---

### Categoría D: Configuraciones Multi-GPU Caseras (Doble Tarjeta BBB)

#### 7. Doble RTX 3060 12GB (Total 24GB VRAM)
- **Costo total de GPU:** ~$400 – $480 USD (en mercado usado).
- **Cómo opera:** Ollama (desde v0.4+) y `llama.cpp` reparten las capas del modelo automáticamente entre ambas tarjetas (`tensor-split 1,1`). No se requiere puente SLI ni soporte NVLink; la comunicación de activaciones entre capas viaja por el bus PCIe.
- **Rendimiento en 32B Q4_K_M:** ~14 – 16 tokens/segundo.
- **Requisitos:** Placa base con al menos dos ranuras PCIe x16 físicas (funcionando a x8/x8 o x16/x4) y fuente de poder de 650W - 750W.

---

## 2. Comparativa de Sistemas Operativos: Windows vs. Linux

| Criterio | Windows 11 | Linux (Ubuntu / Fedora / Arch) |
| :--- | :--- | :--- |
| **Facilidad para Principiantes** | ⭐⭐⭐⭐⭐ LM Studio y Ollama se instalan con 1 clic con instalador `.exe`. | ⭐⭐⭐ Requiere familiaridad con terminal, permisos de drivers y gestión de paquetes. |
| **Soporte NVIDIA (CUDA)** | Nativo y excelente. Drivers oficiales de consumo estables. | Nativo y óptimo. Rendimiento prefill ligeramente superior (~5-10%). |
| **Soporte AMD (Radeon)** | DirectML (más lento) o HIP experimental en LM Studio. | **ROCm nativo:** Máximo rendimiento oficial, comparable a CUDA. |
| **Soporte Intel Arc** | Buen soporte mediante IPEX-LLM para Windows y llama.cpp Vulkan. | oneAPI / SYCL disponible; excelente para scripts y entornos Docker. |
| **Consumo de VRAM en Reposo** | **Alto:** El compositor DWM y la interfaz reservan entre 400 MB y 900 MB de VRAM. | **Mínimo:** En servidores headless ~50 MB; con escritorio ligero (XFCE/KDE) ~150-250 MB. |
| **Despliegue de Servidores 24/7** | Mayor consumo energético, reinicios forzados por actualizaciones de Windows. | **Excelente:** `systemd` para servicios Ollama/vLLM, Docker sin capa de virtualización WSL2. |

> [!TIP]
> **Veredicto de Sistema Operativo:**  
> - Si eres usuario de escritorio que quiere jugar y chatear con su modelo localmente de forma interactiva: **Windows + LM Studio / Ollama**.  
> - Si tu objetivo es una estación de trabajo dedicada a IA, tienes gráfica AMD, o buscas la máxima eficiencia en memoria VRAM libre: **Linux (Ubuntu 24.04 LTS)** es la opción superior.

---

## 3. Matriz Resumen de Coste y Eficiencia (BBB Index)

| Opción de Hardware | VRAM / Memoria | Inversión Estimada (USD) | Tokens/s (Modelo 8B Q4) | Tokens/s (Modelo 14B Q4) | Modelo Máximo Recomendado | Nivel de Dificultad de Montaje |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RTX 3060 12GB (Usada)** | 12 GB | ~$200 – $240 | ~48 – 55 t/s | ~25 – 30 t/s | 14B Q4_K_M | Muy Fácil (Enchufar y listo) |
| **RTX 2060 12GB (Usada)** | 12 GB | ~$150 – $190 | ~40 – 46 t/s | ~20 – 24 t/s | 14B Q4_K_M | Muy Fácil |
| **Tesla P40 24GB (Usada)** | 24 GB | ~$170 – $230 (+ $30 mod) | ~50 – 60 t/s | ~30 – 35 t/s | 32B Q4_K_M | Avanzado (Refrigeración y cables) |
| **Intel Arc A770 16GB** | 16 GB | ~$280 – $340 | ~70 – 85 t/s | ~40 – 48 t/s | 14B Q8 / 32B IQ3 | Medio (Requiere ReBAR y configuración) |
| **RX 7600 XT 16GB** | 16 GB | ~$320 – $380 | ~45 – 50 t/s | ~24 – 28 t/s | 14B Q5 / 32B IQ3 | Medio (Fácil en Linux, moderado en Win) |
| **Mini PC Ryzen 7 + 64GB DDR5** | 64 GB unificada | ~$520 – $600 (PC Completo) | ~16 – 20 t/s | ~8 – 10 t/s | 32B / 70B (Baja vel.) | Muy Fácil (Equipo compacto) |
| **Dual RTX 3060 12GB (24GB)** | 24 GB | ~$420 – $480 (2 tarjetas) | ~50 t/s | ~28 t/s | 32B Q4_K_M | Medio (Placa base con 2 PCIe y fuente) |
