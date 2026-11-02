# Enlaces y Fuentes Oficiales de Benchmarks de IA Local

Este documento recopila los enlaces y repositorios comunitarios verificados para contrastar mediciones de velocidad (tokens/segundo) y rendimiento de modelos de lenguaje en hardware económico.

---

## 1. Repositorios Oficiales y Herramientas de Benchmark

- **llama.cpp (Repositorio Oficial en GitHub):**  
  [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)  
  *Contiene el código fuente y las versiones compiladas que incluyen `llama-bench`.*
- **Releases y Binarios Compilados de llama.cpp (Windows y Linux):**  
  [https://github.com/ggml-org/llama.cpp/releases](https://github.com/ggml-org/llama.cpp/releases)  
  *Descargas directas de binarios precompilados con soporte CUDA (cu12.x), ROCm, Vulkan y CPU.*
- **Ollama (Repositorio Oficial):**  
  [https://github.com/ollama/ollama](https://github.com/ollama/ollama)  
  *Documentación oficial para ejecutar modelos con estadísticas detalladas de tokens/segundo (`ollama run --verbose`).*
- **Intel IPEX-LLM (Optimizaciones para Intel Arc A770):**  
  [https://github.com/intel/ipex-llm](https://github.com/intel/ipex-llm)  
  *Biblioteca oficial de aceleración para GPUs Intel Arc con ejemplos de benchmarking.*

---

## 2. Comunidades de Pruebas y Hilos de Benchmarks

- **Comunidad r/LocalLLaMA en Reddit:**  
  [https://www.reddit.com/r/LocalLLaMA/](https://www.reddit.com/r/LocalLLaMA/)  
  *El foro de referencia internacional donde miles de usuarios publican pruebas de hardware real.*
- **Discusiones de Rendimiento y Benchmarks en llama.cpp:**  
  [https://github.com/ggml-org/llama.cpp/discussions](https://github.com/ggml-org/llama.cpp/discussions)  
  *Hilos técnicos con registros de rendimiento (`llama-bench`) para NVIDIA Pascal, Ampere, Ada, AMD RDNA y Apple Silicon.*
- **Análisis de Rendimiento de Tom's Hardware en GPUs para IA Local:**  
  [https://www.tomshardware.com/pc-components/gpus/ai-gpu-benchmarks-test-local-llms-on-your-pc](https://www.tomshardware.com/pc-components/gpus/ai-gpu-benchmarks-test-local-llms-on-your-pc)  
  *Metodología de laboratorio estandarizada midiendo tokens/segundo en diferentes modelos y GPUs de consumo.*
