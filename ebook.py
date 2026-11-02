"""Willowhush: the 'Good Vibrations' ebook page, home-page feature and journal promo card.
Imported by build.py. The checkout link itself lives in build.py (EBOOK_CHECKOUT_URL)."""
import html, json

EBOOK = {
  "title": "Good Vibrations",
  "subtitle": "The Layers of Personal Vibration: How They Work & How to Raise Yours",
  "kicker": "A practical, science-honest guide",
  "pages": 52, "format": "PDF", "edition": "First edition, 2026",
  "sample": "assets/ebook/good-vibrations-sample.pdf",
  "sample_pages": "pages 1 to 9 of the book (cover, contents, introduction and all of Chapter 1), plus a closing page",
  "sample_mb": "1.2 MB",
  "suggested": [5, 9, 15], "default": 9, "min": 1, "currency": "$",
  "cover_alt": "Cover of Good Vibrations: a person meditating on still water at sunset, ripples spreading outward beneath glowing waves of light",
}

# (number, title, page in the book, one-line summary written from the chapter)
CHAPTERS = [
  (1, "What Vibration Really Is", 5, "Frequency, amplitude, resonance and entrainment: the real physics, and exactly where the metaphor begins."),
  (2, "What People Mean by \u201cPersonal Vibration\u201d", 10, "A friendly map of a popular idea, the five-layer model, and three evidence labels to read everything else by."),
  (3, "The Physical Layer: Your Body\u2019s Rhythms", 15, "Sleep, movement and food: the foundation with the strongest evidence and the fastest feedback."),
  (4, "Breath & Heart: Your Built-in Resonance", 19, "Heart rate variability, resonance breathing at about six breaths a minute, and the cyclic sigh."),
  (5, "The Emotional Layer: Feelings as Waves", 23, "Why naming a feeling helps, how emotions spread between people, and how to ride the wave."),
  (6, "The Mental Layer: Attention & Brainwaves", 26, "What EEG rhythms do and don\u2019t tell us, and why attention is the steering wheel."),
  (7, "The Energetic & Spiritual Layer", 29, "Meaning, values, awe and practice, with traditions like prana and chakras respected and honestly labelled."),
  (8, "Sound, Music & Resonance in Daily Life", 32, "Music and mood, binaural beats, the 3-minute hum, and tuning your sound environment."),
  (9, "The Environmental & Social Layer", 35, "Connection as a health behaviour, a measurable dose of nature, and spaces that support you."),
  (10, "Daily Practices & Routines", 38, "A sample day, a practice menu for one, five or more minutes, and how to make habits stick."),
  (11, "Your 30-Day Plan", 41, "Four themed weeks, one small practice a day, and a closing ritual to integrate it all."),
  (12, "Reflection Worksheets & Checklists", 44, "A habit wheel, a layer check-in, a weekly review, journal prompts and a daily tune-up checklist."),
]

LAYERS = [
  ("Physical", "Sleep, movement, food, breath, heart", "#e3e8dc"),
  ("Emotional", "Feelings, mood, stress responses", "#f6dccb"),
  ("Mental", "Attention, thinking habits, beliefs", "#dfe6ef"),
  ("Energetic / Spiritual", "Meaning, values, awe, contemplative practice", "#e6def0"),
  ("Environmental & Social", "People, places, light, sound, nature", "#efe6d8"),
]

# Short, verbatim excerpts (page numbers refer to the PDF)
QUOTES = [
  ("You can find meaning in them without mistaking them for measurements.", "Welcome, p. 4"),
  ("But you can decide, right now, to breathe more slowly \u2014 and when you do, other rhythms follow.", "Chapter 4, p. 19"),
  ("The goal is to feel, name, and respond \u2014 not to avoid.", "Chapter 5, p. 23"),
  ("In other words: friendship isn\u2019t a luxury. It\u2019s a core part of health.", "Chapter 9, p. 35"),
  ("Consistency beats intensity.", "Chapter 10, p. 38"),
  ("Don\u2019t aim for perfection; aim to show up.", "Chapter 11, p. 41"),
]

