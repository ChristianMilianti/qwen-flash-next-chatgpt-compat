#!/usr/bin/env python3
"""Apply the tested Qwen app-compatibility fix to a freshly downloaded GGUF.

SPDX-License-Identifier: Apache-2.0
Uses only the Python standard library. Patch before importing into Ollama.
"""
import argparse
import hashlib
import os
from pathlib import Path
import sys

SOURCE_SHA = '84b49b7443eaad3f98af9d1cf9933130a6ca7720266deb6a9a6849eaa5d8cf0b'
PATCHED_SHA = '07b1744a131c293bae4cc45c3f236ed0b0a2e348ce0d609f57dab157842efb80'
MODEL_BYTES = 72546461152
OLD = b"{{- raise_exception('System message must be at the beginning.') }}"
NEW = b"{{- '<|im_start|>system\\n' + content + '<|im_end|>\\n' }}".ljust(len(OLD))

def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            block = f.read(32 * 1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()

def patch_file(path, expected_source=SOURCE_SHA, expected_result=PATCHED_SHA, expected_bytes=MODEL_BYTES):
    path = Path(path)
    if path.is_symlink():
        raise ValueError('Use a regular downloaded file, not a symlink or Ollama cache entry.')
    if path.stat().st_size != expected_bytes:
        raise ValueError('Wrong file size or incomplete download; no changes made.')
    print('Verifying the full model checksum...', flush=True)
    digest = sha256(path)
    if digest == expected_result:
        print('Already patched; checksum matches. No changes needed.', flush=True)
        return 'already_patched'
    if digest != expected_source:
        raise ValueError('Model checksum does not match the pinned upstream file; no changes made.')
    if path.stat().st_nlink != 1:
        raise ValueError('File has hard links. Patch a fresh download before Ollama import, not a shared cache file.')
    with path.open('rb') as f:
        header = f.read(64 * 1024 * 1024)
    if header[:4] != b'GGUF' or header.count(OLD) != 1:
        raise ValueError('Expected template branch not found exactly once; no changes made.')
    offset = header.index(OLD)
    try:
        with path.open('r+b') as f:
            f.seek(offset)
            if f.read(len(OLD)) != OLD:
                raise ValueError('File changed during verification.')
            f.seek(offset)
            f.write(NEW)
            f.flush()
            os.fsync(f.fileno())
        print('Checking the patched model checksum...', flush=True)
        if sha256(path) != expected_result:
            raise ValueError('Patched checksum mismatch.')
    except BaseException:
        with path.open('r+b') as f:
            f.seek(offset)
            f.write(OLD)
            f.flush()
            os.fsync(f.fileno())
        raise
    print('Patched successfully. Tensor bytes and offsets are unchanged.', flush=True)
    print('SHA-256:', expected_result, flush=True)
    return 'patched'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path, help='Freshly downloaded IQ1_S GGUF, before Ollama import')
    parser.add_argument('--in-place', action='store_true', required=True, help='Explicitly modify only the template in this file, avoiding a second 72 GB copy')
    args = parser.parse_args()
    try:
        patch_file(args.model)
    except (ValueError, OSError) as error:
        print('Error:', error, file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
