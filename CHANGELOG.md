# Changelog

## 1.0.0

- Reproduce the tested chat-template compatibility fix for the pinned whm0627 Qwen3.8-Flash-Next IQ1_S PLElast GGUF.
- Render later system/developer instructions as system blocks while preserving instruction content and order.
- Preserve native thinking, tool formatting, tensor bytes, and tensor offsets.
- Verify the complete original and resulting model checksums.
- Refuse incomplete downloads, other model revisions, symlinks, and unpatched shared hard-link files.
- Provide a 64k Ollama configuration and portable Python patch script.
- Include fixture tests, automated Windows/Linux/macOS checks, validation notes, provenance, and Apache-2.0 license.

Full-model generation was tested on macOS with an M1 Max and 64 GB unified memory. Fixture tests are separate from hardware-specific inference benchmarks.
