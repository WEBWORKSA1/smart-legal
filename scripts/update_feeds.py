#!/usr/bin/env python3
"""Daily auto-refresh: legal news (Google News RSS) + latest legal-education videos (YouTube channel RSS).
Writes data/news.json and data/videos.json. Keeps previous data for any source that fails."""
import json, os, re, urllib.request, urllib.parse, datetime, email.utils
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UA = {"User-Agent": "Mozilla/5.0 (compatible; SmartLegalBot/1.0; +https://smart.legal)"}
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

NEWS_TOPICS = {
    "Courts & Supreme Court": '"Supreme Court" ruling',
    "Consumer Rights": "consumer protection law OR FTC lawsuit OR class action settlement",
    "Employment Law": "employment law OR labor law ruling OR wage lawsuit",
    "Housing & Tenants": "tenant rights OR eviction law OR rent control",
    "Immigration": "immigration law OR visa policy court",
    "Privacy & AI Law": "privacy law OR AI regulation OR data protection fine",
    "Personal Injury": "personal injury verdict OR settlement lawsuit injury",
    "Family Law": "family law OR child custody ruling OR divorce law",
    "Business & Contracts": "contract lawsuit OR corporate law OR antitrust ruling",
    "Criminal Justice": "criminal justice reform OR sentencing ruling OR police court",
}
CHANNELS = {
    "LegalEagle": "UCpa-Zb0ZcQjTCPP1Dx_1M8Q",
    "Law By Mike": "UCKmmERguliWTynG9OIoDhDw",
    "Law Talk With Mike": "UCYWtiAEcmR-Fb7fGF0hQfog",
    "Uncivil Law": "UCGmglDvqKzQmiCoyN61YGjw",
}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()

def load(name, default):
    try:
        with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save(name, obj):
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)

def news():
    old = load("news.json", {"topics": {}})
    topics = {}
    for name, q in NEWS_TOPICS.items():
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q + " when:7d", "hl": "en-US", "gl": "US", "ceid": "US:en"})
        try:
            root = ET.fromstring(fetch(url))
            items = []
            for it in root.iter("item"):
                title = (it.findtext("title") or "").strip()
                src_el = it.find("source")
                source = (src_el.text or "").strip() if src_el is not None else ""
                if source and title.endswith(" - " + source):
                    title = title[: -len(source) - 3]
                try:
                    date = email.utils.parsedate_to_datetime(it.findtext("pubDate")).isoformat()
                except Exception:
                    date = NOW
                link = (it.findtext("link") or "").strip()
                if title and link:
                    items.append({"title": title, "link": link, "source": source, "date": date})
                if len(items) >= 9:
                    break
            topics[name] = items or old.get("topics", {}).get(name, [])
            print(f"news  {name}: {len(items)}")
        except Exception as e:
            print(f"news  {name}: FAILED {e}")
            topics[name] = old.get("topics", {}).get(name, [])
    if any(topics.values()):
        save("news.json", {"updated": NOW, "topics": topics})

def videos():
    old = load("videos.json", {"videos": []})
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
    vids, ok = [], 0
    for name, cid in CHANNELS.items():
        try:
            root = ET.fromstring(fetch("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid))
            n = 0
            for e in root.findall("a:entry", ns):
                vid = e.findtext("yt:videoId", namespaces=ns)
                title = e.findtext("a:title", namespaces=ns) or ""
                if not vid or re.search(r"#shorts", title, re.I):
                    continue
                vids.append({"id": vid, "title": title, "channel": name, "published": e.findtext("a:published", namespaces=ns) or NOW})
                n += 1
                if n >= 8:
                    break
            ok += 1
            print(f"video {name}: {n}")
        except Exception as e:
            print(f"video {name}: FAILED {e}")
            vids += [v for v in old.get("videos", []) if v.get("channel") == name]
    vids.sort(key=lambda v: v["published"], reverse=True)
    if vids:
        save("videos.json", {"updated": NOW if ok else old.get("updated"), "videos": vids[:40],
                             "channels": [{"name": n, "id": c} for n, c in CHANNELS.items()]})

if __name__ == "__main__":
    news()
    videos()
