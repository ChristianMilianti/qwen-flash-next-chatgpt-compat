# v1.0.0 — Qwen Flash Next desktop app compatibility

I ran into `System message must be at the beginning` when trying to use Qwen3.8-Flash-Next through Ollama in the ChatGPT desktop app. The model ran in Ollama, but failed when the app added instructions later in the conversation. Here is the patch I used to get it working, with the installation steps and checksums so you can reproduce the fix.

This release fixes `Jinja Exception: System message must be at the beginning` for the exact whm0627 Qwen3.8-Flash-Next IQ1_S PLElast GGUF documented in the README.

The patch preserves later system/developer instructions instead of rejecting them. Native reasoning and tool formatting are retained. Only template bytes change; the model's tensors and their offsets remain unchanged.

## Included

- Portable Python patch script with full checksum verification and rollback if the resulting checksum is wrong.
- Ollama Modelfile requesting 64k context.
- Installation instructions, provenance, tests, validation limits, and Apache-2.0 license.

Model weights and inference runtimes are obtained separately. The patch itself requires only Python's standard library.

## Validation

Full-model tests passed on an Apple M1 Max with 64 GB unified memory using Ollama 0.40.2: late instructions, multi-turn chat, structured tool calls, tool-result replay, and `none`/`high` reasoning through the desktop app's local Responses proxy. Ollama reported 64k context, 100% GPU, 44 GB allocation, and zero swap during short tests.

The portable script's five fixture tests passed locally. The included GitHub workflow runs those tests on Windows, Linux, and macOS; see the repository's Actions tab for hosted results.

## Installation

1. Obtain the exact pinned GGUF linked in the README, or transfer an already-patched copy.
2. Apply the script to a freshly downloaded file before Ollama import.
3. Import with the included Modelfile, adjusting context and offload for the target hardware.
4. Select `qwen-flash-next` in the app and verify generation.

## Scope

Targets one exact model file and revision. New upstream files require separate verification. Windows/Linux full-model performance and sustained long-context workloads have not been benchmarked. This is an independent compatibility patch, not an official Qwen, Unsloth, Ollama, or OpenAI release.
