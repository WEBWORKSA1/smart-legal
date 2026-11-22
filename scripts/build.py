#!/usr/bin/env python3
"""Render every Smart.Legal page from one layout. Run from repo root: python3 scripts/build.py"""
import json, os, sys, datetime, html
sys.path.insert(0, os.path.dirname(__file__))
from layout import page, hero, breadcrumb, lead_widget, esc, SITE, NAME, TAGLINE
from content_guides import GUIDES
from content_glossary import TERMS
from content_pages import LEGAL_AID, PRACTICE_AREAS, REGIONS, privacy_body, terms_body, disclaimer_body, trademark_body

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TODAY = datetime.date.today().isoformat()
written = []

def out(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    written.append(path)

def load(name, default):
    try:
        with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

NEWS = load("news.json", {"updated": None, "topics": {}})
VIDEOS = load("videos.json", {"updated": None, "videos": [], "channels": []})

def fmt_date(s):
    try:
        return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).strftime("%b %d, %Y")
    except Exception:
        return ""

def news_cards(items, limit=None):
    items = items[:limit] if limit else items
    if not items:
        return '<p class="muted">Headlines refresh automatically every day. Check back shortly.</p>'
    return '<div class="news-grid">' + "".join(
        f'<article class="news-card"><span class="tag">{esc(n.get("topic",""))}</span>'
        f'<h3><a href="{esc(n["link"])}" target="_blank" rel="noopener nofollow">{esc(n["title"])}</a></h3>'
        f'<p class="meta">{esc(n.get("source",""))} &middot; {fmt_date(n.get("date",""))}</p></article>' for n in items) + "</div>"

def all_news():
    seen, items = set(), []
    for topic, lst in NEWS.get("topics", {}).items():
        for n in lst:
            if n["link"] in seen: continue
            seen.add(n["link"]); n = dict(n); n["topic"] = topic; items.append(n)
    items.sort(key=lambda n: n.get("date", ""), reverse=True)
    return items

def video_cards(vids, limit=None):
    vids = vids[:limit] if limit else vids
    return '<div class="video-grid">' + "".join(
        f'<figure class="yt" data-id="{esc(v["id"])}"><button class="yt-play" aria-label="Play: {esc(v["title"])}">'
        f'<img loading="lazy" src="https://i.ytimg.com/vi/{esc(v["id"])}/hqdefault.jpg" alt="" width="480" height="360"><span class="play">&#9658;</span></button>'
        f'<figcaption>{esc(v["title"])}<small>{esc(v.get("channel",""))} &middot; {fmt_date(v.get("published",""))}</small></figcaption></figure>'
        for v in vids) + "</div>"

FALLBACK_CHANNELS = [
    ("LegalEagle", "UCpa-Zb0ZcQjTCPP1Dx_1M8Q"), ("Law By Mike", "UCKmmERguliWTynG9OIoDhDw"),
    ("Law Talk With Mike", "UCYWtiAEcmR-Fb7fGF0hQfog"), ("Uncivil Law", "UCGmglDvqKzQmiCoyN61YGjw")]

def playlist_cards():
    return '<div class="video-grid">' + "".join(
        f'<figure class="yt yt-list" data-list="UU{cid[2:]}"><button class="yt-play" aria-label="Play latest from {esc(n)}">'
        f'<span class="yt-ph">&#9878;<b>{esc(n)}</b><small>Latest uploads playlist</small></span><span class="play">&#9658;</span></button>'
        f'<figcaption>{esc(n)} — latest legal explainers</figcaption></figure>' for n, cid in FALLBACK_CHANNELS) + "</div>"

def videos_for(keywords, limit=3):
    vids = [v for v in VIDEOS.get("videos", []) if any(k in v["title"].lower() for k in keywords)]
    return vids[:limit]

# ---------------------------------------------------------------- HOME
def build_home():
    topics = "".join(
        f'<a class="topic" href="guides/{g["slug"]}.html"><span class="ti">{g["icon"]}</span><h3>{esc(g["title"])}</h3><p>{esc(g["summary"])}</p></a>'
        for g in GUIDES)
    chips = "".join(f'<a class="chip" href="navigator.html?area={esc(g["area"])}">{g["icon"]} {esc(g["area"])}</a>' for g in GUIDES[:8])
    vids = VIDEOS.get("videos", [])
    vid_html = video_cards(vids, 3) if vids else playlist_cards()
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="kicker">Free legal information &middot; Smart tools &middot; Real attorneys</p>
      <h1>Legal problems, <span class="hl">solved smarter.</span></h1>
      <p class="lead">Understand your rights in plain English, generate letters and agreements in minutes, run the numbers with free calculators — and when you need a professional, get a free case review from an independent attorney.</p>
      <form class="hero-search" action="guides.html" onsubmit="event.preventDefault();window.SL&&SL.openSearch(this.q.value)">
        <label for="heroQ" class="sr">Search</label>
        <input id="heroQ" name="q" type="search" placeholder="e.g. landlord won't return deposit">
        <button class="btn btn-gold" type="submit">Search</button>
      </form>
      <div class="chips">{chips}</div>
      <div class="hero-ctas"><a class="btn btn-gold lg" href="free-case-review.html">Get a free case review</a><a class="btn btn-ghost lg" href="navigator.html">Find my next step &rarr;</a></div>
    </div>
    <div class="hero-card">
      <div class="tip"><p class="kicker">&#128161; Legal tip of the day</p><p id="tipOfDay">Put important agreements in writing — a dated email confirming what was agreed is better than nothing.</p></div>
      <ul class="trust">
        <li><b>12</b> practice-area guides</li><li><b>12</b> document generators</li>
        <li><b>6</b> legal calculators</li><li><b>{len(TERMS)}+</b> legal terms explained</li>
        <li><b>Daily</b> legal news refresh</li><li><b>100%</b> free to use</li>
      </ul>
    </div>
  </div>
</section>

<section class="section"><div class="wrap">
  <div class="sec-head"><h2>What do you need help with?</h2><a href="guides.html">All guides &rarr;</a></div>
  <div class="topic-grid">{topics}</div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="sec-head"><h2>Smart legal tools</h2><p>Free, private, and they run right in your browser — nothing you type in a tool leaves your device unless you submit a form.</p></div>
  <div class="tool-grid">
    <a class="tool" href="navigator.html"><span>&#129517;</span><h3>Legal Issue Navigator</h3><p>Answer 4 questions and get a personalised action plan.</p></a>
    <a class="tool" href="documents.html"><span>&#128221;</span><h3>Document Generator</h3><p>Demand letters, NDAs, notices and more with live preview.</p></a>
    <a class="tool" href="calculators.html"><span>&#129518;</span><h3>Legal Calculators</h3><p>Settlement estimates, deadlines, interest, fees and rent.</p></a>
    <a class="tool" href="dictionary.html"><span>&#128214;</span><h3>Legal Dictionary</h3><p>{len(TERMS)}+ legal terms in plain English.</p></a>
    <a class="tool" href="quiz.html"><span>&#127942;</span><h3>Know-Your-Rights Quiz</h3><p>Test yourself and enter the monthly challenge.</p></a>
    <a class="tool" href="legal-aid.html"><span>&#129309;</span><h3>Free Legal Aid Finder</h3><p>Official free and low-cost help by country.</p></a>
  </div>
