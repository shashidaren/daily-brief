async function loadNews() {
  const cacheBuster = Date.now();
  const res = await fetch(`news/news.json?cb=${cacheBuster}`);
  if (!res.ok) throw new Error('Failed to load news.json');
  const data = await res.json();
  return data;
}

function formatTime(iso) {
  const d = new Date(iso);
  return d.toLocaleString(undefined, { hour12: false });
}

function render(list) {
  const feed = document.getElementById('feed');
  feed.innerHTML = '';
  list.forEach(item => {
    const el = document.createElement('article');
    el.className = 'card';
    el.innerHTML = `
      <a href="${item.link}" target="_blank" rel="noopener noreferrer"><strong>${item.title}</strong></a>
      <div class="meta">
        <span>${item.source}</span>
        <span>·</span>
        <span>${new URL(item.link).hostname.replace('www.', '')}</span>
        <span>·</span>
        <span>${formatTime(item.published)}</span>
        <span>·</span>
        <span>${item.category}</span>
      </div>
      ${item.summary ? `<div class="summary">${item.summary}</div>` : ''}
    `;
    feed.appendChild(el);
  });
}

function applyFilters(items) {
  const q = document.getElementById('search').value.trim().toLowerCase();
  const cat = document.getElementById('category').value;
  return items.filter(i => {
    const matchCat = (cat === 'all') || (i.category === cat);
    const matchQ = !q || (i.title.toLowerCase().includes(q) || (i.summary||'').toLowerCase().includes(q) || i.source.toLowerCase().includes(q));
    return matchCat && matchQ;
  });
}

async function boot() {
  try {
    const data = await loadNews();
    const items = data.items || [];
    const updatedAt = document.getElementById('updatedAt');
    updatedAt.textContent = `Updated: ${formatTime(data.generatedAt)}`;

    const renderNow = () => render(applyFilters(items));
    document.getElementById('search').addEventListener('input', renderNow);
    document.getElementById('category').addEventListener('change', renderNow);
    document.getElementById('refresh').addEventListener('click', () => location.reload());

    renderNow();
  } catch (err) {
    document.getElementById('feed').innerHTML = `<div class="card">Failed to load news. ${err.message}</div>`;
  }
}

boot();
