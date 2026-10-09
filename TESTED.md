# Tested environment

- Apple M1 Max, 64 GB unified memory, internal Apple SSD.
- Ollama 0.40.2, bundled llama.cpp 0.5.0 runtime.
- Model: pinned IQ1_S PLElast file documented in README.
- Configured context: 65,536 tokens.
- Ollama reports 100% GPU and 44 GB allocation; no swap in short tests.
- Patched SHA-256: `07b1744a131c293bae4cc45c3f236ed0b0a2e348ce0d609f57dab157842efb80`.

The original model reproduced the exact line-110 Jinja exception. The patched model passed late-instruction rendering, multi-turn generation, tool calls, tool-result replay, and the local desktop app's Responses proxy with `none` and `high` reasoning.

An exploratory `low` reasoning request rendered but returned reasoning without a final answer. The app catalog exposes `none` and `high` for this model. Windows/Linux performance and full long-context workloads have not been benchmarked.
