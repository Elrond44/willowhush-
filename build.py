#!/usr/bin/env python3
"""Willowhush static site generator.
Run:  python3 build.py   ->  writes the finished static site to ./docs (served by GitHub Pages)
No dependencies beyond the Python standard library."""
import shutil, re, html
from practices import SESSIONS, session_player, timer_tool, bodyscan_tool, grounding_tool, kindness_tool, breathe_widget, embed
from ebook import ebook_page, home_feature as ebook_home_feature, promo_card as ebook_promo
from pathlib import Path

ROOT = Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "docs"   # docs/ is what GitHub Pages publishes
SITE = {"name": "Willowhush", "tagline": "Quiet practices for a gentler mind",
        "url": "https://elrond44.github.io/willowhush-/", "desc": "Willowhush is a meditation and mindfulness journal: gentle, practical guides to meditation, breathwork, mindful living, and restful sleep."}

# ---- Ebook checkout -------------------------------------------------------------------------------
# Paste the link to your pay-what-you-want product here (Gumroad, Lemon Squeezy, Ko-fi, Payhip...), e.g.
#   EBOOK_CHECKOUT_URL = "https://yourname.gumroad.com/l/good-vibrations"
# While it is empty, the Ebook page shows a "Checkout coming soon" state and points readers to the free sample.
EBOOK_CHECKOUT_URL = ""
# Optional: if your checkout accepts a pre-filled amount as a query parameter, put its name here and the
# chosen amount is appended (e.g. "...?price=9"). Leave empty to let readers enter the amount at checkout.
EBOOK_PRICE_PARAM = ""

LOGO = '''<svg viewBox="0 0 40 40" aria-hidden="true" fill="none"><circle cx="20" cy="20" r="18.5" stroke="currentColor" stroke-width="1.2" opacity=".55"/><path d="M20 6c0 9-1 18-6 27M20 6c1 8 4 15 10 22M20 6c-2 7-6 12-12 15" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/><circle cx="20" cy="6" r="1.6" fill="currentColor"/></svg>'''

