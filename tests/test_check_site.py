"""Pruebas de infraestructura; no sustituyen las futuras pruebas numéricas."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_site import check_site


def html(body=""):
    return (
        '<!doctype html><html lang="es"><head><title>FIM</title>'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'</head><body><main id="inicio">{body}</main></body></html>'
    )


class CheckSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_missing_render(self):
        self.assertTrue(check_site(self.root))

    def test_valid_resources_and_anchors(self):
        self.write("index.html", html(
            '<a href="#inicio">Inicio</a><a href="capitulo/#secci%C3%B3n">Ir</a>'
            '<a href="/capitulo/">Raíz</a><img src="figura.svg" alt="Esquema">'
            '<link href="estilo.css?v=1" rel="stylesheet">'
        ))
        self.write("capitulo/index.html", html('<h2 id="sección">Sección</h2>'))
        self.write("figura.svg", "<svg/>")
        self.write("estilo.css", "body {}")
        self.assertEqual(check_site(self.root), [])

    def test_missing_target_and_fragment(self):
        self.write("index.html", html(
            '<a href="ausente.html">Ir</a><a href="#ausente">Ir</a>'
        ))
        errors = check_site(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("destino inexistente" in e for e in errors))
        self.assertTrue(any("fragmento inexistente" in e for e in errors))

    def test_external_urls_not_fetched(self):
        self.write("index.html", html(
            '<a href="https://example.invalid/">Web</a>'
            '<a href="mailto:docente@example.invalid">Correo</a>'
            '<script src="//example.invalid/script.js"></script>'
        ))
        self.assertEqual(check_site(self.root), [])

    def test_escape_rejected(self):
        self.write("index.html", html('<a href="../fuera.html">No</a>'))
        self.assertIn("fuera del sitio", check_site(self.root)[0])

    def test_accessibility_and_duplicate_ids(self):
        self.write("index.html", html(
            '<img src="data:image/png;base64,AA">'
            '<p id="inicio">Duplicado</p>'
        ).replace('lang="es"', 'lang="en"'))
        errors = check_site(self.root)
        self.assertEqual(len(errors), 3)

    def test_empty_alt_is_allowed_for_decoration(self):
        self.write("index.html", html('<img src="data:image/png;base64,AA" alt="">'))
        self.assertEqual(check_site(self.root), [])

    def test_title_viewport_and_main_required(self):
        self.write("index.html", '<html lang="es"><body>FIM</body></html>')
        self.assertEqual(len(check_site(self.root)), 3)

    def test_text_fragment(self):
        self.write("index.html", html(
            '<a href="#:~:text=FIM">Texto</a>'
            '<a href="#inicio:~:text=FIM">Inicio</a>'
        ))
        self.assertEqual(check_site(self.root), [])


if __name__ == "__main__":
    unittest.main()
