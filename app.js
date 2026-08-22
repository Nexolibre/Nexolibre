(function(){
  /* ---------- analytics (GA4) — poné tu Measurement ID abajo ---------- */
  const GA_ID='';   // ← reemplazar por 'G-XXXXXXXXXX' para activar
  if(GA_ID){
    const s=document.createElement('script');s.async=true;
    s.src='https://www.googletagmanager.com/gtag/js?id='+GA_ID;document.head.appendChild(s);
    window.dataLayer=window.dataLayer||[];
    window.gtag=function(){dataLayer.push(arguments);};
    gtag('js',new Date());gtag('config',GA_ID,{anonymize_ip:true});
    document.addEventListener('click',function(e){
      const a=e.target.closest('a'); if(!a)return;
      const h=a.getAttribute('href')||'';
      if(h.indexOf('wa.me')>-1) gtag('event','whatsapp_click',{page:location.pathname});
      else if(h.indexOf('parte=')>-1) gtag('event','consultar_click',{pieza:(h.match(/parte=([^&]+)/)||[])[1]||'',page:location.pathname});
      else if(/^mailto:/.test(h)) gtag('event','email_click');
      else if(h.indexOf('#lang')<0 && /\/(en|pt)?\/?$/.test(h)===false && h.indexOf('http')===0) gtag('event','outbound_click',{url:h});
    });
  }

  /* ---------- WhatsApp flotante (todas las páginas) ---------- */
  if(!document.querySelector('.wa-float')){
    const wa=document.createElement('a');
    wa.className='wa-float'; wa.href='https://wa.me/5491167410993?text='+encodeURIComponent('Hola Nexolibre, quería consultar por');
    wa.target='_blank'; wa.rel='noopener'; wa.setAttribute('aria-label','WhatsApp');
    wa.innerHTML='<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.1-.6.2-.2.3-.7 1-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5 0-.2-.6-1.5-.9-2-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.3.3-1 1-1 2.3s1 2.7 1.1 2.9c.2.2 2 3.1 5 4.3 2.4 1 2.9.8 3.4.8.5 0 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.2-.6-.4z"/><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.2-1.3c1.4.8 3 1.2 4.7 1.2h.1c5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18h-.1c-1.5 0-3-.4-4.3-1.2l-.3-.2-3.1.8.8-3-.2-.3C4 14.6 3.5 13.3 3.5 12 3.5 7.3 7.3 3.5 12 3.5S20.5 7.3 20.5 12 16.7 20 12 20z"/></svg>';
    document.body.appendChild(wa);
  }

  /* ---------- i18n (idioma por URL: /  /en/  /pt/) ---------- */
  const pageLang=document.documentElement.getAttribute('data-i18n')||document.documentElement.lang||'es';
  function setLang(lang){
    document.documentElement.lang=lang;
    document.querySelectorAll('[data-'+lang+']').forEach(el=>{
      const v=el.getAttribute('data-'+lang);
      if(v!==null) el.innerHTML=v;
    });
    document.querySelectorAll('[data-'+lang+'-ph]').forEach(el=>{
      el.setAttribute('placeholder',el.getAttribute('data-'+lang+'-ph'));
    });
    document.querySelectorAll('#lang button').forEach(b=>b.classList.toggle('active',b.dataset.lang===lang));
  }
  function localeUrl(lang){
    let p=location.pathname.replace(/^\/(en|pt)(?=\/|$)/,'');
    if(!p.startsWith('/')) p='/'+p;
    if(lang!=='es') p='/'+lang+p;
    return p+location.search+location.hash;
  }
  document.querySelectorAll('#lang button').forEach(b=>b.addEventListener('click',()=>{location.href=localeUrl(b.dataset.lang);}));
  setLang(pageLang);

  /* ---------- header scroll ---------- */
  const header=document.getElementById('header');
  if(header) window.addEventListener('scroll',()=>header.classList.toggle('scrolled',window.scrollY>10));

  /* ---------- mobile menu ---------- */
  const burger=document.getElementById('burger'), nav=document.getElementById('nav');
  if(burger && nav){
    burger.addEventListener('click',()=>nav.parentElement.classList.toggle('mobile-open'));
    document.querySelectorAll('.nav-links a').forEach(a=>a.addEventListener('click',()=>nav.parentElement.classList.remove('mobile-open')));
  }

  /* ---------- reveal on scroll ---------- */
  const io=new IntersectionObserver((entries)=>{
    entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});
  },{threshold:.12});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

  /* ---------- count up ---------- */
  const cio=new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(!e.isIntersecting) return;
      const el=e.target, end=parseInt(el.dataset.count,10), pre=el.dataset.prefix||'', suf=el.dataset.suffix||'';
      let cur=0; const step=Math.max(1,Math.round(end/40));
      const t=setInterval(()=>{cur+=step; if(cur>=end){cur=end;clearInterval(t);} el.textContent=pre+cur+suf;},22);
      cio.unobserve(el);
    });
  },{threshold:.5});
  document.querySelectorAll('[data-count]').forEach(el=>cio.observe(el));

  /* ---------- testimonials ---------- */
  const slides=[...document.querySelectorAll('.tslide')], tnav=document.getElementById('tnav');
  if(tnav && slides.length){
    let idx=0;
    slides.forEach((s,i)=>{const b=document.createElement('button'); if(i===0)b.classList.add('active'); b.addEventListener('click',()=>go(i)); tnav.appendChild(b);});
    const dots=[...tnav.children];
    function go(i){slides[idx].classList.remove('active');dots[idx].classList.remove('active');idx=i;slides[idx].classList.add('active');dots[idx].classList.add('active');}
    if(slides.length>1) setInterval(()=>go((idx+1)%slides.length),6000);
  }

  /* ---------- video de fondo: forzar autoplay al cargar ---------- */
  (function(){
    const vids=[...document.querySelectorAll('.statshero-vid, .topmedia-vid')];
    if(!vids.length) return;
    function play(){vids.forEach(v=>{try{v.muted=true;v.setAttribute('muted','');const p=v.play();if(p&&p.catch)p.catch(()=>{});}catch(e){}});}
    play();
    // reintenta apenas haya interacción o cuando la pestaña vuelve a estar visible
    ['click','touchstart','scroll','keydown'].forEach(ev=>window.addEventListener(ev,play,{once:true,passive:true}));
    document.addEventListener('visibilitychange',()=>{if(!document.hidden)play();});
  })();

  /* ---------- marquee de clientes (loop infinito) ---------- */
  document.querySelectorAll('[data-marquee]').forEach(track=>{
    const originals=[...track.children];
    originals.forEach(node=>track.appendChild(node.cloneNode(true)));
  });

  /* ---------- carrusel de laboratorios ---------- */
  document.querySelectorAll('[data-carousel]').forEach(car=>{
    const track=car.querySelector('.lab-track');
    const slides=[...car.querySelectorAll('.lab-slide')];
    const dotsWrap=car.querySelector('.lab-dots');
    if(!track || slides.length<=1) return;
    let i=0, timer;
    slides.forEach((_,n)=>{const b=document.createElement('button'); if(n===0)b.classList.add('active'); b.setAttribute('aria-label','Foto '+(n+1)); b.addEventListener('click',()=>{go(n);start();}); dotsWrap.appendChild(b);});
    const dots=[...dotsWrap.children];
    function go(n){i=(n+slides.length)%slides.length; track.style.transform='translateX(-'+(i*100)+'%)'; dots.forEach((d,k)=>d.classList.toggle('active',k===i));}
    function start(){clearInterval(timer); timer=setInterval(()=>go(i+1),5500);}
    const next=car.querySelector('.lab-nav.next'), prev=car.querySelector('.lab-nav.prev');
    if(next) next.addEventListener('click',()=>{go(i+1);start();});
    if(prev) prev.addEventListener('click',()=>{go(i-1);start();});
    car.addEventListener('mouseenter',()=>clearInterval(timer));
    car.addEventListener('mouseleave',start);
    start();
  });

  /* ---------- form (Web3Forms) ---------- */
  const form=document.getElementById('demoForm'), ok=document.getElementById('formOk');
  const formErr=document.getElementById('formErr');
  if(form) form.addEventListener('submit',async (ev)=>{
    ev.preventDefault();
    if(!form.checkValidity()){form.reportValidity();return;}
    const lang=document.documentElement.lang;
    const btn=form.querySelector('button[type=submit]');
    const orig=btn?btn.innerHTML:'';
    if(btn){btn.disabled=true;btn.textContent=(lang==='en'?'Sending…':lang==='pt'?'Enviando…':'Enviando…');}
    if(ok)ok.classList.remove('show'); if(formErr)formErr.classList.remove('show');
    try{
      const res=await fetch('https://api.web3forms.com/submit',{
        method:'POST',headers:{'Accept':'application/json'},body:new FormData(form)
      });
      const json=await res.json();
      if(json.success){ if(ok)ok.classList.add('show'); if(window.gtag)gtag('event','generate_lead',{form:'contacto'}); form.reset(); }
      else { if(formErr)formErr.classList.add('show'); }
    }catch(e){ if(formErr)formErr.classList.add('show'); }
    finally{ if(btn){btn.disabled=false;btn.innerHTML=orig;} }
  });

  /* ---------- lead magnet: catálogo PDF por email ---------- */
  const pdfForm=document.getElementById('pdfForm');
  if(pdfForm) pdfForm.addEventListener('submit',async (ev)=>{
    ev.preventDefault();
    if(!pdfForm.checkValidity()){pdfForm.reportValidity();return;}
    const lang=document.documentElement.lang, sending={es:'Enviando…',en:'Sending…',pt:'Enviando…'}[lang]||'Enviando…';
    const btn=pdfForm.querySelector('button[type=submit]'), orig=btn?btn.innerHTML:'';
    const ok=document.getElementById('pdfOk'), er=document.getElementById('pdfErr');
    if(ok)ok.classList.remove('show'); if(er)er.classList.remove('show');
    if(btn){btn.disabled=true;btn.textContent=sending;}
    const pdf='/assets/catalogo-nexolibre-'+(['es','en','pt'].includes(lang)?lang:'es')+'.pdf';
    try{
      const res=await fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Accept':'application/json'},body:new FormData(pdfForm)});
      const json=await res.json();
      if(json.success){
        if(window.gtag)gtag('event','generate_lead',{form:'lead_magnet'});
        const a=document.createElement('a');a.href=pdf;a.download='';document.body.appendChild(a);a.click();a.remove();
        if(ok)ok.classList.add('show'); pdfForm.reset();
      } else { if(er)er.classList.add('show'); }
    }catch(e){ if(er)er.classList.add('show'); }
    finally{ if(btn){btn.disabled=false;btn.innerHTML=orig;} }
  });

  /* ---------- prefill from catalog (?parte=) ---------- */
  if(form){
    const pp=new URLSearchParams(location.search).get('parte');
    if(pp){
      const m=form.querySelector('[name=mensaje]');
      if(m && !m.value) m.value=(document.documentElement.lang==='en'?'Inquiry about part: ':'Consulta por la pieza: ')+pp;
      const pr=form.querySelector('[name=producto]');
      if(pr){const opt=[...pr.options].find(o=>/repuesto|spare/i.test(o.textContent));if(opt)pr.value=opt.value;}
    }
  }
})();
