(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const cards = [...document.querySelectorAll('.project-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const count = document.querySelector('#project-count');
  const more = document.querySelector('.more-projects');
  let category = 'all';
  let expanded = false;
  const renderProjects = () => {
    const matches = cards.filter(card => category === 'all' || card.dataset.category === category);
    cards.forEach(card => { card.hidden = true; });
    matches.forEach((card, index) => { card.hidden = !expanded && index >= 8; });
    const shown = expanded ? matches.length : Math.min(8, matches.length);
    if (count) count.textContent = shown < matches.length
      ? `Showing ${shown} of ${matches.length} projects`
      : `${matches.length} project${matches.length === 1 ? '' : 's'}`;
    if (more) {
      more.parentElement.hidden = expanded || matches.length <= 8;
      more.setAttribute('aria-expanded', String(expanded));
    }
    return matches;
  };
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    expanded = false;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    renderProjects();
  }));
  more?.addEventListener('click', () => {
    expanded = true;
    const matches = renderProjects();
    const firstNewLink = matches[8]?.querySelector('a');
    firstNewLink?.focus({ preventScroll: true });
    matches[8]?.scrollIntoView({ behavior: reduced.matches ? 'instant' : 'smooth', block: 'start' });
  });
  renderProjects();
  if ('IntersectionObserver' in window && !reduced.matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-entering');
        observer.unobserve(entry.target);
      }
    }), { threshold: .08 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  }
  let scheduled = false;
  const progress = document.querySelector('.reading-progress');
  const updateScroll = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.transform = `scaleX(${max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0})`;
    document.body.classList.toggle('has-scrolled', window.scrollY > 15);
    scheduled = false;
  };
  window.addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateScroll); } }, { passive: true });
  window.addEventListener('resize', updateScroll);
  updateScroll();
  document.querySelectorAll('.back-top').forEach(button => button.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: reduced.matches ? 'instant' : 'smooth' });
    document.querySelector('.wordmark')?.focus({ preventScroll: true });
  }));
  const dialog = document.querySelector('.lightbox');
  let imageTrigger = null;
  if (dialog && typeof dialog.showModal === 'function') {
    const image = dialog.querySelector('img');
    const caption = dialog.querySelector('p');
    document.querySelectorAll('.zoom-image').forEach(button => button.addEventListener('click', () => {
      imageTrigger = button;
      image.src = button.dataset.image;
      image.alt = button.dataset.caption || 'Project detail';
      caption.textContent = button.dataset.caption || '';
      dialog.showModal();
      document.body.classList.add('image-open');
    }));
    dialog.querySelector('.close-lightbox').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { if (event.target === dialog) { const box = dialog.getBoundingClientRect(); if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close(); } });
    dialog.addEventListener('close', () => { document.body.classList.remove('image-open'); imageTrigger?.focus({ preventScroll: true }); });
  } else {
    document.querySelectorAll('.zoom-image').forEach(button => button.addEventListener('click', () => { window.location.href = button.dataset.image; }));
  }
  const copy = document.querySelector('.copy-email');
  const status = document.querySelector('.copy-status');
  copy?.addEventListener('click', async () => {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(copy.dataset.email);
      status.textContent = 'Email copied. I look forward to hearing from you.';
    } catch {
      status.textContent = 'Select the email address to copy it, or click it to open your email app.';
    }
  });
})();

// A light pointer accent: native cursor retained, sparse 7px sparkles, mouse only.
(() => {
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const halo = document.createElement('span');
  halo.className = 'cursor-halo';
  halo.setAttribute('aria-hidden', 'true');
  document.body.appendChild(halo);
  const sparks = new Set();
  let lastTime = 0, lastX = -100, lastY = -100;
  const clear = () => { halo.classList.remove('is-visible'); sparks.forEach(s => s.remove()); sparks.clear(); };
  const allowed = () => fine.matches && !reduce.matches && !document.hidden;
  document.addEventListener('pointermove', event => {
    if (!allowed() || event.pointerType !== 'mouse') { clear(); return; }
    const x = event.clientX, y = event.clientY;
    halo.style.transform = `translate(${x}px,${y}px) translate(-50%,-50%)`;
    halo.classList.add('is-visible');
    const target = event.target instanceof Element ? event.target : null;
    halo.classList.toggle('is-interactive', !!target?.closest('a,button,summary'));
    if (target?.closest('input,textarea,select,[contenteditable=true]')) return;
    const now = performance.now();
    if (now - lastTime < 150 || Math.hypot(x-lastX,y-lastY) < 24 || sparks.size >= 4) return;
    lastTime = now; lastX = x; lastY = y;
    const spark = document.createElement('span');
    spark.className = 'cursor-spark'; spark.textContent = '✦'; spark.setAttribute('aria-hidden','true');
    spark.style.setProperty('--spark-x', `${x + 8}px`);
    spark.style.setProperty('--spark-y', `${y + 8}px`);
    spark.style.setProperty('--drift-x', `${Math.random()*8-4}px`);
    document.body.appendChild(spark); sparks.add(spark);
    const remove = () => { spark.remove(); sparks.delete(spark); };
    spark.addEventListener('animationend', remove, { once: true });
    setTimeout(remove, 650);
  }, { passive: true });
  document.documentElement.addEventListener('pointerleave', clear);
  window.addEventListener('blur', clear);
  document.addEventListener('visibilitychange', clear);
  fine.addEventListener('change', clear); reduce.addEventListener('change', clear);
})();

