/* Suéllen Bezerra: comportamento do site. Sem dependências. */
(() => {
  const d = document, w = window;
  const rm = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const largo = w.matchMedia('(min-width:761px)');

  /* revelações (com reserva: nada fica invisível) */
  const alvos = [...d.querySelectorAll('.rv')];
  if ('IntersectionObserver' in w) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -6% 0px' });
    alvos.forEach(el => io.observe(el));
  } else alvos.forEach(el => el.classList.add('in'));
  setTimeout(() => alvos.forEach(el => { if (el.getBoundingClientRect().top < innerHeight) el.classList.add('in'); }), 2500);

  /* topo sólido e foto da capa subindo devagar */
  const topo = d.querySelector('.top');
  const foto = d.querySelector('[data-paralaxe]');
  const zap = d.querySelector('.zap');
  let pendente = false;
  const quadro = () => {
    pendente = false;
    const y = w.scrollY;
    topo && topo.classList.toggle('solid', y > 30);
    zap && zap.classList.toggle('ver', y > innerHeight * 0.55);
    if (foto && !rm && largo.matches && y < innerHeight * 1.2) foto.style.transform = `translate3d(0,${(y * 0.12).toFixed(1)}px,0)`;
  };
  const pedir = () => { if (!pendente) { pendente = true; requestAnimationFrame(quadro); } };
  w.addEventListener('scroll', pedir, { passive: true });
  quadro();

  /* dúvidas: uma aberta por vez */
  const itens = [...d.querySelectorAll('.faq__item')];
  itens.forEach(it => it.addEventListener('toggle', () => { if (it.open) itens.forEach(o => { if (o !== it) o.open = false; }); }));
})();