POSTS = [
  {"slug": "body-scan-for-restless-nights", "title": "A body scan for restless nights", "cat": "Sleep & Rest", "img": "post-sleep",
   "alt": "Rumpled linen bedding with a sprig of lavender, lit by moonlight from a tall window",
   "excerpt": "A slow, guided journey through the body to help you unclench and drift toward sleep, with an interactive scan to follow in the dark.",
   "date": "November 1, 2026", "iso": "2026-11-01", "read": "8 min read"},
  {"slug": "tea-ritual", "title": "The tea ritual: one cup, fully tasted", "cat": "Mindful Living", "img": "post-living",
   "alt": "Two hands cupping a speckled ceramic tea bowl on a linen cloth beside eucalyptus leaves",
   "excerpt": "How a single cup of tea, made and drunk with attention, can become a daily moment of rest.",
   "date": "November 1, 2026", "iso": "2026-11-01", "read": "7 min read"},
  {"slug": "loving-kindness", "title": "Loving-kindness: a gentle practice for a softer heart", "cat": "Meditation Basics", "img": "post-kindness",
   "alt": "Two cupped hands holding a small glowing tealight in a dusky lavender room",
   "excerpt": "Four simple phrases, offered in widening circles. A warm, beginner-friendly introduction to metta meditation.",
   "date": "October 31, 2026", "iso": "2026-10-31", "read": "8 min read"},
  {"slug": "grounding-5-4-3-2-1", "title": "5-4-3-2-1: a grounding practice for busy minds", "cat": "Meditation Basics", "img": "post-grounding",
   "alt": "Bare feet resting on soft moss and smooth stones beside a misty forest stream",
   "excerpt": "When your thoughts are racing ahead, your senses can bring you home. A five-step practice you can do anywhere.",
   "date": "October 31, 2026", "iso": "2026-10-31", "read": "7 min read"},
  {"slug": "evening-wind-down", "title": "A 20-minute evening wind-down", "cat": "Sleep & Rest", "img": "post-winddown",
   "alt": "A glowing paper lamp, a closed book and a cup of herbal tea on a wooden stool at dusk",
   "excerpt": "Close the day gently: a simple four-part routine for dimming the lights, setting down your thoughts, and letting rest arrive.",
   "date": "October 30, 2026", "iso": "2026-10-30", "read": "8 min read"},
  {"slug": "mindful-journaling-prompts", "title": "Mindful journaling: 12 prompts for a quieter mind", "cat": "Mindful Living", "img": "post-journal",
   "alt": "An open linen journal with blank pages and a pencil on an oak table beside lavender and a ceramic cup",
   "excerpt": "Five minutes, one page, no rules. Gentle prompts for mornings, evenings, and the hard days in between.",
   "date": "October 30, 2026", "iso": "2026-10-30", "read": "8 min read"},
  {"slug": "the-long-exhale", "title": "The long exhale: a softer breath for anxious moments", "cat": "Breathwork", "img": "post-exhale",
   "alt": "A single white feather floating on still lavender water, ripples spreading outward at twilight",
   "excerpt": "Breathe out a little longer than you breathe in. Why this tiny change feels so settling, and how to practice it.",
   "date": "October 29, 2026", "iso": "2026-10-29", "read": "7 min read"},
  {"slug": "morning-meditation", "title": "A 5-minute morning meditation for beginners", "cat": "Meditation Basics", "img": "post-morning",
   "alt": "A dusky-rose meditation cushion on a woven mat beside a sunlit window, with a steaming cup of tea and a small plant",
   "excerpt": "No special equipment, no empty mind required. A gentle, four-stage practice to set the tone for your whole day.",
   "date": "October 28, 2026", "iso": "2026-10-28", "read": "6 min read"},
  {"slug": "box-breathing", "title": "Box breathing: how to calm your nervous system", "cat": "Breathwork", "img": "post-box",
   "alt": "A cairn of four smooth stones balanced in still lake water at twilight, with soft ripples and misty hills",
   "excerpt": "Four sides, four counts. Why this simple breathing pattern works, and how to use it before stress takes hold.",
   "date": "October 21, 2026", "iso": "2026-10-21", "read": "6 min read"},
  {"slug": "mindful-walking", "title": "Mindful walking: meditation in motion", "cat": "Mindful Living", "img": "post-walking",
   "alt": "A lone walker on a leaf-covered forest path as golden sunbeams slant through mist and moss-covered trees",
   "excerpt": "Reclaim the thousands of steps you take each day. Two ways to turn an ordinary walk into a moving meditation.",
   "date": "October 14, 2026", "iso": "2026-10-14", "read": "7 min read"},
]
SOON = []  # "coming soon" cards: dicts with title, cat, img, alt, excerpt
CATS = ["Meditation Basics", "Mindful Living", "Breathwork", "Sleep & Rest"]
BASE = SITE["url"].rstrip("/")   # absolute site root (no trailing slash) for canonical/OG/sitemap URLs
slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'

def head(title, desc, path, r, img="og-image.jpg", otype="website"):
    full = f"{title} · {SITE['name']}" if title != SITE["name"] else f"{SITE['name']} — {SITE['tagline']}"
    url = f"{BASE}/{path}"
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#3a3148">
<meta property="og:type" content="{otype}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/images/{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(full)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE}/assets/images/{img}">
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{r}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{r}apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="{r}assets/css/style.css">
<script>document.documentElement.classList.remove('no-js')</script>
</head>'''

def header(r, active, hero=False):
    links = [("Home", "index.html"), ("Journal", "blog/index.html"), ("Practice", "practice.html"), ("Guided", "guided.html"), ("Ebook", "ebook.html"), ("About", "about.html"), ("Contact", "contact.html")]
    lis = "".join(f'<li><a href="{r}{h}"{" aria-current=\"page\"" if n==active else ""}>{n}</a></li>' for n, h in links)
    return f'''<body class="{'hero-page' if hero else ''}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header{'' if hero else ' solid'}">
  <nav class="container nav" aria-label="Main">
    <a class="brand" href="{r}index.html">{LOGO}<span>{SITE['name']}</span></a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav-links"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="nav-links">{lis}</ul>
  </nav>