// Photo cards support mouse, touch, and keyboard interaction.
(() => {
  const stack = document.querySelector('.about-photo-stack');
  if (!stack) return;
  const cards = [...stack.querySelectorAll('.about-photo')];
  const reset = () => cards.forEach(card => {
    card.classList.remove('is-active');
    card.setAttribute('aria-pressed', 'false');
  });
  cards.forEach(card => card.addEventListener('click', () => {
    const activate = !card.classList.contains('is-active');
    reset();
    if (activate) {
      card.classList.add('is-active');
      card.setAttribute('aria-pressed', 'true');
    }
  }));
  stack.addEventListener('keydown', event => {
    if (event.key === 'Escape') reset();
  });
  document.addEventListener('click', event => {
    if (!stack.contains(event.target)) reset();
  });
})();

// Accessible publication reader; all spreads remain available without JavaScript.
(() => {
  const reader = document.querySelector('.editorial-reader');
  if (!reader) return;
  const slides = [...reader.querySelectorAll('.editorial-slide')];
  const thumbs = [...reader.querySelectorAll('[data-spread]')];
  const prev = reader.querySelector('[data-reader-prev]');
  const next = reader.querySelector('[data-reader-next]');
  const status = reader.querySelector('.editorial-reader-status');
  let current = 0;
  function show(index) {
    current = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((slide, i) => { slide.hidden = i !== current; });
    thumbs.forEach((thumb, i) => thumb.setAttribute('aria-pressed', String(i === current)));
    prev.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    status.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')} · ${slides[current].querySelector('figcaption').textContent}`;
  }
  prev.addEventListener('click', () => show(current - 1));
  next.addEventListener('click', () => show(current + 1));
  thumbs.forEach((thumb, i) => thumb.addEventListener('click', () => show(i)));
  reader.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); show(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
})();

// A single, gentle letter wave on heading hover; retain the full accessible name.
(() => {
  const heading = document.querySelector('.hero h1');
  if (!heading) return;
  heading.setAttribute('aria-label', 'Thoughtful design. Human connections.');
  const walker = document.createTreeWalker(heading, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  let index = 0;
  nodes.forEach(node => {
    const fragment = document.createDocumentFragment();
    node.textContent.split(/(\s+)/).forEach(word => {
      if (!word.trim()) { fragment.appendChild(document.createTextNode(word)); return; }
      const wrapper = document.createElement('span');
      wrapper.className = 'hero-word'; wrapper.setAttribute('aria-hidden', 'true');
      [...word].forEach(letter => {
        const span = document.createElement('span');
        span.className = 'hero-letter'; span.textContent = letter;
        span.style.setProperty('--letter-index', index++);
        wrapper.appendChild(span);
      });
      fragment.appendChild(wrapper);
    });
    node.replaceWith(fragment);
  });
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let waveTimer;
  const playWave = () => {
    if (reducedMotion.matches) return;
    clearTimeout(waveTimer);
    heading.classList.remove('is-waving');
    void heading.offsetWidth;
    heading.classList.add('is-waving');
    waveTimer = setTimeout(() => heading.classList.remove('is-waving'), 550 + index * 16 + 50);
  };
  heading.addEventListener('pointerenter', event => {
    if (event.pointerType !== 'touch') playWave();
  });
  const start = () => requestAnimationFrame(() => requestAnimationFrame(playWave));
  if (document.fonts) document.fonts.ready.then(start); else start();
})();