</div></section>

<section class="section"><div class="wrap lead-split">
  <div>
    <p class="kicker">Free case review</p>
    <h2>Talk to someone who can actually help.</h2>
    <p>Legal problems get more expensive the longer they wait. Tell us what happened and we will route your request to independent attorneys who handle your type of case in your area.</p>
    <ul class="ticks"><li>Free and no obligation</li><li>Takes about 60 seconds</li><li>Injury, family, employment, housing, immigration, criminal, business and more</li><li>Many injury and employment lawyers work on contingency — no fee unless you win</li></ul>
    <p class="tiny">Smart.Legal is not a law firm. Submitting does not create an attorney-client relationship.</p>
  </div>
  {lead_widget()}
</div></section>

<section class="section alt"><div class="wrap">
  <div class="sec-head"><h2>Latest legal news</h2><a href="news.html">All news &rarr;</a></div>
  {news_cards(all_news(), 6)}
</div></section>

<section class="section"><div class="wrap">
  <div class="sec-head"><h2>Watch &amp; learn</h2><a href="videos.html">Video library &rarr;</a></div>
  {vid_html}
</div></section>

<section class="section alt"><div class="wrap">
  <h2 class="center">How Smart.Legal works</h2>
  <div class="steps3">
    <div><b>1</b><h3>Understand</h3><p>Read a plain-language guide or let the Navigator map your situation.</p></div>
    <div><b>2</b><h3>Act</h3><p>Generate the letter, notice or agreement you need and calculate what is at stake.</p></div>
    <div><b>3</b><h3>Escalate</h3><p>When it matters, request a free case review with an independent attorney.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap community">
  <a class="com" href="support.html"><h3>&#10084;&#65039; Support free legal help</h3><p>Donations keep every tool free. Sponsor a guide or a tool.</p></a>
  <a class="com" href="contests.html"><h3>&#127941; Contests &amp; prizes</h3><p>Know-Your-Rights Challenge, essay award and legal-tech idea sprint.</p></a>
  <a class="com" href="careers.html"><h3>&#128188; Work with us</h3><p>Legal writers, reviewers, developers and marketers.</p></a>
  <a class="com" href="for-lawyers.html"><h3>&#9878;&#65039; For lawyers</h3><p>Receive exclusive case inquiries and sponsor practice-area guides.</p></a>
</div></section>
"""
    faq = [("Is Smart.Legal free?", "Yes. Guides, tools, calculators, the dictionary and case-review requests are free for visitors."),
           ("Is Smart.Legal a law firm?", "No. Smart.Legal provides legal information and connects visitors with independent attorneys. It does not give legal advice."),
           ("Who will contact me after a case review?", "Independent attorneys or legal-service partners who handle your type of matter in your area may contact you. You are never obliged to hire anyone."),
           ("Which countries do you cover?", "Guides are written to be useful everywhere, with notes for the US, Canada, UK, India and Australia. The legal-aid finder lists official resources by country.")]
    body += '<section class="section alt"><div class="wrap narrow"><h2 class="center">Frequently asked questions</h2>' + "".join(
        f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq) + "</div></section>"
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE,
               "potentialAction": {"@type": "SearchAction", "target": SITE + "/guides.html?q={search_term_string}", "query-input": "required name=search_term_string"}},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                  {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    out("index.html", page("index.html", f"{NAME} — Free Legal Help, Smart Tools & Free Case Review",
        "Plain-language legal guides, free document generators, legal calculators, live legal news and a free case review with independent attorneys.", body, schema=schema))

# ---------------------------------------------------------------- GUIDES
def build_guides():
    cards = "".join(
        f'<a class="topic" href="guides/{g["slug"]}.html"><span class="ti">{g["icon"]}</span><h3>{esc(g["title"])}</h3><p>{esc(g["summary"])}</p><span class="more">Read guide &rarr;</span></a>' for g in GUIDES)
    body = hero("Legal guides", "Plain-language legal guides", "Twelve in-depth guides covering the problems people search for most — your rights, a step-by-step plan, what documents to gather, what it costs and when to call a lawyer.") + \
        f'<section class="section"><div class="wrap"><div class="topic-grid">{cards}</div></div></section>'
    out("guides.html", page("guides.html", "Legal Guides — Know Your Rights in Plain English",
        "Free plain-English legal guides: personal injury, divorce, employment, landlord-tenant, immigration, criminal defence, business, wills, consumer, traffic, IP and privacy.", body, active="guides.html"))
    for g in GUIDES:
        pre = "../"
        rights = "".join(f"<li>{esc(r)}</li>" for r in g["rights"])
        steps = "".join(f"<li><strong>{esc(t)}.</strong> {esc(d)}</li>" for t, d in g["steps"])
        docs = "".join(f"<li>{esc(d)}</li>" for d in g["docs"])
        faq = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in g["faq"])
        tools = "".join(f'<a class="chip" href="{pre}{u}">{esc(t)}</a>' for t, u in g["tools"])
        others = "".join(f'<li><a href="{o["slug"]}.html">{o["icon"]} {esc(o["title"])}</a></li>' for o in GUIDES if o is not g)
        vids = videos_for(g["video_kw"])
        vhtml = video_cards(vids) if vids else '<div class="yt-dyn" data-kw="' + esc(",".join(g["video_kw"])) + '"></div>'
        body = breadcrumb([("Guides", "guides.html"), (g["title"], None)], pre) + f"""
<section class="page-hero slim"><div class="wrap"><p class="kicker">{g["icon"]} Legal guide &middot; Updated {datetime.date.today().strftime("%B %Y")}</p><h1>{esc(g["title"])}</h1><p class="lead">{esc(g["summary"])}</p></div></section>
<div class="wrap article-grid">
<article class="prose">
  <p class="intro">{esc(g["intro"])}</p>
  <nav class="toc"><b>On this page</b><a href="#rights">Your rights</a><a href="#steps">Step-by-step</a><a href="#docs">Documents</a><a href="#costs">Costs</a><a href="#lawyer">When to call a lawyer</a><a href="#faq">FAQ</a></nav>
  <h2 id="rights">Your key rights</h2><ul class="ticks">{rights}</ul>
  <h2 id="steps">Step-by-step plan</h2><ol class="steps">{steps}</ol>
  <div class="inline-cta"><p><b>Not sure where you stand?</b> Get a free, no-obligation case review from an independent attorney who handles {esc(g["area"].lower())} matters.</p><a class="btn btn-gold" href="{pre}free-case-review.html?area={esc(g["area"])}">Free case review</a></div>
  <h2 id="docs">Documents to gather</h2><ul class="cols2">{docs}</ul>
  <h2 id="costs">What it may cost</h2><p>{esc(g["costs"])}</p>
  <h2 id="lawyer">When to talk to a lawyer</h2><p>{esc(g["lawyer"])}</p>
  <h2>Helpful tools</h2><div class="chips">{tools}</div>
  <h2>Videos</h2>{vhtml}
  <h2 id="faq">Frequently asked questions</h2>{faq}
  <p class="note">This guide is general legal information, not legal advice. Laws differ by country, state and province and change over time. For advice on your situation, consult a licensed lawyer.</p>
