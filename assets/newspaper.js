async function loadNews(){
  const res = await fetch('news/news.json?cb=' + Date.now());
  if(!res.ok) throw new Error('news.json missing');
  return res.json();
}
function formatTime(iso){ const d=new Date(iso); return d.toLocaleString(undefined,{hour12:false}); }
function applyFilters(items){
  const q=document.getElementById('search').value.trim().toLowerCase();
  const cat=document.getElementById('category').value;
  return items.filter(i=>{
    const matchCat=(cat==='all')||(i.category===cat);
    const matchQ=!q||i.title.toLowerCase().includes(q)||(i.summary||'').toLowerCase().includes(q)||i.source.toLowerCase().includes(q);
    return matchCat && matchQ;
  });
}
function render(list){
  const wrap=document.getElementById('list'); wrap.innerHTML='';
  list.forEach(it=>{
    const el=document.createElement('article');
    el.className='story';
    el.innerHTML=`<a href="${it.link}" target="_blank" rel="noopener"><strong>${it.title}</strong></a>
      <div class="meta">
        <span>${it.source}</span><span>·</span>
        <span>${new URL(it.link).hostname.replace('www.','')}</span><span>·</span>
        <span>${formatTime(it.published)}</span><span>·</span>
        <span>${it.category}</span>
      </div>
      ${it.summary?`<div class="summary">${it.summary}</div>`:''}`;
    wrap.appendChild(el);
  });
}
(async function boot(){
  try{
    const data=await loadNews();
    document.getElementById('updatedAt').textContent = 'Updated: ' + formatTime(data.generatedAt);
    const items=data.items||[];
    const renderNow=()=>render(applyFilters(items));
    document.getElementById('search').addEventListener('input', renderNow);
    document.getElementById('category').addEventListener('change', renderNow);
    document.getElementById('refresh').addEventListener('click', ()=>location.reload());
    renderNow();
  }catch(e){
    document.getElementById('list').innerHTML='<div class="story">Failed to load news. '+e.message+'</div>';
  }
})();