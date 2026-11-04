#!/usr/bin/env python3
"""Monta o site da nutricionista Suéllen Bezerra (landing de agendamento) e a ponte /obrigado para o WhatsApp.

    python3 build.py

Copy a partir da bio e do post fixado do Instagram (@suellenbezerranutricionista), sem inventar
serviço, preço, local ou resultado. Fotos do Instagram dela (tools/fotos.py gera os WebP).
O CSS vai minificado para dentro do <head>; o site.js leva o hash do conteúdo no nome.
"""
import hashlib, json, re
from datetime import date
from html import escape as e
from pathlib import Path

RAIZ = Path(__file__).parent
DOMINIO = "https://suellenbezerra.vercel.app"
INDEXAR = False                  # True depois da aprovação e do domínio
WHATSAPP = "5551992858882"       # o link da bio dela
TEL_VER = "+55 51 99285-8882"
INSTAGRAM = "https://www.instagram.com/suellenbezerranutricionista/"
CRN = "CRN 11028"
CSS, JS = RAIZ / "assets/css/site.css", RAIZ / "assets/js/site.js"

SETA = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5"/></svg>'
ZAP = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.6-.3z"/></svg>')
IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>'
I = {  # ícones de traço fino, 24x24 (os 5 pilares do post fixado)
    "pessoa": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4.5-6 8-6s7 2 8 6"/>',
    "coracao": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "talheres": '<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 3c-2 2-2 6 0 8v10"/>',
    "moeda": '<circle cx="12" cy="12" r="9"/><path d="M14.5 9.2c-.5-.8-1.4-1.2-2.5-1.2-1.4 0-2.5.8-2.5 2s1.1 1.7 2.5 2 2.5.8 2.5 2-1.1 2-2.5 2c-1.1 0-2-.4-2.5-1.2M12 6.5v11"/>',
    "grafico": '<path d="M4 20h16M7 16v-4M12 16V8M17 16v-7"/><path d="M5 10l5-4 4 3 5-5"/>',
}


def ic(nome):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[nome]}</svg>'


# ------------------------------------------------------------------ copy (bio + post fixado de 29/10)
HERO_H1 = "Emagreça sem dieta restritiva."
HERO_P = ("Eu direciono mulheres a emagrecer entendendo o seu comportamento alimentar, com um plano que respeita "
          "seus gostos, a sua rotina e a sua realidade financeira.")
FAIXA = ["Sem dieta restritiva", "Sem culpa ao comer", "Comida de verdade", "Do jeito da sua rotina",
         "Cabe no seu orçamento", "Resultados que duram"]