</article>
<aside class="sidebar">{lead_widget(g["area"], pre)}<div class="side-box"><h3>Other guides</h3><ul class="side-links">{others}</ul></div></aside>
</div>"""
        schema = [{"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["summary"],
                   "dateModified": TODAY, "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME}},
                  {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                      {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]}]
        out(f"guides/{g['slug']}.html", page(f"guides/{g['slug']}.html", f"{g['title']}: Your Rights & Next Steps", g["summary"], body,
            depth=1, schema=schema, active="guides.html", og_type="article"))

# ---------------------------------------------------------------- TOOLS
def build_navigator():
    body = hero("Legal Issue Navigator", "Find your smart next step", "Answer four quick questions. You will get a personalised action plan, the right guide and tools, and a pre-filled free case review.") + """
<section class="section"><div class="wrap narrow">
  <div class="wizard" id="navigator" aria-live="polite"></div>
  <noscript><p>The Navigator needs JavaScript. You can browse all <a href="guides.html">legal guides</a> instead.</p></noscript>
  <p class="note">The Navigator runs entirely in your browser and gives general information only — not legal advice.</p>
</div></section>"""
    out("navigator.html", page("navigator.html", "Legal Issue Navigator — Get a Personalised Action Plan",
        "Answer four questions about your legal problem and get a free, personalised action plan, guide, tools and case review.", body, active="navigator.html"))

DOC_LIST = [("demand", "Demand letter for money owed"), ("cease", "Cease & desist letter"), ("nda", "Mutual non-disclosure agreement"),
            ("service", "Freelance / service agreement"), ("lease", "Residential lease summary"), ("deposit", "Security-deposit return demand"),
            ("sale", "Bill of sale"), ("note", "Promissory note"), ("poa", "Power-of-attorney worksheet"), ("refund", "Refund / chargeback request"),
            ("data", "Data access request (GDPR / CCPA)"), ("reference", "Employment verification / reference request")]

def build_documents():
    lst = "".join(f'<button class="doc-btn" data-doc="{k}" id="{k}">{esc(t)}</button>' for k, t in DOC_LIST)
    body = hero("Document generator", "Free legal letters & agreements", "Pick a template, fill in the blanks and watch your document build itself. Copy it, download it or print it to PDF — free, and nothing leaves your browser.") + f"""
<section class="section"><div class="wrap doc-layout">
  <div class="doc-list" role="tablist" aria-label="Templates">{lst}</div>
  <div class="doc-work">
    <form id="docForm" class="doc-form" autocomplete="off"></form>
    <div class="doc-preview-wrap">
      <div class="doc-actions"><button class="btn btn-ghost sm" id="docCopy">Copy</button><button class="btn btn-ghost sm" id="docTxt">Download .txt</button><button class="btn btn-ghost sm" id="docDoc">Download .doc</button><button class="btn btn-gold sm" id="docPrint">Print / PDF</button></div>
      <pre id="docPreview" class="doc-preview" aria-live="polite"></pre>
    </div>
  </div>
</div>
<div class="wrap narrow"><p class="note">Templates are general starting points, not legal advice, and may not meet the formal requirements of your jurisdiction. Have important documents reviewed by a lawyer. Want a professional to draft it? <a href="free-case-review.html">Request a free case review</a>.</p></div></section>
<section class="section alt"><div class="wrap narrow prose"><h2>How to use these templates well</h2>
<p>A good legal letter is specific, calm and dated. State the facts in order, cite the agreement or rule you are relying on, say exactly what you want and give a reasonable deadline. Keep a copy and send it in a way you can prove — email with a read receipt, tracked post or a courier.</p>
<p>For agreements, both parties should read every clause, fill in all blanks and sign and date each copy. If a contract involves significant money, property, employees or intellectual property, a short review by a lawyer is inexpensive insurance.</p></div></section>"""
    out("documents.html", page("documents.html", "Free Legal Document Generator — Letters, NDAs & Agreements",
        "Create demand letters, cease and desist letters, NDAs, service agreements, bills of sale, promissory notes, data-access requests and more for free.", body, active="documents.html"))

def build_calculators():
    body = hero("Legal calculators", "Run the numbers before you decide", "Six free calculators for the questions people ask lawyers every day. Estimates only — use them to prepare, not to replace advice.") + """
<section class="section"><div class="wrap calc-grid">
<form class="calc" id="settlement" data-calc="settlement"><h2>Injury settlement estimator</h2><p class="muted">Uses the common "multiplier" method insurers start from.</p>
 <label>Medical bills (past &amp; future)<input type="number" name="med" min="0" value="12000"></label>
 <label>Lost wages<input type="number" name="wages" min="0" value="4000"></label>
 <label>Property damage<input type="number" name="prop" min="0" value="3000"></label>
 <label>Injury severity<select name="mult"><option value="1.5">Minor (soft tissue, quick recovery)</option><option value="2.5" selected>Moderate (weeks of treatment)</option><option value="3.5">Serious (fractures, surgery)</option><option value="5">Severe / permanent</option></select></label>
 <label>Your share of fault (%)<input type="number" name="fault" min="0" max="100" value="0"></label>
 <label>Lawyer contingency fee (%)<input type="number" name="fee" min="0" max="50" value="33"></label>
 <div class="result" aria-live="polite"></div></form>

<form class="calc" id="fees" data-calc="fees"><h2>Contingency vs. hourly fee</h2><p class="muted">Compare what you would pay under each fee model.</p>
 <label>Expected recovery<input type="number" name="rec" min="0" value="60000"></label>
 <label>Contingency %<input type="number" name="pct" min="0" max="50" value="33"></label>
 <label>Hourly rate<input type="number" name="rate" min="0" value="300"></label>
 <label>Estimated hours<input type="number" name="hours" min="0" value="60"></label>
 <label>Case costs (filing, experts)<input type="number" name="costs" min="0" value="2500"></label>
 <div class="result" aria-live="polite"></div></form>

<form class="calc" id="deadline" data-calc="deadline"><h2>Deadline &amp; day counter</h2><p class="muted">Add days to a date, or count days between two dates.</p>
 <label>Start date<input type="date" name="start"></label>
 <label>Add this many days<input type="number" name="days" min="0" value="30"></label>
 <label>Count<select name="mode"><option value="cal">Calendar days</option><option value="bus">Business days (Mon–Fri)</option></select></label>
 <label>…or count days until<input type="date" name="end"></label>
 <div class="result" aria-live="polite"></div></form>

<form class="calc" id="interest" data-calc="interest"><h2>Unpaid debt / wages interest</h2><p class="muted">Simple or compound interest on money owed.</p>
 <label>Amount owed<input type="number" name="amt" min="0" value="5000"></label>
 <label>Annual interest rate (%)<input type="number" name="rate" min="0" step="0.01" value="5"></label>
 <label>Due date<input type="date" name="from"></label>
 <label>Calculate to<input type="date" name="to"></label>
 <label>Method<select name="method"><option value="simple">Simple</option><option value="compound">Compounded monthly</option></select></label>
 <div class="result" aria-live="polite"></div></form>

