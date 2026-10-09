# Qwen3.8-Flash-Next app compatibility patch

**Release: v1.0.0.** An independent compatibility patch; not an official Qwen, Unsloth, Ollama, or OpenAI release.

I ran into this error while trying to use Qwen3.8-Flash-Next through Ollama in the ChatGPT desktop app:

```text
Jinja Exception: System message must be at the beginning.
```

The model worked in Ollama, but its chat template rejected system/developer instructions added later in a conversation. This is the patch I used to get it working. The steps below let you apply the same fix to the exact model file I tested.

Reproduce the fix for `Jinja Exception: System message must be at the beginning` when using the specialised whm0627 IQ1_S GGUF through the local ChatGPT/Codex app integration.

This repository contains a small patch script and Ollama configuration. Model weights are downloaded separately from Hugging Face. No OpenAI API key is needed for this local fix.

## Exact upstream file

- Repository: `whm0627/Qwen3.8-Flash-Next-177B-A3B-fits64GB-PLElast-GGUF`
- Revision: `8945f87bd117558a4bcdd930e622c5ff763c8f26`
- Filename: `Qwen3.8-Flash-Next-IQ1_S-PLElast.gguf`
- Bytes: `72546461152`
- Original SHA-256: `84b49b7443eaad3f98af9d1cf9933130a6ca7720266deb6a9a6849eaa5d8cf0b`
- Patched SHA-256: `07b1744a131c293bae4cc45c3f236ed0b0a2e348ce0d609f57dab157842efb80`

Download link: https://huggingface.co/whm0627/Qwen3.8-Flash-Next-177B-A3B-fits64GB-PLElast-GGUF/resolve/8945f87bd117558a4bcdd930e622c5ff763c8f26/Qwen3.8-Flash-Next-IQ1_S-PLElast.gguf

## Install on another computer

If you already have the working patched GGUF, you can transfer `Qwen3.8-Flash-Next-IQ1_S-PLElast-compat.gguf` from the first computer using an external SSD. Put it beside `Modelfile`, change the `FROM` line to that filename, and run `ollama create`. This avoids downloading the weights again. The patched SHA-256 above identifies the exact working file.

1. Install Python 3.9 or newer and a recent Ollama runtime with `qwen4exp` GGUF support. Ollama 0.40.2 was tested on macOS; other operating systems and hardware need their own generation test.
2. Download the exact pinned GGUF into this folder. Reuse an existing complete download if its original checksum matches. Do not patch a file already imported into Ollama's cache.
3. Apply the patch **before importing**:

```sh
python3 patch_gguf.py Qwen3.8-Flash-Next-IQ1_S-PLElast.gguf --in-place
```

On Windows, use `python` in place of `python3` if that is the installed command. The script has no third-party Python dependencies.

4. Import and run:

```sh
ollama create qwen-flash-next -f Modelfile
ollama run qwen-flash-next --think=false
```

Ollama's normal import may allocate a separate cache file depending on the operating system and importer. The patch itself does not create another model-sized file.

5. In the Ollama app, expose/select this model in its ChatGPT integration as appropriate. Retry a multi-turn chat in the desktop app. Check the allocated context and offload:

```sh
ollama ps
```

The supplied configuration requests 64k context and full GPU offload. Adjust it for the other computer's available RAM and GPU. The original performance and memory results were obtained on an M1 Max with 64 GB unified memory, not on every PC.

## What changes

The native template's rejection of later system/developer messages is replaced by a system instruction block at that message's original position. Content is preserved; developer instructions map to system blocks consistently with the original template and Ollama's local app proxy. Reasoning and tool-call formatting are retained.

The replacement is the same byte length, so the GGUF metadata length, tensor offsets, and tensor contents remain unchanged. The script verifies both the full original and resulting model hashes. It refuses other model revisions, incomplete downloads, symlinks, and unpatched shared hard-link files. Re-running it on the verified patched file is a no-op.

## Validation

The resulting model hash matches the model successfully tested on the M1 Max. Tests covered late system/developer instructions, structured tool calls, OpenAI-style JSON arguments, tool-result replay, and both `none` and `high` reasoning through `/api/codex/v1/responses`. Every synthetic instruction was retained once and in order. This does not guarantee the model will obey every instruction or support every app tool.

`TESTED.md` records the tested environment and limits. The patch script's fixture tests cover byte preservation, idempotence, checksum refusal, hard-link refusal, and rollback after a mismatched result.

Run the fixture tests locally with:

```sh
python3 -m unittest discover -s . -p test_patch.py -v
```

The GitHub workflow runs these tests on Windows, Linux, and macOS with Python 3.12 and 3.14. It does not download model weights. Actions are pinned to specific official commit hashes and the workflow uses read-only repository permissions. See the repository's Actions tab for hosted results.

## Publishing and preservation

Push this small folder to a GitHub repository, then create a version tag/release such as `v1.0.0`. Keep a copy of the ZIP on another drive as well. Publish the script, configuration, documentation, and license; `.gitignore` excludes the large GGUF files.

Use `RELEASE_NOTES.md` as the release description and `SHA256SUMS` to verify the source files. The source archive contains only explicitly selected release files, without local logs, cache files, Git history, credentials, or personal paths.

This patch intentionally targets one exact upstream file. New releases should be verified and tested separately, not accepted by disabling the checksum check. If the native upstream template is fixed later, this patch may no longer be needed.

## Credits and license

Base model: Qwen/Qwen3.8-Flash-Next. Quantization and native template: Unsloth. SSD-friendly PLElast repack: whm0627. Model weights remain subject to their upstream license and provenance.

The patch script and configuration are distributed under Apache-2.0; see `LICENSE`.