CUIDADO = [
    "Acredito que a nutrição vai muito além de entregar um plano alimentar. Para mim, cada paciente é única e merece um "
    "atendimento pensado de acordo com seus objetivos, sua rotina, seus gostos, suas preferências e, principalmente, sua realidade financeira.",
    "Meu objetivo é encontrar estratégias que unam qualidade nutricional, praticidade e acessibilidade, sem deixar de lado o prazer de comer.",
]
PILARES = [
    ("pessoa", "Atendimento individualizado", "Cada paciente é única. Seu plano é feito com base na sua rotina, no seu perfil e nos seus objetivos."),
    ("coracao", "Emagrecimento sem radicalismos", "Estratégias que respeitam seus gostos, sua rotina e o que faz sentido para você."),
    ("talheres", "Qualidade e preferência alimentar", "Valorizo alimentos reais, práticos e que você gosta. Porque alimentação saudável também precisa ser prazerosa."),
    ("moeda", "Considero sua realidade financeira", "Busco sempre as melhores opções, com equilíbrio entre qualidade, custo e praticidade."),
    ("grafico", "Acompanhamento e evolução", "Juntas, vamos construindo hábitos sustentáveis, com mais saúde, autoestima e bem-estar."),
]
FRASE_DIETA = ("Você não precisa viver em função de uma dieta.", "Precisa aprender a cuidar de si de uma forma que faça sentido para a sua vida.")
PARA_QUEM = [
    "Já começou várias dietas e não conseguiu manter nenhuma.",
    "Vive no efeito sanfona: emagrece, desanima e volta tudo.",
    "Pensa \"já que eu saí da dieta, vou chutar o balde\".",
    "Quer emagrecer sem cortar tudo o que gosta de comer.",
    "Tem a rotina corrida e precisa de um plano que caiba nela.",
    "Quer um resultado que dure, e não só para o próximo verão.",
]
SOBRE = [
    "Sou formada em Nutrição pela UniRitter, Ritter dos Reis, em Porto Alegre (RS), e atuo na área clínica desde 2024.",
    "Minha formação me trouxe o conhecimento técnico, mas é na prática, ao lado de cada paciente, que eu construo o meu maior "
    "aprendizado: entender as individualidades e transformar hábitos em resultados reais e duradouros.",
    "Trabalho especialmente com o emagrecimento feminino, ajudando mulheres a conquistarem seus resultados sem dietas impossíveis, "
    "restrições desnecessárias ou culpa ao comer. E, nas horas vagas, sou corredora de rua: eu sei, na pele, o que é encaixar saúde numa rotina real.",
]
PASSOS = [
    ("Você me chama no WhatsApp", "Conte rapidinho o que você busca e combinamos o melhor horário para a sua consulta."),
    ("Na consulta, eu te escuto", "Falamos da sua rotina, dos seus gostos, do seu histórico, dos seus objetivos e da sua realidade financeira."),
    ("Seu plano, do seu jeito", "Você recebe um plano individualizado, com comida de verdade, prático e possível de seguir."),
    ("A gente ajusta junto", "No acompanhamento, avaliamos a evolução e ajustamos o que for preciso para o resultado durar."),
]
FAQ = [
    ("Preciso cortar tudo o que eu gosto para emagrecer?",
     "Não. O plano é montado com os alimentos que você gosta e que fazem parte da sua vida. A ideia é emagrecer sem radicalismos e sem culpa ao comer."),
    ("Vou passar fome?",
     "O objetivo é o contrário: comer bem, com volume e qualidade, fazendo escolhas mais inteligentes. Dieta que dá fome não se sustenta."),
    ("E se a minha rotina for corrida?",
     "O plano é feito em cima da sua rotina real, com opções práticas para os dias mais apertados."),
    ("O plano cabe no meu orçamento?",
     "Sim, esse é um dos pilares do meu trabalho. Busco sempre o equilíbrio entre qualidade, custo e praticidade."),
    ("Como faço para agendar a minha consulta?",
     "É só tocar em qualquer botão de agendamento: a conversa abre no meu WhatsApp e eu te passo horários, formato do atendimento e valores."),
]


