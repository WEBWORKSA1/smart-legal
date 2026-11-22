# Smart.Legal

Free plain-language legal information, smart tools and a free case review — a static, self-updating site for **smart.legal**, hosted on GitHub Pages (main branch, root).

## What's inside
- 12 long-form legal guides (`/guides/`), 124-term legal dictionary, free legal-aid finder
- Legal Issue Navigator, 12-template document generator, 6 legal calculators, Know-Your-Rights quiz
- Free Case Review multi-step lead form + compact lead widgets on every guide, Ask-a-Question, For-Lawyers partner form
- Support/donations, sponsorship, contests, careers pages
- Daily auto-refreshed legal news and YouTube explainers (`.github/workflows/auto-refresh.yml`)
- Google AdSense loader on every page, `ads.txt`, sitemap, robots, JSON-LD schema
- Privacy, Terms, Legal Disclaimer, Trademark & Copyright Disclosure

## Edit & rebuild
Content lives in `scripts/content_*.py`; layout in `scripts/layout.py`.
```
python3 scripts/update_feeds.py   # optional: refresh news & videos
python3 scripts/build.py          # regenerate all HTML, sitemap and search index
```
Manual AdSense ad units: add slot IDs to `AD_SLOTS` in `assets/js/app.js`.

See `PROMPT.md` (phase-wise build prompt) and `RESEARCH.md` (39-site competitive research).
