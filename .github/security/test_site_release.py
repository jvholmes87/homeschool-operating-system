import base64
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from site_release import ReleaseError, stage, scan_artifact, artifact_manifest, verify


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.source = root / 'source'
        self.source.mkdir()
        self.output = root / 'output'
        self.allowlist = root / 'allowlist.txt'
        self.allowlist.write_text('index.html\n', encoding='utf-8')
        self.page = self.source / 'index.html'
        self.page.write_text('<p>Fictional public page</p>', encoding='utf-8')

    def test_stage_publishes_only_the_allowlist(self):
        (self.source / 'private.txt').write_text('invented fixture', encoding='utf-8')
        stage(self.source, self.output, self.allowlist)
        self.assertEqual([path.name for path in self.output.iterdir()], ['index.html'])

    def test_stage_refuses_path_traversal_without_creating_output(self):
        self.allowlist.write_text('index.html\n../notes.txt\n', encoding='utf-8')
        with self.assertRaises(ReleaseError):
            stage(self.source, self.output, self.allowlist)
        self.assertFalse(self.output.exists())

    def test_stage_refuses_missing_asset_without_creating_output(self):
        self.allowlist.write_text('index.html\nstyle.css\n', encoding='utf-8')
        with self.assertRaises(ReleaseError):
            stage(self.source, self.output, self.allowlist)
        self.assertFalse(self.output.exists())

    def test_privacy_scan_requires_rules(self):
        stage(self.source, self.output, self.allowlist)
        with patch.dict('os.environ', {'PRIVATE_DENY_PATTERNS_JSON': ''}):
            with self.assertRaises(ReleaseError):
                scan_artifact(self.output)

    def test_privacy_scan_rejects_encoded_identifiers_without_printing_them(self):
        self.page.write_text('<p>Invented-&#65;lpha</p>', encoding='utf-8')
        stage(self.source, self.output, self.allowlist)
        with patch.dict('os.environ', {'PRIVATE_DENY_PATTERNS_JSON': '["Invented-Alpha"]'}):
            with self.assertRaises(ReleaseError) as failure:
                scan_artifact(self.output)
        self.assertNotIn('Invented-Alpha', str(failure.exception))

    def test_manifest_changes_on_byte_changes_and_added_files(self):
        stage(self.source, self.output, self.allowlist)
        before = artifact_manifest(self.output)
        self.assertEqual(set(json.loads(before)['files']), {'index.html'})
        (self.output / 'index.html').write_bytes(b'Fictional alternate page')
        self.assertNotEqual(before, artifact_manifest(self.output))
        (self.output / 'index.html').write_bytes(self.page.read_bytes())
        (self.output / 'extra.txt').write_bytes(b'Fictional extra page')
        self.assertNotEqual(before, artifact_manifest(self.output))

    def test_signature_can_only_authorize_matching_assets(self):
        stage(self.source, self.output, self.allowlist)
        root = Path(self.temp.name)
        private = root / 'temporary-test-key.pem'
        public = root / 'public.pem'
        manifest = root / 'manifest.json'
        signed = root / 'signature.bin'
        proof = root / 'signature.txt'
        openssl = os.environ.get('OPENSSL_BIN', 'openssl')
        subprocess.run([openssl, 'genpkey', '-algorithm', 'ed25519', '-out', str(private)], check=True)
        subprocess.run([openssl, 'pkey', '-in', str(private), '-pubout', '-out', str(public)], check=True)
        manifest.write_bytes(artifact_manifest(self.output))
        subprocess.run([openssl, 'pkeyutl', '-sign', '-rawin', '-inkey', str(private),
                        '-in', str(manifest), '-out', str(signed)], check=True)
        proof.write_bytes(base64.b64encode(signed.read_bytes()))
        verify(self.output, public, proof, openssl)
        (self.output / 'index.html').write_bytes(b'Fictional unmatched content')
        with self.assertRaises(ReleaseError):
            verify(self.output, public, proof, openssl)


if __name__ == '__main__':
    unittest.main()
