# Smart.Legal — Phase-wise Build Prompt

## The idea (why this wins)

**Smart.Legal = "the smart front door to the law."** A free, plain-language legal self-help platform (guides, issue navigator, document generators, calculators, dictionary, live legal news, videos) whose real business is **converting high-intent visitors into paid attorney leads**, with Google AdSense on top.

Why legal is the right play for this domain:

- **Highest-value ad vertical.** "Lawyer/attorney" keywords sit among the most expensive search terms in Google Ads (personal-injury, mesothelioma, DUI, divorce terms commonly run $50–$300+ CPC). Legal content pages therefore earn far above average AdSense RPM.
- **Leads are worth more than ads.** Exclusive personal-injury leads typically sell to law firms for roughly $100–$500+, family/criminal/immigration roughly $25–$150. A site at 50k visits/month converting 1% to case reviews = 500 leads/month. Even at a blended $40/lead that is ~$20k/month potential, vs. roughly $1.5k–$5k/month from AdSense at the same traffic.
- **The domain is the brand.** "Smart.Legal" reads as a product, not a law firm — ideal for a tools-first platform that can later sell subscriptions, sponsorships or the domain itself.

Revenue stack (in order of value): 1) lead sales to partner attorneys, 2) AdSense, 3) attorney/legal-tech sponsorships & featured placements, 4) donations, 5) affiliate (legal-tech, e-sign, formation services), 6) domain/website sale or partnership.

---

## Master prompt

> Build **Smart.Legal**, a modern, interactive, responsive, self-updating static website hosted free on GitHub Pages (main branch, root). Brand: "Smart.Legal — Know your rights. Take the smart next step." Positioning: free plain-language legal information + smart tools + free case review that connects visitors with independent attorneys. It must be AdSense-approvable (publisher ca-pub-6620975821265271), with the AdSense loader in every page `<head>`, `ads.txt` at the root, original long-form content, privacy policy covering Google cookies, terms, disclaimer, about and contact pages. Never present anything as legal advice; state on every page that Smart.Legal is not a law firm or lawyer-referral service and that using the site creates no attorney-client relationship.

### Phase 1 — Foundation & compliance
1. Static architecture: HTML + one CSS file + vanilla JS; Python build script renders all pages from a single layout so header/footer/banner stay identical.
2. Every page top: banner "Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership" linking to the owner's contact page (URL hidden behind the link text).
3. All forms post through a client-side handler to one private inbox; the address is stored only in obfuscated form and never appears in HTML, text, metadata or the repository docs.
4. Pages: Home, About, Contact, Privacy (incl. Google AdSense/DoubleClick cookies, opt-out links, CCPA/GDPR rights), Terms, Legal Disclaimer, Trademark & Copyright Disclosure, 404.
5. SEO: unique titles/descriptions, canonical URLs, Open Graph, JSON-LD (Organization, WebSite+SearchAction, FAQPage, Article), `sitemap.xml`, `robots.txt`, `ads.txt`, `CNAME`, web manifest, SVG favicon.
6. Cookie notice, dark/light mode, accessibility (skip link, ARIA, focus states, reduced motion).

### Phase 2 — Content engine (AdSense approval)
1. 12 original long-form guides: Personal Injury, Family & Divorce, Employment & Workplace, Landlord & Tenant, Immigration, Criminal Defense, Business & Contracts, Wills & Estates, Consumer Rights & Debt, Traffic & DUI, Intellectual Property & Online, Privacy & Data. Each: overview, your key rights, step-by-step plan, documents to gather, costs, when to hire a lawyer, FAQ (with FAQPage schema), related tools, related videos, inline lead CTA.
2. Legal dictionary: 120+ original plain-English definitions, A–Z jump bar, instant search.
3. Free legal-aid directory by country (US, Canada, UK, India, Australia, international) linking to official/non-profit sources.
4. Site-wide instant search across guides, tools and dictionary.

### Phase 3 — Smart tools (traffic magnets)
1. **Legal Issue Navigator** — a 4-step triage wizard (area → situation → urgency → location) producing a personalised action plan, the right guide, the right tools, and a pre-filled case review.
2. **Document generator** — 12 fill-in templates with live preview, copy, download (.txt/.doc) and print-to-PDF: demand letter, cease & desist, mutual NDA, freelance/service agreement, residential lease summary, security-deposit return demand, bill of sale, promissory note, general power-of-attorney worksheet, refund/chargeback request, data-access (GDPR/CCPA) request, employment reference/verification request.
3. **Calculators** — injury settlement estimator (multiplier method), contingency vs. hourly fee comparison, deadline/day counter (calendar & business days), unpaid debt interest, small-claims cost/benefit, rent-increase percentage checker.
4. **Know-Your-Rights quiz** with score, explanations, share and contest entry.

### Phase 4 — Lead generation (core revenue)
1. Dedicated **Free Case Review** page: multi-step form with progress bar (legal area → details → urgency & timeline → location → contact), consent checkbox, honeypot, success state, UTM capture, page-source capture.
2. Compact lead widgets on every guide, tool result and the home page; sticky "Free Case Review" button on mobile.
3. **Ask a Legal Question** form; **For Lawyers** page selling exclusive leads, featured listings and sponsored guides with an application form.

### Phase 5 — Monetization & community
1. AdSense Auto ads + optional manual slots configured in one JS object.
2. **Support** page: donation tiers (one-time/monthly), pledge form, sponsorship packages, "sponsor a tool/guide".
3. **Contests**: Know-Your-Rights Challenge, Plain-Language Law Essay Award, Legal-Tech Idea Sprint — with official rules (no purchase necessary, eligibility, judging, privacy) and entry forms.
4. **Careers**: open roles (legal writers, paralegal reviewers, front-end devs, SEO/marketing, outreach, video editors) + application form.
5. Promotions: newsletter, share buttons, partner/advertise inquiries.

### Phase 6 — Automation (self-updating)
1. GitHub Actions workflow (daily + manual + on script changes) runs `scripts/update_feeds.py` → pulls legal news RSS per topic and the latest videos from vetted legal-education YouTube channels into `data/*.json`, then `scripts/build.py` re-renders news/videos pages and the sitemap, and commits only when content changed.
2. Daily "Legal tip of the day", "last updated" stamps, auto-refresh of feeds in the browser.

### Phase 7 — QA & launch
1. Validate every page renders, links resolve, forms submit, no exposed address, Lighthouse-friendly (lazy video embeds, deferred JS).
2. Push to GitHub `WEBWORKSA1/smart-legal` (main), enable Pages (main / root), point DNS for smart.legal to GitHub Pages, enforce HTTPS, submit sitemap to Search Console, then apply to AdSense.