# ------------------------------------------------------------------ utilidades
def minificar(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "\n", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return re.sub(r"\n+", "", css).replace("../fonts/", "/assets/fonts/").strip()


def hash_de(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:10] if p.exists() else "0"


def foto(nome, alt, sizes, lazy=True, larguras=(800, 1200), classe=""):
    """<img> a partir de assets/img/fotos/<nome>-<largura>.webp, com as dimensões reais."""
    w, h = larguras[-1], round(larguras[-1] * 1.25)
    try:
        from PIL import Image
        with Image.open(RAIZ / f"assets/img/fotos/{nome}-{larguras[-1]}.webp") as im:
            w, h = im.size
    except Exception:
        print(f"  ! foto faltando: {nome}-{larguras[-1]}.webp")
    srcset = ", ".join(f"/assets/img/fotos/{nome}-{x}.webp {x}w" for x in larguras)
    lz = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    cl = f' class="{classe}"' if classe else ""
    return (f'<img{cl} src="/assets/img/fotos/{nome}-{larguras[-1]}.webp" srcset="{srcset}" sizes="{sizes}" alt="{e(alt)}" '
            f'width="{w}" height="{h}"{lz} decoding="async">')


def cta(rotulo="Agendar minha consulta", c="cta", tipo="pri"):
    return f'<a class="btn btn--{tipo}" href="/obrigado?c={c}">{ZAP if tipo != "linha" else ""}<span>{e(rotulo)}</span></a>'


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'


def schema():
    return ld({"@context": "https://schema.org", "@graph": [
        {"@type": ["Person"], "@id": f"{DOMINIO}/#suellen", "name": "Suéllen Bezerra", "jobTitle": "Nutricionista",
         "description": "Nutricionista clínica com foco em emagrecimento feminino sem dieta restritiva.",
         "alumniOf": {"@type": "CollegeOrUniversity", "name": "UniRitter, Centro Universitário Ritter dos Reis"},
         "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "Registro profissional", "name": CRN},
         "image": f"{DOMINIO}/assets/img/og-image.jpg", "sameAs": [INSTAGRAM], "url": f"{DOMINIO}/"},
        {"@type": "MedicalBusiness", "@id": f"{DOMINIO}/#consultorio", "name": "Nutricionista Suéllen Bezerra",
         "medicalSpecialty": "Nutrition", "founder": {"@id": f"{DOMINIO}/#suellen"}, "telephone": TEL_VER,
         "url": f"{DOMINIO}/", "image": f"{DOMINIO}/assets/img/og-image.jpg", "sameAs": [INSTAGRAM], "areaServed": "BR",
         "description": "Atendimento nutricional individualizado para mulheres que querem emagrecer sem dieta restritiva."},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in FAQ]},
    ]})


def pagina(titulo, desc, corpo, rota="/", preload="", robots=None, casca=True, extra=""):
    robots = robots or ("index,follow,max-image-preview:large" if INDEXAR else "noindex,nofollow")
    topo = f'''<header class="top"><div class="wrap top__in">
  <a class="marca" href="/" aria-label="Suéllen Bezerra, nutricionista, início"><img class="marca__sb" src="/assets/img/sb-monograma.svg" alt="" width="40" height="46"><span class="marca__txt"><b>Suéllen Bezerra</b><span>Nutricionista</span></span></a>
  <nav class="nav" aria-label="Principal"><a href="/#como">Como eu trabalho</a><a href="/#sobre">Quem sou</a><a href="/#passos">Como funciona</a><a href="/#duvidas">Dúvidas</a></nav>
  {cta("Agendar consulta", "topo")}
</div></header>''' if casca else ""
    rodape = f'''<footer class="rod"><div class="wrap rod__in">
  <div class="rod__marca"><img class="rod__sb" src="/assets/img/sb-monograma-claro.svg" alt="" width="48" height="56" loading="lazy"><b>Suéllen Bezerra</b><span>Nutricionista · {CRN}</span><p>Emagrecimento feminino sem dieta restritiva.</p></div>
  <div class="rod__col"><a href="/obrigado?c=rodape">{ZAP} {TEL_VER}</a><a href="{INSTAGRAM}" target="_blank" rel="noopener">{IG} @suellenbezerranutricionista</a><a href="/privacidade">Política de privacidade</a></div>
</div><p class="rod__fim wrap">© {date.today().year} Suéllen Bezerra, nutricionista. {CRN}.</p></footer>
<a class="zap" href="/obrigado?c=flutuante" aria-label="Agendar consulta pelo WhatsApp">{ZAP}<span>Agendar consulta</span></a>''' if casca else ""
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{DOMINIO}{rota}">
<meta name="theme-color" content="#FBF6F1">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="Suéllen Bezerra, nutricionista">
<meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{DOMINIO}{rota}">
<meta property="og:image" content="{DOMINIO}/assets/img/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml"><link rel="icon" href="/assets/img/favicon.png" type="image/png" sizes="64x64"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/poppins-300.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/poppins-500.woff2" as="font" type="font/woff2" crossorigin>
{preload}
<script>document.documentElement.classList.add('js')</script>
<style>{minificar(CSS.read_text())}</style>
{extra}
</head>
<body>
{topo}
<main>
{corpo}
</main>
{rodape}
<script src="/assets/js/site.js?v={hash_de(JS)}" defer></script>
</body>
</html>'''


SLIDES = [  # a primeira abre o slideshow; as outras entram sozinhas, em ciclo
    ("sobre", "Suéllen Bezerra de jaleco branco", (800, 1200)),
    ("formatura", "Formatura de Suéllen Bezerra em Nutrição, com o nome dela no telão", (600, 900)),
    ("slide-jaleco", "Suéllen de jaleco, sorrindo", (600, 900)),
    ("slide-corrida", "Suéllen correndo numa estrada arborizada", (600, 900)),
    ("slide-perfil", "Suéllen de jaleco, com a mão no queixo", (600, 900)),
    ("slide-represa", "Suéllen num passeio ao ar livre", (600, 900)),
    ("slide-consultorio", "Suéllen sentada no consultório", (600, 900)),
    ("slide-jardim", "Suéllen num jardim", (600, 900)),
]


def slides():
    return "".join(f'<figure class="slide{" on" if i == 0 else ""}">{foto(n, a, "(max-width:760px) 88vw, 40vw", lazy=True, larguras=l)}</figure>'
                   for i, (n, a, l) in enumerate(SLIDES))


# ------------------------------------------------------------------ páginas
def home():
    faixa = "".join(f"<span>{e(t)}</span><i></i>" for t in FAIXA)
    pilares = "".join(f'''<article class="pilar" style="--i:{i}">
      <span class="pilar__n">{i + 1:02d}</span><div class="pilar__ic">{ic(ico)}</div>
      <h3>{e(t)}</h3><p>{e(d)}</p></article>''' for i, (ico, t, d) in enumerate(PILARES))
    para_quem = "".join(f'<li class="rv" data-d="{i % 3}"><span>{i + 1:02d}</span>{e(t)}</li>' for i, t in enumerate(PARA_QUEM))
    passos = "".join(f'<li class="passo rv"><b>{i + 1:02d}</b><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(PASSOS))
    faq = "".join(f'<details class="faq__item"><summary>{e(p)}<i aria-hidden="true"></i></summary><p>{e(r)}</p></details>' for p, r in FAQ)
    corpo = f'''
