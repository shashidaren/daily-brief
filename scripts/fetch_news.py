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
        "https://www.thestar.com.my/rss/news",
        "https://soyacincau.com/feed/"
    ],
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.reuters.com/world/rss",
        "https://rss.cnn.com/rss/edition_world.rss"
    ],
    "tech": [
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://www.gsmarena.com/rss-news.php3",
        "https://www.techmeme.com/feed.xml"
    ],
    "ai": [
        "https://ai.googleblog.com/atom.xml",
        "https://www.technologyreview.com/feed/ai/",
        "https://www.theverge.com/artificial-intelligence/rss/index.xml"
    ],
    "events": [
        "https://www.producthunt.com/feed",
        "https://www.meetup.com/topics/technology/rss/"
    ],
    "deals": [
        "https://www.theverge.com/deals/rss/index.xml",
        "https://9to5toys.com/feed/",
        "https://www.lowyat.net/feed/"
    ],
    "gadgets": [
        "https://www.gsmarena.com/rss-news.php3",
        "https://www.theverge.com/tech/rss/index.xml"
    ]
}

MAX_ITEMS_PER_FEED = 20
TOTAL_LIMIT = 180

def norm(s:str)->str: return (s or '').strip()

def make_id(link,title): return hashlib.sha1(((link or '')+'|'+(title or '')).encode('utf-8')).hexdigest()

def parse_feed(url, category):
    fp = feedparser.parse(url)
    out = []
    for e in fp.entries[:MAX_ITEMS_PER_FEED]:
        title = norm(getattr(e,'title','')); link = norm(getattr(e,'link','')); summary = norm(getattr(e,'summary',''))
        if getattr(e,'published_parsed',None):
            published = datetime(*e.published_parsed[:6], tzinfo=timezone.utc).isoformat()
        elif getattr(e,'updated_parsed',None):
            published = datetime(*e.updated_parsed[:6], tzinfo=timezone.utc).isoformat()
        else:
            published = datetime.now(timezone.utc).isoformat()
        source = fp.feed.get('title', urlparse(url).hostname or 'RSS')
        out.append({"id":make_id(link,title),"title":title,"link":link,"summary":summary,"published":published,"source":norm(source),"category":category})
    return out

def main():
    all_items=[]
    for cat, urls in FEEDS.items():
        for u in urls:
            try: all_items.extend(parse_feed(u, cat))
            except Exception as ex: print(f"[warn] failed {u}: {ex}")
    # dedupe
    uniq = {it["id"]: it for it in all_items}
    items = list(uniq.values())
    items.sort(key=lambda x: x["published"], reverse=True)
    items = items[:TOTAL_LIMIT]
    payload = {"generatedAt": datetime.now(timezone.utc).isoformat(), "counts":{"total":len(items)}, "items": items}
    import os; os.makedirs("news", exist_ok=True)
    with open("news/news.json","w",encoding="utf-8") as f: json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Wrote news/news.json with {len(items)} items")

if __name__ == "__main__":
    main()
