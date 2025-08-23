async function loadNews(){
  const res = await fetch('news/news.json?cb=' + Date.now());
  if(!res.ok) return {items:[]};
  return res.json();
}
function formatTime(iso){ const d=new Date(iso); return d.toLocaleString(undefined,{hour12:false}); }
function renderLatest(items){
  const el=document.getElementById('latest'); el.innerHTML='';
  items.slice(0,6).forEach(it=>{
    const card=document.createElement('article');
    card.className='card';
    card.innerHTML=`<a href="${it.link}" target="_blank" rel="noopener"><h2>${it.title}</h2></a>
      <div class="meta"><span>${it.source}</span><span>·</span>
      <span>${new URL(it.link).hostname.replace('www.','')}</span><span>·</span>
      <span>${formatTime(it.published)}</span><span>·</span><span>${it.category}</span></div>`;
    el.appendChild(card);
  });
}
(async function(){
  try{ const data = await loadNews(); renderLatest(data.items||[]); }catch(e){}
})();