PEEK = [(3, "The contents"), (7, "Chapter 1: resonance"), (11, "The five layers"), (42, "The 30-day plan"), (44, "Habit wheel worksheet")]

ICON_DL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 19h14"/></svg>'


def book_mockup(r, size="lg", lazy=False):
    """A shadowed, slightly turned 3D book built from the rendered cover (pure CSS)."""
    src = "ebook-cover.webp" if size == "lg" else "ebook-cover-sm.webp"
    w, h = (720, 1080) if size == "lg" else (400, 600)
    return (f'<div class="book book-{size}"><div class="book-3d">'
            f'<img class="book-cover" src="{r}assets/images/{src}" alt="{html.escape(EBOOK["cover_alt"])}" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""}>'
            f'<span class="book-pages" aria-hidden="true"></span><span class="book-back" aria-hidden="true"></span></div>'
            f'<span class="book-shadow" aria-hidden="true"></span></div>')


def sample_btn(r, cls="btn btn-outline"):
    return f'<a class="{cls}" href="{r}{EBOOK["sample"]}" download>{ICON_DL}<span>Download free sample</span></a>'


def buy_box(r, checkout, price_param=""):
    e = EBOOK; cur = e["currency"]
    live = bool(checkout.strip())
    chips = "".join(f'<button type="button" data-amount="{a}" aria-pressed="{"true" if a == e["default"] else "false"}"{"" if live else " disabled"}>{cur}{a}</button>' for a in e["suggested"])
    chips += f'<button type="button" data-amount="custom" aria-pressed="false"{"" if live else " disabled"}>Custom</button>'
    custom = (f'<div class="pwyw-custom" hidden><label for="pwyw-amt">Your amount (minimum {cur}{e["min"]})</label>'
              f'<div class="pwyw-input"><span aria-hidden="true">{cur}</span><input id="pwyw-amt" type="number" inputmode="decimal" min="{e["min"]}" step="1" value="{e["default"]}" aria-describedby="pwyw-err"></div>'
              f'<p class="pwyw-err" id="pwyw-err" role="alert"></p></div>')
    if live:
        cta = (f'<a class="btn btn-primary btn-buy" href="{html.escape(checkout)}" data-checkout="{html.escape(checkout)}" rel="noopener">'
               f'Get the ebook <span class="pwyw-label">· {cur}{e["default"]}</span></a>'
               f'<p class="pwyw-note">You\u2019ll finish on a secure checkout page, where you can confirm or change the amount. The PDF is delivered there, usually as an instant download link plus an email copy.</p>')
        state = "live"
    else:
        cta = (f'<span class="btn btn-primary btn-buy is-soon" aria-disabled="true" role="link">Checkout coming soon</span>'
               f'<p class="pwyw-note">Secure checkout is being set up. In the meantime, the whole first chapter is free: download the sample and read at your own pace.</p>'
               f'{sample_btn(r, "btn btn-outline pwyw-sample")}')
        state = "soon"
    return f'''<div class="pwyw" data-pwyw data-state="{state}" data-price-param="{html.escape(price_param)}" data-min="{e["min"]}" data-currency="{cur}">
      <div class="pwyw-head"><span class="eyebrow">Pay what you want</span><h2 id="buy-h">Name your price</h2>
        <p>Pay what feels fair to you, from {cur}{e["min"]}. We suggest {cur}{e["default"]}, but every amount is welcome and everyone gets the same book. It helps keep Willowhush going.</p></div>
      <div class="chip-row pwyw-chips" role="group" aria-label="Suggested amounts">{chips}</div>
      {custom}
      <div class="pwyw-cta">{cta}</div>
      <ul class="pwyw-facts"><li>{e["format"]} · {e["pages"]} pages</li><li>12 chapters</li><li>30-day plan + worksheets</li><li>First edition 2026</li></ul>
    </div>'''


