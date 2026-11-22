"""Shared layout for every Smart.Legal page."""
import html, json, datetime, zlib

SITE = "https://smart.legal"
NAME = "Smart.Legal"
TAGLINE = "Know your rights. Take the smart next step."
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
BANNER_URL = "https://web.works/contact"
YEAR = datetime.date.today().year

NAV = [
    ("Guides", "guides.html"),
    ("Navigator", "navigator.html"),
    ("Documents", "documents.html"),
    ("Calculators", "calculators.html"),
    ("Dictionary", "dictionary.html"),
    ("News", "news.html"),
    ("Videos", "videos.html"),
    ("Legal Aid", "legal-aid.html"),
]

FOOTER_COLS = [
    ("Get help", [("Free Case Review", "free-case-review.html"), ("Ask a Legal Question", "ask.html"),
                  ("Legal Issue Navigator", "navigator.html"), ("Free Legal Aid", "legal-aid.html")]),
    ("Smart tools", [("Document Generator", "documents.html"), ("Legal Calculators", "calculators.html"),
                     ("Legal Dictionary", "dictionary.html"), ("Know-Your-Rights Quiz", "quiz.html")]),
    ("Community", [("Support / Donate", "support.html"), ("Contests & Prizes", "contests.html"),
                   ("Careers", "careers.html"), ("For Lawyers & Advertisers", "for-lawyers.html")]),
    ("Company", [("About", "about.html"), ("Contact", "contact.html"), ("Privacy Policy", "privacy.html"),
                 ("Terms of Use", "terms.html"), ("Legal Disclaimer", "disclaimer.html"),
                 ("Trademark & Copyright", "trademark.html")]),
]

CUR = ' aria-current="page"'

def esc(s):
    return html.escape(str(s), quote=True)

