#!/usr/bin/env python3
"""Fotos do site a partir do Instagram dela (assets/src/instagram/, fora do git).

    python3 tools/fotos.py

Cada foto: (arquivo, nome no site, recorte (x0, y0, x1, y1) em fração ou None, larguras).
A capa usa o recorte sem fundo (hero-recorte.png, Vision da Apple via lift.swift).
Gera também favicon, apple-touch-icon e og-image.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
SRC = RAIZ / "assets/src/instagram"
OUT = RAIZ / "assets/img/fotos"
FONTE = Path.home() / "Library/Fonts/Poppins-Light.ttf"
FONTE_M = Path.home() / "Library/Fonts/Poppins-Medium.ttf"

FOTOS = [
    ("sb-114.jpg", "cuidado", (0, .02, 1, .77), (800, 1200)),       # mão no queixo (a pose do post dela)
    ("sb-120.jpg", "sobre", (0, 0, 1, .75), (800, 1200)),           # jaleco, olhar direto
    ("sb-122.jpg", "formatura", (.03, 0, .97, 1), (600, 900)),      # formatura, nome no telão
    ("sb-047.jpg", "frase", (0, .24, 1, 1), (800, 1200, 1600)),     # de branco com café, sem o texto do post
    ("sb-125.jpg", "final", (0, 0, 1, .82), (800, 1200, 1600)),     # jaleco e planta
    # seção 2 no celular continua com o retrato; no computador, a versão com o fundo estendido (Firefly)
    ("cuidado-expandida.png", "cuidado-larga", (0, .014, 1, 1), (1200, 1800, 2400)),
    # slideshow do "Prazer, sou a Suéllen" (4:5)
    ("sb-118.jpg", "slide-jaleco", ("45", .05), (600, 900)),
    ("sb-060.jpg", "slide-corrida", ("45", .5), (600, 900)),
    ("sb-perfil.jpg", "slide-perfil", ("45", .3), (600, 900)),
    ("sb-113.jpg", "slide-represa", ("45", .5), (600, 900)),
    ("sb-079.jpg", "slide-consultorio", ("45", .3), (600, 900)),
    ("sb-119.jpg", "slide-jardim", ("45", .5), (600, 900)),
]


def salvar(im, nome, larguras, q=78):
    for w in larguras:
        alvo = w                              # o nome segue a largura pedida (o img lê o tamanho real)
        w = min(w, im.width)
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(OUT / f"{nome}-{alvo}.webp", "WEBP", quality=q, method=6)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # capa: recorte sem fundo, aparado ao contorno
    rec = Image.open(SRC / "hero-recorte.png").convert("RGBA")
    rec = rec.crop(rec.getbbox())
    salvar(rec, "hero", (700, 1100), q=82)
    for arq, nome, caixa, larguras in FOTOS:
        im = Image.open(SRC / arq).convert("RGB")
        if caixa and caixa[0] == "45":           # 4:5 exato, âncora vertical caixa[1] (0 = topo)
            W, H = im.size
            w, h = (W, round(W * 1.25)) if W * 1.25 <= H else (round(H * .8), H)
            x0, y0 = (W - w) // 2, round((H - h) * caixa[1])
            im = im.crop((x0, y0, x0 + w, y0 + h))
        elif caixa:
            W, H = im.size
            im = im.crop((round(caixa[0] * W), round(caixa[1] * H), round(caixa[2] * W), round(caixa[3] * H)))
        salvar(im, nome, larguras)
    # os ícones da aba saem do monograma SB: tools/marca.py
    # compartilhamento: foto à direita, nome e promessa à esquerda
    og = Image.new("RGB", (1200, 630), (251, 246, 241)); d = ImageDraw.Draw(og)
    d.ellipse((640, 60, 1240, 660), fill=(237, 213, 203))
    r = rec.copy(); r.thumbnail((560, 620), Image.LANCZOS)
    og.paste(r, (1200 - r.width - 20, 630 - r.height), r)
    mono = RAIZ / "assets/src/marca/sb-og.png"           # gerado pelo tools/marca.py
    if mono.exists():
        m = Image.open(mono).convert("RGBA"); m = m.crop(m.getbbox()); m.thumbnail((110, 120), Image.LANCZOS)
        og.paste(m, (72, 60), m)
    d.text((70, 196), "Suéllen Bezerra", font=ImageFont.truetype(str(FONTE_M), 58), fill=(59, 38, 34))
    d.text((72, 274), "Nutricionista · CRN 11028", font=ImageFont.truetype(str(FONTE), 28), fill=(125, 103, 98))
    d.text((70, 350), "Emagreça sem\ndieta restritiva.", font=ImageFont.truetype(str(FONTE), 52), fill=(163, 90, 71), spacing=10)
    og.save(RAIZ / "assets/img/og-image.jpg", quality=86)
    print("ok:", sorted(p.name for p in OUT.glob("*.webp")))


if __name__ == "__main__":
    main()
