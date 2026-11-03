#!/usr/bin/env python3
"""Check the published tree after Hugo generation, including retained legacy pages."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_URL = '/lib/jquery/jquery-3.7.1.min.js'
EXPECTED_SHA256 = 'fc9a93dd241f6b045cbff0481cf4e1901becd0e12fb45166a8f17f95823f0b1a'


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.jquery = []

    def handle_starttag(self, tag, attrs):
        src = dict(attrs).get('src', '')
        if tag == 'script' and 'jquery' in src.lower():
            self.jquery.append(src)


errors = []
library = ROOT / EXPECTED_URL.lstrip('/')
if not library.is_file() or sha256(library.read_bytes()).hexdigest() != EXPECTED_SHA256:
    errors.append('The canonical jQuery file differs from the official 3.7.1 distribution.')

pages = 0
for path in ROOT.rglob('*.html'):
    parser = Scripts()
    parser.feed(path.read_text(encoding='utf-8'))
    if parser.jquery:
        pages += 1
        if parser.jquery != [EXPECTED_URL]:
            errors.append(f'{path.relative_to(ROOT)}: unexpected jQuery scripts: {parser.jquery}')

copies = []
for path in ROOT.rglob('*.js'):
    if re.search(rb'jQuery v\d+\.\d+\.\d+', path.read_bytes()):
        copies.append(path.relative_to(ROOT).as_posix())
if copies != [EXPECTED_URL.lstrip('/')]:
    errors.append(f'Unexpected vendored jQuery copies: {copies}')
if not pages:
    errors.append('No pages using jQuery were found; check the published-tree path.')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {pages} pages use the single, unmodified official jQuery 3.7.1 distribution.')