</header>'''

def footer(r, extra_js=False):
    cats = "".join(f'<li><a href="{r}blog/index.html#{slugify(c)}">{c}</a></li>' for c in CATS)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div><a class="brand" href="{r}index.html">{LOGO}<span>{SITE['name']}</span></a>
        <p style="max-width:340px">{SITE['tagline']}. Gentle, practical guides for meditation, breath, and a slower way of being.</p></div>
      <div><h4>Explore</h4><ul><li><a href="{r}index.html">Home</a></li><li><a href="{r}blog/index.html">Journal</a></li><li><a href="{r}practice.html">Practice</a></li><li><a href="{r}guided.html">Guided meditations</a></li><li><a href="{r}ebook.html">Ebook: Good Vibrations</a></li><li><a href="{r}about.html">About</a></li><li><a href="{r}contact.html">Contact</a></li></ul></div>
      <div><h4>Topics</h4><ul>{cats}</ul></div>
    </div>
    <div class="footer-bottom"><span>© 2026 {SITE['name']}. Written with care.</span><span>Breathe in. Breathe out. You're here.</span></div>
  </div>
</footer>
<script src="{r}assets/js/main.js" defer></script>{f'<script src="{r}assets/js/practice.js" defer></script>' if extra_js else ''}
</body></html>'''

def card(p, r, delay=0, soon=False):
    d = f" d{delay}" if delay else ""
    img = f'<div class="card-img"><img src="{r}assets/images/{p["img"]}-sm.webp" alt="{html.escape(p["alt"])}" width="640" height="480" loading="lazy"><span class="tag">{p["cat"]}</span>{"<span class=\"soon-badge\">Coming soon</span>" if soon else ""}</div>'
    if soon:
        return f'<article class="card soon reveal{d}" data-category="{slugify(p["cat"])}">{img}<div class="card-body"><h3>{p["title"]}</h3><p>{p["excerpt"]}</p><div class="meta"><span>In the works</span></div></div></article>'
    return f'<a class="card reveal{d}" href="{r}blog/{p["slug"]}.html" data-category="{slugify(p["cat"])}">{img}<div class="card-body"><h3>{p["title"]}</h3><p>{p["excerpt"]}</p><div class="meta"><time datetime="{p["iso"]}">{p["date"]}</time><span class="dot"></span><span>{p["read"]}</span></div></div></a>'

ICONS = {
 "sit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><circle cx="12" cy="5" r="2.2"/><path d="M12 8v5M6 18c2-1 4-4 6-5 2 1 4 4 6 5M4 20h16"/></svg>',
 "breath": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h7"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15M5 19l7-7"/></svg>',
}

