import contextlib
import hashlib
import io
import os
from pathlib import Path
import tempfile
import unittest

import patch_gguf as patch

class PatchTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.file = Path(self.directory.name) / 'fixture.gguf'
        self.original = b'GGUF\x03\x00\x00\x00template\n' + patch.OLD + b'\n' + bytes(range(256))
        self.expected = self.original.replace(patch.OLD, patch.NEW)
        self.file.write_bytes(self.original)
        self.args = {'expected_source': hashlib.sha256(self.original).hexdigest(), 'expected_result': hashlib.sha256(self.expected).hexdigest(), 'expected_bytes': len(self.original)}

    def run_patch(self, **overrides):
        with contextlib.redirect_stdout(io.StringIO()):
            return patch.patch_file(self.file, **(self.args | overrides))

    def test_bytes_and_idempotence(self):
        self.assertEqual(self.run_patch(), 'patched')
        self.assertEqual(self.file.read_bytes(), self.expected)
        self.assertEqual(len(self.expected), len(self.original))
        self.assertEqual(self.run_patch(), 'already_patched')
        self.assertEqual(self.file.read_bytes(), self.expected)

    def test_wrong_source_checksum_does_not_modify(self):
        with self.assertRaises(ValueError):
            self.run_patch(expected_source='0' * 64)
        self.assertEqual(self.file.read_bytes(), self.original)

    def test_shared_hard_link_is_refused(self):
        second = Path(self.directory.name) / 'shared.gguf'
        os.link(self.file, second)
        with self.assertRaises(ValueError):
            self.run_patch()
        self.assertEqual(second.read_bytes(), self.original)

    def test_bad_result_checksum_rolls_back(self):
        with self.assertRaises(ValueError):
            self.run_patch(expected_result='0' * 64)
        self.assertEqual(self.file.read_bytes(), self.original)

    def test_incomplete_file_is_refused(self):
        self.file.write_bytes(self.original[:-1])
        with self.assertRaises(ValueError):
            self.run_patch()
        self.assertEqual(self.file.read_bytes(), self.original[:-1])

if __name__ == '__main__':
    unittest.main()
