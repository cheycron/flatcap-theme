"""Core integrity and regression tests, Python 3.10+ standard library only."""
import copy
import json
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build
import validate


class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = []
        self.labels = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.references.extend(values[k] for k in ('src', 'href') if k in values)
        if 'id' in values:
            self.ids.append(values['id'])
        if tag == 'label' and 'for' in values:
            self.labels.append(values['for'])


class ThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = build.load()

    def test_integrity_and_exact_roles(self):
        validate.integrity(self.data)
        self.assertEqual(len(self.data['themes']['slate']), 43)
        self.assertEqual(set(self.data['themes']['slate']), set(self.data['themes']['daylight']))

    def test_missing_role_rejected(self):
        data = copy.deepcopy(self.data)
        del data['themes']['daylight']['focus.ring']
        with self.assertRaises(ValueError):
            validate.integrity(data)

    def test_alpha_and_lowercase_rejected(self):
        for bad in ('#ffffff', '#FFFFFF80', 'rgb(1 2 3)', '#FFF'):
            with self.subTest(value=bad):
                data = copy.deepcopy(self.data)
                data['themes']['slate']['bg.canvas'] = bad
                with self.assertRaises(ValueError):
                    validate.integrity(data)

    def test_missing_foundation_density_or_brand_role_rejected(self):
        for group, role in [('typography', 'font.ui'), ('metrics', 'focus.width')]:
            with self.subTest(group=group):
                data = copy.deepcopy(self.data)
                del data[group][role]
                with self.assertRaises(ValueError):
                    validate.integrity(data)
        data = copy.deepcopy(self.data)
        del data['branding']['roles']['wordmark']
        with self.assertRaises(ValueError):
            validate.integrity(data)

    def test_known_contrast_values(self):
        self.assertEqual(validate.contrast('#000000', '#FFFFFF'), 21)
        self.assertEqual(validate.contrast('#808080', '#808080'), 1)
        self.assertAlmostEqual(validate.luminance('#FF0000'), .2126)
        self.assertAlmostEqual(validate.contrast('#777777', '#FFFFFF'), 4.478089453577214)

    def test_contrast_contracts(self):
        report = validate.contracts(self.data)
        self.assertEqual(report['total'], 372)
        self.assertEqual(report['passed'], report['total'])

    def test_bad_palette_fails_contract(self):
        data = copy.deepcopy(self.data)
        data['themes']['slate']['text.primary'] = data['themes']['slate']['bg.canvas']
        report = validate.contracts(data)
        self.assertLess(report['passed'], report['total'])

    def test_generated_exports_match(self):
        for path, expected in build.outputs(self.data).items():
            with self.subTest(path=path.name):
                self.assertEqual(path.read_text(), expected)
        subprocess.run([sys.executable, 'scripts/build.py', '--check'], cwd=ROOT, check=True, capture_output=True)

    def test_css_token_export_parity(self):
        css = build.css(self.data)
        # Every color appears under its semantic property; no numbered compatibility aliases.
        for theme in self.data['themes'].values():
            for key, value in theme.items():
                self.assertIn(f'{build.prop(key)}: {value};', css)
        for key in ('typography', 'metrics'):
            for token, value in self.data[key].items():
                self.assertIn(f'{build.prop(token)}: {value};', css)
        self.assertNotIn('--flatcap-0:', css)
        self.assertNotIn('body {', css)
        self.assertNotIn('@font-face', css)

    def test_css_preferences_contract(self):
        css = build.css(self.data)
        for selector in ('data-fc-theme="daylight"', 'data-fc-theme="system"', 'data-fc-contrast="more"', 'data-fc-contrast="system"', 'data-fc-density="compact"'):
            self.assertIn(selector, css)
        self.assertIn('--fc-text-primary: var(--fc-contrast-text-primary);', css)
        self.assertIn('prefers-reduced-motion: reduce', css)
        self.assertNotIn('font.dense', json.dumps(self.data['density']))

    def test_svg_roles_and_provenance(self):
        namespace = {'s': 'http://www.w3.org/2000/svg'}
        palette = {**self.data['themes'][self.data['branding']['theme']], **self.data['branding']['colors']}
        for name in ('logo.svg', 'readme_logo.svg'):
            source = (ROOT / 'src' / name).read_text()
            svg = ET.fromstring(source)
            self.assertIsNotNone(svg.find('s:title', namespace))
            self.assertIsNotNone(svg.find('s:desc', namespace))
            self.assertIn('Vexels.com', source)
            self.assertNotIn('<text', source)
            count = 0
            for element in svg.iter():
                if 'data-fc-role' in element.attrib:
                    count += 1
                    self.assertEqual(element.attrib['fill'], palette[self.data['branding']['roles'][element.attrib['data-fc-role']]])
            self.assertGreaterEqual(count, 4)

    def test_brand_mineral_is_separate_from_ui(self):
        self.assertEqual(self.data['branding']['colors'], {'cap.band': '#638BAA', 'cap.underside': '#344D62'})
        self.assertEqual(self.data['themes']['slate']['syntax.function'], '#ABC9CB')
        self.assertEqual(self.data['themes']['slate']['bg.raised'], '#292F36')
        for color in self.data['branding']['colors'].values():
            self.assertNotIn(color, build.css(self.data))
            self.assertNotIn(color, build.scss(self.data))

    def test_invalid_branding_color_rejected(self):
        data = copy.deepcopy(self.data)
        data['branding']['colors']['cap.band'] = '#638BAA80'
        with self.assertRaises(ValueError):
            validate.integrity(data)

    def test_svg_generation_idempotent_preserves_geometry(self):
        for name in ('logo.svg', 'readme_logo.svg'):
            source = (ROOT / 'src' / name).read_text()
            altered = source.replace('fill="#9BBFDF"', 'fill="#000000"')
            self.assertEqual(build.svg_colors(altered, self.data), source)
            self.assertEqual(build.svg_colors(source, self.data), source)

    def test_markdown_local_links(self):
        paths = [ROOT / 'README.md', ROOT / 'SKILL.md', *(ROOT / 'docs').rglob('*.md')]
        for path in paths:
            # Code fences contain illustrative consumer paths, not navigable repo links.
            text = re.sub(r'```[^\n]*\n.*?```', '', path.read_text(), flags=re.S)
            links = re.findall(r'\]\(([^)]+)\)', text)
            links += re.findall(r'(?:src|href)="([^"]+)"', text)
            for link in links:
                url = urlsplit(link.split(' "')[0])
                if url.scheme or url.netloc or not url.path:
                    continue
                with self.subTest(file=path.relative_to(ROOT), link=link):
                    self.assertTrue((path.parent / unquote(url.path)).exists())

    def test_example_resources_labels_and_ids(self):
        parser = ResourceParser()
        parser.feed((ROOT / 'examples/index.html').read_text())
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        for label in parser.labels:
            self.assertIn(label, parser.ids)
        for link in parser.references:
            url = urlsplit(link)
            self.assertFalse(url.scheme, 'Example must not depend on external resources')
            if url.path:
                self.assertTrue((ROOT / 'examples' / url.path).exists(), link)
            if url.fragment:
                self.assertIn(url.fragment, parser.ids)

    def test_example_uses_only_known_custom_properties(self):
        css = (ROOT / 'examples/example.css').read_text()
        defined = set(re.findall(r'(--fc-[a-z0-9-]+):', build.css(self.data)))
        used = set(re.findall(r'var\((--fc-[a-z0-9-]+)', css))
        self.assertFalse(used - defined, used - defined)

    def test_skill_portable_contract(self):
        source = (ROOT / 'SKILL.md').read_text()
        self.assertTrue(source.startswith('---\nname: flatcap-design\n'))
        self.assertNotIn('/mnt/', source)
        self.assertNotIn('docs/v2/', source)
        self.assertIn('43 roles', source)


if __name__ == '__main__':
    unittest.main()