def home():
    r = ""
    cards = "".join(card(p, r, (i % 3) + 1) for i, p in enumerate(POSTS[:6]))
    return head(SITE["name"], SITE["desc"], "", r) + header(r, "Home", hero=True) + f'''
<main id="main">
  <section class="hero" aria-label="Welcome">
    <div class="hero-bg" style="background-image:url(assets/images/hero.webp)" role="img" aria-label="A person sits on a rock beside a misty mountain lake at dawn, the sky glowing lavender and peach"></div>
    <div class="container"><div class="hero-content">
      <span class="eyebrow reveal">A meditation &amp; mindfulness journal</span>
      <h1 class="reveal d1">Come back to <em>this breath,</em> this moment.</h1>
      <p class="lead reveal d2">Willowhush offers quiet practices for a gentler mind: simple meditations, breathwork, and mindful rituals to help you slow down and feel at home in yourself.</p>
      <div class="hero-actions reveal d3"><a class="btn btn-primary" href="#breathe" style="background:var(--cream);color:var(--dusk-deep)">Breathe with me</a><a class="btn btn-ghost" href="blog/index.html">Read the journal →</a></div>
    </div></div>
    <span class="scroll-cue" aria-hidden="true">Scroll</span>
  </section>

  <section class="container" aria-labelledby="intro-h">
    <div class="intro">
      <div class="intro-text reveal">
        <span class="eyebrow">Welcome, friend</span>
        <h2 id="intro-h">Stillness isn't somewhere you go. It's something you return to.</h2>
        <p>Like a willow that bends in the wind without breaking, a mindful life is not rigid or perfect. It is supple. It sways, and it comes back to center.</p>
        <p>Here you'll find warm, plain-spoken guides for real people with full lives: practices you can do in five minutes, explanations without jargon, and gentle encouragement to begin again as many times as you need.</p>
        <a class="btn btn-outline" href="about.html">Our story</a>
      </div>
      <blockquote class="intro-quote reveal d1">“Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor.”<cite>Thich Nhat Hanh</cite></blockquote>
    </div>
    <div class="pillars">
      <div class="pillar reveal">{ICONS['sit']}<h3>Meditation basics</h3><p>Clear, friendly first steps for sitting with yourself, without pressure to empty your mind.</p></div>
      <div class="pillar reveal d1">{ICONS['breath']}<h3>Breathwork</h3><p>Simple breathing patterns that steady your nervous system wherever you are.</p></div>
      <div class="pillar reveal d2">{ICONS['leaf']}<h3>Mindful living</h3><p>Small rituals for walking, eating, resting, and moving through the day with presence.</p></div>
    </div>
  </section>

  <section class="posts" aria-labelledby="posts-h">
    <div class="container">
      <div class="section-head reveal"><div><span class="eyebrow">From the journal</span><h2 id="posts-h" style="margin:0">Fresh practices</h2></div><p>New guides, written slowly. Read one, try it today, and notice what changes.</p></div>
      <div class="grid">{cards}</div>
      <div style="text-align:center;margin-top:3rem" class="reveal"><a class="btn btn-outline" href="blog/index.html">Browse all articles</a></div>
    </div>
  </section>


  <section class="practice-feature" aria-labelledby="pf-h">
    <div class="container">
      <div class="section-head reveal"><div><span class="eyebrow">Practice with us</span><h2 id="pf-h" style="margin:0">Don't just read. Breathe along.</h2></div><p>Interactive tools and guided meditations, right here in your browser. No sign-up, no app, nothing to install.</p></div>
      <div class="feature-duo">
        <a class="feature reveal" href="practice.html">
          <img src="assets/images/post-grounding-sm.webp" srcset="assets/images/post-grounding-sm.webp 640w, assets/images/post-grounding.webp 1152w" sizes="(max-width:960px) 100vw, 50vw" alt="Bare feet resting on soft moss and smooth stones beside a misty forest stream" width="1152" height="864" loading="lazy">
          <div class="feature-body"><span class="eyebrow">Interactive practices</span><h3>The practice room</h3><p>A meditation timer with a gentle bell, a guided body scan, 5-4-3-2-1 grounding, and a loving-kindness flow.</p>
            <ul class="feature-list"><li>Meditation timer</li><li>Body scan</li><li>Grounding</li><li>Loving-kindness</li><li>Breathing circle</li></ul><span class="go">Open the practice room →</span></div>
        </a>
        <a class="feature reveal d1" href="guided.html">
          <img src="assets/video/lake-poster-sm.webp" srcset="assets/video/lake-poster-sm.webp 640w, assets/video/lake-poster.webp 1280w" sizes="(max-width:960px) 100vw, 50vw" alt="A still, misty mountain lake at dawn under a lavender and peach sky" width="1280" height="720" loading="lazy">
          <div class="feature-body"><span class="eyebrow">Guided meditation videos</span><h3>Guided sessions</h3><p>Slow, looping scenes of mist, forest light, candlelight and open sky, with soft spoken or on-screen guidance.</p>
            <ul class="feature-list">{"".join(f"<li>{s['title']} · {s['mins']} min</li>" for s in SESSIONS)}</ul><span class="go">Begin a guided session →</span></div>
        </a>
      </div>
    </div>
  </section>
{ebook_home_feature(r)}
  <section class="breathe" id="breathe" aria-labelledby="breathe-h">
    <div class="container">
      <span class="eyebrow">An interlude</span>
      <h2 id="breathe-h">Breathe with me</h2>
      <p class="sub">Choose a rhythm, press begin, and let the circle lead. Soften your shoulders. There's nowhere else you need to be.</p>
      <div class="breath-stage" data-breathe aria-live="polite">
        <div class="breath-ring r2"></div><div class="breath-ring"></div>
        <div class="breath-circle"></div>
        <span class="breath-label">Ready</span>
        <span class="breath-count"></span>
      </div>
      <div class="breath-controls">
        <div class="pattern-select" role="group" aria-label="Breathing pattern">
          <button data-pattern="box" aria-pressed="true">Box 4·4·4·4</button>
          <button data-pattern="calm" aria-pressed="false">Calm 4·7·8</button>
          <button data-pattern="even" aria-pressed="false">Even 5·5</button>
        </div>
        <button class="btn btn-primary" data-breathe-toggle aria-pressed="false">Begin</button>
      </div>
    </div>
  </section>

  <section class="newsletter" aria-labelledby="nl-h">
    <div class="container"><div class="newsletter-card reveal">
      <span class="eyebrow">The Sunday Stillness letter</span>
      <h2 id="nl-h">A quiet note, once a week</h2>
      <p>One short practice, one reflection, and nothing you'll feel guilty about not reading. Unsubscribe any time.</p>
      <form class="inline-form" data-placeholder="Thank you. This is a preview, so nothing was sent yet, but your seat by the window is saved in spirit." novalidate>
        <label for="nl-email" class="sr-only">Email address</label>
        <input id="nl-email" type="email" name="email" placeholder="you@example.com" required autocomplete="email">
        <button class="btn btn-primary" type="submit">Subscribe</button>
      </form>
      <p class="form-msg" role="status"></p>
      <p class="form-note">Signup is a placeholder for now. No email is stored or sent.</p>
    </div></div>
  </section>
</main>''' + footer(r)

