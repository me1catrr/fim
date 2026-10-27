"""Comprueba el HTML local de Quarto sin dependencias ni acceso a la red."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.errors = []
        self.lang = ""
        self.viewport = False
        self.main = False
        self.in_title = False
        self.title = ""
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identifier = attrs.get("id")
        if identifier:
            if identifier in self.ids:
                self.errors.append(f"id duplicado: {identifier}")
            self.ids.add(identifier)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = "width=device-width" in attrs.get("content", "")
        if tag == "main":
            self.main = True
        if tag == "title":
            self.in_title = True
        if tag == "img" and "alt" not in attrs:
            self.errors.append("imagen sin atributo alt")
        for name in ("href", "src", "poster"):
            if attrs.get(name):
                self.links.append(attrs[name])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check_site(root):
    """Devuelve errores; comprueba ficheros y fragmentos, no URLs externas."""
    root = Path(root).resolve()
    if not (root / "index.html").is_file():
        return ["No existe index.html; ejecutar primero quarto render."]
    pages = {
        path.resolve(): Page(path.read_text(encoding="utf-8"))
        for path in root.rglob("*.html")
    }
    errors = []
    for path, page in pages.items():
        label = str(path.relative_to(root))
        issues = list(page.errors)
        if not page.lang.lower().startswith("es"):
            issues.append("falta idioma español")
        if not page.viewport:
            issues.append("falta viewport responsive")
        if not page.main:
            issues.append("falta elemento main")
        if not page.title.strip():
            issues.append("falta título")
        for link in page.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            local = unquote(parts.path)
            target = (
                root / local.lstrip("/") if local.startswith("/")
                else path.parent / local if local else path
            ).resolve()
            if not target.is_relative_to(root):
                issues.append(f"enlace fuera del sitio: {link}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                issues.append(f"destino inexistente: {link}")
                continue
            fragment = unquote(parts.fragment)
            # Los fragmentos de PDF/SVG y las directivas de texto no son ids HTML.
            if target in pages and fragment and not fragment.startswith(":~:text="):
                anchor = fragment.split(":~:text=", 1)[0]
                if anchor and anchor not in pages[target].ids:
                    issues.append(f"fragmento inexistente: {link}")
        errors.extend(f"{label}: {issue}" for issue in issues)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "site", nargs="?", type=Path,
        default=Path(__file__).resolve().parents[1] / "_book",
    )
    args = parser.parse_args()
    errors = check_site(args.site)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("HTML, recursos y enlaces internos: OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
