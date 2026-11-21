"""Stage and verify the exact static files approved for publication."""

import argparse
import base64
import hashlib
import html
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath


class ReleaseError(Exception):
    pass


TEXT = {'.css', '.html', '.svg', '.txt', '.webmanifest', '.xml'}
BINARY = {'.ico', '.pdf', '.png', '.woff2'}
SPECIAL = {'.nojekyll', 'CNAME', 'LICENSE', '_headers'}
MAX_FILE_BYTES = 10 * 1024 * 1024


def stage(source, output, allowlist):
    if output.exists() or output.is_symlink():
        raise ReleaseError('The publication output must be a new directory.')
    names = allowlist.read_text(encoding='utf-8').splitlines()
    if not names or 'index.html' not in names or len(set(names)) != len(names):
        raise ReleaseError('The publication file list is invalid.')
    for name in names:
        path = PurePosixPath(name)
        if (not re.fullmatch(r'[A-Za-z0-9._/-]+', name) or path.is_absolute()
                or path.as_posix() != name or '..' in path.parts
                or (name not in SPECIAL and path.suffix not in TEXT | BINARY)):
            raise ReleaseError('A publication path is invalid.')
        current = source
        for component in path.parts:
            current = current / component
            if current.is_symlink():
                raise ReleaseError('A publication path is a symbolic link.')
        if not current.is_file() or current.stat().st_size > MAX_FILE_BYTES:
            raise ReleaseError('An allowlisted asset is missing or too large.')
    output.mkdir(parents=True)
    for name in names:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)


def artifact_files(root):
    if root.is_symlink() or not (root / 'index.html').is_file():
        raise ReleaseError('The staged site is missing its homepage.')
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or (not path.is_dir() and not path.is_file()):
            raise ReleaseError('The staged site contains a non-regular entry.')
        if path.is_file():
            if path.stat().st_size > MAX_FILE_BYTES:
                raise ReleaseError('A staged asset is too large.')
            yield path


def artifact_manifest(root):
    hashes = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in artifact_files(root)}
    return (json.dumps({'version': 1, 'files': hashes}, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')


class HTMLText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def text_parts(path, data):
    if path.name in SPECIAL or path.suffix in TEXT:
        text = data.decode('utf-8')
        yield text
        decoded = html.unescape(text)
        if decoded != text:
            yield decoded
        if path.suffix in {'.html', '.svg'}:
            parser = HTMLText()
            parser.feed(text)
            yield ''.join(parser.parts)
    elif path.suffix == '.pdf':
        from pypdf import PdfReader

        pdf = PdfReader(io.BytesIO(data), strict=True)
        if pdf.is_encrypted or pdf.attachments or pdf.xfa:
            raise ReleaseError('A staged PDF uses an unsupported feature.')
        yield str(pdf.metadata or '')
        for page in pdf.pages:
            yield page.extract_text()
    elif path.suffix in {'.png', '.ico'}:
        from PIL import Image

        with Image.open(io.BytesIO(data)) as image:
            if image.width * image.height > 16_000_000:
                raise ReleaseError('A staged image is too large to inspect.')
            image.load()
            for value in image.info.values():
                if isinstance(value, str):
                    yield value
    elif path.suffix != '.woff2':
        raise ReleaseError('A staged asset has an unsupported format.')


def scan_artifact(root):
    from leak_scan import private_checks, scan

    try:
        private_checks()
    except RuntimeError:
        raise ReleaseError('Private privacy rules are missing or invalid.') from None

    files = list(artifact_files(root))
    for path in files:
        try:
            parts = (path.relative_to(root).as_posix(), *text_parts(path, path.read_bytes()))
            blocked = any(scan(part) for part in parts)
        except ReleaseError:
            raise
        except Exception:
            raise ReleaseError('A staged asset could not be inspected.') from None
        if blocked:
            raise ReleaseError('A staged asset failed privacy review. Match and path withheld.')
    return len(files)


def verify(root, public_key, signature, openssl='openssl'):
    with tempfile.TemporaryDirectory() as scratch:
        manifest = Path(scratch) / 'manifest.json'
        manifest.write_bytes(artifact_manifest(root))
        signature_bytes = Path(scratch) / 'signature'
        signature_bytes.write_bytes(base64.b64decode(signature.read_bytes().strip(), validate=True))
        result = subprocess.run(
            [openssl, 'pkeyutl', '-verify', '-pubin', '-inkey', str(public_key),
             '-rawin', '-in', str(manifest), '-sigfile', str(signature_bytes)],
            capture_output=True, check=False,
        )
        if result.returncode:
            raise ReleaseError('Privacy approval does not match this exact artifact.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    staging = commands.add_parser('stage')
    staging.add_argument('source', type=Path)
    staging.add_argument('output', type=Path)
    staging.add_argument('allowlist', type=Path)
    scanning = commands.add_parser('scan')
    scanning.add_argument('output', type=Path)
    checking = commands.add_parser('verify')
    checking.add_argument('output', type=Path)
    checking.add_argument('public_key', type=Path)
    checking.add_argument('signature', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'stage':
            stage(args.source, args.output, args.allowlist)
        elif args.command == 'scan':
            print(f'Privacy review passed for {scan_artifact(args.output)} staged files.')
        else:
            verify(args.output, args.public_key, args.signature)
            print('Privacy approval matches the exact staged files.')
    except ReleaseError as error:
        print(error, file=sys.stderr)
        return 1
    except (OSError, ValueError):
        print('The publication check could not complete.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