<form class="calc" id="smallclaims" data-calc="smallclaims"><h2>Small-claims: is it worth it?</h2><p class="muted">Weigh what you could recover against costs and time.</p>
 <label>Amount you are claiming<input type="number" name="claim" min="0" value="3000"></label>
 <label>Chance of winning (%)<input type="number" name="chance" min="0" max="100" value="70"></label>
 <label>Chance of actually collecting (%)<input type="number" name="collect" min="0" max="100" value="75"></label>
 <label>Filing &amp; service fees<input type="number" name="fees" min="0" value="150"></label>
 <label>Hours you will spend<input type="number" name="hours" min="0" value="12"></label>
 <label>Value of your hour<input type="number" name="hourval" min="0" value="30"></label>
 <div class="result" aria-live="polite"></div></form>

<form class="calc" id="rent" data-calc="rent"><h2>Rent-increase checker</h2><p class="muted">See the increase as a percentage and compare it with a cap.</p>
 <label>Current monthly rent<input type="number" name="old" min="0" value="1800"></label>
 <label>Proposed monthly rent<input type="number" name="new" min="0" value="1950"></label>
 <label>Local cap / guideline (%) — optional<input type="number" name="cap" min="0" step="0.1" value="2.5"></label>
 <div class="result" aria-live="polite"></div></form>
</div>
<div class="wrap narrow"><p class="note">Calculators provide rough estimates using simplified assumptions and are not legal, tax or financial advice. Real outcomes depend on facts, evidence, insurance limits, local law and negotiation. <a href="free-case-review.html">Get a free case review</a> for an assessment of your situation.</p></div></section>"""
    out("calculators.html", page("calculators.html", "Free Legal Calculators — Settlement, Fees, Deadlines & Interest",
        "Free injury settlement estimator, contingency fee calculator, legal deadline counter, debt interest calculator, small-claims and rent-increase checkers.", body, active="calculators.html"))

def build_dictionary():
    letters = sorted({t[0][0].upper() for t in TERMS})
    jump = "".join(f'<a href="#l-{l}">{l}</a>' for l in letters)
    groups = ""
    for l in letters:
        items = "".join(f'<div class="term" id="t-{esc(t.lower().replace(" ", "-").replace("(", "").replace(")", ""))}"><dt>{esc(t)}</dt><dd>{esc(d)}</dd></div>' for t, d in TERMS if t[0].upper() == l)
        groups += f'<section class="letter" id="l-{l}"><h2>{l}</h2><dl>{items}</dl></section>'
    body = hero("Legal dictionary", f"{len(TERMS)}+ legal terms in plain English", "Every definition is written to be understood on the first read. Search instantly or jump by letter.",
                '<input id="dictSearch" class="big-search" type="search" placeholder="Search terms, e.g. probate, tort, subpoena…" aria-label="Search the dictionary">') + \
        f'<div class="wrap"><nav class="az" aria-label="Jump to letter">{jump}</nav><div id="dict">{groups}</div><p id="dictEmpty" class="muted" hidden>No matching terms. Try another word or <a href="ask.html">ask a legal question</a>.</p></div>'
    schema = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Smart.Legal Legal Dictionary",
              "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in TERMS]}
    out("dictionary.html", page("dictionary.html", "Legal Dictionary — Plain-English Legal Terms A–Z",
        "Free plain-English legal dictionary with 120+ legal terms explained: affidavit, probate, tort, subpoena, negligence, injunction and more.", body, schema=schema, active="dictionary.html"))

def build_quiz():
    body = hero("Know-Your-Rights Quiz", "How well do you know your rights?", "Ten questions on everyday law. Get instant explanations — and enter this month's Know-Your-Rights Challenge with your score.") + """
<section class="section"><div class="wrap narrow"><div class="quiz" id="quiz" aria-live="polite"></div>
<p class="note">Questions describe common general principles. The law in your jurisdiction may differ.</p></div></section>"""
    out("quiz.html", page("quiz.html", "Know-Your-Rights Quiz — Test Your Legal Knowledge",
        "Take the free Know-Your-Rights quiz: 10 questions on tenants, workers, consumers and police encounters with instant explanations.", body))

# ---------------------------------------------------------------- NEWS & VIDEOS
NEWS_BLURB = {
    "Courts & Supreme Court": "Major rulings shape everyday rights — from speech to search and seizure.",
    "Consumer Rights": "Recalls, refunds, scams and enforcement actions that affect what you buy.",
    "Employment Law": "Wage rules, workplace discrimination, remote work and non-compete changes.",
    "Housing & Tenants": "Rent rules, eviction trends and tenant-protection laws.",
    "Immigration": "Visa policy, processing times and court decisions on immigration.",
    "Privacy & AI Law": "Data protection, AI regulation and online-safety rules.",
    "Personal Injury": "Verdicts, settlements and safety cases that set expectations.",
    "Family Law": "Divorce, custody and child-support developments.",
    "Business & Contracts": "Corporate, contract and small-business legal changes.",
    "Criminal Justice": "Policing, sentencing and criminal-procedure developments.",
}

def build_news():
    topics = NEWS.get("topics", {})
    tabs = '<button class="tab active" data-topic="all">All</button>' + "".join(f'<button class="tab" data-topic="{esc(t)}">{esc(t)}</button>' for t in topics)
    sections = ""
    for t, lst in topics.items():
        items = [dict(n, topic=t) for n in lst]
        sections += f'<section class="news-topic" data-topic="{esc(t)}"><h2>{esc(t)}</h2><p class="muted">{esc(NEWS_BLURB.get(t, ""))}</p>{news_cards(items, 9)}</section>'
    if not sections:
        sections = news_cards([])
    upd = fmt_date(NEWS.get("updated") or "") or "daily"
    body = hero("Legal news", "Today's legal news, in one place", f"Headlines from trusted publishers across ten areas of law, refreshed automatically every day. Last refresh: <b>{upd}</b>.") + \
        f'<section class="section"><div class="wrap"><div class="tabs" role="tablist">{tabs}</div>{sections}<p class="note">Headlines link to the original publishers; Smart.Legal does not endorse third-party content. Need to know what a development means for you? <a href="ask.html">Ask a legal question</a>.</p></div></section>'
    out("news.html", page("news.html", "Legal News Today — Courts, Consumer, Employment, Housing & More",
        "Daily legal news headlines across courts, consumer rights, employment, housing, immigration, privacy and AI, personal injury, family, business and criminal justice.", body, active="news.html"))

def build_videos():
    vids = VIDEOS.get("videos", [])
    upd = fmt_date(VIDEOS.get("updated") or "") or "daily"
    grid = video_cards(vids, 24) if vids else ""
    body = hero("Video library", "Learn the law by watching", f"The latest explainers from respected legal-education channels, refreshed automatically. Last refresh: <b>{upd}</b>.") + \
        f'<section class="section"><div class="wrap">{grid}<h2>Channel playlists</h2>{playlist_cards()}<p class="note">Videos are embedded from YouTube and remain the property of their creators. They are educational, not legal advice for your situation.</p></div></section>'
    out("videos.html", page("videos.html", "Legal Video Library — Know Your Rights Explainers",
        "Watch the latest know-your-rights and legal explainer videos from leading legal-education YouTube channels, refreshed daily.", body, active="videos.html"))

def build_legal_aid():
    blocks = ""
    for region, items in LEGAL_AID.items():
        lis = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(n)}</a><span>{esc(d)}</span></li>' for n, u, d in items)
        blocks += f'<section class="aid"><h2>{esc(region)}</h2><ul class="aid-list">{lis}</ul></section>'
    body = hero("Free legal help", "Free & low-cost legal aid finder", "Official and non-profit sources of free legal help, organised by country. If you qualify, these services can represent or advise you at little or no cost.") + \
        f'<section class="section"><div class="wrap aid-grid">{blocks}</div><div class="wrap narrow"><p class="note">Links go to independent organisations. Smart.Legal is not affiliated with them. Don\'t qualify for legal aid? <a href="free-case-review.html">Request a free case review</a>.</p></div></section>'
    out("legal-aid.html", page("legal-aid.html", "Free Legal Aid Finder — US, Canada, UK, India, Australia",
        "Find free and low-cost legal aid: official legal-aid bodies, pro bono clinics and self-help centres in the US, Canada, UK, India, Australia and worldwide.", body, active="legal-aid.html"))

# ---------------------------------------------------------------- LEAD & FORMS
def options(lst, placeholder="Select…"):
    return f'<option value="">{placeholder}</option>' + "".join(f"<option>{esc(x)}</option>" for x in lst)

def build_case_review():
    body = hero("Free case review", "Get a free case review in 60 seconds", "Tell us what happened. Independent attorneys who handle your type of case in your area may contact you — free and with no obligation.") + f"""
