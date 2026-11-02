/* Willowhush — interactive practices (vanilla JS, no dependencies)
   Tools: meditation timer, body scan, 5-4-3-2-1 grounding, loving-kindness flow,
   guided video sessions, and printable exercise checklists. */
(function(){
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, el=document) => el.querySelector(s);
  const $$ = (s, el=document) => Array.from(el.querySelectorAll(s));
  const store = {
    get(k, d){ try{ const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); }catch(e){ return d; } },
    set(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){} }
  };
  const fmt = s => { s = Math.max(0, Math.round(s)); return Math.floor(s/60) + ':' + String(s%60).padStart(2,'0'); };

  /* ---------- Bell: a soft singing-bowl tone made with Web Audio ---------- */
  const Bell = {
    ctx: null,
    init(){ if(!this.ctx){ const AC = window.AudioContext || window.webkitAudioContext; if(!AC) return null; this.ctx = new AC(); }
            if(this.ctx.state === 'suspended') this.ctx.resume(); return this.ctx; },
    ring(vol=0.35, base=196){
      const ctx = this.init(); if(!ctx) return;
      const t = ctx.currentTime + 0.02;
      const master = ctx.createGain(); master.gain.value = vol;
      const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 3200;
      master.connect(lp); lp.connect(ctx.destination);
      [[1,1,7],[1.003,0.5,6.5],[2.76,0.38,4.5],[5.4,0.16,2.6],[8.93,0.07,1.6]].forEach(([r,g,d])=>{
        const o = ctx.createOscillator(), e = ctx.createGain();
        o.type = 'sine'; o.frequency.value = base*r;
        e.gain.setValueAtTime(0.0001, t);
        e.gain.exponentialRampToValueAtTime(g, t + 0.015);
        e.gain.exponentialRampToValueAtTime(0.0001, t + d);
        o.connect(e); e.connect(master); o.start(t); o.stop(t + d + 0.1);
      });
    },
    chime(){ this.ring(0.18, 392); }
  };
  window.WillowBell = Bell;

  /* ---------- Speech helper (browser speechSynthesis, calm & slow) ---------- */
  const Speech = {
    ok: 'speechSynthesis' in window,
    voice: null,
    pick(){ if(!this.ok) return; const vs = speechSynthesis.getVoices(); if(!vs.length) return;
      const pref = [/Google UK English Female/i,/Samantha/i,/Serena/i,/Karen/i,/Moira/i,/Female/i,/en-GB/i,/en/i];
      for(const p of pref){ const v = vs.find(v => p.test(v.name) || p.test(v.lang)); if(v){ this.voice = v; return; } } },
    say(text){ if(!this.ok) return; speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(text);
      if(!this.voice) this.pick(); if(this.voice) u.voice = this.voice; u.rate = 0.78; u.pitch = 0.95; u.volume = 0.9; speechSynthesis.speak(u); },
    stop(){ if(this.ok) speechSynthesis.cancel(); }
  };
  if(Speech.ok){ Speech.pick(); speechSynthesis.onvoiceschanged = () => Speech.pick(); }

  /* ---------- Exercise checklists (ticks remembered in localStorage) ---------- */
  $$('.exercise[data-exercise]').forEach(ex => {
    const key = 'wh-ex-' + ex.dataset.exercise;
    const list = $('.checklist', ex); if(!list) return;
    const saved = store.get(key, []);
    const items = $$(':scope > li', list);
    items.forEach((li, i) => {
      const id = key + '-' + i;
      const box = document.createElement('input'); box.type = 'checkbox'; box.id = id; box.checked = !!saved[i];
      const label = document.createElement('label'); label.htmlFor = id;
      label.innerHTML = '<span class="step-n">Step ' + (i+1) + '</span>' + li.innerHTML;
      li.innerHTML = ''; li.append(box, label); li.classList.toggle('done', box.checked);
      box.addEventListener('change', () => { li.classList.toggle('done', box.checked); save(); });
    });
    const bar = document.createElement('div'); bar.className = 'exercise-bar';
    bar.innerHTML = '<div class="ex-progress"><span class="ex-count" aria-live="polite"></span><span class="ex-track" aria-hidden="true"><span></span></span></div>' +
      '<div class="ex-actions"><button type="button" class="btn btn-outline btn-sm" data-print>Print this exercise</button><button type="button" class="btn-link" data-reset>Clear ticks</button></div>';
    list.after(bar);
    const count = $('.ex-count', bar), fill = $('.ex-track span', bar);
    function save(){ const st = items.map(li => $('input', li).checked); store.set(key, st); render(st); }
    function render(st){ const n = st.filter(Boolean).length; count.textContent = n === items.length ? 'All ' + n + ' steps complete. Well done.' : n + ' of ' + items.length + ' steps complete';
      fill.style.width = (n / items.length * 100) + '%'; ex.classList.toggle('complete', n === items.length); }
    render(items.map(li => $('input', li).checked));
    $('[data-reset]', bar).addEventListener('click', () => { items.forEach(li => { $('input', li).checked = false; li.classList.remove('done'); }); save(); });
    $('[data-print]', bar).addEventListener('click', () => {
      document.body.classList.add('print-exercise'); ex.classList.add('printing');
      const done = () => { document.body.classList.remove('print-exercise'); ex.classList.remove('printing'); window.removeEventListener('afterprint', done); };
      window.addEventListener('afterprint', done); window.print(); setTimeout(done, 1500);
    });
  });

  /* ---------- Meditation timer ---------- */
  $$('[data-tool="timer"]').forEach(root => {
    const prefs = store.get('wh-timer', {min: 5, interval: 0});
    const ring = $('.ring-fill', root), timeEl = $('.timer-time', root), stateEl = $('.timer-state', root);
    const startBtn = $('[data-start]', root), resetBtn = $('[data-reset]', root), announce = $('[data-announce]', root);
    const intervalSel = $('[data-interval]', root), custom = $('[data-custom]', root);
    const durBtns = $$('[data-min]', root);
    const C = 2 * Math.PI * 92; ring.style.strokeDasharray = C;
    let total = prefs.min * 60, left = total, running = false, endAt = 0, raf = null, lastInterval = 0;
    intervalSel.value = String(prefs.interval || 0);
    function setDur(min){ min = Math.min(120, Math.max(1, Math.round(min) || 5)); prefs.min = min; store.set('wh-timer', prefs);
      durBtns.forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.min === min)));
      if(custom) custom.value = durBtns.some(b => +b.dataset.min === min) ? '' : min;
      if(!running){ total = left = min * 60; draw(); stateEl.textContent = 'Ready'; } }
    function draw(){ timeEl.textContent = fmt(left).padStart(5,'0'); ring.style.strokeDashoffset = C * (1 - (total - left) / total);
      root.style.setProperty('--timer-p', (total - left) / total); }
    function loop(){ left = Math.max(0, (endAt - performance.now()) / 1000);
      const iv = +intervalSel.value * 60, elapsed = total - left;
      if(iv && left > 1 && Math.floor(elapsed / iv) > lastInterval){ lastInterval = Math.floor(elapsed / iv); Bell.chime(); announce.textContent = 'Interval bell. ' + fmt(left) + ' remaining.'; }
      draw();
      if(left <= 0){ finish(); return; } raf = requestAnimationFrame(loop); }
    function start(){ Bell.init(); if(left <= 0) left = total; running = true; root.classList.add('running');
      endAt = performance.now() + left * 1000; lastInterval = Math.floor((total - left) / ((+intervalSel.value * 60) || 1e9));
      if(left === total){ Bell.ring(); announce.textContent = 'Session started. ' + fmt(total) + ' minutes.'; }
      startBtn.textContent = 'Pause'; startBtn.setAttribute('aria-pressed','true'); stateEl.textContent = 'Sitting'; loop(); }
    function pause(){ running = false; cancelAnimationFrame(raf); root.classList.remove('running'); startBtn.textContent = 'Resume'; startBtn.setAttribute('aria-pressed','false'); stateEl.textContent = 'Paused'; announce.textContent = 'Paused.'; }
    function finish(){ running = false; cancelAnimationFrame(raf); root.classList.remove('running'); left = 0; draw();
      Bell.ring(); setTimeout(() => Bell.ring(0.28), 2200); setTimeout(() => Bell.ring(0.22), 4400);
      const log = store.get('wh-timer-log', 0) + Math.round(total / 60); store.set('wh-timer-log', log); showLog();
      stateEl.textContent = 'Complete'; startBtn.textContent = 'Begin again'; startBtn.setAttribute('aria-pressed','false'); announce.textContent = 'Session complete. Take your time returning.';
      left = total; setTimeout(() => { if(!running){ draw(); } }, 6000); }
    function reset(){ running = false; cancelAnimationFrame(raf); root.classList.remove('running'); left = total; draw(); startBtn.textContent = 'Begin'; startBtn.setAttribute('aria-pressed','false'); stateEl.textContent = 'Ready'; }
    function showLog(){ const el = $('[data-log]', root); if(el){ const m = store.get('wh-timer-log', 0); el.textContent = m ? m + ' quiet minute' + (m === 1 ? '' : 's') + ' completed on this device' : ''; } }
    startBtn.addEventListener('click', () => running ? pause() : start());
    resetBtn.addEventListener('click', reset);
    durBtns.forEach(b => b.addEventListener('click', () => { if(running) reset(); setDur(+b.dataset.min); }));
    if(custom) custom.addEventListener('change', () => { if(custom.value){ if(running) reset(); setDur(+custom.value); } });
    intervalSel.addEventListener('change', () => { prefs.interval = +intervalSel.value; store.set('wh-timer', prefs); });
    const test = $('[data-test-bell]', root); if(test) test.addEventListener('click', () => Bell.ring());
    setDur(prefs.min); showLog();
  });

  /* ---------- Guided body scan ---------- */
  $$('[data-tool="bodyscan"]').forEach(root => {
    const steps = $$('.scan-steps li', root).map(li => ({region: li.dataset.region.split(' '), title: $('strong', li).textContent, text: $('span', li).textContent, li}));
    const titleEl = $('.scan-title', root), textEl = $('.scan-text', root), numEl = $('.scan-num', root), panel = $('.scan-panel', root);
    const playBtn = $('[data-play]', root), prevBtn = $('[data-prev]', root), nextBtn = $('[data-next]', root), paceSel = $('[data-pace]', root), voiceBox = $('[data-voice]', root), bar = $('.scan-bar span', root);
    let i = 0, playing = false, timer = null, t0 = 0, raf = null;
    function show(n, sound){
      i = (n + steps.length) % steps.length; const s = steps[i];
      $$('[data-part]', root).forEach(p => p.classList.toggle('lit', s.region.includes('all') || s.region.includes(p.dataset.part)));
      steps.forEach((x, k) => { x.li.classList.toggle('current', k === i); const b = $('button', x.li); if(b) b.setAttribute('aria-current', k === i ? 'step' : 'false'); });
      panel.classList.remove('swap'); void panel.offsetWidth; panel.classList.add('swap');
      numEl.textContent = (i + 1) + ' / ' + steps.length; titleEl.textContent = s.title; textEl.textContent = s.text;
      if(sound) Bell.chime(); if(voiceBox && voiceBox.checked) Speech.say(s.title + '. ' + s.text);
      if(playing) schedule();
    }
    function schedule(){ clearTimeout(timer); cancelAnimationFrame(raf); const pace = +paceSel.value * 1000; t0 = performance.now();
      const tick = () => { bar.style.width = Math.min(100, (performance.now() - t0) / pace * 100) + '%'; if(playing) raf = requestAnimationFrame(tick); }; tick();
      timer = setTimeout(() => { if(i === steps.length - 1){ stop(true); Bell.ring(0.3); textEl.textContent = 'The scan is complete. Rest here as long as you like.'; return; } show(i + 1, true); }, pace); }
    function play(){ Bell.init(); playing = true; root.classList.add('playing'); playBtn.textContent = 'Pause'; playBtn.setAttribute('aria-pressed','true'); if(i === 0) Bell.ring(0.28); show(i, false); }
    function stop(){ playing = false; root.classList.remove('playing'); clearTimeout(timer); cancelAnimationFrame(raf); bar.style.width = '0'; playBtn.textContent = i ? 'Resume' : 'Begin'; playBtn.setAttribute('aria-pressed','false'); Speech.stop(); }
    playBtn.addEventListener('click', () => playing ? stop() : play());
    prevBtn.addEventListener('click', () => show(i - 1, false));
    nextBtn.addEventListener('click', () => show(i + 1, false));
    paceSel.addEventListener('change', () => { store.set('wh-scan-pace', paceSel.value); if(playing) schedule(); });
    paceSel.value = store.get('wh-scan-pace', paceSel.value);
    if(voiceBox){ if(!Speech.ok) voiceBox.closest('label').hidden = true; voiceBox.addEventListener('change', () => { if(!voiceBox.checked) Speech.stop(); }); }
    steps.forEach((s, k) => { const b = $('button', s.li); if(b) b.addEventListener('click', () => show(k, false)); });
    root.addEventListener('keydown', e => { if(e.target.matches('select,input')) return; if(e.key === 'ArrowRight'){ show(i + 1); e.preventDefault(); } if(e.key === 'ArrowLeft'){ show(i - 1); e.preventDefault(); } });
    show(0, false);
  });

  /* ---------- 5-4-3-2-1 grounding ---------- */
  $$('[data-tool="grounding"]').forEach(root => {
    const stages = [
      {n:5, sense:'see', title:'Five things you can see', hint:'Let your eyes wander slowly. A shadow, a colour, the edge of a cup. Name each one silently.'},
      {n:4, sense:'feel', title:'Four things you can feel', hint:'The weight of your body on the chair, fabric on your skin, air on your face, your feet on the floor.'},
      {n:3, sense:'hear', title:'Three things you can hear', hint:'Near sounds and far sounds. A fridge humming, a car outside, your own breath.'},
      {n:2, sense:'smell', title:'Two things you can smell', hint:'Lean in if you need to: a sleeve, a cup of tea, the air of the room. Or recall two scents you love.'},
      {n:1, sense:'taste', title:'One thing you can taste', hint:'Notice what is already in your mouth, take a sip of water, or simply notice the taste of your breath.'}];
    const stage = $('.ground-stage', root), dotsEl = $('.ground-dots', root), title = $('.ground-title', root), hint = $('.ground-hint', root), big = $('.ground-num', root);
    const noticeBtn = $('[data-notice]', root), nextBtn = $('[data-gnext]', root), restartBtn = $('[data-grestart]', root), live = $('[data-announce]', root), note = $('.ground-note', root), steps = $$('.ground-steps li', root);
    let s = 0, c = 0;
    function render(){
      stage.classList.remove('swap'); void stage.offsetWidth; stage.classList.add('swap');
      steps.forEach((li, k) => { li.classList.toggle('done', k < s); li.classList.toggle('current', k === s); });
      if(s >= stages.length){ root.classList.add('finished'); big.textContent = '✓'; title.textContent = 'You are here.'; hint.textContent = 'Take one slow breath in, and a long breath out. Notice how you feel now, compared with a few minutes ago. Nothing needs to be different.';
        dotsEl.innerHTML = ''; noticeBtn.hidden = true; nextBtn.hidden = true; note.hidden = true; restartBtn.hidden = false; live.textContent = 'Grounding complete.'; restartBtn.focus(); return; }
      root.classList.remove('finished'); const st = stages[s]; big.textContent = st.n; title.textContent = st.title; hint.textContent = st.hint;
      dotsEl.innerHTML = Array.from({length: st.n}, (_, k) => '<span class="' + (k < c ? 'on' : '') + '"></span>').join('');
      noticeBtn.hidden = false; nextBtn.hidden = false; note.hidden = false; restartBtn.hidden = true; note.value = '';
      noticeBtn.textContent = 'I noticed one (' + c + ' of ' + st.n + ')'; noticeBtn.disabled = c >= st.n;
      nextBtn.textContent = s === stages.length - 1 ? 'Finish' : 'Next sense →'; nextBtn.classList.toggle('btn-primary', c >= st.n); nextBtn.classList.toggle('btn-outline', c < st.n);
      note.placeholder = 'Name what you ' + st.sense + ' (optional, never saved)';
    }
    noticeBtn.addEventListener('click', () => { const st = stages[s]; if(c < st.n){ c++; Bell.init(); if(c === st.n) Bell.chime(); }
      const dots = $$('span', dotsEl); if(dots[c-1]) dots[c-1].classList.add('on');
      noticeBtn.textContent = 'I noticed one (' + c + ' of ' + st.n + ')'; noticeBtn.disabled = c >= st.n; live.textContent = c + ' of ' + st.n + ' things you can ' + st.sense + '.';
      nextBtn.classList.toggle('btn-primary', c >= st.n); nextBtn.classList.toggle('btn-outline', c < st.n); if(c >= st.n) nextBtn.focus(); });
    nextBtn.addEventListener('click', () => { s++; c = 0; render(); if(s < stages.length){ live.textContent = stages[s].title + '.'; noticeBtn.focus(); } });
    restartBtn.addEventListener('click', () => { s = 0; c = 0; render(); noticeBtn.focus(); });
    render();
  });

  /* ---------- Loving-kindness phrase flow ---------- */
  $$('[data-tool="kindness"]').forEach(root => {
    const circles = {
      self: {name:'Yourself', intro:'Now turn toward yourself. Place a hand on your heart if you like, and picture yourself just as you are right now.'},
      loved: {name:'Someone you love', intro:'Begin with someone you love. Bring to mind someone who makes you smile easily: a friend, a grandparent, a pet. See their face.'},
      neutral: {name:'Someone neutral', intro:'Picture someone you barely know: a neighbour, a shop assistant, a person you passed on the street.'},
      difficult: {name:'Someone difficult', intro:'If you feel ready, picture someone you find a little difficult. Not the hardest person, just a mild friction.'},
      all: {name:'All beings', intro:'Now let your kindness widen, like light spreading across a sky, to everyone and everything, everywhere.'}};
    const order = ['loved','self','neutral','difficult','all'];
    const DEFAULT = ['May you be happy.','May you be healthy.','May you be safe.','May you live with ease.'];
    const phraseEl = $('.lk-phrase', root), whoEl = $('.lk-who', root), stageEl = $('.lk-stage', root), playBtn = $('[data-play]', root), paceSel = $('[data-pace]', root), voiceBox = $('[data-voice]', root), ta = $('textarea', root), dots = $('.lk-dots', root);
    const chips = $$('[data-circle]', root);
    let phrases = store.get('wh-lk-phrases', DEFAULT), mode = 'journey', queue = [], qi = 0, playing = false, timer = null;
    ta.value = phrases.join('\n');
    function adapt(p, who){ if(who === 'self') return p.replace(/\byou are\b/gi,'I am').replace(/\byourself\b/gi,'myself').replace(/\byour\b/gi,'my').replace(/\byou\b/gi,'I');
      if(who === 'all') return p.replace(/\byou are\b/gi,'all beings are').replace(/\byourself\b/gi,'themselves').replace(/\byour\b/gi,'their').replace(/\byou\b/gi,'all beings'); return p; }
    function build(){ const list = mode === 'journey' ? order : [mode]; queue = [];
      list.forEach(w => { queue.push({who:w, text:circles[w].intro, intro:true}); for(let r = 0; r < 2; r++) phrases.forEach(p => queue.push({who:w, text:adapt(p, w)})); });
      queue.push({who:'end', text:'Rest for a moment in the warmth of these wishes. Notice how you feel.', intro:true}); qi = 0;
      dots.innerHTML = (mode === 'journey' ? order : [mode]).map(w => '<span data-w="' + w + '" title="' + circles[w].name + '"></span>').join(''); }
    function show(){ const q = queue[qi]; phraseEl.classList.remove('in'); 
      setTimeout(() => { phraseEl.textContent = q.text; phraseEl.classList.toggle('intro', !!q.intro); whoEl.textContent = q.who === 'end' ? 'Closing' : circles[q.who].name;
        $$('span', dots).forEach(d => d.classList.toggle('on', d.dataset.w === q.who)); phraseEl.classList.add('in');
        if(voiceBox && voiceBox.checked) Speech.say(q.text); }, reduce ? 0 : 700);
      if(playing){ clearTimeout(timer); const dur = (+paceSel.value + (q.intro ? 4 : 0)) * 1000;
        timer = setTimeout(() => { if(qi < queue.length - 1){ qi++; show(); } else { stop(); Bell.ring(0.25); playBtn.textContent = 'Begin again'; qi = 0; } }, dur); } }
    function play(){ Bell.init(); if(qi === 0){ build(); Bell.ring(0.25); } playing = true; stageEl.classList.add('playing'); playBtn.textContent = 'Pause'; playBtn.setAttribute('aria-pressed','true'); show(); }
    function stop(){ playing = false; clearTimeout(timer); stageEl.classList.remove('playing'); playBtn.textContent = 'Resume'; playBtn.setAttribute('aria-pressed','false'); Speech.stop(); }
    playBtn.addEventListener('click', () => playing ? stop() : play());
    $('[data-next]', root).addEventListener('click', () => { if(!queue.length) build(); qi = Math.min(queue.length - 1, qi + 1); show(); });
    chips.forEach(c => c.addEventListener('click', () => { chips.forEach(x => x.setAttribute('aria-pressed','false')); c.setAttribute('aria-pressed','true'); mode = c.dataset.circle; stop(); build(); playBtn.textContent = 'Begin'; qi = 0; phraseEl.textContent = c.dataset.circle === 'journey' ? 'Five widening circles of kindness, beginning with someone you love.' : circles[mode].intro; phraseEl.classList.add('in'); }));
    $('[data-save]', root).addEventListener('click', () => { const v = ta.value.split('\n').map(s => s.trim()).filter(Boolean); phrases = v.length ? v : DEFAULT; store.set('wh-lk-phrases', phrases); $('[data-saved]', root).textContent = 'Saved on this device.'; build(); qi = 0; });
    $('[data-default]', root).addEventListener('click', () => { phrases = DEFAULT.slice(); ta.value = phrases.join('\n'); store.set('wh-lk-phrases', phrases); $('[data-saved]', root).textContent = 'Restored the traditional phrases.'; build(); qi = 0; });
    if(voiceBox && !Speech.ok) voiceBox.closest('label').hidden = true;
    build(); phraseEl.classList.add('in');
  });

  /* ---------- Guided video sessions ----------
     One session clock drives captions, the voice track and the music track (both plain <audio>, started from the
     user's tap so iOS allows them). Music volume + ducking go through a Web Audio gain node where that is safe
     (everywhere except older iOS, where media.volume is read-only and Web Audio obeys the mute switch). */
  const players = [];
  const AC = window.AudioContext || window.webkitAudioContext;
  const iOS = /iP(hone|ad|od)/.test(navigator.platform || '') || (navigator.userAgent.includes('Mac') && 'ontouchend' in document);
  try{ if(navigator.audioSession) navigator.audioSession.type = 'playback'; }catch(e){}
  const canRoute = !!AC && (!iOS || !!navigator.audioSession);
  const DUCK = 0.63;   /* about -4 dB extra under the voice while it speaks */
  $$('[data-session]').forEach(root => {
    const data = JSON.parse(root.dataset.session); const total = data.total; const cues = data.cues; const speech = data.speech || [];
    const video = $('video', root), audio = $('audio[data-track="voice"]', root), music = $('audio[data-track="music"]', root);
    const cap = $('.caption', root), seek = $('.seek', root), timeEl = $('.ptime', root);
    const playBtn = $('[data-play]', root), bigBtn = $('.big-play', root), voiceBtn = $('[data-voice]', root), musicBtn = $('[data-music]', root), volEl = $('[data-mvol]', root);
    const fsBtn = $('[data-fs]', root), player = $('.player', root), status = $('[data-announce]', root);
    let elapsed = 0, playing = false, last = 0, raf = null, cueIdx = -1, fadeT = null;
    let voice = store.get('wh-voice-v2', true), audioOk = !!audio, musicOn = store.get('wh-music', true), musicOk = !!music;
    let vol = +store.get('wh-music-vol', 0.8), gain = null, routed = false, lastGain = -1;
    seek.max = total; if(volEl) volEl.value = vol;
    function setVoiceUI(){ voiceBtn.setAttribute('aria-pressed', String(voice)); voiceBtn.querySelector('span').textContent = voice ? 'Voice on' : 'Voice off'; }
    function setMusicUI(){ if(!musicBtn) return; musicBtn.setAttribute('aria-pressed', String(musicOn)); musicBtn.querySelector('span').textContent = musicOn ? 'Music on' : 'Music off';
      if(volEl) volEl.disabled = !musicOn; }
    function cueAt(t){ let k = -1; for(let j = 0; j < cues.length; j++){ if(cues[j][0] <= t) k = j; else break; } return k; }
    function speaking(t){ for(const [a, b] of speech){ if(t >= a - 0.3 && t <= b + 0.6) return true; if(a > t) break; } return false; }
    function showCue(k, speak){ cueIdx = k; const text = k >= 0 ? cues[k][1] : '';
      clearTimeout(fadeT); cap.classList.remove('in');
      fadeT = setTimeout(() => { cap.textContent = text; if(text) cap.classList.add('in'); }, reduce ? 0 : 650);
      if(speak && voice && !audioOk && text) Speech.say(text); }
    function ui(){ seek.value = Math.floor(elapsed); timeEl.textContent = fmt(elapsed) + ' / ' + fmt(total);
      seek.setAttribute('aria-valuetext', fmt(elapsed) + ' of ' + fmt(total)); root.style.setProperty('--p', (elapsed / total * 100) + '%'); }
    /* music level: slider volume, ducked while the narration speaks */
    function route(){ if(routed || !canRoute || !music) return; routed = true;
      try{ const ctx = Bell.init(); if(!ctx) return; const src = ctx.createMediaElementSource(music); gain = ctx.createGain(); gain.gain.value = vol; src.connect(gain); gain.connect(ctx.destination); }
      catch(e){ gain = null; } }
    function level(force){ if(!music) return; const g = vol * (voice && audioOk && speaking(elapsed) ? DUCK : 1);
      if(!force && Math.abs(g - lastGain) < 0.001) return; lastGain = g;
      if(gain){ const ctx = Bell.ctx; gain.gain.cancelScheduledValues(ctx.currentTime); gain.gain.setTargetAtTime(g, ctx.currentTime, force ? 0.05 : 0.4); }
      else { try{ music.volume = Math.max(0, Math.min(1, g)); }catch(e){} } }
    let lastSync = 0;
    function keep(el, on, now, force){
      if(!(el && on && playing)) return;
      if(el.readyState >= 1 && (force || (Math.abs(el.currentTime - elapsed) > 0.75 && now - lastSync > 1500))){
        lastSync = now; try{ el.currentTime = Math.min(elapsed, (el.duration || total) - 0.05); }catch(e){} }
      if(el.paused && !el.ended){ const p = el.play(); if(p && p.catch) p.catch(err => { if(err && err.name === 'NotAllowedError') return; if(el === audio) audioOk = false; else musicOk = false; }); }
    }
    function syncAll(now, force){ keep(audio, voice && audioOk, now, force); keep(music, musicOn && musicOk, now, force); }
    function frame(now){ if(!playing) return;
      elapsed += Math.min(0.25, (now - last) / 1000); last = now;   /* session clock; voice + music follow it */
      if(elapsed >= total){ end(); return; }
      const k = cueAt(elapsed); if(k !== cueIdx) showCue(k, true);
      syncAll(now, false); level(false); ui(); raf = requestAnimationFrame(frame); }
    function prime(el){ if(el && el.readyState < 1){ el.preload = 'auto'; el.addEventListener('loadedmetadata', () => keep(el, el === audio ? voice && audioOk : musicOn && musicOk, performance.now(), true), {once: true}); } }
    function startTracks(){ if(voice && audioOk) prime(audio); if(musicOn && musicOk){ route(); prime(music); }
      level(true); syncAll(performance.now(), true); }   /* play() is called synchronously inside the tap */
    function play(){ players.forEach(p => p !== api && p.pause()); Bell.init();
      if(elapsed === 0) Bell.ring(0.3);
      playing = true; root.classList.add('playing', 'started'); playBtn.setAttribute('aria-label','Pause'); playBtn.setAttribute('aria-pressed','true');
      if(!reduce){ const p = video.play(); if(p && p.catch) p.catch(() => {}); }
      startTracks(); last = performance.now(); cueIdx = -2; raf = requestAnimationFrame(frame); status.textContent = 'Playing ' + data.title; }
    function pause(){ if(!playing) return; playing = false; cancelAnimationFrame(raf); root.classList.remove('playing'); playBtn.setAttribute('aria-label','Play'); playBtn.setAttribute('aria-pressed','false');
      video.pause(); if(audio) audio.pause(); if(music) music.pause(); Speech.stop(); status.textContent = 'Paused'; }
    function end(){ pause(); elapsed = 0; ui(); Bell.ring(0.3); setTimeout(() => Bell.ring(0.22), 2400);
      [audio, music].forEach(el => { if(el) try{ el.currentTime = 0; }catch(e){} });
      root.classList.remove('started'); cap.textContent = 'Session complete. Thank you for practicing.'; cap.classList.add('in'); status.textContent = 'Session complete'; cueIdx = -1;
      const done = store.get('wh-guided-done', {}); done[data.id] = (done[data.id] || 0) + 1; store.set('wh-guided-done', done); }
    function seekTo(t){ elapsed = Math.max(0, Math.min(total - 0.5, t)); lastSync = 0; showCue(cueAt(elapsed), false); cueIdx = cueAt(elapsed); ui();
      [audio, music].forEach(el => { if(el && el.readyState >= 1) try{ el.currentTime = elapsed; }catch(e){} }); level(true); syncAll(performance.now(), true); }
    const api = {pause};
    players.push(api);
    playBtn.addEventListener('click', () => playing ? pause() : play());
    bigBtn.addEventListener('click', () => { play(); playBtn.focus(); });
    seek.addEventListener('input', () => seekTo(+seek.value));
    voiceBtn.addEventListener('click', () => { voice = !voice; store.set('wh-voice-v2', voice); setVoiceUI();
      if(voice){ if(playing){ if(audioOk){ prime(audio); keep(audio, true, performance.now(), true); } else if(cueIdx >= 0) Speech.say(cues[cueIdx][1]); } }
      else { if(audio) audio.pause(); Speech.stop(); }
      level(true); });
    if(musicBtn) musicBtn.addEventListener('click', () => { musicOn = !musicOn; store.set('wh-music', musicOn); setMusicUI();
      if(musicOn){ if(playing && musicOk){ route(); prime(music); level(true); keep(music, true, performance.now(), true); } }
      else if(music) music.pause(); });
    if(volEl) volEl.addEventListener('input', () => { vol = +volEl.value; store.set('wh-music-vol', vol); level(true); });
    if(audio) audio.addEventListener('error', () => { audioOk = false; if(voice && playing && cueIdx >= 0) Speech.say(cues[cueIdx][1]); level(true); });
    if(music) music.addEventListener('error', () => { musicOk = false; if(musicBtn) musicBtn.closest('.music-ctl').hidden = true; });
    if(music && !canRoute && iOS && volEl) volEl.hidden = true;   /* older iOS: volume is fixed by the hardware buttons */
    fsBtn.addEventListener('click', () => { const d = document; if(d.fullscreenElement){ d.exitFullscreen(); } else if(player.requestFullscreen){ player.requestFullscreen().catch(() => {}); } else if(video.webkitEnterFullscreen){ video.webkitEnterFullscreen(); } });
    player.addEventListener('keydown', e => { if(e.target === seek || e.target === volEl) return; if(e.key === ' ' || e.key === 'k'){ if(e.target.tagName === 'BUTTON') return; e.preventDefault(); playing ? pause() : play(); } });
    document.addEventListener('visibilitychange', () => { if(document.hidden && playing && !((voice && audioOk) || (musicOn && musicOk))) pause(); });
    /* if the video goes native-fullscreen on iOS and the user pauses/plays there, follow it */
    video.addEventListener('webkitendfullscreen', () => { if(playing){ const p = video.play(); if(p && p.catch) p.catch(() => {}); } });
    setVoiceUI(); setMusicUI(); ui();
  });
})();
