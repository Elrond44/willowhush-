/* Willowhush — interactions (vanilla JS) */
(function(){
  document.documentElement.classList.remove('no-js');
  const header=document.querySelector('.site-header');
  const onScroll=()=>{ if(header) header.classList.toggle('scrolled', window.scrollY>40);
    const bar=document.querySelector('.progress');
    if(bar){const h=document.documentElement; const p=h.scrollTop/(h.scrollHeight-h.clientHeight||1); bar.style.width=(p*100)+'%';}
  };
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();

  // Mobile menu
  const btn=document.querySelector('.menu-btn');
  if(btn){btn.addEventListener('click',()=>{const open=document.body.classList.toggle('menu-open');btn.setAttribute('aria-expanded',open);});
    document.querySelectorAll('.nav-links a').forEach(a=>a.addEventListener('click',()=>{document.body.classList.remove('menu-open');btn.setAttribute('aria-expanded','false');}));
    document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.body.classList.remove('menu-open');btn.setAttribute('aria-expanded','false');}});
  }

  // Reveal on scroll
  const els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    const io=new IntersectionObserver(entries=>entries.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}}),{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    els.forEach(el=>io.observe(el));
  } else els.forEach(el=>el.classList.add('in'));

  // Placeholder forms (no data is sent anywhere)
  document.querySelectorAll('form[data-placeholder]').forEach(f=>{
    f.addEventListener('submit',e=>{e.preventDefault();
      if(!f.checkValidity()){f.reportValidity();return;}
      const msg=f.parentElement.querySelector('.form-msg')||f.querySelector('.form-msg');
      if(msg) msg.textContent=f.dataset.placeholder;
      f.reset();
    });
  });

  // Blog filters
  const filterBtns=document.querySelectorAll('.filters button');
  filterBtns.forEach(b=>b.addEventListener('click',()=>{
    filterBtns.forEach(x=>x.setAttribute('aria-pressed','false'));
    b.setAttribute('aria-pressed','true');
    const cat=b.dataset.filter;
    document.querySelectorAll('[data-category]').forEach(c=>{
      const show=cat==='all'||c.dataset.category===cat;
      c.classList.toggle('hide',!show);
      if(show){c.classList.remove('fade-in-card');void c.offsetWidth;c.classList.add('fade-in-card');}
    });
    const empty=document.querySelector('.empty-state');
    if(empty) empty.hidden=document.querySelectorAll('[data-category]:not(.hide)').length>0;
  }));

  // Breathing widget
  const stage=document.querySelector('[data-breathe]');
  if(stage){
    const circle=stage.querySelector('.breath-circle'), label=stage.querySelector('.breath-label'), count=stage.querySelector('.breath-count');
    const toggle=document.querySelector('[data-breathe-toggle]');
    const patterns={box:[['Breathe in',4,'grow'],['Hold',4,'hold'],['Breathe out',4,'shrink'],['Hold',4,'hold']],
                    calm:[['Breathe in',4,'grow'],['Hold',7,'hold'],['Breathe out',8,'shrink']],
                    even:[['Breathe in',5,'grow'],['Breathe out',5,'shrink']],
                    exhale:[['Breathe in',4,'grow'],['Breathe out',6,'shrink']]};
    let pattern='box', running=false, timer=null, tick=null, cycles=0;
    const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function step(i){
      const ph=patterns[pattern][i]; let left=ph[1];
      label.textContent=ph[0];
      if(ph[2]!=='hold'){circle.style.transitionDuration=reduce?'0s':ph[1]+'s'; circle.classList.toggle('grow',ph[2]==='grow');}
      count.textContent=left;
      clearInterval(tick);
      tick=setInterval(()=>{left--; if(left>0) count.textContent=left;},1000);
      timer=setTimeout(()=>{const n=(i+1)%patterns[pattern].length; if(n===0){cycles++;} step(n);},ph[1]*1000);
    }
    function stop(){running=false;clearTimeout(timer);clearInterval(tick);circle.style.transitionDuration='1.5s';circle.classList.remove('grow');label.textContent='Ready';count.textContent='';toggle.textContent='Begin';toggle.setAttribute('aria-pressed','false');}
    toggle.addEventListener('click',()=>{ if(running){stop();return;} running=true;cycles=0;toggle.textContent='Pause';toggle.setAttribute('aria-pressed','true');step(0);});
    document.querySelectorAll('[data-pattern]').forEach(b=>b.addEventListener('click',()=>{
      document.querySelectorAll('[data-pattern]').forEach(x=>x.setAttribute('aria-pressed','false'));
      b.setAttribute('aria-pressed','true'); pattern=b.dataset.pattern; if(running){clearTimeout(timer);clearInterval(tick);step(0);}
    }));
  }
  // Ebook: pay-what-you-want amount picker. The checkout link comes from EBOOK_CHECKOUT_URL in build.py;
  // with no link configured the box renders in a "coming soon" state and this does nothing.
  document.querySelectorAll('[data-pwyw]').forEach(box=>{
    if(box.dataset.state!=='live') return;
    const chips=box.querySelectorAll('[data-amount]'), custom=box.querySelector('.pwyw-custom'), input=box.querySelector('#pwyw-amt'),
          err=box.querySelector('.pwyw-err'), buy=box.querySelector('.btn-buy'), label=box.querySelector('.pwyw-label');
    const min=parseFloat(box.dataset.min)||1, cur=box.dataset.currency||'$', param=box.dataset.priceParam, base=buy.dataset.checkout;
    let amount=parseFloat((box.querySelector('[data-amount][aria-pressed="true"]')||{}).dataset?.amount)||min;
    const fmt=n=>cur+(Number.isInteger(n)?n:n.toFixed(2));
    const update=()=>{
      const ok=amount>=min && isFinite(amount);
      err.textContent=ok?'':`Please enter at least ${fmt(min)}.`;
      label.textContent=ok?'· '+fmt(amount):'';
      buy.classList.toggle('is-invalid',!ok); buy.setAttribute('aria-disabled',ok?'false':'true');
      if(param && ok){const u=new URL(base,location.href);u.searchParams.set(param,String(amount));buy.href=u.toString();} else buy.href=base;
    };
    chips.forEach(c=>c.addEventListener('click',()=>{
      chips.forEach(x=>x.setAttribute('aria-pressed','false')); c.setAttribute('aria-pressed','true');
      if(c.dataset.amount==='custom'){custom.hidden=false; amount=parseFloat(input.value); input.focus();}
      else {custom.hidden=true; amount=parseFloat(c.dataset.amount);}
      update();
    }));
    input.addEventListener('input',()=>{amount=parseFloat(input.value); update();});
    buy.addEventListener('click',e=>{ if(buy.getAttribute('aria-disabled')==='true'){e.preventDefault(); input.focus();} });
    update();
  });
})();