<section class="section"><div class="wrap lead-page">
<form class="msf" data-form="LEAD: Free Case Review" novalidate>
  <div class="progress"><span style="width:20%"></span></div>
  <p class="step-label">Step <b class="cur">1</b> of 5</p>
  <fieldset class="step active"><legend>What type of legal issue is it?</legend>
    <div class="opt-grid">{"".join(f'<label class="opt"><input type="radio" name="legal_area" value="{esc(a)}" required><span>{esc(a)}</span></label>' for a in PRACTICE_AREAS)}</div>
  </fieldset>
  <fieldset class="step"><legend>Tell us what happened</legend>
    <label>Briefly describe your situation<textarea name="details" rows="5" required placeholder="What happened, when, and who is involved?"></textarea></label>
    <label>When did it happen?<select name="when" required>{options(["Within the last week", "Within the last month", "1–6 months ago", "6–12 months ago", "1–2 years ago", "More than 2 years ago", "It is ongoing"])}</select></label>
    <label>Have you already hired a lawyer for this?<select name="has_lawyer" required>{options(["No", "Yes, but I want a second opinion", "Yes, I want to change lawyers"])}</select></label>
  </fieldset>
  <fieldset class="step"><legend>How urgent is it?</legend>
    <label>Urgency<select name="urgency" required>{options(["Emergency — court date or deadline within 7 days", "Urgent — within 30 days", "Soon — within 3 months", "Just exploring my options"])}</select></label>
    <label>Is there a court date or deadline? (optional)<input type="date" name="deadline"></label>
    <label>Preferred contact<select name="contact_pref">{options(["Phone", "Email", "Text message", "Any"], "No preference")}</select></label>
    <label>Fee arrangement you are open to<select name="fee_pref">{options(["Contingency (no win, no fee)", "Fixed fee", "Hourly", "Free / legal aid only", "Not sure"])}</select></label>
  </fieldset>
  <fieldset class="step"><legend>Where are you located?</legend>
    <label>Country / region<select name="region" required>{options(REGIONS)}</select></label>
    <label>State / province<input name="state" required placeholder="e.g. California, Ontario, Maharashtra"></label>
    <label>City and ZIP / postal code<input name="city" required></label>
  </fieldset>
  <fieldset class="step"><legend>Where should we send your free review?</legend>
    <div class="two"><label>First name<input name="first_name" required autocomplete="given-name"></label><label>Last name<input name="last_name" required autocomplete="family-name"></label></div>
    <label>Email<input type="email" name="email" required autocomplete="email"></label>
    <label>Phone<input type="tel" name="phone" required autocomplete="tel"></label>
    <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree that Smart.Legal and independent attorneys or legal-service partners may contact me by phone, email or text about my request. Consent is not a condition of any purchase. I understand Smart.Legal is not a law firm and no attorney-client relationship is created.</label>
    <label class="check"><input type="checkbox" name="newsletter" value="yes"> Send me occasional legal tips (optional).</label>
  </fieldset>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <div class="msf-nav"><button type="button" class="btn btn-ghost" data-prev hidden>&larr; Back</button><button type="button" class="btn btn-gold" data-next>Continue &rarr;</button><button type="submit" class="btn btn-gold" hidden>Get my free case review</button></div>
  <p class="form-msg" aria-live="polite"></p>
</form>
<aside class="lead-aside">
  <h3>Why request a review?</h3>
  <ul class="ticks"><li>Free and no obligation</li><li>Your information is shared only to respond to your request</li><li>Many attorneys offer free first consultations</li><li>Deadlines (limitation periods) can end your claim — acting early protects your options</li></ul>
  <div class="side-box"><h4>What happens next?</h4><ol><li>We review your request.</li><li>We route it to independent attorneys or legal-aid resources that handle your issue and location.</li><li>You decide whether to speak with them.</li></ol></div>
  <p class="tiny">Smart.Legal is not a law firm or lawyer referral service and does not endorse any attorney. Attorneys may pay to advertise or to receive inquiries. In an emergency, contact local emergency services.</p>
</aside>
</div></section>"""
    out("free-case-review.html", page("free-case-review.html", "Free Case Review — Connect With an Independent Attorney",
        "Request a free, no-obligation case review. Injury, divorce, employment, housing, immigration, criminal, business and more.", body))

def build_ask():
    body = hero("Ask a legal question", "Ask a legal question — free", "Send us your question. We use real questions to write new guides and FAQs, and if your matter needs a lawyer we can route it for a free case review.") + f"""
<section class="section"><div class="wrap lead-split">
<form class="card-form" data-form="Ask a Legal Question" novalidate>
  <label>Topic<select name="topic" required>{options(PRACTICE_AREAS)}</select></label>
  <label>Your question<textarea name="question" rows="6" required placeholder="Do not include confidential details you would not want published anonymously."></textarea></label>
  <label>Country / region<select name="region" required>{options(REGIONS)}</select></label>
  <label>State / province<input name="state"></label>
  <label>Name (optional)<input name="name"></label>
  <label>Email<input type="email" name="email" required></label>
  <label class="check"><input type="checkbox" name="route_to_attorney" value="yes"> I would also like a free case review from an independent attorney.</label>
  <label class="check"><input type="checkbox" name="consent" value="yes" required> I understand answers are general information, my question may be used anonymously to create content, and no attorney-client relationship is created.</label>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <button class="btn btn-gold" type="submit">Send my question</button><p class="form-msg" aria-live="polite"></p>
