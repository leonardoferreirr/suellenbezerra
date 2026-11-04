# Suéllen Bezerra, nutricionista

Landing de agendamento da nutricionista Suéllen Bezerra (CRN 11028), foco em emagrecimento feminino sem dieta restritiva.
Estático, sem dependências: `python3 build.py` gera `index.html`, `privacidade.html` e `obrigado.html` (ponte para o WhatsApp).

## De onde veio cada coisa
- **Copy:** bio e post fixado do Instagram (@suellenbezerranutricionista): os 5 pilares, as frases dela, formação, CRN e "desde 2024". O "para você que..." e o FAQ seguem o que ela publica.
- **Fotos:** do Instagram dela (originais em `assets/src/instagram/`, fora do git). `python3 tools/fotos.py` gera os WebP e a og-image. A capa usa o recorte sem fundo (`hero-recorte.png`, Vision da Apple).
  - Carrossel do "Prazer, sou a Suéllen": duas fotos de academia são frames dos reels de treino (recortados acima da legenda do vídeo) e a pós-corrida é a 2ª foto de um post dela.
  - Frase "Você não precisa viver em função de uma dieta": a foto foi cortada abaixo do texto do post e o topo (cabelo e fundo do café) foi refeito no Firefly, para a cabeça não cortar.
- **Ícones:** `python3 tools/marca.py`. A aba do navegador usa o monograma com fundo transparente; o ícone do iPhone fica num quadrado creme, porque o iOS pinta transparência de preto.
- **Referência:** a landing da Nutri Clau (`~/dev/nutriclau-landing`), com parallax, CTA em todas as seções e o botão fixo de agendar.

## Confirmar com ela
- A corrida de rua no texto "Prazer, sou a Suéllen" saiu dos vídeos dela.
- Atendimento online ou presencial, endereço e valores. O site manda perguntar no WhatsApp e não inventa.
- Fotos: se ela não gostar de alguma, as reservas estão em `assets/src/instagram/`.
- Ficaram de fora os desafios com meta de quilos e qualquer antes e depois (promessa de resultado, restrita pelo código de ética do nutricionista).
- Domínio: depois de ligar, trocar `DOMINIO` e virar `INDEXAR = True`.

## Prévia local
`python3 tools/serve.py 4225`
