#!/usr/bin/env python3
"""Ícones a partir do monograma SB vetorizado (assets/img/sb-monograma.svg).

    python3 tools/marca.py

O monograma veio do ChatGPT (opção 1 de 4, em assets/src/marca/) e foi vetorizado com potrace.
Gera favicon.svg, favicon.png (64), apple-touch-icon.png (180) e assets/src/marca/sb-og.png
(monograma transparente, usado pela og-image do tools/fotos.py).
"""
import asyncio, os, re
from pathlib import Path
from playwright.async_api import async_playwright

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "assets/img"
CH = os.path.expanduser("~/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell")
CREME, TERRA = "#FBF6F1", "#A35A47"


def icone_svg():
    """Monograma terracota centralizado num quadrado creme arredondado (lê bem na aba clara e na escura)."""
    s = (IMG / "sb-monograma.svg").read_text()
    W, H = [float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups()]
    miolo = re.search(r"<g .*</g>", s).group(0)
    lado = max(W, H) * 1.36
    tx, ty = (lado - W) / 2, (lado - H) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lado:.0f} {lado:.0f}">'
            f'<rect width="{lado:.0f}" height="{lado:.0f}" rx="{lado * .22:.0f}" fill="{CREME}"/>'
            f'<g transform="translate({tx:.0f} {ty:.0f})">{miolo}</g></svg>')


async def main():
    ic = icone_svg()
    (IMG / "favicon.svg").write_text(ic)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CH)
        pg = await b.new_page()
        for lado, nome in ((64, "favicon.png"), (180, "apple-touch-icon.png")):
            await pg.set_viewport_size({"width": lado, "height": lado})
            await pg.set_content(f'<html><body style="margin:0;background:transparent">{ic.replace("<svg ", f"<svg width={lado} height={lado} ", 1)}</body></html>')
            await pg.screenshot(path=str(IMG / nome), omit_background=True)
        mono = (IMG / "sb-monograma.svg").read_text().replace("<svg ", '<svg height="360" ', 1)
        await pg.set_viewport_size({"width": 400, "height": 360})
        await pg.set_content(f'<html><body style="margin:0;background:transparent">{mono}</body></html>')
        await pg.screenshot(path=str(RAIZ / "assets/src/marca/sb-og.png"), omit_background=True,
                            clip={"x": 0, "y": 0, "width": 312, "height": 360})
        await b.close()
    print("ok: favicon.svg, favicon.png, apple-touch-icon.png, sb-og.png")


if __name__ == "__main__":
    asyncio.run(main())
