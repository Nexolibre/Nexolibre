(function(){
  /* ---------- i18n ---------- */
  const STORAGE='nexo_lang';
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
    try{localStorage.setItem(STORAGE,lang);}catch(e){}
  }
  document.querySelectorAll('#lang button').forEach(b=>b.addEventListener('click',()=>setLang(b.dataset.lang)));
  let saved='es';
  try{saved=localStorage.getItem(STORAGE)||'es';}catch(e){}
  setLang(saved);

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
      if(json.success){ if(ok)ok.classList.add('show'); form.reset(); }
      else { if(formErr)formErr.classList.add('show'); }
    }catch(e){ if(formErr)formErr.classList.add('show'); }
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
