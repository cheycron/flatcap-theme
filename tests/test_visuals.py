"""README presentation assets stay traceable to canonical inputs (no image libs)."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_visuals', ROOT / 'scripts/build_visuals.py')
visuals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visuals)


class VisualTests(unittest.TestCase):
    def test_generated_board_is_current(self):
        self.assertEqual((ROOT / 'docs/visual-preview.html').read_text(), visuals.render())

    def test_visual_manifest_hashes_and_png_dimensions(self):
        manifest = json.loads((ROOT / 'images/readme/manifest.json').read_text())
        self.assertEqual(manifest['version'], json.loads((ROOT / 'src/theme.json').read_text())['version'])
        for name, digest in manifest['inputs'].items():
            with self.subTest(input=name):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
        for name, entry in manifest['images'].items():
            with self.subTest(image=name):
                content = (ROOT / name).read_bytes()
                self.assertEqual(content[:8], b'\x89PNG\r\n\x1a\n')
                self.assertEqual(list(struct.unpack('>II', content[16:24])), entry['dimensions'])
                self.assertEqual(hashlib.sha256(content).hexdigest(), entry['sha256'])

    def test_readme_image_links_and_alt_text(self):
        readme = (ROOT / 'README.md').read_text()
        import re
        images = re.findall(r'!\[([^\]]*)\]\((images/readme/[^)]+)\)', readme)
        self.assertEqual(len(images), 4)
        for alt, name in images:
            self.assertGreater(len(alt), 20)
            self.assertTrue((ROOT / name).is_file())
        self.assertIn('(images/readme/example-mobile.png)', readme)
        self.assertTrue((ROOT / 'images/readme/README.md').is_file())

    def test_readme_presents_the_core_not_a_status_report(self):
        readme = (ROOT / 'README.md').read_text()
        self.assertIn('core of Flatcap', readme)
        for heading in ('## Design principles', '## Typography', '## Motion', '## Build with Flatcap'):
            self.assertIn(heading, readme)
        for obsolete in ('**Implementation:**', 'docs/validation.md',
                         '## Develop and verify', '## Existing integrations',
                         'not a claim of a published release',
                         'Detailed guides are in Spanish', '5.4% narrower'):
            self.assertNotIn(obsolete, readme)

    def test_example_copy_is_english(self):
        html = (ROOT / 'examples/index.html').read_text()
        self.assertIn('<html lang="en"', html)
        self.assertIn('Less noise. More context.', html)
        self.assertIn('Save example', html)
        self.assertNotIn('Guardar muestra', html)
        self.assertIn('Example saved:', (ROOT / 'examples/example.js').read_text())