</form>
<div class="prose"><h2>Before you ask</h2><p>Many questions are already answered in our <a href="guides.html">legal guides</a> and <a href="dictionary.html">dictionary</a>. For time-sensitive matters — a court date, an eviction notice, an arrest — do not wait for a published answer: use the <a href="free-case-review.html">free case review</a> or contact <a href="legal-aid.html">legal aid</a> now.</p>
<h3>Good questions include</h3><ul class="ticks"><li>Your country and state or province</li><li>A short timeline of what happened</li><li>What outcome you want</li><li>Any deadline you have been given</li></ul></div>
</div></section>"""
    out("ask.html", page("ask.html", "Ask a Legal Question — Free", "Ask a free legal question about injury, family, employment, housing, immigration, criminal, business or consumer law.", body))

def build_for_lawyers():
    body = hero("For lawyers &amp; advertisers", "Grow your practice with high-intent clients", "Smart.Legal visitors arrive with a specific problem and an intent to act. Receive exclusive case inquiries in your practice area and location, or sponsor the guides and tools your future clients already use.") + f"""
<section class="section"><div class="wrap">
<div class="pkg-grid">
  <div class="pkg"><h3>Exclusive case inquiries</h3><p class="price">Pay per qualified inquiry</p><ul class="ticks"><li>Filtered by practice area, location and urgency</li><li>Delivered in real time by email</li><li>Never shared with competing firms (exclusive tier)</li></ul></div>
  <div class="pkg featured"><h3>Practice-area sponsor</h3><p class="price">Monthly placement</p><ul class="ticks"><li>Featured on a guide (e.g. Personal Injury) in your region</li><li>Branded lead widget and profile card</li><li>Monthly performance report</li></ul></div>
  <div class="pkg"><h3>Tool &amp; content sponsor</h3><p class="price">Campaign-based</p><ul class="ticks"><li>Sponsor a calculator or document generator</li><li>Newsletter and video placements</li><li>Ideal for legal-tech, insurance and e-signature brands</li></ul></div>
</div>
<div class="lead-split" style="margin-top:2rem">
<form class="card-form" data-form="LAWYER / ADVERTISER inquiry" novalidate>
  <h2>Apply to become a partner</h2>
  <div class="two"><label>Your name<input name="name" required></label><label>Firm / company<input name="firm" required></label></div>
  <label>Email<input type="email" name="email" required></label>
  <label>Phone<input type="tel" name="phone"></label>
  <label>Interested in<select name="interest" required>{options(["Exclusive case inquiries", "Practice-area sponsorship", "Tool / content sponsorship", "Display advertising", "Partnership / acquisition", "Other"])}</select></label>
  <label>Practice areas<input name="areas" placeholder="e.g. Personal injury, Employment"></label>
  <label>Jurisdictions served<input name="jurisdictions" placeholder="e.g. Texas, Ontario"></label>
  <label>Bar admission / licence number (lawyers)<input name="bar"></label>
  <label>Monthly budget<select name="budget">{options(["Under $500", "$500–$2,000", "$2,000–$5,000", "$5,000+"])}</select></label>
  <label>Message<textarea name="message" rows="3"></textarea></label>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <button class="btn btn-gold" type="submit">Request partner info</button><p class="form-msg" aria-live="polite"></p>
</form>
<div class="prose"><h2>Compliance first</h2><p>Partners must be licensed and in good standing where they practise, and must follow their professional rules on advertising and solicitation. Smart.Legal is an advertising and information platform — not a lawyer referral service — and does not split fees or recommend particular lawyers.</p><p>Interested in the domain, the platform or a strategic partnership? Use the contact link at the top of any page.</p></div>
</div></div></section>"""
    out("for-lawyers.html", page("for-lawyers.html", "For Lawyers & Advertisers — Exclusive Legal Leads & Sponsorship",
        "Receive exclusive legal case inquiries, sponsor practice-area guides and legal tools, or advertise on Smart.Legal.", body))

def build_support():
    tiers = [("Supporter", "$10", "Keeps the calculators online for a day."), ("Advocate", "$25", "Funds a plain-language FAQ update."),
             ("Champion", "$100", "Funds a new document template."), ("Patron", "$500+", "Funds a full new guide or translation.")]
    tier_html = "".join(f'<button type="button" class="tier" data-amount="{esc(a)}"><b>{esc(n)}</b><span>{esc(a)}</span><small>{esc(d)}</small></button>' for n, a, d in tiers)
    body = hero("Support Smart.Legal", "Keep legal help free for everyone", "Smart.Legal is free to use. Donations and sponsors pay for hosting, legal review of content, new tools, translations, promotion, contests and the people who build them.") + f"""
<section class="section"><div class="wrap lead-split">
<form class="card-form" id="donateForm" data-form="DONATION pledge" novalidate>
  <h2>Make a donation</h2>
  <div class="tiers">{tier_html}</div>
  <div class="two"><label>Amount<input name="amount" required placeholder="$"></label><label>Frequency<select name="frequency"><option>One-time</option><option>Monthly</option><option>Yearly</option></select></label></div>
  <label>Preferred payment method<select name="method">{options(["PayPal", "Card (Stripe)", "Bank transfer / Interac e-Transfer", "UPI", "Crypto", "Cheque"])}</select></label>
  <label>Direct my gift to<select name="fund">{options(["Where it is needed most", "Operations & hosting", "New tools & guides", "Promotions & marketing", "Hiring writers & reviewers", "Contest prizes"])}</select></label>
  <div class="two"><label>Name<input name="name" required></label><label>Email<input type="email" name="email" required></label></div>
  <label class="check"><input type="checkbox" name="public_thanks" value="yes"> List my name on the supporters wall</label>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <button class="btn btn-gold" type="submit">Pledge my donation</button><p class="form-msg" aria-live="polite"></p>
  <p class="tiny">After you pledge, we send secure payment instructions for your chosen method. Smart.Legal is not a registered charity; donations are not tax-deductible unless stated otherwise.</p>
</form>
<div class="prose">
  <h2>Where your support goes</h2>
  <div class="bars"><p>Operations &amp; hosting <span style="--w:20%"></span></p><p>New tools &amp; guides <span style="--w:35%"></span></p><p>Promotion &amp; marketing <span style="--w:20%"></span></p><p>Hiring talent <span style="--w:15%"></span></p><p>Contests &amp; prizes <span style="--w:10%"></span></p></div>
  <h2>Sponsorship packages</h2>
  <ul class="ticks"><li><b>Sponsor a tool</b> — your brand on a calculator or generator used daily.</li><li><b>Sponsor a guide</b> — "made possible by" placement on a practice-area guide.</li><li><b>Sponsor a contest</b> — fund prizes and get featured to every entrant.</li><li><b>Translation partner</b> — fund Spanish, French or Hindi versions.</li></ul>
  <form class="card-form" data-form="SPONSORSHIP inquiry" novalidate><h3>Sponsorship inquiry</h3>
    <div class="two"><label>Name<input name="name" required></label><label>Organisation<input name="org" required></label></div>
    <label>Email<input type="email" name="email" required></label>
    <label>Package<select name="package">{options(["Sponsor a tool", "Sponsor a guide", "Sponsor a contest", "Translation partner", "Custom"])}</select></label>
    <label>Message<textarea name="message" rows="3"></textarea></label>
    <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
    <button class="btn btn-gold" type="submit">Send inquiry</button><p class="form-msg" aria-live="polite"></p></form>