<section class="capa" id="inicio">
  <div class="capa__fundo" aria-hidden="true"><i></i><i></i></div>
  <div class="capa__foto" data-paralaxe>{foto("hero", "Suéllen Bezerra, nutricionista, de jaleco branco e óculos, sorrindo", "(max-width:760px) 100vw, 46vw", lazy=False, larguras=(700, 1100))}</div>
  <div class="wrap capa__in">
    <div class="capa__txt">
      <h1>{e(HERO_H1)}</h1>
      <p>{e(HERO_P)}</p>
      <div class="ctas">{cta("Agendar minha consulta", "hero")}<a class="btn btn--linha" href="#como"><span>Como eu trabalho</span>{SETA}</a></div>
      <p class="capa__crn">Nutricionista · {CRN}</p>
    </div>
  </div>
</section>
<div class="faixa" aria-hidden="true"><div class="faixa__t">{faixa * 3}</div></div>

<section class="cuidado">
  <div class="cuidado__bg"><picture><source media="(max-width:760px)" srcset="/assets/img/fotos/cuidado-800.webp 800w, /assets/img/fotos/cuidado-1200.webp 1200w" sizes="100vw">{foto("cuidado-larga", "Suéllen Bezerra no consultório, de jaleco, com a mão no queixo", "100vw", larguras=(1200, 1800, 2400))}</picture></div>
  <div class="wrap cuidado__in">
  <div class="cuidado__txt rv">
    <h2>Mais do que uma dieta, é um cuidado individualizado.</h2>
    {"".join(f"<p>{e(p)}</p>" for p in CUIDADO)}
    <div class="ctas">{cta("Quero um plano do meu jeito", "cuidado")}</div>
  </div>
</div></section>

<section class="pilares-sec" id="como"><div class="wrap">
  <div class="cab rv"><h2>Como eu trabalho</h2></div>
  <div class="pilares">{pilares}</div>
  <div class="fim rv">{cta("Agendar minha consulta", "pilares")}</div>
