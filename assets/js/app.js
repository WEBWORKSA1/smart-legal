/* Smart.Legal — site script (vanilla JS, no dependencies) */
(function () {
  "use strict";
  var ROOT = document.body.getAttribute("data-root") || "";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (n) { return (isFinite(n) ? n : 0).toLocaleString(undefined, { style: "currency", currency: "USD", maximumFractionDigits: 0 }); };
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  var params = new URLSearchParams(location.search);
  window.SL = window.SL || {};

  /* ---------- Optional manual AdSense units: add slot IDs here after creating units in AdSense ---------- */
  var AD_SLOTS = { inArticle: "", footer: "" };
  (function ads() {
    Object.keys(AD_SLOTS).forEach(function (k) {
      if (!AD_SLOTS[k]) return;
      $$('[data-ad="' + k + '"]').forEach(function (el) {
        el.innerHTML = '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-6620975821265271" data-ad-slot="' + AD_SLOTS[k] + '" data-ad-format="auto" data-full-width-responsive="true"></ins>';
        try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
      });
    });
  })();

  /* ---------- Theme, menu, cookie ---------- */
  var themeBtn = $("#themeBtn");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var d = document.documentElement, t = d.dataset.theme === "dark" ? "light" : "dark";
    d.dataset.theme = t; store.set("sl-theme", t);
  });
  var menuBtn = $("#menuBtn"), nav = $("#mainNav");
  if (menuBtn) menuBtn.addEventListener("click", function () {
    var open = nav.classList.toggle("open"); menuBtn.setAttribute("aria-expanded", open);
  });
  var cookie = $("#cookie");
  if (cookie && !store.get("sl-cookie")) { cookie.hidden = false; $("#cookieOk").addEventListener("click", function () { store.set("sl-cookie", "1"); cookie.hidden = true; }); }

  /* ---------- Last updated + tip of the day ---------- */
  fetch(ROOT + "data/meta.json", { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (m) {
    var el = $("#lastUpdated"); if (el && (m.news_updated || m.built)) el.textContent = "Content refreshed: " + new Date(m.news_updated || m.built).toLocaleDateString();
  }).catch(function () {});
  var TIPS = [
    "Put important agreements in writing — a dated email confirming what was agreed is better than nothing.",
    "Limitation periods can end a claim forever. Note the date something happened and check your deadline early.",
    "You can usually decline a recorded statement to the other side's insurer.",
    "Photograph a rental at move-in and move-out — it is the best evidence in deposit disputes.",
    "Paying a traffic ticket is usually a guilty plea. Check the points and insurance impact first.",
    "Never sign a severance agreement on the spot. You can ask for time to have it reviewed.",
    "Debt collectors generally must verify a debt if you dispute it in writing.",
    "Electronic signatures are valid for most contracts in most countries.",
    "A will only works after death. A power of attorney protects you while you are alive.",
    "Keep a copy of every form you submit to a court or government agency.",
    "Saying 'I want to remain silent and I want a lawyer' is your right — then stop talking.",
    "You can ask most organisations for a copy of the personal data they hold about you.",
    "Freelancers usually own their work unless a written contract assigns it to the client.",
    "Mediation is often faster and cheaper than court — and many courts require you to try it first.",
    "Read the termination clause first. It tells you how to exit a contract.",
    "A demand letter with a clear deadline settles many disputes before court."
  ];
  var tipEl = $("#tipOfDay");
  if (tipEl) { var day = Math.floor(Date.now() / 864e5); tipEl.textContent = TIPS[day % TIPS.length]; }

  /* ---------- Search ---------- */
  var overlay = $("#searchOverlay"), sInput = $("#siteSearch"), sRes = $("#searchResults"), INDEX = null;
  function loadIndex(cb) { if (INDEX) return cb(); fetch(ROOT + "data/search.json").then(function (r) { return r.json(); }).then(function (d) { INDEX = d; cb(); }).catch(function () { INDEX = []; cb(); }); }
  function runSearch(q) {
    q = (q || "").toLowerCase().trim();
    if (!q) { sRes.innerHTML = ""; return; }
    var words = q.split(/\s+/);
    var hits = INDEX.map(function (it) {
      var hay = (it.t + " " + it.d + " " + it.k).toLowerCase(), score = 0;
      words.forEach(function (w) { if (it.t.toLowerCase().indexOf(w) > -1) score += 5; if (hay.indexOf(w) > -1) score += 1; });
      return { it: it, s: score };
    }).filter(function (h) { return h.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 12);
    sRes.innerHTML = hits.length ? hits.map(function (h) { return '<li><a href="' + ROOT + h.it.u + '">' + esc(h.it.t) + "<small>" + esc(h.it.d) + "</small></a></li>"; }).join("")
      : '<li class="muted" style="padding:.7rem">No results. Try the <a href="' + ROOT + 'navigator.html">Navigator</a> or <a href="' + ROOT + 'ask.html">ask a question</a>.</li>';
  }
  SL.openSearch = function (q) { overlay.hidden = false; sInput.value = q || ""; sInput.focus(); loadIndex(function () { runSearch(sInput.value); }); };
  if (overlay) {
    $("#searchBtn").addEventListener("click", function () { SL.openSearch(""); });
    $("#searchClose").addEventListener("click", function () { overlay.hidden = true; });
    overlay.addEventListener("click", function (e) { if (e.target === overlay) overlay.hidden = true; });
    sInput.addEventListener("input", function () { loadIndex(function () { runSearch(sInput.value); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") overlay.hidden = true;
      if (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); SL.openSearch(""); }
    });
    if (params.get("q")) SL.openSearch(params.get("q"));
  }

  /* ---------- Forms (delivered through a relay; destination kept obfuscated) ---------- */
  var _k = [116, 118, 106, 53, 115, 112, 104, 116, 110, 71, 56, 104, 122, 114, 121, 118, 126, 105, 108, 126];
  function _d() { return String.fromCharCode.apply(null, _k.map(function (c) { return c - 7; })).split("").reverse().join(""); }
  function utm() { var o = {}; ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid"].forEach(function (k) { var v = params.get(k) || store.get("sl-" + k); if (v) { o[k] = v; store.set("sl-" + k, v); } }); return o; }
  utm();
  function submitForm(form) {
    var msg = $(".form-msg", form), btn = $('button[type="submit"]', form);
    if (form._honey && form._honey.value) return;
    var data = {};
    new FormData(form).forEach(function (v, k) { if (k === "_honey") return; data[k] = data[k] ? data[k] + ", " + v : v; });
    var kind = form.getAttribute("data-form") || "Form";
    data._subject = "Smart.Legal — " + kind + (data.legal_area ? " — " + data.legal_area : "");
    data._template = "table"; data._captcha = "false";
    data.form_type = kind; data.page = location.href; data.submitted_at = new Date().toISOString();
    Object.assign(data, utm());
    if (data.email) data._replyto = data.email;
    btn && (btn.disabled = true); if (msg) { msg.className = "form-msg"; msg.textContent = "Sending…"; }
    fetch("https://formsubmit.co/ajax/" + _d(), { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function () {
        if (msg) { msg.className = "form-msg ok"; msg.textContent = /LEAD/i.test(kind) ? "Thank you — your free case review request has been received. Watch your email and phone." : "Thank you — we received your submission."; }
        form.reset(); form.dispatchEvent(new CustomEvent("sl:sent"));
      })
      .catch(function () { if (msg) { msg.className = "form-msg err"; msg.textContent = "Sorry, that did not go through. Please check your connection and try again."; } })
      .then(function () { btn && (btn.disabled = false); });
  }
  $$("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      submitForm(form);
    });
  });

  /* ---------- Multi-step lead form ---------- */
  $$(".msf").forEach(function (form) {
    var steps = $$(".step", form), i = 0, bar = $(".progress span", form), cur = $(".cur", form);
    var prev = $("[data-prev]", form), next = $("[data-next]", form), sub = $('button[type="submit"]', form);
    var area = params.get("area");
    if (area) { $$('input[name="legal_area"]', form).forEach(function (r) { if (r.value.toLowerCase().indexOf(area.toLowerCase().split(/[ /&]/)[0]) === 0) r.checked = true; }); }
    var pre = store.get("sl-nav-summary"); if (pre && $('textarea[name="details"]', form) && params.get("from") === "navigator") $('textarea[name="details"]', form).value = pre;
    function show(n) {
      i = n; steps.forEach(function (s, k) { s.classList.toggle("active", k === i); });
      bar.style.width = ((i + 1) / steps.length * 100) + "%"; cur.textContent = i + 1;
      prev.hidden = i === 0; next.hidden = i === steps.length - 1; sub.hidden = i !== steps.length - 1;
    }
    function valid() { var ok = true; $$("input,select,textarea", steps[i]).forEach(function (f) { if (ok && !f.checkValidity()) { f.reportValidity(); ok = false; } }); return ok; }
    next.addEventListener("click", function () { if (valid()) show(i + 1); });
    prev.addEventListener("click", function () { show(i - 1); });
    $$('input[type="radio"]', steps[0]).forEach(function (r) { r.addEventListener("change", function () { setTimeout(function () { show(1); }, 180); }); });
    form.addEventListener("sl:sent", function () { show(0); });
    show(0);
  });

  /* ---------- Donation tiers ---------- */
  $$(".tier").forEach(function (t) {
    t.addEventListener("click", function () {
      $$(".tier").forEach(function (x) { x.classList.remove("active"); }); t.classList.add("active");
      var f = $("#donateForm"); if (f) f.amount.value = t.getAttribute("data-amount");
    });
  });

  /* ---------- Lazy YouTube embeds ---------- */
  function wireYT(scope) {
    $$(".yt .yt-play", scope).forEach(function (b) {
      if (b._w) return; b._w = 1;
      b.addEventListener("click", function () {
        var fig = b.parentNode, id = fig.getAttribute("data-id"), list = fig.getAttribute("data-list");
        var src = id ? "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0" : "https://www.youtube-nocookie.com/embed/videoseries?list=" + list + "&autoplay=1&rel=0";
        var f = document.createElement("iframe");
        f.src = src; f.title = "YouTube video"; f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"; f.allowFullscreen = true; f.loading = "lazy";
        b.replaceWith(f);
      });
    });
  }
  wireYT();
  $$(".yt-dyn").forEach(function (box) {
    var kw = (box.getAttribute("data-kw") || "").split(",");
    fetch(ROOT + "data/videos.json").then(function (r) { return r.json(); }).then(function (d) {
      var vids = (d.videos || []).filter(function (v) { var t = v.title.toLowerCase(); return kw.some(function (k) { return k && t.indexOf(k) > -1; }); });
      if (!vids.length) vids = (d.videos || []).slice(0, 3);
      if (!vids.length) { box.innerHTML = '<div class="video-grid"><figure class="yt" data-list="UUpa-Zb0ZcQjTCPP1Dx_1M8Q"><button class="yt-play" aria-label="Play legal explainers"><span class="yt-ph">&#9878;<b>Legal explainers</b><small>Latest uploads</small></span><span class="play">&#9658;</span></button><figcaption>Latest legal explainers</figcaption></figure></div>'; wireYT(box); return; }
      box.innerHTML = '<div class="video-grid">' + vids.slice(0, 3).map(function (v) {
        return '<figure class="yt" data-id="' + esc(v.id) + '"><button class="yt-play" aria-label="Play: ' + esc(v.title) + '"><img loading="lazy" src="https://i.ytimg.com/vi/' + esc(v.id) + '/hqdefault.jpg" alt=""><span class="play">&#9658;</span></button><figcaption>' + esc(v.title) + "<small>" + esc(v.channel) + "</small></figcaption></figure>";
      }).join("") + "</div>";
      wireYT(box);
    }).catch(function () {});
  });

  /* ---------- News tabs ---------- */
  $$(".tabs .tab").forEach(function (t) {
    t.addEventListener("click", function () {
      $$(".tabs .tab").forEach(function (x) { x.classList.remove("active"); }); t.classList.add("active");
      var topic = t.getAttribute("data-topic");
      $$(".news-topic").forEach(function (s) { s.hidden = topic !== "all" && s.getAttribute("data-topic") !== topic; });
    });
  });

  /* ---------- Dictionary search ---------- */
  var dict = $("#dictSearch");
  if (dict) dict.addEventListener("input", function () {
    var q = dict.value.toLowerCase().trim(), any = false;
    $$(".term").forEach(function (t) { var m = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !m; if (m) any = true; });
    $$(".letter").forEach(function (l) { l.hidden = !$$(".term", l).some(function (t) { return !t.hidden; }); });
    $("#dictEmpty").hidden = any;
  });

  /* ---------- Calculators ---------- */
  var today = new Date().toISOString().slice(0, 10);
  $$('input[type="date"]').forEach(function (d) { if (!d.value && d.name === "start") d.value = today; if (!d.value && d.name === "from") { var y = new Date(); y.setFullYear(y.getFullYear() - 1); d.value = y.toISOString().slice(0, 10); } if (!d.value && d.name === "to") d.value = today; });
  var CALC = {
    settlement: function (v) {
      var special = v.med + v.wages + v.prop, general = v.med * v.mult, gross = special + general;
      var low = gross * 0.75, high = gross * 1.25, net = function (x) { return x * (1 - v.fault / 100) * (1 - v.fee / 100); };
      return "<strong>" + money(low * (1 - v.fault / 100)) + " – " + money(high * (1 - v.fault / 100)) + "</strong>Estimated claim value after your share of fault. Economic losses " + money(special) + "; pain &amp; suffering ≈ " + money(general) + ".<br>After a " + v.fee + "% fee you might net roughly <b>" + money(net(low)) + " – " + money(net(high)) + "</b>. Policy limits often cap real settlements.";
    },
    fees: function (v) {
      var cont = v.rec * v.pct / 100, hourly = v.rate * v.hours;
      var nc = v.rec - cont - v.costs, nh = v.rec - hourly - v.costs, better = nc > nh ? "contingency" : "hourly";
      return "<strong>You keep " + money(nc) + " (contingency) vs " + money(nh) + " (hourly)</strong>Contingency fee: " + money(cont) + " · Hourly fee: " + money(hourly) + " · Costs: " + money(v.costs) + ".<br>On these numbers <b>" + better + "</b> leaves you more — but contingency shifts the risk of losing to the lawyer.";
    },
    deadline: function (v, f) {
      var s = f.start.value ? new Date(f.start.value + "T12:00:00") : null, out = "";
      if (s && f.days.value !== "") {
        var d = new Date(s), n = parseInt(f.days.value, 10) || 0;
        if (f.mode.value === "bus") { var c = 0; while (c < n) { d.setDate(d.getDate() + 1); if (d.getDay() % 6) c++; } }
        else d.setDate(d.getDate() + n);
        out += "<strong>" + d.toDateString() + "</strong>" + n + " " + (f.mode.value === "bus" ? "business" : "calendar") + " days after " + s.toDateString() + ". Courts may also exclude public holidays.";
      }
      if (s && f.end.value) {
        var e = new Date(f.end.value + "T12:00:00"), diff = Math.round((e - s) / 864e5), b = 0, x = new Date(s);
        while (x < e) { x.setDate(x.getDate() + 1); if (x.getDay() % 6) b++; }
        out += "<br><b>" + diff + "</b> calendar days (" + b + " business days) between the dates.";
      }
      return out || "Pick a start date.";
    },
    interest: function (v, f) {
      var a = new Date(f.from.value), b = new Date(f.to.value);
      var yrs = Math.max(0, (b - a) / (365.25 * 864e5)), r = v.rate / 100, i;
      i = f.method.value === "compound" ? v.amt * (Math.pow(1 + r / 12, yrs * 12) - 1) : v.amt * r * yrs;
      return "<strong>" + money(v.amt + i) + " total</strong>Interest: " + money(i) + " over " + (yrs * 12).toFixed(1) + " months at " + v.rate + "% (" + f.method.value + "). Check the contract or your local statutory/judgment rate.";
    },
    smallclaims: function (v) {
      var ev = v.claim * (v.chance / 100) * (v.collect / 100), cost = v.fees + v.hours * v.hourval, net = ev - cost;
      return "<strong>Expected value: " + money(net) + "</strong>Probability-weighted recovery " + money(ev) + " minus costs and your time " + money(cost) + ".<br>" + (net > 0 ? "On these numbers, filing looks <b>worth it</b>. Send a demand letter first — many disputes settle." : "On these numbers it may <b>not</b> be worth it — try a demand letter or mediation.");
    },
    rent: function (v) {
      var pct = v.old ? (v.new - v.old) / v.old * 100 : 0, over = v.cap && pct > v.cap;
      return "<strong>" + pct.toFixed(2) + "% increase</strong>" + money(v.new - v.old) + " more per month (" + money((v.new - v.old) * 12) + " per year)." + (v.cap ? "<br>" + (over ? "This is <b>above</b> the " + v.cap + "% guideline you entered — check whether your unit is covered by rent control and whether notice was proper." : "This is within the " + v.cap + "% guideline you entered.") : "");
    }
  };
  $$("form[data-calc]").forEach(function (f) {
    var fn = CALC[f.getAttribute("data-calc")], res = $(".result", f);
    function run() { var v = {}; $$("input[type=number],select", f).forEach(function (el) { v[el.name] = parseFloat(el.value) || 0; }); try { res.innerHTML = fn(v, f); } catch (e) { res.textContent = "Check your inputs."; } }
    f.addEventListener("input", run); f.addEventListener("submit", function (e) { e.preventDefault(); }); run();
  });

  /* ---------- Document generator ---------- */
  var T = function (s) { return s || "________"; };
  var DATE = function () { return new Date().toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" }); };
  var DOCS = {
    demand: { t: "Demand Letter for Money Owed", f: [["you", "Your full name"], ["youAddr", "Your address"], ["them", "Recipient name / business"], ["themAddr", "Recipient address"], ["amount", "Amount owed", "number"], ["reason", "What the money is for", "textarea", "unpaid invoice #1042 for website design services delivered on 1 March"], ["days", "Days to pay", "number", "14"]],
      r: function (v) { return v.you + "\n" + T(v.youAddr) + "\n\n" + DATE() + "\n\n" + T(v.them) + "\n" + T(v.themAddr) + "\n\nRE: FORMAL DEMAND FOR PAYMENT — " + money(+v.amount) + "\n\nDear " + T(v.them) + ",\n\nThis letter is a formal demand for payment of " + money(+v.amount) + " owed to me for " + T(v.reason) + ".\n\nDespite previous requests, this amount remains unpaid. Please pay the full amount within " + T(v.days) + " days of the date of this letter.\n\nIf payment is not received by that date, I intend to pursue all available remedies without further notice, which may include filing a claim in small claims court and seeking interest and costs as permitted by law.\n\nI would prefer to resolve this without court. If you believe this amount is not owed, please respond in writing within the same period explaining why.\n\nSincerely,\n\n\n" + T(v.you); } },
    cease: { t: "Cease and Desist Letter", f: [["you", "Your name / business"], ["them", "Recipient name"], ["conduct", "Conduct that must stop", "textarea", "copying and publishing my original photographs on your website without permission"], ["right", "Your right being violated", "text", "copyright in the photographs"], ["days", "Days to comply", "number", "10"]],
      r: function (v) { return DATE() + "\n\nTo: " + T(v.them) + "\n\nRE: DEMAND TO CEASE AND DESIST\n\nDear " + T(v.them) + ",\n\nIt has come to my attention that you have been " + T(v.conduct) + ". This conduct violates my " + T(v.right) + ".\n\nI hereby demand that you immediately:\n  1. Cease and desist from the conduct described above;\n  2. Remove or destroy any materials resulting from it; and\n  3. Confirm in writing within " + T(v.days) + " days that you have complied.\n\nIf you fail to comply, I am prepared to take further action to protect my rights, which may include seeking an injunction, damages and costs.\n\nNothing in this letter waives any of my rights or remedies, all of which are expressly reserved.\n\nSincerely,\n\n\n" + T(v.you); } },
    nda: { t: "Mutual Non-Disclosure Agreement", f: [["a", "Party A (name)"], ["b", "Party B (name)"], ["purpose", "Purpose of sharing", "text", "evaluating a potential business relationship"], ["years", "Confidentiality period (years)", "number", "3"], ["law", "Governing law (state/province/country)"]],
      r: function (v) { return "MUTUAL NON-DISCLOSURE AGREEMENT\n\nThis Agreement is made on " + DATE() + " between " + T(v.a) + " and " + T(v.b) + " (each a \"Party\").\n\n1. PURPOSE. The Parties wish to share confidential information for the purpose of " + T(v.purpose) + " (the \"Purpose\").\n\n2. CONFIDENTIAL INFORMATION means any non-public business, technical, financial or personal information disclosed by one Party to the other, in any form, that is marked confidential or would reasonably be understood to be confidential.\n\n3. OBLIGATIONS. Each Party will (a) use the other's Confidential Information only for the Purpose; (b) not disclose it to anyone except employees or advisers who need to know it and are bound by similar obligations; and (c) protect it with at least reasonable care.\n\n4. EXCLUSIONS. Obligations do not apply to information that is or becomes public through no fault of the recipient, was already lawfully known to the recipient, is independently developed, or is lawfully received from a third party. Disclosure required by law is permitted with prompt notice where lawful.\n\n5. TERM. These obligations last " + T(v.years) + " years from the date of disclosure.\n\n6. RETURN. On request, each Party will return or destroy the other's Confidential Information.\n\n7. NO LICENCE. No rights or licences are granted except as stated here.\n\n8. REMEDIES. Unauthorised disclosure may cause irreparable harm, and the disclosing Party may seek injunctive relief in addition to other remedies.\n\n9. GOVERNING LAW. This Agreement is governed by the laws of " + T(v.law) + ".\n\n\n_____________________          _____________________\n" + T(v.a) + "                  " + T(v.b) + "\nDate:                           Date:"; } },
    service: { t: "Freelance / Service Agreement", f: [["client", "Client name"], ["provider", "Service provider name"], ["scope", "Services / deliverables", "textarea", "Design and build a 5-page responsive website"], ["fee", "Total fee", "number"], ["schedule", "Payment schedule", "text", "50% upfront, 50% on delivery"], ["deadline", "Delivery date", "date"], ["law", "Governing law"]],
      r: function (v) { return "SERVICE AGREEMENT\n\nDate: " + DATE() + "\nClient: " + T(v.client) + "\nService Provider: " + T(v.provider) + "\n\n1. SERVICES. The Provider will deliver: " + T(v.scope) + ".\n\n2. DELIVERY. Services will be delivered by " + T(v.deadline) + ", subject to timely client feedback and materials.\n\n3. FEES. The Client will pay " + money(+v.fee) + " as follows: " + T(v.schedule) + ". Invoices are due within 14 days. Late amounts may bear interest as permitted by law.\n\n4. CHANGES. Work outside the scope above requires written agreement and may incur additional fees.\n\n5. OWNERSHIP. On full payment, the Provider assigns to the Client all rights in the final deliverables, excluding the Provider's pre-existing tools and know-how, which are licensed to the Client for use with the deliverables.\n\n6. CONFIDENTIALITY. Each party will keep the other's non-public information confidential.\n\n7. INDEPENDENT CONTRACTOR. The Provider is an independent contractor, not an employee.\n\n8. WARRANTY & LIABILITY. Services will be performed with reasonable skill and care. Each party's total liability is limited to the fees paid under this Agreement, except for breach of confidentiality or wilful misconduct.\n\n9. TERMINATION. Either party may terminate on 14 days' written notice. The Client will pay for work performed up to termination.\n\n10. GOVERNING LAW. " + T(v.law) + ".\n\n\nClient: _____________________   Provider: _____________________"; } },
    lease: { t: "Residential Lease Summary (Key Terms)", f: [["landlord", "Landlord"], ["tenant", "Tenant(s)"], ["address", "Rental address"], ["rent", "Monthly rent", "number"], ["deposit", "Security deposit", "number"], ["start", "Start date", "date"], ["end", "End date", "date"], ["utilities", "Utilities paid by tenant", "text", "Electricity, internet"]],
      r: function (v) { return "RESIDENTIAL LEASE — SUMMARY OF KEY TERMS\n(Attach to, but do not replace, the full lease required by local law.)\n\nLandlord: " + T(v.landlord) + "\nTenant(s): " + T(v.tenant) + "\nPremises: " + T(v.address) + "\nTerm: " + T(v.start) + " to " + T(v.end) + "\nRent: " + money(+v.rent) + " per month, due on the 1st\nSecurity deposit: " + money(+v.deposit) + " (held and returned as required by law)\nUtilities paid by Tenant: " + T(v.utilities) + "\n\nRepairs: Tenant reports repairs in writing; Landlord maintains the premises in habitable condition.\nEntry: Landlord gives notice before entry except in emergencies, as required by law.\nPets / smoking / subletting: as stated in the full lease.\nMove-in inspection completed on: ________\n\nLandlord: __________________   Tenant: __________________"; } },
    deposit: { t: "Security-Deposit Return Demand", f: [["you", "Tenant name"], ["landlord", "Landlord name"], ["address", "Rental address"], ["amount", "Deposit amount", "number"], ["moveout", "Move-out date", "date"], ["forward", "Your forwarding address"]],
      r: function (v) { return DATE() + "\n\nTo: " + T(v.landlord) + "\n\nRE: Return of security deposit — " + T(v.address) + "\n\nDear " + T(v.landlord) + ",\n\nI vacated the above property on " + T(v.moveout) + " and returned the keys. My security deposit of " + money(+v.amount) + " has not been returned, and I have not received an itemised statement of any deductions.\n\nLocal law requires a landlord to return the deposit, or provide an itemised list of lawful deductions, within a set period after move-out. Please return the full deposit, or a written itemised statement with the balance, to the forwarding address below within 14 days.\n\nForwarding address: " + T(v.forward) + "\n\nIf I do not receive the deposit or a lawful statement, I intend to file a claim in small claims court, where penalties may apply for wrongful withholding.\n\nSincerely,\n\n" + T(v.you); } },
    sale: { t: "Bill of Sale", f: [["seller", "Seller"], ["buyer", "Buyer"], ["item", "Item description (make, model, serial/VIN)", "textarea"], ["price", "Price", "number"], ["asis", "Condition", "text", "Sold as-is, with no warranties"]],
      r: function (v) { return "BILL OF SALE\n\nDate: " + DATE() + "\n\nFor the sum of " + money(+v.price) + ", receipt of which is acknowledged, " + T(v.seller) + " (\"Seller\") sells and transfers to " + T(v.buyer) + " (\"Buyer\") the following property:\n\n" + T(v.item) + "\n\nThe Seller states that they are the lawful owner of the property, that it is free of liens and encumbrances, and that they have the right to sell it.\n\nCondition: " + T(v.asis) + ".\n\nSeller signature: ___________________\nBuyer signature: ___________________"; } },
    note: { t: "Promissory Note", f: [["borrower", "Borrower"], ["lender", "Lender"], ["amount", "Principal amount", "number"], ["rate", "Annual interest rate (%)", "number", "5"], ["due", "Final due date", "date"], ["pay", "Repayment terms", "text", "12 equal monthly payments starting next month"]],
      r: function (v) { return "PROMISSORY NOTE\n\nDate: " + DATE() + "\nPrincipal: " + money(+v.amount) + "\n\nFor value received, " + T(v.borrower) + " (\"Borrower\") promises to pay to " + T(v.lender) + " (\"Lender\") the principal sum of " + money(+v.amount) + " with interest at " + T(v.rate) + "% per year on the unpaid balance.\n\nRepayment: " + T(v.pay) + ", with the full balance due no later than " + T(v.due) + ".\n\nPrepayment is allowed without penalty. If any payment is more than 15 days late, the Lender may declare the full balance due. The Borrower agrees to pay reasonable collection costs as permitted by law.\n\nBorrower: ___________________   Date: ________\nWitness: ___________________"; } },
    poa: { t: "Power of Attorney — Planning Worksheet", f: [["you", "Your name (principal)"], ["agent", "Agent you trust"], ["alt", "Alternate agent"], ["powers", "Powers to grant", "textarea", "Banking, paying bills, managing investments, dealing with government agencies"], ["when", "When it takes effect", "text", "Immediately and continues if I lose capacity"]],
      r: function (v) { return "POWER OF ATTORNEY — PLANNING WORKSHEET\n(Use this to prepare for your lawyer or your jurisdiction's official form. It is not itself a valid power of attorney.)\n\nPrincipal: " + T(v.you) + "\nAgent (attorney-in-fact): " + T(v.agent) + "\nAlternate agent: " + T(v.alt) + "\nPowers: " + T(v.powers) + "\nEffective: " + T(v.when) + "\n\nLimits / special instructions: ______________________\nShould the agent be compensated? ______\nWho should receive copies? ______\n\nNext steps: obtain the official form for your state/province/country, sign before the required witnesses or notary, and give copies to your agent and bank."; } },
    refund: { t: "Refund / Chargeback Request", f: [["you", "Your name"], ["merchant", "Merchant"], ["order", "Order / reference number"], ["amount", "Amount", "number"], ["date", "Purchase date", "date"], ["problem", "What went wrong", "textarea", "The item never arrived and the tracking number is invalid."]],
      r: function (v) { return DATE() + "\n\nTo: " + T(v.merchant) + " — Customer Service\n\nRE: Refund request — Order " + T(v.order) + "\n\nOn " + T(v.date) + " I paid " + money(+v.amount) + " for order " + T(v.order) + ". " + T(v.problem) + "\n\nUnder your terms and applicable consumer-protection law, I request a full refund of " + money(+v.amount) + " to my original payment method within 10 days.\n\nIf this is not resolved, I will dispute the charge with my card issuer and file a complaint with the relevant consumer-protection authority.\n\nThank you,\n" + T(v.you); } },
    data: { t: "Personal Data Access Request (GDPR / CCPA)", f: [["you", "Your full name"], ["email", "Email linked to your account", "email"], ["org", "Organisation"], ["law", "Law relied on", "text", "Article 15 GDPR / California Consumer Privacy Act"], ["delete", "Also request deletion? (yes/no)", "text", "no"]],
      r: function (v) { return DATE() + "\n\nTo: Data Protection Officer, " + T(v.org) + "\n\nRE: Request for access to personal data\n\nUnder " + T(v.law) + ", I request:\n  1. Confirmation of whether you process my personal data;\n  2. A copy of all personal data you hold about me;\n  3. The purposes of processing, categories of data, recipients, retention periods and the source of the data;\n  4. Whether my data has been sold or shared for advertising, and with whom." + (/^y/i.test(v.delete) ? "\n  5. Deletion of my personal data where no legal exception applies." : "") + "\n\nIdentifying details: " + T(v.you) + ", " + T(v.email) + ".\n\nPlease respond within the statutory period (generally one month under GDPR or 45 days under CCPA).\n\nSincerely,\n" + T(v.you); } },
    reference: { t: "Employment Verification / Reference Request", f: [["you", "Your name"], ["employer", "Former employer"], ["title", "Job title"], ["from", "Start date", "date"], ["to", "End date", "date"], ["send", "Send to (name/organisation)"]],
      r: function (v) { return DATE() + "\n\nTo: Human Resources, " + T(v.employer) + "\n\nRE: Request for employment verification\n\nI was employed by " + T(v.employer) + " as " + T(v.title) + " from " + T(v.from) + " to " + T(v.to) + ". I request a written confirmation of my dates of employment and job title, to be sent to " + T(v.send) + ".\n\nI authorise you to release this information for that purpose.\n\nThank you,\n" + T(v.you); } }
  };
  var docForm = $("#docForm");
  if (docForm) {
    var curDoc = null, prev = $("#docPreview");
    var render = function () { var v = {}; $$("[name]", docForm).forEach(function (el) { v[el.name] = el.value; }); prev.textContent = DOCS[curDoc].r(v); };
    var pick = function (key) {
      if (!DOCS[key]) key = "demand"; curDoc = key;
      $$(".doc-btn").forEach(function (b) { b.classList.toggle("active", b.getAttribute("data-doc") === key); });
      docForm.innerHTML = "<h2>" + esc(DOCS[key].t) + "</h2>" + DOCS[key].f.map(function (x) {
        var type = x[2] || "text", val = esc(x[3] || "");
        return "<label>" + esc(x[1]) + (type === "textarea" ? '<textarea name="' + x[0] + '" rows="3">' + val + "</textarea>" : '<input type="' + type + '" name="' + x[0] + '" value="' + val + '">') + "</label>";
      }).join("") + '<p class="tiny">Fill in the fields — the preview updates as you type.</p>';
      render();
    };
    docForm.addEventListener("input", render);
    $$(".doc-btn").forEach(function (b) { b.addEventListener("click", function () { pick(b.getAttribute("data-doc")); history.replaceState(null, "", "#" + b.getAttribute("data-doc")); }); });
    pick(location.hash.slice(1));
    var dl = function (ext, mime) { var a = document.createElement("a"), body = ext === "doc" ? "<html><body><pre style=\"font-family:Georgia;font-size:12pt;white-space:pre-wrap\">" + esc(prev.textContent) + "</pre></body></html>" : prev.textContent; a.href = URL.createObjectURL(new Blob([body], { type: mime })); a.download = DOCS[curDoc].t.replace(/[^a-z0-9]+/gi, "-").toLowerCase() + "." + ext; a.click(); };
    $("#docCopy").addEventListener("click", function () { navigator.clipboard && navigator.clipboard.writeText(prev.textContent); this.textContent = "Copied!"; var b = this; setTimeout(function () { b.textContent = "Copy"; }, 1500); });
    $("#docTxt").addEventListener("click", function () { dl("txt", "text/plain"); });
    $("#docDoc").addEventListener("click", function () { dl("doc", "application/msword"); });
    $("#docPrint").addEventListener("click", function () { window.print(); });
  }

  /* ---------- Legal Issue Navigator ---------- */
  var NAV = {
    "Personal Injury": { g: "personal-injury", s: ["Car / vehicle accident", "Slip, trip or fall", "Injured at work", "Medical error", "Dog bite / other"], a: ["Get medical treatment and keep every record", "Do not give a recorded statement to the other insurer", "Check the limitation period for injury claims"], t: [["Settlement estimator", "calculators.html#settlement"], ["Demand letter", "documents.html#demand"]] },
    "Family & Divorce": { g: "family-divorce", s: ["Starting a divorce / separation", "Custody or parenting time", "Child or spousal support", "Domestic violence / safety", "Dividing property"], a: ["If safety is at risk, contact emergency services or seek a protection order", "Gather 3 years of financial records", "Consider mediation before litigation"], t: [["Deadline counter", "calculators.html#deadline"], ["Legal aid finder", "legal-aid.html"]] },
    "Employment": { g: "employment", s: ["Fired / laid off", "Unpaid wages or overtime", "Discrimination or harassment", "Severance offer", "Workplace injury"], a: ["Write a timeline with dates and witnesses", "Do not sign a severance agreement before review", "Check short agency filing deadlines"], t: [["Wages interest", "calculators.html#interest"], ["Reference request", "documents.html#reference"]] },
    "Housing / Landlord-Tenant": { g: "landlord-tenant", s: ["Eviction notice or court papers", "Repairs not done", "Deposit not returned", "Rent increase", "Landlord problem tenant"], a: ["Respond to any court papers immediately", "Put requests in writing and keep copies", "Photograph the property's condition"], t: [["Deposit demand", "documents.html#deposit"], ["Rent checker", "calculators.html#rent"]] },
    "Immigration": { g: "immigration", s: ["Work or study visa", "Family sponsorship", "Permanent residence / citizenship", "Removal or deportation", "Asylum / refugee"], a: ["Use only official forms and fee schedules", "Track status expiry dates", "Verify any adviser is licensed"], t: [["Deadline counter", "calculators.html#deadline"], ["Legal aid finder", "legal-aid.html"]] },
    "Criminal Defense": { g: "criminal-defense", s: ["Arrested or charged", "Police want to question me", "Court date coming up", "Clearing a record", "Bail / release conditions"], a: ["Exercise your right to remain silent and ask for a lawyer", "Never miss a court date", "Stay off social media about the case"], t: [["Know-your-rights quiz", "quiz.html"], ["Legal aid finder", "legal-aid.html"]] },
    "Business & Contracts": { g: "business-contracts", s: ["Client will not pay", "Contract dispute", "Starting a business", "Need an NDA or agreement", "Partner / co-founder dispute"], a: ["Collect the contract and all written communications", "Send a formal demand with a deadline", "Consider mediation before court"], t: [["NDA", "documents.html#nda"], ["Service agreement", "documents.html#service"]] },
    "Wills & Estates": { g: "wills-estates", s: ["Making a will", "Power of attorney", "Someone died — probate", "Contesting a will", "Setting up a trust"], a: ["List assets, debts and beneficiaries", "Choose executor and guardians", "Check signing and witnessing rules"], t: [["POA worksheet", "documents.html#poa"], ["Dictionary", "dictionary.html"]] },
    "Consumer & Debt": { g: "consumer-debt", s: ["Refund refused", "Debt collector calls", "Scam or fraud", "Credit report error", "Being sued for a debt"], a: ["Make your complaint in writing", "Ask collectors to validate the debt", "Report scams to your bank immediately"], t: [["Refund request", "documents.html#refund"], ["Small-claims calculator", "calculators.html#smallclaims"]] },
    "Traffic / DUI": { g: "traffic-dui", s: ["Speeding / traffic ticket", "DUI / impaired driving", "Licence suspension", "Accident ticket", "Commercial licence"], a: ["Do not just pay — check points and insurance impact", "Request disclosure of the evidence", "For DUI, request the licence hearing quickly"], t: [["Deadline counter", "calculators.html#deadline"], ["Fee comparison", "calculators.html#fees"]] },
    "Intellectual Property": { g: "intellectual-property", s: ["Someone copied my work", "I received a cease & desist", "Protecting a brand name", "Freelancer ownership", "DMCA takedown"], a: ["Save evidence with URLs and dates", "Check who owns the rights in writing", "Search trademark databases before branding"], t: [["Cease & desist", "documents.html#cease"], ["NDA", "documents.html#nda"]] },
    "Privacy & Data": { g: "privacy-data", s: ["Data breach", "Get or delete my data", "Online harassment", "Defamation", "AI / tracking concerns"], a: ["Change passwords and enable 2FA", "Send a data-access request", "Preserve evidence before it is deleted"], t: [["Data request", "documents.html#data"], ["Cease & desist", "documents.html#cease"]] }
  };
  var wiz = $("#navigator");
  if (wiz) {
    var st = { area: params.get("area") || "", sit: "", urg: "", loc: "" }, step = st.area && NAV[st.area] ? 1 : 0;
    var opts = function (list, key) { return '<div class="opt-grid">' + list.map(function (o) { return '<label class="opt"><input type="radio" name="w" value="' + esc(o) + '"' + (st[key] === o ? " checked" : "") + "><span>" + esc(o) + "</span></label>"; }).join("") + "</div>"; };
    var draw = function () {
      var html = '<div class="progress"><span style="width:' + ((Math.min(step, 4) + 1) * 20) + '%"></span></div><p class="step-label">Step ' + Math.min(step + 1, 5) + " of 5</p>";
      if (step === 0) html += "<h2>What area is your issue in?</h2>" + opts(Object.keys(NAV), "area");
      else if (step === 1) html += "<h2>Which best describes your situation?</h2>" + opts(NAV[st.area].s, "sit");
      else if (step === 2) html += "<h2>How urgent is it?</h2>" + opts(["Court date or deadline within 7 days", "Within the next month", "Within a few months", "No deadline — just exploring"], "urg");
      else if (step === 3) html += "<h2>Where are you?</h2>" + opts(["United States", "Canada", "United Kingdom", "India", "Australia", "Other"], "loc");
      else {
        var n = NAV[st.area], urgent = /7 days|month/.test(st.urg);
        var summary = st.area + " — " + st.sit + ". Urgency: " + st.urg + ". Location: " + st.loc + ".";
        store.set("sl-nav-summary", summary);
        html += "<h2>Your smart next steps</h2><p class=\"muted\">" + esc(summary) + "</p><div class=\"plan\">" +
          (urgent ? "<p><b>&#9888; Time-sensitive:</b> because you have a near deadline, contact a lawyer or legal-aid service today. Missing a court date or filing window can cost you your rights.</p>" : "") +
          "<ol>" + n.a.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ol>" +
          '<p><b>Read:</b> <a href="' + ROOT + "guides/" + n.g + '.html">Full guide: ' + esc(st.area) + "</a></p>" +
          "<p><b>Use:</b> " + n.t.map(function (x) { return '<a class="chip" href="' + ROOT + x[1] + '">' + esc(x[0]) + "</a>"; }).join(" ") + "</p>" +
          '<p><b>Low income?</b> <a href="' + ROOT + 'legal-aid.html">Find free legal aid in ' + esc(st.loc) + "</a>.</p></div>" +
          '<div class="inline-cta"><p><b>Want a professional opinion?</b> Send this summary for a free case review.</p><a class="btn btn-gold" href="' + ROOT + "free-case-review.html?from=navigator&area=" + encodeURIComponent(st.area) + '">Get my free case review</a></div>';
      }
      html += '<div class="msf-nav">' + (step > 0 ? '<button type="button" class="btn btn-ghost" id="wBack">&larr; Back</button>' : "") + (step === 4 ? '<button type="button" class="btn btn-ghost" id="wRestart">Start over</button>' : "") + "</div>";
      wiz.innerHTML = html;
      $$('input[name="w"]', wiz).forEach(function (r) {
        r.addEventListener("change", function () {
          var key = ["area", "sit", "urg", "loc"][step]; st[key] = r.value; if (step === 0) st.sit = "";
          setTimeout(function () { step++; draw(); wiz.scrollIntoView({ behavior: "smooth", block: "start" }); }, 150);
        });
      });
      var b = $("#wBack"); if (b) b.addEventListener("click", function () { step--; draw(); });
      var rs = $("#wRestart"); if (rs) rs.addEventListener("click", function () { step = 0; st = { area: "", sit: "", urg: "", loc: "" }; draw(); });
    };
    draw();
  }

  /* ---------- Quiz ---------- */
  var QUIZ = [
    ["A police officer asks to search your car without a warrant. In most common-law countries you…", ["Must always agree", "Can say you do not consent", "Must pay a fee to refuse", "Lose your licence if you refuse"], 1, "You can calmly say you do not consent. Police may still search if they have legal authority, but your refusal preserves your right to challenge it later."],
    ["Your landlord wants you out. Can they change the locks without a court process?", ["Yes, if rent is late", "Yes, with 24 hours' notice", "Generally no — 'self-help' evictions are illegal in most places", "Only on weekends"], 2, "Most jurisdictions require a legal eviction process; lock-outs and utility shut-offs are usually unlawful."],
    ["What is a limitation period?", ["A cap on damages", "The deadline to start a lawsuit", "The time a judge has to decide", "A probation term"], 1, "Miss it and your claim is usually barred forever, no matter how strong it is."],
    ["A contingency fee means…", ["You pay hourly in advance", "The lawyer is paid a percentage only if you recover money", "The court pays your lawyer", "A fixed fee for any case"], 1, "Common in injury and some employment cases — always ask how costs are handled."],
    ["Who usually owns copyright in work a freelancer creates for a client, with no written agreement?", ["The client", "The freelancer", "The government", "Whoever paid the most"], 1, "Without a written assignment, the creator often keeps copyright. Put ownership in the contract."],
    ["A debt collector calls repeatedly. In many countries you can…", ["Be arrested for not paying", "Request written validation of the debt", "Be forced to pay by phone", "Lose your job automatically"], 1, "Collectors generally must verify a disputed debt and may not harass or deceive you."],
    ["Is an electronic signature legally valid for most contracts?", ["No, never", "Only for amounts under $100", "Yes, in most countries for most contracts", "Only if notarised"], 2, "E-signature laws recognise them for most agreements, with exceptions such as some wills and property transfers."],
    ["Paying a traffic ticket usually…", ["Has no effect on your record", "Counts as a guilty plea", "Gets the ticket dismissed", "Lowers your insurance"], 1, "It is typically a conviction that can add points and raise premiums."],
    ["What does a power of attorney do?", ["Distributes property after death", "Lets someone act for you while you are alive", "Makes you a lawyer", "Replaces a will"], 1, "A will works after death; a power of attorney covers financial or health decisions while you are alive."],
    ["Under GDPR-style laws you can usually ask a company for…", ["Its trade secrets", "A copy of the personal data it holds about you", "Its employees' salaries", "Free products"], 1, "The right of access lets you see what data is held and how it is used."]
  ];
  var qz = $("#quiz");
  if (qz) {
    var qi = 0, score = 0;
    var qdraw = function () {
      if (qi >= QUIZ.length) {
        qz.innerHTML = "<h2>You scored " + score + "/" + QUIZ.length + "</h2><p>" + (score >= 8 ? "Excellent — you know your rights." : score >= 5 ? "Good foundation. Our guides will fill the gaps." : "Lots to learn — start with our guides.") + '</p><div class="hero-ctas"><a class="btn btn-gold" href="' + ROOT + "contests.html?score=" + score + '">Enter the Know-Your-Rights Challenge</a><button class="btn btn-ghost" id="qAgain">Try again</button><button class="btn btn-ghost" id="qShare">Share</button></div>';
        $("#qAgain").addEventListener("click", function () { qi = 0; score = 0; qdraw(); });
        $("#qShare").addEventListener("click", function () { var t = "I scored " + score + "/10 on the Smart.Legal Know-Your-Rights quiz!"; if (navigator.share) navigator.share({ title: "Smart.Legal quiz", text: t, url: location.href }); else { navigator.clipboard && navigator.clipboard.writeText(t + " " + location.href); this.textContent = "Link copied"; } });
        return;
      }
      var q = QUIZ[qi];
      qz.innerHTML = '<div class="progress"><span style="width:' + ((qi + 1) / QUIZ.length * 100) + '%"></span></div><p class="step-label">Question ' + (qi + 1) + " of " + QUIZ.length + " · Score " + score + "</p><h2>" + esc(q[0]) + '</h2><div class="q-opts">' + q[1].map(function (o, k) { return '<button class="q-opt" data-k="' + k + '">' + esc(o) + "</button>"; }).join("") + '</div><div id="qExp"></div>';
      $$(".q-opt", qz).forEach(function (b) {
        b.addEventListener("click", function () {
          var k = +b.getAttribute("data-k");
          $$(".q-opt", qz).forEach(function (x) { x.disabled = true; if (+x.getAttribute("data-k") === q[2]) x.classList.add("right"); });
          if (k === q[2]) score++; else b.classList.add("wrong");
          $("#qExp").innerHTML = '<p class="plan">' + esc(q[3]) + '</p><button class="btn btn-gold" id="qNext">' + (qi === QUIZ.length - 1 ? "See my score" : "Next question") + " &rarr;</button>";
          $("#qNext").addEventListener("click", function () { qi++; qdraw(); });
        });
      });
    };
    qdraw();
  }
  var sc = params.get("score"), scoreField = $('input[name="score"]');
  if (sc && scoreField) scoreField.value = sc + "/10";
})();