</div></div></section>"""
    out("support.html", page("support.html", "Support Smart.Legal — Donate or Sponsor Free Legal Help",
        "Donate or sponsor Smart.Legal to keep free legal guides, tools and calculators online, fund new content, promotion, contests and hiring.", body))

def build_contests():
    contests = [
        ("Know-Your-Rights Challenge", "Monthly", "Score 10/10 on our quiz, then answer a tie-breaker question in 50 words or less. The most accurate, clearest answers win.", "Prize pool funded by sponsors — winners receive gift cards and featured recognition; amounts are announced at the start of each round."),
        ("Plain-Language Law Essay Award", "Quarterly", "Explain one legal concept to a 15-year-old in 600–900 words. Open to students and writers aged 18+.", "Top essay is published on Smart.Legal with a cash award, plus runner-up prizes when sponsored."),
        ("Legal-Tech Idea Sprint", "Twice a year", "Pitch a free tool that would help people solve a legal problem. Winning ideas may be built into Smart.Legal.", "Winner receives a cash prize and a paid build collaboration when the round is sponsored."),
    ]
    cards = "".join(f'<div class="pkg"><h3>{esc(t)}</h3><p class="price">{esc(f)}</p><p>{esc(d)}</p><p class="muted">{esc(p)}</p></div>' for t, f, d, p in contests)
    body = hero("Contests &amp; prizes", "Learn the law. Win prizes.", "Smart.Legal runs regular contests that reward people for learning and explaining the law clearly.") + f"""
<section class="section"><div class="wrap"><div class="pkg-grid">{cards}</div>
<div class="lead-split" style="margin-top:2rem">
<form class="card-form" data-form="CONTEST entry" novalidate>
  <h2>Enter a contest</h2>
  <label>Contest<select name="contest" required>{options([c[0] for c in contests])}</select></label>
  <div class="two"><label>Full name<input name="name" required></label><label>Email<input type="email" name="email" required></label></div>
  <label>Country / region<select name="region" required>{options(REGIONS)}</select></label>
  <label>Quiz score (Challenge only)<input name="score" placeholder="e.g. 10/10"></label>
  <label>Your entry (answer, essay or idea)<textarea name="entry" rows="7" required></textarea></label>
  <label>Link to entry (optional — Google Doc, PDF, video)<input type="url" name="link"></label>
  <label class="check"><input type="checkbox" name="age18" value="yes" required> I am 18 or older and accept the official rules.</label>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <button class="btn btn-gold" type="submit">Submit my entry</button><p class="form-msg" aria-live="polite"></p>
</form>
<div class="prose"><h2>Official rules (summary)</h2><ul>
<li><b>No purchase or donation necessary.</b> A donation does not improve your chances of winning.</li>
<li>Open to individuals aged 18+ where contests are lawful. Void where prohibited or restricted.</li>
<li>One entry per person per round. Entries must be your original work.</li>
<li>Entries are judged on accuracy, clarity and usefulness by the Smart.Legal editorial team and any named guest judges.</li>
<li>Prizes, amounts, round dates and judging dates are announced on this page before each round opens. Winners are notified by email and must respond within 14 days.</li>
<li>By entering you grant Smart.Legal a non-exclusive licence to publish your entry with credit. You keep your copyright.</li>
<li>Winners are responsible for any taxes. Smart.Legal may substitute a prize of equal or greater value.</li>
<li>Personal information is used only to run the contest — see our <a href="privacy.html">Privacy Policy</a>.</li></ul>
<p>Want to fund a prize? <a href="support.html">Sponsor a contest</a>.</p></div></div></div></section>"""
    out("contests.html", page("contests.html", "Contests & Prizes — Know-Your-Rights Challenge & Essay Award",
        "Enter Smart.Legal contests: the monthly Know-Your-Rights Challenge, the Plain-Language Law Essay Award and the Legal-Tech Idea Sprint.", body))

def build_careers():
    roles = [("Legal Content Writer", "Remote · Freelance", "Write plain-language guides and FAQs. Law degree, paralegal or legal-writing background preferred."),
             ("Paralegal / Lawyer Reviewer", "Remote · Part-time", "Review guides and templates for accuracy in your jurisdiction."),
             ("Front-end Developer", "Remote · Contract", "Build new calculators and generators in vanilla JS with accessibility in mind."),
             ("SEO & Growth Marketer", "Remote · Contract", "Grow organic traffic and partnerships in the legal vertical."),
             ("Attorney Partnerships Manager", "Remote · Commission", "Sign and manage law-firm partners and sponsors."),
             ("Video Editor / Creator", "Remote · Freelance", "Produce short know-your-rights explainers."),
             ("Translator (Spanish, French, Hindi)", "Remote · Freelance", "Translate and localise guides and tools.")]
    rc = "".join(f'<div class="role"><h3>{esc(t)}</h3><p class="muted">{esc(w)}</p><p>{esc(d)}</p></div>' for t, w, d in roles)
    body = hero("Careers", "Help millions understand the law", "Smart.Legal is a remote-first team building the most useful free legal-information platform on the web.") + f"""
<section class="section"><div class="wrap"><div class="role-grid">{rc}</div>
<div class="lead-split" style="margin-top:2rem">
<form class="card-form" data-form="JOB application" novalidate>
  <h2>Apply</h2>
  <label>Role<select name="role" required>{options([r[0] for r in roles] + ["Open application"])}</select></label>
  <div class="two"><label>Full name<input name="name" required></label><label>Email<input type="email" name="email" required></label></div>
  <label>Location / time zone<input name="location" required></label>
  <label>Portfolio, LinkedIn or CV link<input type="url" name="portfolio" required></label>
  <label>Availability<select name="availability">{options(["Full-time", "Part-time", "Freelance / per project"])}</select></label>
  <label>Why you?<textarea name="message" rows="5" required></textarea></label>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <button class="btn btn-gold" type="submit">Send application</button><p class="form-msg" aria-live="polite"></p>
</form>
<div class="prose"><h2>How we work</h2><ul class="ticks"><li>Remote and asynchronous</li><li>Paid per project or monthly retainer</li><li>Accuracy and plain language over jargon</li><li>Equal-opportunity: we welcome applicants of every background</li></ul></div>
</div></div></section>"""
    out("careers.html", page("careers.html", "Careers — Legal Writers, Reviewers, Developers & Marketers",
        "Join Smart.Legal: remote roles for legal content writers, paralegal and lawyer reviewers, developers, SEO marketers, partnership managers and translators.", body))

# ---------------------------------------------------------------- COMPANY & LEGAL
def build_company():
    about = hero("About", "About Smart.Legal", TAGLINE) + """