</div></section>

<section class="frase" data-fundo><div class="frase__bg">{foto("frase", "", "100vw", larguras=(800, 1200))}</div><div class="wrap"><div class="frase__txt rv">
  <p class="frase__grande">{e(FRASE_DIETA[0])}<br>{e(FRASE_DIETA[1])}</p>
  <div class="ctas">{cta("Começar agora", "frase", "claro")}</div>
</div></div></section>

<section class="sec quem"><div class="wrap">
  <div class="cab rv"><h2>Esse acompanhamento é para você que</h2></div>
  <ul class="quem__lista">{para_quem}</ul>
  <div class="fim rv">{cta("Isso é pra mim", "para-quem")}</div>
</div></section>

<section class="sec sobre" id="sobre"><div class="wrap sobre__in">
  <div class="slides rv" data-slides aria-roledescription="carrossel" aria-label="Fotos da Suéllen">
    {slides()}
    <div class="slides__pontos" aria-hidden="true">{"".join("<i></i>" for _ in SLIDES)}</div>
  </div>
  <div class="sobre__txt rv" data-d="1">
    <h2>Prazer, sou a Suéllen.</h2>
    {"".join(f"<p>{e(p)}</p>" for p in SOBRE)}
    <dl class="sobre__dados"><div><dt>Formação</dt><dd>Nutrição, UniRitter (RS)</dd></div><div><dt>Registro</dt><dd>{CRN}</dd></div><div><dt>Na clínica</dt><dd>desde 2024</dd></div></dl>
    <div class="ctas">{cta("Falar com a Suéllen", "sobre")}<a class="btn btn--linha" href="{INSTAGRAM}" target="_blank" rel="noopener">{IG}<span>Instagram</span></a></div>
  </div>
</div></section>

<section class="sec passos-sec" id="passos"><div class="wrap passos-in">
  <div class="passos-cab rv"><h2>Como funciona</h2>{cta("Agendar minha consulta", "passos")}</div>
  <ol class="passos">{passos}</ol>
</div></section>

<section class="final" data-fundo><div class="final__bg">{foto("final", "", "100vw", larguras=(800, 1200))}</div><div class="wrap"><div class="final__txt rv">
  <h2>Seu objetivo é o meu propósito.</h2>
  <p>Mais do que prescrever dietas, quero ajudar você a construir resultados que durem.</p>
  <div class="ctas">{cta("Agendar minha consulta", "final", "claro")}</div>
</div></div></section>

<section class="sec faq-sec" id="duvidas"><div class="wrap faq">
  <div class="faq__cab rv"><h2>Dúvidas frequentes</h2>{cta("Tirar minha dúvida", "faq")}</div>
  <div class="faq__lista rv" data-d="1">{faq}</div>
</div></section>'''
    preload = ('<link rel="preload" as="image" imagesrcset="/assets/img/fotos/hero-700.webp 700w, /assets/img/fotos/hero-1100.webp 1100w" '
               'imagesizes="(max-width:760px) 100vw, 46vw" fetchpriority="high">')
    return pagina("Suéllen Bezerra | Nutricionista: emagrecimento feminino sem dieta restritiva",
                  "Nutricionista Suéllen Bezerra (CRN 11028): emagrecimento feminino sem dieta restritiva, com plano individualizado que respeita seus gostos, sua rotina e seu orçamento. Agende pelo WhatsApp.",
                  corpo, "/", preload, extra=schema())


def privacidade():
    corpo = f'''<section class="sec texto-pag"><div class="wrap texto">
