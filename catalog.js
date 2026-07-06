(function(){
  const grid=document.getElementById('catGrid');
  if(!grid) return;
  const q=document.getElementById('catSearch');
  const fCat=document.getElementById('fCat'), fMod=document.getElementById('fMod'), fMarca=document.getElementById('fMarca'), fLoc=document.getElementById('fLoc');
  const count=document.getElementById('catCount');
  const pager=document.getElementById('catPager');
  const PER=12;                 // piezas por página (cambiá a 9 si preferís)
  let parts=[], page=1;

  const lang=()=>document.documentElement.lang||'es';
  const T={
    es:{consultar:'Consultar',ver:'Ver publicación',marca:'Marca',modelo:'Compatible',parte:'N° parte',garantia:'Garantía',ubic:'Ubicación',none:'No encontramos piezas con esos filtros.',err:'No se pudo cargar el catálogo.',all:['Todas las categorías','Todas las modalidades','Todas las marcas','Todas las ubicaciones'],res:r=>r+(r===1?' pieza':' piezas')},
    en:{consultar:'Ask',ver:'View listing',marca:'Brand',modelo:'Fits',parte:'Part No.',garantia:'Warranty',ubic:'Location',none:'No parts match these filters.',err:'Could not load the catalog.',all:['All categories','All modalities','All brands','All locations'],res:r=>r+(r===1?' part':' parts')},
    pt:{consultar:'Consultar',ver:'Ver anúncio',marca:'Marca',modelo:'Compatível',parte:'Nº peça',garantia:'Garantia',ubic:'Localização',none:'Não encontramos peças com esses filtros.',err:'Não foi possível carregar o catálogo.',all:['Todas as categorias','Todas as modalidades','Todas as marcas','Todas as localizações'],res:r=>r+(r===1?' peça':' peças')}
  };
  const t=()=>T[lang()]||T.es;
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  window.catPh=()=>'<svg width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="14" rx="2"/><circle cx="12" cy="13" r="3.5"/><path d="M8 6l1.5-2h5L16 6"/></svg>';

  function imgSrc(v){ if(!v) return ''; return /^https?:\/\//i.test(v)?v:('/assets/parts/'+v); }
  // Una pieza puede tener varias fotos: separadas por ; o , o salto de línea
  function imgsOf(p){ return String(p.imagen||'').split(/[;,\n]+/).map(s=>s.trim()).filter(Boolean).map(imgSrc); }
  function uniq(key){return [...new Set(parts.map(p=>p[key]).filter(Boolean))].sort((a,b)=>a.localeCompare(b));}
  function fillSelect(sel,key,labelAll){if(!sel)return;const cur=sel.value;sel.innerHTML='<option value="">'+esc(labelAll)+'</option>'+uniq(key).map(v=>'<option>'+esc(v)+'</option>').join('');sel.value=cur;}

  function badge(disp){
    const d=(disp||'').toLowerCase();
    if(!disp) return '';
    if(d.includes('stock')) return '<span class="badge badge-stock">'+esc(disp)+'</span>';
    if(d.includes('pedido')||d.includes('order')) return '<span class="badge badge-order">'+esc(disp)+'</span>';
    return '<span class="badge badge-soft">'+esc(disp)+'</span>';
  }

  function card(p){
    const tt=t();
    const imgs=imgsOf(p);
    const imgsAttr = imgs.length ? " data-imgs=\""+esc(JSON.stringify(imgs))+"\"" : "";
    const alt = esc([p.marca,p.nombre,p.categoria,p.modalidad].filter(Boolean).join(' '));
    const mainHtml = imgs.length
      ? '<img src="'+esc(imgs[0])+'" alt="'+alt+'" loading="lazy" decoding="async" onerror="this.parentNode.innerHTML=catPh()">'
      : catPh();
    const thumbs = imgs.length>1
      ? '<div class="part-thumbs">'+imgs.map((u,i)=>'<button type="button" class="pthumb'+(i===0?' active':'')+'" data-img="'+esc(u)+'"><img src="'+esc(u)+'" alt=""></button>').join('')+'</div>'
      : '';
    const meta=[
      p.marca?'<div><b>'+tt.marca+':</b> '+esc(p.marca)+'</div>':'',
      p.modelo_compatible?'<div><b>'+tt.modelo+':</b> '+esc(p.modelo_compatible)+'</div>':'',
      (p.nro_parte&&p.nro_parte!=='-')?'<div><b>'+tt.parte+':</b> '+esc(p.nro_parte)+'</div>':'',
      p.ubicacion?'<div><b>'+tt.ubic+':</b> '+esc(p.ubicacion)+'</div>':'',
      (p.garantia&&p.garantia!=='-')?'<div><b>'+tt.garantia+':</b> '+esc(p.garantia)+'</div>':''
    ].join('');
    const tags=[p.categoria,p.modalidad,p.estado].filter(Boolean).map(x=>'<span class="badge badge-soft">'+esc(x)+'</span>').join('');
    const ext='';  // link externo NO se muestra: el cliente consulta a Nexolibre (el dato queda solo para uso interno)
    return '<article class="part">'
      +'<div class="part-img'+(imgs.length?' has-img':'')+'"'+imgsAttr+'>'+mainHtml+'</div>'
      + thumbs
      +'<div class="part-body">'
      +'<div class="part-tags">'+tags+'</div>'
      +'<h3>'+esc(p.nombre)+'</h3>'
      +'<div class="meta">'+meta+'</div>'
      +(p.descripcion?'<p class="meta">'+esc(p.descripcion)+'</p>':'')
      +'<div class="part-foot">'+badge(p.disponibilidad)
      +'<a class="btn btn-primary" style="padding:9px 16px;font-size:14px" href="/contacto/?parte='+encodeURIComponent(p.ref||p.nombre||'')+'">'+tt.consultar+'</a>'
      +'</div>'+(ext?'<div style="padding-top:4px">'+ext+'</div>':'')
      +'</div></article>';
  }

  function filterParts(){
    const s=(q&&q.value||'').toLowerCase().trim();
    return parts.filter(p=>{
      if(fCat&&fCat.value&&p.categoria!==fCat.value)return false;
      if(fMod&&fMod.value&&p.modalidad!==fMod.value)return false;
      if(fMarca&&fMarca.value&&p.marca!==fMarca.value)return false;
      if(fLoc&&fLoc.value&&p.ubicacion!==fLoc.value)return false;
      if(s){const hay=[p.nombre,p.nro_parte,p.modelo_compatible,p.marca,p.ref,p.categoria].filter(Boolean).join(' ').toLowerCase();if(!hay.includes(s))return false;}
      return true;
    });
  }

  function pgBtn(n,label,o){o=o||{};return '<button class="pg'+(o.active?' active':'')+'"'+(o.disabled?' disabled':'')+' data-page="'+n+'">'+(label||n)+'</button>';}
  function renderPager(pages){
    if(!pager) return;
    if(pages<=1){pager.innerHTML='';return;}
    let html=pgBtn(page-1,'‹',{disabled:page===1}), last=0;
    for(let i=1;i<=pages;i++){
      if(i===1||i===pages||Math.abs(i-page)<=1){
        if(last && i-last>1) html+='<span class="pg-dots">…</span>';
        html+=pgBtn(i,String(i),{active:i===page}); last=i;
      }
    }
    html+=pgBtn(page+1,'›',{disabled:page===pages});
    pager.innerHTML=html;
  }

  function render(){
    const res=filterParts();
    const pages=Math.max(1,Math.ceil(res.length/PER));
    if(page>pages)page=pages; if(page<1)page=1;
    const slice=res.slice((page-1)*PER,(page-1)*PER+PER);
    if(count)count.textContent=t().res(res.length);
    grid.innerHTML=res.length?slice.map(card).join(''):'<div class="cat-empty">'+t().none+'</div>';
    renderPager(pages);
  }

  /* ---------- interacciones de imagen (miniaturas + lightbox) ---------- */
  let lb,lbImg,lbImgs=[],lbIdx=0;
  function ensureLB(){
    if(lb) return;
    lb=document.createElement('div'); lb.className='lightbox';
    lb.innerHTML='<button class="lb-close" aria-label="Cerrar">×</button><button class="lb-prev" aria-label="Anterior">‹</button><img alt=""><button class="lb-next" aria-label="Siguiente">›</button>';
    document.body.appendChild(lb);
    lbImg=lb.querySelector('img');
    lb.addEventListener('click',e=>{ if(e.target===lb||e.target.classList.contains('lb-close')) lb.classList.remove('open'); });
    lb.querySelector('.lb-prev').addEventListener('click',()=>navLB(-1));
    lb.querySelector('.lb-next').addEventListener('click',()=>navLB(1));
    document.addEventListener('keydown',e=>{ if(!lb.classList.contains('open'))return; if(e.key==='Escape')lb.classList.remove('open'); if(e.key==='ArrowLeft')navLB(-1); if(e.key==='ArrowRight')navLB(1); });
  }
  function showLB(){ lbImg.src=lbImgs[lbIdx]; const m=lbImgs.length>1?'':'none'; lb.querySelector('.lb-prev').style.display=m; lb.querySelector('.lb-next').style.display=m; }
  function openLB(imgs,idx){ ensureLB(); lbImgs=imgs; lbIdx=idx||0; showLB(); lb.classList.add('open'); }
  function navLB(d){ lbIdx=(lbIdx+d+lbImgs.length)%lbImgs.length; showLB(); }

  grid.addEventListener('click',e=>{
    const th=e.target.closest('.pthumb');
    if(th){
      const part=th.closest('.part'); const main=part.querySelector('.part-img img');
      if(main) main.src=th.dataset.img;
      part.querySelectorAll('.pthumb').forEach(b=>b.classList.toggle('active',b===th));
      return;
    }
    const pi=e.target.closest('.part-img.has-img');
    if(pi){
      try{
        const imgs=JSON.parse(pi.getAttribute('data-imgs'));
        const cur=pi.querySelector('img'); const idx=cur?Math.max(0,imgs.indexOf(cur.getAttribute('src'))):0;
        openLB(imgs,idx);
      }catch(_){}
    }
  });

  [q,fCat,fMod,fMarca,fLoc].forEach(el=>el&&el.addEventListener('input',()=>{page=1;render();}));
  if(pager) pager.addEventListener('click',e=>{
    const b=e.target.closest('button[data-page]'); if(!b||b.disabled) return;
    const n=parseInt(b.dataset.page,10); if(!n||n===page) return;
    page=n; render();
    const top=document.querySelector('.cat-tools'); if(top) top.scrollIntoView({behavior:'smooth',block:'start'});
  });
  document.querySelectorAll('#lang button').forEach(b=>b.addEventListener('click',()=>setTimeout(()=>{
    const a=t().all; fillSelect(fCat,'categoria',a[0]);fillSelect(fMod,'modalidad',a[1]);fillSelect(fMarca,'marca',a[2]);fillSelect(fLoc,'ubicacion',a[3]); render();
  },0)));

  fetch('/parts.json?v='+Date.now(),{cache:'no-store'}).then(r=>r.json()).then(data=>{
    parts=Array.isArray(data)?data:[];
    const a=t().all;
    fillSelect(fCat,'categoria',a[0]);fillSelect(fMod,'modalidad',a[1]);fillSelect(fMarca,'marca',a[2]);fillSelect(fLoc,'ubicacion',a[3]);
    render();
    injectSeo(parts);
  }).catch(()=>{grid.innerHTML='<div class="cat-empty">'+t().err+'</div>';});

  // Datos estructurados (SEO/GEO): catálogo como ItemList de Product
  function injectSeo(list){
    try{
      var BASE='https://nexolibre.com';
      var items=list.slice(0,100).map(function(p,i){
        var imgs=imgsOf(p).map(function(u){return /^https?:/.test(u)?u:BASE+'/'+u;});
        var avail=/stock/i.test(p.disponibilidad||'')?'InStock':(/pedido|order/i.test(p.disponibilidad||'')?'PreOrder':'LimitedAvailability');
        var prod={
          '@type':'Product',
          name:[p.marca,p.nombre].filter(Boolean).join(' '),
          sku:p.ref||undefined,
          mpn:(p.nro_parte&&p.nro_parte!=='-')?p.nro_parte:undefined,
          brand:p.marca?{'@type':'Brand',name:p.marca}:undefined,
          category:[p.categoria,p.modalidad].filter(Boolean).join(' / ')||undefined,
          description:p.descripcion||undefined,
          image:imgs.length?imgs:undefined,
          itemCondition:/usad|used|recond|recuper/i.test(p.estado||'')?'https://schema.org/UsedCondition':'https://schema.org/RefurbishedCondition',
          offers:{'@type':'Offer',availability:'https://schema.org/'+avail,priceCurrency:'USD',seller:{'@id':BASE+'/#organization'},
                  url:BASE+'/contacto/?parte='+encodeURIComponent(p.ref||p.nombre||'')}
        };
        Object.keys(prod).forEach(function(k){if(prod[k]===undefined)delete prod[k];});
        return {'@type':'ListItem',position:i+1,item:prod};
      });
      var ld={'@context':'https://schema.org','@type':'ItemList',name:'Catálogo de repuestos MRI/CT — Nexolibre',numberOfItems:list.length,itemListElement:items};
      var s=document.createElement('script');s.type='application/ld+json';s.textContent=JSON.stringify(ld);document.head.appendChild(s);
    }catch(e){}
  }
})();
