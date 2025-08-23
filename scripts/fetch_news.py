#!/usr/bin/env python3
import json, hashlib
from datetime import datetime, timezone
from urllib.parse import urlparse

import feedparser

FEEDS = {
    "malaysia": [
        "https://www.bharian.com.my/terkini/rss",
        "https://www.nst.com.my/rss",
        "https://www.malaymail.com/feed/rss",
        "https://www.bernama.com/en/rss.php",
    ],
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.reuters.com/world/rss",
        "https://rss.cnn.com/rss/edition_world.rss",
    ],
    "tech": [
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
    ],
}

MAX_ITEMS_PER_FEED = 15
TOTAL_LIMIT = 120

def norm_text(s: str) -> str:
    return (s or '').strip()

def item_id(link: str, title: str) -> str:
    raw = (link or '') + '|' + (title or '')
    return hashlib.sha1(raw.encode('utf-8')).hexdigest()

def parse_feed(url: str, category: str):
    fp = feedparser.parse(url)
    out = []
    for e in fp.entries[:MAX_ITEMS_PER_FEED]:
        title = norm_text(getattr(e, 'title', ''))
        link = norm_text(getattr(e, 'link', ''))
        summary = norm_text(getattr(e, 'summary', ''))
        if getattr(e, 'published_parsed', None):
            published = datetime(*e.published_parsed[:6], tzinfo=timezone.utc).isoformat()
        elif getattr(e, 'updated_parsed', None):
            published = datetime(*e.updated_parsed[:6], tzinfo=timezone.utc).isoformat()
        else:
            published = datetime.now(timezone.utc).isoformat()
        source = fp.feed.get('title', urlparse(url).hostname or 'RSS')
        out.append({
            'id': item_id(link, title),
            'title': title,
            'link': link,
            'summary': summary,
            'published': published,
            'source': norm_text(source),
            'category': category,
        })
    return out

def main():
    all_items = []
    for category, urls in FEEDS.items():
        for u in urls:
            try:
                all_items.extend(parse_feed(u, category))
            except Exception as ex:
                print(f'[warn] failed {u}: {ex}')
    # dedupe
    uniq = {}
    for it in all_items:
        uniq.setdefault(it['id'], it)
    items = list(uniq.values())
    # sort + trim
    items.sort(key=lambda x: x['published'], reverse=True)
    items = items[:TOTAL_LIMIT]
    payload = {
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'counts': {'total': len(items)},
        'items': items,
    }
    with open('news/news.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f'Wrote news/news.json with {len(items)} items')

if __name__ == '__main__':
    main()