<h1>Política de Privacidade</h1>
<p>Como os seus dados são tratados neste site, conforme a LGPD (Lei 13.709/2018).</p>
<h2>Quem cuida dos seus dados</h2><p>Este site é da nutricionista Suéllen Bezerra ({CRN}), responsável pelo tratamento dos dados enviados por meio dele.</p>
<h2>Que dados recebemos</h2><p>Este site não tem formulário. Ao tocar em um botão de agendamento, você é levada ao WhatsApp e só envia o que escrever lá.</p>
<h2>Sigilo</h2><p>As informações de saúde compartilhadas no atendimento são sigilosas, conforme o Código de Ética do Nutricionista.</p>
<h2>Cookies</h2><p>Este site não usa cookies de publicidade nem de rastreamento. Se ferramentas de medição forem adicionadas, você será avisada.</p>
<h2>Seus direitos</h2><p>Você pode pedir acesso, correção ou exclusão dos seus dados a qualquer momento pelo WhatsApp {TEL_VER}.</p>
</div></section>'''
    return pagina("Política de Privacidade | Suéllen Bezerra", "Política de privacidade (LGPD) do site da nutricionista Suéllen Bezerra.", corpo, "/privacidade")


def obrigado():
    corpo = f'''<section class="obrigado"><div>
  <img class="obrigado__sb" src="/assets/img/sb-monograma.svg" alt="" width="62" height="72">
  <p class="obrigado__nome">Suéllen Bezerra</p>
  <h1>Abrindo o WhatsApp.</h1>
  <p>Em instantes você fala comigo para agendar a sua consulta.</p>
  <div class="gira" aria-hidden="true"></div>
  <div class="ctas"><a class="btn btn--pri" id="vai" href="https://wa.me/{WHATSAPP}">{ZAP}<span>Abrir o WhatsApp</span></a><a class="btn btn--linha" href="/"><span>Voltar</span></a></div>
</div></section>
<script>
(function(){{
  var W='{WHATSAPP}', msg='Olá, Suéllen! Vim pelo seu site e quero agendar uma consulta.';
  var dest='https://wa.me/'+W+'?text='+encodeURIComponent(msg); document.getElementById('vai').href=dest;
  var c=(new URLSearchParams(location.search).get('c')||'site').replace(/[^a-z0-9_-]/gi,'');
  var t0=Date.now(), partiu=false;
  function vai(){{ if(partiu) return; partiu=true; location.replace(dest); }}
  function talvez(){{ var f=900-(Date.now()-t0); setTimeout(vai, f>0?f:0); }}
  window.dataLayer=window.dataLayer||[]; window.dataLayer.push({{event:'conversao_whatsapp',contexto:c,eventCallback:talvez,eventTimeout:2000}});
  if(!window.google_tag_manager) talvez();
  setTimeout(vai,2600);
}})();
</script>'''
    return pagina("Abrindo o WhatsApp | Suéllen Bezerra", "Abrindo o WhatsApp da nutricionista Suéllen Bezerra.", corpo, "/obrigado", robots="noindex,nofollow", casca=False)


def main():
    paginas = {"index.html": home(), "privacidade.html": privacidade(), "obrigado.html": obrigado()}
    for arq, html in paginas.items():
        (RAIZ / arq).write_text(html)
    hoje = date.today().isoformat()
    (RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      + "".join(f"<url><loc>{DOMINIO}{r}</loc><lastmod>{hoje}</lastmod></url>" for r in ("/", "/privacidade")) + "</urlset>\n")
    (RAIZ / "robots.txt").write_text("User-agent: *\n" + ("Allow: /\n" if INDEXAR else "Disallow:\n") + f"\nSitemap: {DOMINIO}/sitemap.xml\n")
    (RAIZ / "llms.txt").write_text(
        f"# Suéllen Bezerra, nutricionista\n\n> {HERO_H1} {HERO_P}\n\n{CRN}. Formada em Nutrição pela UniRitter (Porto Alegre, RS), na área clínica desde 2024.\n\n## Como trabalha\n"
        + "\n".join(f"- {t}: {d}" for _, t, d in PILARES)
        + "\n\n## Perguntas frequentes\n" + "\n".join(f"- {p} {r}" for p, r in FAQ)
        + f"\n\n## Contato\nWhatsApp: {TEL_VER}\nInstagram: {INSTAGRAM}\nSite: {DOMINIO}/\n")
    print(f"  {len(paginas)} páginas  site.js v={hash_de(JS)}  indexar={INDEXAR}")


if __name__ == "__main__":
    main()