def ebook_page(r, checkout, head, header, footer, base, price_param=""):
    e = EBOOK
    chapters = "".join(f'<li class="reveal{" d" + str(i % 3) if i % 3 else ""}"><span class="ch-n">{n:02d}</span><div><h3>{html.escape(t)}</h3><p>{d}</p></div><span class="ch-p">p.&nbsp;{p}</span></li>' for i, (n, t, p, d) in enumerate(CHAPTERS))
    layers = "".join(f'<li><span class="sw" style="background:{c}" aria-hidden="true"></span><strong>{n}</strong><span>{d}</span></li>' for n, d, c in LAYERS)
    quotes = "".join(f'<figure class="ex-quote reveal{" d" + str(i % 3) if i % 3 else ""}"><blockquote>\u201c{q}\u201d</blockquote><figcaption>{c}</figcaption></figure>' for i, (q, c) in enumerate(QUOTES))
    peek = "".join(f'<figure class="peek-page reveal{" d" + str(min(i, 3)) if i else ""}"><img src="{r}assets/images/ebook-page-{p}.webp" alt="Page {p} of the ebook: {c.lower()}" width="360" height="540" loading="lazy"><figcaption>{c}<span>p. {p}</span></figcaption></figure>' for i, (p, c) in enumerate(PEEK))
    ld = {"@context": "https://schema.org", "@type": "Book", "name": f'{e["title"]}: {e["subtitle"]}', "bookFormat": "https://schema.org/EBook",
          "numberOfPages": e["pages"], "inLanguage": "en", "datePublished": "2026", "bookEdition": "First edition",
          "image": f"{base}/assets/images/ebook-cover.webp", "url": f"{base}/ebook.html",
          "author": {"@type": "Person", "name": "Elrond"}, "publisher": {"@type": "Organization", "name": "Willowhush"}}
    desc = "Good Vibrations, the Willowhush ebook: a practical, science-honest guide to the layers of personal vibration, with practices, a 30-day plan and worksheets. 52-page PDF, pay what you want. Free sample chapter."
    faq = [
      ("How does \u201cpay what you want\u201d work?", f"You choose the price, from {e['currency']}{e['min']}. The suggested amounts ({', '.join(e['currency'] + str(a) for a in e['suggested'])}) are only a guide; pay whatever feels fair for where you are right now. Everyone gets exactly the same book."),
      ("What format is it, and will it work on my device?", f"It\u2019s a {e['pages']}-page PDF (6 \u00d7 9 inch pages), which reads well on any tablet, computer or e-reader that opens PDFs, and prints cleanly. The worksheets and the 30-day plan are laid out so you can print them and fill them in by hand."),
      ("Can I read some of it first?", f"Yes. The free sample includes {e['sample_pages']}. It\u2019s a {e['sample_mb']} PDF, no email required."),
      ("Is this a spiritual book or a science book?", "A bit of both, clearly labelled. Every idea carries one of three labels: <em>well supported</em>, <em>promising / mixed</em>, or <em>tradition / metaphor</em>. Chakras, Solfeggio frequencies and the Map of Consciousness are presented with respect, as frameworks, not as measurements."),
      ("Do I need any equipment or experience?", "No. The book says it best: \u201cYou don\u2019t need any equipment, beliefs or special skills. Just curiosity and a willingness to try small things consistently.\u201d"),
      ("What if it\u2019s not right for me?", "Read the free sample first so you know the voice and approach before paying anything. If something goes wrong with your purchase or download, get in touch through the contact page and we\u2019ll put it right."),
      ("Is this medical advice?", "No. This book is for general education and is not medical or psychological advice. Please consult a qualified professional about any health concern, and keep taking any treatment you\u2019ve been prescribed."),
    ]
    faq_html = "".join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    return head("Good Vibrations: the ebook", desc, "ebook.html", r, img="ebook-og.jpg", otype="book").replace("</head>", f'<script type="application/ld+json">{json.dumps(ld)}</script></head>') + header(r, "Ebook") + f'''
<main id="main">
  <section class="ebook-hero" aria-labelledby="eb-h">
    <div class="container ebook-hero-grid">
      <div class="ebook-hero-copy">
        <span class="eyebrow reveal">The Willowhush ebook · {e["kicker"]}</span>
        <h1 id="eb-h" class="reveal d1">Good <em>Vibrations</em></h1>
        <p class="ebook-sub reveal d1">{e["subtitle"]}</p>
        <p class="lead reveal d2">From the physics of frequency and resonance to breath, emotion, attention, meaning and connection: a warm, honest guide to what \u201craising your vibration\u201d really means, and the small daily practices that actually help.</p>
        <ul class="ebook-meta reveal d2" aria-label="Book details"><li>{e["format"]}</li><li>{e["pages"]} pages</li><li>12 chapters</li><li>30-day plan</li><li>{e["edition"]}</li></ul>
        <div class="hero-actions reveal d3"><a class="btn btn-primary" href="#buy">Pay what you want</a>{sample_btn(r)}</div>
      </div>
      <div class="ebook-hero-art reveal d1">{book_mockup(r)}</div>
    </div>
  </section>

  <section class="ebook-why" aria-labelledby="why-h"><div class="container intro">
    <div class="intro-text reveal">
      <span class="eyebrow">Why this book</span>
      <h2 id="why-h">A popular phrase, taken seriously and honestly.</h2>
      <p>\u201cRaise your vibration\u201d can sound vague, mystical or a little off-putting. Yet behind it is something almost everyone wants: to feel more energetic, calmer, kinder, clearer and more connected.</p>
      <p>Good Vibrations starts with what vibration actually is, because the real science of frequency, resonance and synchronization turns out to be surprisingly relevant to your body. Then it walks through five interacting layers of personal vibration, each with how it works, what the research says, and simple practices to try.</p>
      <p>Ideas from spiritual traditions and popular culture are welcome here too, offered with respect and clearly labelled where they haven\u2019t been scientifically validated.</p>
    </div>
    <figure class="layers-fig reveal d1">
      <img src="{r}assets/images/ebook-layers.webp" alt="Diagram of five nested rings: Physical at the centre, then Emotional, Mental, Energetic / Spiritual, and Environmental &amp; Social on the outside" width="720" height="720" loading="lazy">
      <figcaption>The layered model at the heart of the book: an organizing tool, not an anatomical structure.</figcaption>
    </figure>
  </div>
  <div class="container"><ul class="layer-list reveal" aria-label="The five layers">{layers}</ul></div></section>

  <section class="ebook-chapters" aria-labelledby="ch-h"><div class="container">
    <div class="section-head reveal"><div><span class="eyebrow">What\u2019s inside</span><h2 id="ch-h" style="margin:0">Twelve chapters, physics to practice</h2></div>
      <p>Read cover to cover, jump to the layer that feels most out of tune, or go straight to action: Chapters 10 to 12 hold the routines, the plan and the worksheets.</p></div>
    <ol class="chapter-list">{chapters}<li class="reveal ch-back"><span class="ch-n">+</span><div><h3>Sources &amp; Further Reading</h3><p>The research and guidance behind every chapter, grouped by chapter, with links.</p></div><span class="ch-p">p.&nbsp;49</span></li></ol>
  </div></section>

  <section class="ebook-peek" aria-labelledby="peek-h"><div class="container">
    <div class="section-head reveal"><div><span class="eyebrow">Look inside</span><h2 id="peek-h" style="margin:0">Calm pages, clear diagrams</h2></div>
      <p>Original diagrams, evidence labels on every claim, and practice boxes you can follow on the spot.</p></div>
    <div class="peek-row" role="region" aria-label="Sample pages from the ebook" tabindex="0">{peek}</div>
  </div></section>

  <section class="ebook-for" aria-labelledby="for-h"><div class="container for-grid">
    <div class="for-card reveal"><span class="eyebrow">Who it\u2019s for</span><h2 id="for-h">For curious, gentle skeptics</h2>
      <ul class="tick-list">
        <li>You\u2019re drawn to \u201cvibration\u201d language but want to know what\u2019s real.</li>
        <li>You feel flat, scattered or wound up, and want small, doable ways back.</li>
        <li>You love meditation, yoga or sound baths and would like the science behind them.</li>
        <li>You\u2019re a skeptic who still wants more energy, calm and connection.</li>
        <li>You like a plan, a checklist and a page to write on.</li>
      </ul></div>
    <div class="for-card reveal d1"><span class="eyebrow">What you\u2019ll be able to do</span><h2>Tune each layer, on purpose</h2>
      <ul class="tick-list">
        <li>Explain frequency, resonance and entrainment, and spot where the metaphor begins.</li>
        <li>Use resonance breathing and the cyclic sigh to steady your body in minutes.</li>
        <li>Name and ride difficult emotions instead of fighting them.</li>
        <li>Build a daily rhythm from a menu of one- and five-minute practices.</li>
        <li>Follow a 30-day plan and track energy and mood as you go.</li>
        <li>Recognise misleading \u201cvibration\u201d claims before you pay for them.</li>
      </ul></div>
  </div></section>

  <section class="ebook-quotes" aria-labelledby="q-h"><div class="container">
    <div class="section-head reveal"><div><span class="eyebrow">From the pages</span><h2 id="q-h" style="margin:0">A few lines to sit with</h2></div><p>Short excerpts, quoted exactly as they appear in the book.</p></div>
    <div class="quote-grid">{quotes}</div>
  </div></section>

  <section class="ebook-buy" id="buy" aria-labelledby="buy-h"><div class="container buy-grid">
    <div class="buy-art reveal">{book_mockup(r, "sm", lazy=True)}</div>
    <div class="reveal d1">{buy_box(r, checkout, price_param)}</div>
  </div></section>

  <section class="ebook-faq" aria-labelledby="faq-h"><div class="narrow">
    <span class="eyebrow reveal">Questions</span><h2 id="faq-h" class="reveal d1">Before you begin</h2>
    <div class="faq reveal d2">{faq_html}</div>
    <p class="ebook-disclaimer reveal">This book is for general education and is not medical or psychological advice. Consult a qualified professional about any health concern. Illustrations: original diagrams and AI-generated artwork.</p>
    <p style="text-align:center;margin-top:2rem" class="reveal">{sample_btn(r)}</p>
  </div></section>
</main>''' + footer(r)