def blog_index():
    r = "../"
    feat = POSTS[0]
    rest = "".join(card(p, r, (i % 3)) for i, p in enumerate(POSTS[1:]))  # featured post is shown above, not repeated
    soon = "".join(card(p, r, (i % 3) + 1, soon=True) for i, p in enumerate(SOON))
    btns = '<button data-filter="all" aria-pressed="true">All</button>' + "".join(f'<button data-filter="{slugify(c)}" aria-pressed="false">{c}</button>' for c in CATS)
    return head("Journal", "Articles on meditation basics, mindful living, breathwork, and sleep from the Willowhush journal.", "blog/", r) + header(r, "Journal") + f'''
<main id="main">
  <header class="page-hero"><div class="container">
    <span class="eyebrow reveal">The journal</span>
    <h1 class="reveal d1">Notes on a slower life</h1>
    <p class="reveal d2">Practical guides and gentle reflections on meditation, breath, rest, and paying attention.</p>
  </div></header>
  <section style="padding-top:2rem"><div class="container">
    <a class="featured reveal" href="{feat['slug']}.html" data-category="{slugify(feat['cat'])}">
      <div class="card-img"><img src="../assets/images/{feat['img']}.webp" alt="{html.escape(feat['alt'])}" width="1152" height="864" style="width:100%;height:100%;object-fit:cover"></div>
      <div class="featured-body"><span class="eyebrow">Featured · {feat['cat']}</span><h2>{feat['title']}</h2><p>{feat['excerpt']}</p><div class="meta"><time datetime="{feat['iso']}">{feat['date']}</time><span class="dot"></span><span>{feat['read']}</span></div></div>
    </a>
    <div class="filters reveal" role="group" aria-label="Filter articles by category">{btns}</div>
    <div class="grid">{rest}{soon}</div>
    <p class="empty-state" hidden style="text-align:center;color:var(--muted)">Nothing here yet. New pieces are on their way.</p>
    <div class="promo-wrap">{ebook_promo(r)}</div>
  </div></section>
</main>
<script>
  // Allow deep links like blog/index.html#breathwork to preselect a filter
  window.addEventListener('DOMContentLoaded',()=>{{const h=location.hash.slice(1);const b=h&&document.querySelector('.filters [data-filter="'+h+'"]');if(b)b.click();}});
</script>''' + footer(r)

def post_page(p):
    r = "../"
    body = (SRC / "posts" / f"{p['slug']}.html").read_text()
    uses_tools = "<!--tool:" in body or 'class="exercise"' in body
    body = re.sub(r"<!--tool:([a-z:]+)-->", lambda m: embed(m.group(1), r), body)
    rel = [x for x in POSTS if x is not p and x["cat"] == p["cat"]] + [x for x in POSTS if x is not p and x["cat"] != p["cat"]]
    others = "".join(card(o, r, i+1) for i, o in enumerate(rel[:3]))
    ld = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BlogPosting","headline":"{p["title"]}","datePublished":"{p["iso"]}","image":"{SITE["url"]}/assets/images/{p["img"]}.webp","author":{{"@type":"Person","name":"Elrond"}},"publisher":{{"@type":"Organization","name":"{SITE["name"]}"}}}}</script>'
    return head(p["title"], p["excerpt"], f"blog/{p['slug']}.html", r, img=f"{p['img']}.webp", otype="article").replace("</head>", ld + "</head>") + header(r, "Journal", hero=True) + f'''
<div class="progress" aria-hidden="true"></div>
<main id="main">
  <article>
    <header class="article-hero">
      <img src="../assets/images/{p['img']}.webp" alt="{html.escape(p['alt'])}" width="1152" height="864">
      <div class="narrow">
        <a class="eyebrow" href="index.html#{slugify(p['cat'])}" style="text-decoration:none">{p['cat']}</a>
        <h1>{p['title']}</h1>
        <div class="meta"><span>By Elrond</span><span class="dot"></span><time datetime="{p['iso']}">{p['date']}</time><span class="dot"></span><span>{p['read']}</span></div>
      </div>
    </header>
    <div class="narrow prose">{body}</div>
    <div class="narrow article-foot">
      <img class="avatar" src="../assets/images/about-sm.webp" alt="Candles glowing on a wooden bench, the Willowhush emblem image">
      <p><strong style="color:var(--dusk-deep)">Written by Elrond</strong><br>Founder of Willowhush. Practicing, forgetting, and beginning again, one breath at a time. <a href="../about.html">More about Willowhush →</a></p>
    </div>
    <div class="narrow">{ebook_promo(r)}</div>
  </article>
  <section class="posts" aria-labelledby="more-h"><div class="container">
    <div class="section-head reveal"><div><span class="eyebrow">Keep reading</span><h2 id="more-h" style="margin:0">More gentle practices</h2></div></div>
    <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">{others}</div>
  </div></section>
</main>''' + footer(r, extra_js=uses_tools)