def page(path, title, description, body, depth=0, schema=None, active=None, og_type="website", extra_head=""):
    """Render a full HTML page. path = output path relative to site root."""
    pre = "../" * depth
    canonical = SITE + "/" + ("" if path == "index.html" else path)
    full_title = title if title.startswith(NAME) else f"{title} | {NAME}"
    schemas = [{
        "@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": SITE,
        "logo": SITE + "/assets/img/logo.svg", "description": TAGLINE}]
    if schema:
        schemas += schema if isinstance(schema, list) else [schema]
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    nav = "".join(
        f'<a href="{pre}{u}"{CUR if active == u else ""}>{esc(t)}</a>' for t, u in NAV)
    cols = "".join(
        f'<div><h3>{esc(h)}</h3><ul>' + "".join(f'<li><a href="{pre}{u}">{esc(t)}</a></li>' for t, u in links) + "</ul></div>"
        for h, links in FOOTER_COLS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b1b33">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{pre}manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/style.css">
{ADSENSE}
{ld}
{extra_head}
<script>try{{var t=localStorage.getItem('sl-theme');if(t)document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
</head>
<body data-root="{pre}">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><a href="{BANNER_URL}" target="_blank" rel="noopener">&#9993; Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership</a></div>
<header class="site-header">
  <div class="wrap hdr">
    <a class="brand" href="{pre}index.html" aria-label="{NAME} home"><img src="{pre}assets/img/logo.svg" alt="" width="34" height="34"><span>Smart<b>.Legal</b></span></a>
    <nav class="main-nav" id="mainNav" aria-label="Main">{nav}</nav>
    <div class="hdr-actions">
      <button class="icon-btn" id="searchBtn" aria-label="Search the site">&#128269;</button>
      <button class="icon-btn" id="themeBtn" aria-label="Toggle dark mode">&#9790;</button>
      <a class="btn btn-gold sm hide-sm" href="{pre}free-case-review.html">Free Case Review</a>
      <button class="icon-btn menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="mainNav">&#9776;</button>
    </div>
  </div>
</header>
<div class="search-overlay" id="searchOverlay" hidden>
  <div class="search-box" role="dialog" aria-label="Search Smart.Legal">
    <input id="siteSearch" type="search" placeholder="Search guides, tools and legal terms…" autocomplete="off">
    <ul id="searchResults"></ul>
    <button class="icon-btn close" id="searchClose" aria-label="Close search">&#10005;</button>
  </div>
</div>
<main id="main">
{body}
</main>
<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2>Have a legal problem right now?</h2><p>Get a free, no-obligation case review. Tell us what happened in 60 seconds and an independent attorney in your area may contact you.</p></div>
    <a class="btn btn-gold lg" href="{pre}free-case-review.html">Start my free case review &rarr;</a>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand"><a class="brand" href="{pre}index.html"><img src="{pre}assets/img/logo.svg" alt="" width="30" height="30"><span>Smart<b>.Legal</b></span></a>
        <p>{TAGLINE} Free plain-language legal information, smart tools and a direct path to independent attorneys.</p>
        <form class="newsletter" data-form="Newsletter signup" novalidate>
          <label for="nl-{zlib.crc32(path.encode())%99999}" class="sr">Email</label>
          <input id="nl-{zlib.crc32(path.encode())%99999}" type="email" name="email" placeholder="Your email for weekly legal tips" required>
          <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
          <button class="btn btn-gold sm" type="submit">Subscribe</button>
          <p class="form-msg" aria-live="polite"></p>
        </form>
      </div>
      <div class="foot-cols">{cols}</div>
    </div>
    <p class="disclaimer"><strong>Important:</strong> Smart.Legal is an independent legal-information website. It is not a law firm, does not provide legal advice and is not a lawyer referral service. Using this site or submitting a form does not create an attorney-client relationship. Attorneys who may contact you are independent and may pay to advertise or receive inquiries. Laws change and vary by location — always confirm with a licensed lawyer in your jurisdiction. Smart.Legal is not affiliated with any company, product or law firm with a similar name. See our <a href="{pre}disclaimer.html">Legal Disclaimer</a> and <a href="{pre}trademark.html">Trademark &amp; Copyright Disclosure</a>.</p>
    <p class="copy">&copy; {YEAR} Smart.Legal. All rights reserved. <span id="lastUpdated"></span></p>
  </div>
</footer>
<a class="sticky-cta" href="{pre}free-case-review.html">&#9878; Free Case Review</a>
<div class="cookie" id="cookie" hidden><p>We use cookies for essential functions, analytics and personalised ads by Google. See our <a href="{pre}privacy.html">Privacy Policy</a>.</p><button class="btn btn-gold sm" id="cookieOk">Got it</button></div>
<script src="{pre}assets/js/app.js" defer></script>
</body>
</html>
"""

def hero(kicker, title, sub, extra=""):
    return f'<section class="page-hero"><div class="wrap"><p class="kicker">{kicker}</p><h1>{title}</h1><p class="lead">{sub}</p>{extra}</div></section>'

def breadcrumb(items, pre=""):
    parts = [f'<a href="{pre}index.html">Home</a>'] + [
        (f'<a href="{pre}{u}">{esc(t)}</a>' if u else f'<span>{esc(t)}</span>') for t, u in items]
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"

def lead_widget(area="", pre="", title="Get a free case review"):
    """Compact inline lead form."""
    return f"""<aside class="lead-card" id="lead">
<h3>{esc(title)}</h3>
<p>Free &amp; no obligation. Describe your situation and an independent attorney may contact you.</p>
<form data-form="Lead: Quick case review" novalidate>
  <input type="hidden" name="legal_area" value="{esc(area)}">
  <label>Your name<input name="name" required autocomplete="name"></label>
  <label>Email<input type="email" name="email" required autocomplete="email"></label>
  <label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
  <label>Location (city, state/province, country)<input name="location" required></label>
  <label>What happened?<textarea name="details" rows="3" required></textarea></label>
  <label class="check"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted about my request. No attorney-client relationship is created.</label>
  <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
  <button class="btn btn-gold block" type="submit">Get my free review</button>
  <p class="form-msg" aria-live="polite"></p>
</form>
<p class="tiny">Prefer more detail? <a href="{pre}free-case-review.html">Use the full case review &rarr;</a></p>
</aside>"""