def home_feature(r):
    return f'''
  <section class="ebook-feature" aria-labelledby="ebf-h">
    <div class="container"><div class="ebook-feature-card">
      <div class="ebook-feature-art reveal">{book_mockup(r, "sm", lazy=True)}</div>
      <div class="ebook-feature-copy reveal d1">
        <span class="eyebrow">New · The Willowhush ebook</span>
        <h2 id="ebf-h">Good Vibrations</h2>
        <p class="ebook-sub">The layers of personal vibration: how they work, and how to raise yours.</p>
        <p>A practical, science-honest guide from the physics of resonance to breath, emotion, attention, meaning and connection. With simple practices, a 30-day plan and reflection worksheets.</p>
        <ul class="feature-list ebook-chips"><li>{EBOOK["pages"]}-page PDF</li><li>12 chapters</li><li>30-day plan</li><li>Pay what you want</li></ul>
        <div class="hero-actions"><a class="btn btn-primary" href="{r}ebook.html">Explore the ebook</a>{sample_btn(r)}</div>
      </div>
    </div></div>
  </section>'''


def promo_card(r, heading="h2"):
    return f'''<aside class="ebook-promo reveal" aria-label="The Willowhush ebook">
      <a class="ebook-promo-art" href="{r}ebook.html" tabindex="-1" aria-hidden="true"><img src="{r}assets/images/ebook-cover-sm.webp" alt="" width="400" height="600" loading="lazy"></a>
      <div><span class="eyebrow">The Willowhush ebook</span><{heading}>Good Vibrations</{heading}>
        <p>Breath, emotion, attention, meaning and connection: a practical, science-honest guide with a 30-day plan and worksheets. Pay what you want, with a free sample chapter.</p>
        <a class="go" href="{r}ebook.html">Look inside the ebook →</a></div>
    </aside>'''