def about():
    r = ""
    return head("About", "The story behind Willowhush, a meditation and mindfulness journal of quiet practices for a gentler mind.", "about.html", r, img="about.webp") + header(r, "About") + f'''
<main id="main">
  <header class="page-hero"><div class="container">
    <span class="eyebrow reveal">About</span>
    <h1 class="reveal d1">Bend, sway, return.</h1>
    <p class="reveal d2">Willowhush is a small, unhurried corner of the internet for people who want to feel a little more present, and a lot less rushed.</p>
  </div></header>
  <section style="padding-top:2rem"><div class="container about-grid">
    <div class="about-img reveal"><img src="assets/images/about.webp" alt="Beeswax candles of different heights glowing on a low wooden bench beside dried pampas grass and a wool blanket at dusk" width="864" height="1152"></div>
    <div class="reveal d1">
      <span class="eyebrow">Our story</span>
      <h2>Why a willow?</h2>
      <p>A willow tree doesn't resist the wind. It bends deeply, lets the weather move through its branches, and then returns to stillness. That, to us, is what mindfulness looks like in a real life: not an unshakable calm, but a gentle ability to come back.</p>
      <p>Willowhush began as a personal notebook, a place to record the practices that actually helped on hard days: a few slow breaths in a parked car, a walk without headphones, five minutes on a cushion before the house woke up. Over time those notes became guides, and the guides became this journal.</p>
      <p>Everything here is written for beginners and for anyone who has ever felt "bad at meditating." There's no dogma, no upsell, and no expectation of perfection. Just simple, well-researched practices offered with warmth.</p>
      <div class="values">
        <div><h3>Simple</h3><p>Practices you can start today, in minutes, with nothing but your breath.</p></div>
        <div><h3>Grounded</h3><p>Clear explanations, honest about what meditation can and can't do.</p></div>
        <div><h3>Gentle</h3><p>No streaks to protect, no guilt. Beginning again is the practice.</p></div>
        <div><h3>Open</h3><p>Rooted in contemplative traditions, welcoming to every background.</p></div>
      </div>
    </div>
  </div></section>
  <section class="newsletter" aria-label="A gentle note"><div class="container"><div class="newsletter-card reveal">
    <h2>A gentle note</h2>
    <p>Willowhush shares general wellbeing practices and isn't a substitute for medical or mental-health care. If you are struggling, please reach out to a qualified professional or a local support line.</p>
    <a class="btn btn-primary" href="blog/index.html">Start with the journal</a>
  </div></div></section>
</main>''' + footer(r)