<section class="section"><div class="wrap narrow prose">
<p>Most people meet the law at a stressful moment — an accident, a dismissal, an eviction notice, a contract gone wrong. They search online and find either dense legal text or sales pages. Smart.Legal exists to close that gap.</p>
<h2>What we do</h2><ul class="ticks"><li><b>Explain</b> — plain-language guides and a legal dictionary written for non-lawyers.</li><li><b>Equip</b> — free tools: an issue navigator, document generators and calculators that run privately in your browser.</li><li><b>Connect</b> — a free case review that routes people to independent attorneys and to free legal aid when they qualify.</li><li><b>Update</b> — legal news and video explainers refreshed automatically every day.</li></ul>
<h2>Our principles</h2><ul><li><b>Information, not advice.</b> We never pretend a web page can replace a lawyer who knows your facts.</li><li><b>Free at the point of use.</b> Advertising, sponsorships, partner attorneys and donations fund the platform.</li><li><b>Transparent.</b> We label sponsorships and explain how we make money.</li><li><b>Private by design.</b> Tools process what you type in your own browser; only forms you choose to submit are sent to us.</li></ul>
<h2>How Smart.Legal is funded</h2><p>Smart.Legal displays advertising served by Google AdSense, offers sponsorship placements, receives fees from independent attorneys and legal-service partners who receive inquiries, and accepts donations. None of these affect the accuracy of our guides.</p>
<p><a class="btn btn-gold" href="contact.html">Contact us</a></p></div></section>"""
    out("about.html", page("about.html", "About Smart.Legal", "About Smart.Legal: free plain-language legal information, smart legal tools and a free case review with independent attorneys.", about))

    contact = hero("Contact", "Contact Smart.Legal", "Questions, corrections, partnerships, press or advertising — send us a message and we will reply by email.") + f"""
<section class="section"><div class="wrap lead-split">
<form class="card-form" data-form="CONTACT message" novalidate>
  <label>Reason<select name="reason" required>{options(["General question", "Report an error in a guide", "Advertising / sponsorship", "Partnership / domain inquiry", "Press / media", "Privacy request", "Technical issue", "Other"])}</select></label>
  <div class="two"><label>Name<input name="name" required></label><label>Email<input type="email" name="email" required></label></div>
  <label>Subject<input name="subject" required></label>
  <label>Message<textarea name="message" rows="6" required></textarea></label>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <button class="btn btn-gold" type="submit">Send message</button><p class="form-msg" aria-live="polite"></p>
</form>
<div class="prose"><h2>Need legal help instead?</h2><p>We cannot give legal advice by email. Use the <a href="free-case-review.html">free case review</a> to connect with an independent attorney, or find <a href="legal-aid.html">free legal aid</a> near you.</p>
<h2>Interested in this website or domain?</h2><p>For acquisition, sponsorship, advertising or partnership of Smart.Legal, use the contact link at the very top of any page.</p></div>
</div></section>"""
    out("contact.html", page("contact.html", "Contact Smart.Legal", "Contact Smart.Legal for questions, corrections, advertising, sponsorship, partnerships and press.", contact))

    for slug, title, desc, fn in [("privacy", "Privacy Policy", "How Smart.Legal collects, uses and protects information, including Google AdSense cookies and your privacy rights.", privacy_body),
                                  ("terms", "Terms of Use", "The terms that govern use of Smart.Legal, its tools, forms and content.", terms_body),
                                  ("disclaimer", "Legal Disclaimer", "Smart.Legal provides legal information, not legal advice, and is not a law firm or lawyer referral service.", disclaimer_body),
                                  ("trademark", "Trademark & Copyright Disclosure", "Trademark, copyright and non-affiliation disclosure for Smart.Legal.", trademark_body)]:
        body = hero("Legal", title, f"Last updated {datetime.date.today().strftime('%B %d, %Y')}") + f'<section class="section"><div class="wrap narrow prose">{fn()}</div></section>'
        out(f"{slug}.html", page(f"{slug}.html", title, desc, body))

    nf = hero("404", "That page could not be found", "It may have moved. Try a search, or start from one of these popular pages.") + \
        '<section class="section"><div class="wrap center"><a class="btn btn-gold" href="/index.html">Home</a> <a class="btn btn-ghost" href="/guides.html">Guides</a> <a class="btn btn-ghost" href="/free-case-review.html">Free case review</a></div></section>'
    import re
    html404 = page("404.html", "Page not found", "Page not found.", nf).replace('data-root=""', 'data-root="/"')
    html404 = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|data:)', r'\1="/', html404)
    html404 = html404.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    out("404.html", html404)

# ---------------------------------------------------------------- SEO / DATA
def build_meta():
    pages = [p for p in written if p.endswith(".html") and p != "404.html"]
    urls = "".join(f"<url><loc>{SITE}/{'' if p == 'index.html' else p}</loc><lastmod>{TODAY}</lastmod><changefreq>{'daily' if p in ('index.html','news.html','videos.html') else 'weekly'}</changefreq><priority>{'1.0' if p=='index.html' else '0.8' if p.startswith('guides') or p in ('free-case-review.html','navigator.html','documents.html','calculators.html') else '0.6'}</priority></url>" for p in sorted(pages))
    out("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    out("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /scripts/\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    out("ads.txt", "google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    idx = [{"t": g["title"], "u": f"guides/{g['slug']}.html", "d": g["summary"], "k": "guide " + g["area"] + " " + " ".join(g["video_kw"])} for g in GUIDES]
    idx += [{"t": t + " (template)", "u": f"documents.html#{k}", "d": "Free document generator", "k": "letter template document"} for k, t in DOC_LIST]
    idx += [{"t": t, "u": u, "d": d, "k": k} for t, u, d, k in [
        ("Injury settlement estimator", "calculators.html#settlement", "Estimate a personal-injury settlement range", "calculator accident"),
        ("Contingency vs hourly fees", "calculators.html#fees", "Compare lawyer fee models", "calculator lawyer cost"),
        ("Deadline & day counter", "calculators.html#deadline", "Count calendar or business days", "calculator limitation date"),
        ("Debt & wages interest", "calculators.html#interest", "Interest on money owed", "calculator invoice unpaid"),
        ("Small-claims cost/benefit", "calculators.html#smallclaims", "Is small claims worth it?", "calculator court"),
        ("Rent-increase checker", "calculators.html#rent", "Rent increase percentage", "calculator landlord tenant"),
        ("Legal Issue Navigator", "navigator.html", "Personalised legal action plan", "wizard help start"),
        ("Free case review", "free-case-review.html", "Connect with an independent attorney", "lawyer attorney help"),
        ("Free legal aid finder", "legal-aid.html", "Free legal help by country", "pro bono free lawyer"),
        ("Know-your-rights quiz", "quiz.html", "Test your legal knowledge", "quiz contest"),
        ("Legal news", "news.html", "Today's legal headlines", "news"),
        ("Legal videos", "videos.html", "Know-your-rights videos", "youtube video")]]
    idx += [{"t": t, "u": "dictionary.html#t-" + t.lower().replace(" ", "-").replace("(", "").replace(")", ""), "d": d[:110], "k": "definition dictionary"} for t, d in TERMS]
    out("data/search.json", json.dumps(idx, ensure_ascii=False, separators=(",", ":")))
    out("data/meta.json", json.dumps({"built": TODAY, "news_updated": NEWS.get("updated"), "videos_updated": VIDEOS.get("updated")}))

if __name__ == "__main__":
    for fn in [build_home, build_guides, build_navigator, build_documents, build_calculators, build_dictionary, build_quiz,
               build_news, build_videos, build_legal_aid, build_case_review, build_ask, build_for_lawyers, build_support,
               build_contests, build_careers, build_company, build_meta]:
        fn()
    print(f"Built {len(written)} files")