def contact():
    r = ""
    return head("Contact", "Get in touch with Willowhush: questions, reflections, and collaboration ideas are all welcome.", "contact.html", r) + header(r, "Contact") + f'''
<main id="main">
  <header class="page-hero"><div class="container">
    <span class="eyebrow reveal">Contact</span>
    <h1 class="reveal d1">Say hello</h1>
    <p class="reveal d2">A question about a practice, a reflection to share, or an idea to explore together. Every note is read slowly.</p>
  </div></header>
  <section style="padding-top:2rem"><div class="container contact-grid">
    <div class="contact-aside reveal">
      <h2>Let's talk, softly.</h2>
      <p>We try to reply within a few days. If your message is about a specific article, include its title so we can find it quickly.</p>
      <ul>
        <li><span>Email</span>hello@willowhush.example</li>
        <li><span>Replies</span>Usually within 3 to 5 days</li>
        <li><span>Elsewhere</span>Social links coming soon</li>
      </ul>
    </div>
    <div class="reveal d1">
      <form class="contact-form" data-placeholder="Thank you for writing. This form is a preview, so your message wasn't sent, but it was received in spirit." novalidate>
        <div class="field"><label for="c-name">Your name</label><input id="c-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required autocomplete="email"></div>
        <div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic"><option>A question about a practice</option><option>Sharing a reflection</option><option>Collaboration</option><option>Something else</option></select></div>
        <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea></div>
        <button class="btn btn-primary" type="submit">Send message</button>
        <p class="form-msg" role="status"></p>
        <p class="form-note">This form is a placeholder. Nothing is sent or stored yet.</p>
      </form>
    </div>
  </div></section>
</main>''' + footer(r)


def practice():
    r = ""
    blocks = [
      ("timer", "Meditation timer", "Sit for as long as you like.", "Choose a length, press begin, and let a soft singing-bowl bell mark the start and the end. Add interval bells if you like a gentle check-in along the way.",
       ["Bells are made in your browser with Web Audio, so turn your volume up a little.", "Your chosen length and interval are remembered on this device.", "The breathing glow in the centre is optional company, not a pace to follow."], timer_tool(), "blog/morning-meditation.html", "A 5-minute morning meditation"),
      ("breathing", "Breathing circle", "Let the circle lead the breath.", None, None, None, "blog/the-long-exhale.html", "The long exhale"),
      ("body-scan", "Guided body scan", "Travel slowly from crown to toes.", "Eleven gentle stops, each highlighted on the figure as you go. Let it run at your own pace or step through by hand; switch on read-aloud to close your eyes.",
       ["Use the arrows (or your keyboard's arrow keys) to move between areas.", "Choose how long to rest in each place.", "A quiet chime marks each new area."], bodyscan_tool(), "blog/body-scan-for-restless-nights.html", "A body scan for restless nights"),
      ("grounding", "5-4-3-2-1 grounding", "Come back through your senses.", "When your thoughts are racing, name five things you see, four you feel, three you hear, two you smell, and one you taste. Tap once for each thing you notice.",
       ["Typing is optional, and nothing you type is saved or sent.", "There's no wrong answer; small things count.", "Skip any sense that isn't available to you."], grounding_tool(), "blog/grounding-5-4-3-2-1.html", "5-4-3-2-1: a grounding practice"),
      ("loving-kindness", "Loving-kindness flow", "Warm wishes, in widening circles.", "Traditional metta phrases appear slowly, one at a time, as you offer them to yourself, a loved one, a neutral person, someone difficult, and finally all beings.",
       ["Choose the full journey, or one circle.", "Write your own phrases; they're saved only on this device.", "Read-aloud uses your browser's built-in voice."], kindness_tool(), "blog/loving-kindness.html", "Loving-kindness for beginners"),
    ]
    nav = "".join(f'<a href="#{b[0]}">{b[1]}</a>' for b in blocks) + '<a href="guided.html">Guided videos →</a>'
    out = []
    for i, (bid, name, h, desc, tips, tool, link, ltitle) in enumerate(blocks):
        if bid == "breathing":
            out.append(f'''<section class="breathe practice-block" id="breathing" aria-labelledby="breathing-h"><div class="container">
      <span class="eyebrow">{name}</span><h2 id="breathing-h">{h}</h2>
      <p class="sub">Four rhythms to choose from. Box breathing steadies, 4·7·8 and the long exhale soften. Breathe through your nose if you can, and stop if you feel light-headed.</p>
      {breathe_widget()}
      <p style="margin-top:2rem;font-size:.92rem"><a href="{link}" style="color:var(--peach)">Read: {ltitle} →</a></p></div></section>''')
            continue
        lis = "".join(f"<li>{t}</li>" for t in tips)
        out.append(f'''<section class="practice-block" id="{bid}" aria-labelledby="{bid}-h"><div class="container practice-grid">
      <div class="practice-copy reveal"><span class="eyebrow">{name}</span><h2 id="{bid}-h">{h}</h2><p>{desc}</p><ul>{lis}</ul><p class="more"><a href="{link}">Read: {ltitle} →</a></p></div>
      <div class="reveal d1">{tool}</div></div></section>''')
    return head("Practice", "Interactive meditation tools from Willowhush: a meditation timer with a gentle bell, a guided body scan, 5-4-3-2-1 grounding, a loving-kindness flow, and a breathing circle.", "practice.html", r, img="post-grounding.webp") + header(r, "Practice") + f'''
<main id="main">
  <header class="page-hero"><div class="container">
    <span class="eyebrow reveal">The practice room</span>
    <h1 class="reveal d1">Practice, right here</h1>
    <p class="reveal d2">Gentle interactive tools to sit, breathe, scan and soften, in a few quiet minutes. Everything runs in your browser; nothing is tracked or sent.</p>
    <nav class="practice-nav reveal d3" aria-label="Practices on this page">{nav}</nav>
  </div></header>
  {"".join(out)}
  <section class="newsletter" aria-label="Guided meditations"><div class="container"><div class="newsletter-card reveal">
    <span class="eyebrow">Prefer to be guided?</span><h2>Guided meditation videos</h2>
    <p>Slow, looping nature scenes with soft captions and optional spoken guidance: a three-minute breath, a body scan, an evening wind-down, and loving-kindness.</p>
    <a class="btn btn-primary" href="guided.html">Begin a guided session</a>
  </div></div></section>
</main>''' + footer(r, extra_js=True)

def guided():
    r = ""
    sess = "".join(session_player(s, r) for s in SESSIONS)
    return head("Guided meditations", "Free guided meditation videos from Willowhush: a 3-minute breath, a 5-minute body scan, an evening wind-down, and loving-kindness, with soft captions and optional voice.", "guided.html", r, img="og-image.jpg") + header(r, "Guided") + f'''
<main id="main">
  <header class="page-hero"><div class="container">
    <span class="eyebrow reveal">Guided meditations</span>
    <h1 class="reveal d1">Sit with us a while</h1>
    <p class="reveal d2">Choose a session, press begin, and let the scene and the words lead. Gentle captions appear as you go; switch the voice on if you'd like to close your eyes.</p>
  </div></header>
  <section style="padding-top:2rem"><div class="container">
    <div class="sessions">{sess}</div>
  </div></section>
  <section class="posts" aria-label="About these sessions" style="padding:4rem 0"><div class="container">
    <p class="guided-note">Headphones help. The voice is a calm, computer-generated narrator, and the footage was generated for Willowhush. If you'd rather keep the screen still, your device's reduced-motion setting is respected: the scene pauses and only the captions change. These sessions are for everyday wellbeing and aren't a substitute for medical or mental-health care.</p>
    <p style="text-align:center;margin-top:2rem"><a class="btn btn-outline" href="practice.html">Explore interactive practices</a></p>
  </div></section>
</main>''' + footer(r, extra_js=True)

def build():
    if DIST.exists(): shutil.rmtree(DIST)
    shutil.copytree(SRC / "assets", DIST / "assets")
    for f in ["favicon.svg", "favicon-32.png", "apple-touch-icon.png", "robots.txt"]:
        if (SRC / f).exists(): shutil.copy(SRC / f, DIST / f)
    (DIST / "blog").mkdir()
    pages = {"index.html": home(), "practice.html": practice(), "guided.html": guided(), "ebook.html": ebook_page("", EBOOK_CHECKOUT_URL, head, header, footer, BASE, EBOOK_PRICE_PARAM), "about.html": about(), "contact.html": contact(), "blog/index.html": blog_index()}
    for p in POSTS: pages[f"blog/{p['slug']}.html"] = post_page(p)
    for path, content in pages.items(): (DIST / path).write_text(content)
    urls = "".join(f"<url><loc>{BASE}/{p.replace('index.html','')}</loc></url>" for p in pages)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    # Safety net: the only PDF allowed on the public site is the free sample (the full ebook is sold, never published)
    stray = [p for p in DIST.rglob("*.pdf") if p.name != "good-vibrations-sample.pdf"]
    if stray: raise SystemExit(f"Refusing to publish PDFs other than the ebook sample: {stray}")
    (DIST / ".nojekyll").write_text("")   # serve files as-is on GitHub Pages
    print("Built", len(pages), "pages ->", DIST)

if __name__ == "__main__": build()
