"""Willowhush: HTML for the interactive practice tools and data for the guided sessions.
Imported by build.py (pages) and make_narration.py (voice audio)."""
import json, html

# ---------------------------------------------------------------- guided sessions
# cues: [seconds, caption]. Captions double as the narration script.
SESSIONS = [
  {"id": "breath", "title": "Three-minute breath", "mins": 3, "total": 180, "clip": "lake", "kind": "Breathwork",
   "alt": "A still, misty mountain lake at dawn under a lavender and peach sky",
   "desc": "A short reset for any moment of the day. Follow the breath, soften the body, and come back to the still water.",
   "cues": [[0, "Welcome. Settle into a comfortable seat, and let your hands rest."],
            [10, "If it feels right, let your eyes close, or soften your gaze."],
            [19, "Take a slow breath in through your nose."],
            [26, "And let it go, a little longer on the way out."],
            [34, "Again. Breathing in, the belly gently rising."],
            [42, "Breathing out, the shoulders softening."],
            [51, "Now let the breath find its own rhythm. There's no need to control it."],
            [64, "Notice where you feel it most. The nose, the chest, or the belly."],
            [78, "Rest your attention there, like a hand resting on still water."],
            [94, "When the mind wanders, and it will, simply notice, and return."],
            [110, "Each return is the practice. Nothing has gone wrong."],
            [124, "Breathing in, I know I am breathing in."],
            [134, "Breathing out, I know I am breathing out."],
            [146, "Let one more breath be slow and full."],
            [155, "And a long, unhurried breath out."],
            [164, "Gently open your eyes. Carry this steadiness with you."],
            [174, "Thank you for practicing."]]},
  {"id": "bodyscan", "title": "Five-minute body scan", "mins": 5, "total": 300, "clip": "forest", "kind": "Body scan",
   "alt": "Golden sunbeams slanting through mist in a quiet, mossy forest",
   "desc": "A slow walk of attention from the crown of the head to the soles of the feet. Lovely lying down, before sleep or after a long day.",
   "cues": [[0, "Welcome. Lie down or sit comfortably, and let your body be supported."],
            [11, "Take three slow breaths, letting each exhale be a little longer."],
            [26, "Bring your attention to the top of your head. Simply notice what is there."],
            [40, "Let the forehead smooth. Soften the space between the eyebrows."],
            [53, "Unclench the jaw. Let the tongue rest. Let the face be easy."],
            [67, "Move down to the neck and shoulders. Let them drop, just a little."],
            [83, "Feel your arms, heavy and resting. Notice the hands, and the fingertips."],
            [100, "Bring awareness to the chest. Feel it rise and fall with each breath."],
            [116, "Now the belly. Let it be soft. There's no need to hold it in."],
            [132, "Notice your back, wherever it meets the chair, the floor, or the bed."],
            [148, "Move to the hips. Let them grow heavy."],
            [163, "Feel the thighs, the knees, and the lower legs. Let them be still."],
            [180, "Bring your attention to your feet. The heels, the soles, the toes."],
            [198, "Now sense the whole body at once. Breathing, resting, here."],
            [216, "If any place feels tight, breathe toward it, and let it be as it is."],
            [236, "You don't need to feel anything special. Noticing is enough."],
            [254, "Take a deeper breath, and gently wiggle your fingers and toes."],
            [270, "When you're ready, open your eyes, or let yourself drift toward sleep."],
            [287, "Thank you for taking this time."]]},
  {"id": "winddown", "title": "Evening wind-down", "mins": 5, "total": 300, "clip": "candle", "kind": "Sleep & rest",
   "alt": "A single beeswax candle flame glowing softly in a dim plum-toned room",
   "desc": "Set the day down gently. A candlelit practice for releasing what's done, noticing what went well, and letting rest arrive.",
   "cues": [[0, "Good evening. Let the day begin to settle, like dust in still air."],
            [12, "Rest your eyes on the candle, or let them close."],
            [23, "Breathe in gently, and breathe out slowly, as if fogging a window."],
            [37, "Again, letting the out-breath be long and unhurried."],
            [51, "Think of one thing from today that you can set down now."],
            [66, "Imagine placing it on a shelf. It will be there in the morning, if you need it."],
            [84, "Now think of one small thing that went well today."],
            [99, "A kind word. A warm drink. A moment of quiet. Let it be enough."],
            [117, "Let your shoulders lower. Let your hands grow warm and heavy."],
            [135, "With each breath out, silently say: let go."],
            [153, "Let go of the planning. Let go of the replaying."],
            [171, "There is nothing left to do tonight. Rest is the only task."],
            [190, "Feel the weight of your body, sinking, supported."],
            [208, "Let your breath slow, all by itself."],
            [228, "If thoughts arrive, let them drift past, like smoke from a candle."],
            [248, "You have done enough today. You are allowed to rest."],
            [268, "Stay here as long as you like, or let sleep come."],
            [288, "Goodnight."]]},
  {"id": "kindness", "title": "Loving-kindness under open sky", "mins": 4, "total": 240, "clip": "clouds", "kind": "Loving-kindness",
   "alt": "Soft pastel clouds drifting slowly across a lavender and peach evening sky",
   "desc": "Four minutes of warm wishes, offered to someone you love, to yourself, and outward to everyone beneath the same sky.",
   "cues": [[0, "Welcome. Sit comfortably, and place a hand on your heart if you like."],
            [10, "Take a slow breath, and let your face soften into a small smile."],
            [22, "Bring to mind someone who makes you feel safe and cared for."],
            [35, "Silently offer them: may you be happy."],
            [45, "May you be healthy. May you be at ease."],
            [57, "Now turn these wishes toward yourself, just as you are."],
            [69, "May I be happy."],
            [77, "May I be healthy."],
            [85, "May I be at ease."],
            [95, "If it feels awkward, that's alright. Simply say the words kindly."],
            [110, "Bring to mind someone you barely know. A neighbour, or a shopkeeper."],
            [124, "May you be happy. May you be healthy. May you be at ease."],
            [140, "Now let your kindness spread outward, like light through clouds."],
            [154, "To everyone in this town, this country, under this whole wide sky."],
            [169, "May all beings be happy. May all beings be at ease."],
            [186, "Rest in the warmth of these wishes for a few breaths."],
            [205, "Notice how you feel now. Nothing to change."],
            [219, "Gently return, carrying this kindness into your day."],
            [232, "Thank you."]]},
]

PLAY_ICON = '<svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg><svg class="i-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7.5 5h3v14h-3zM13.5 5h3v14h-3z" fill="currentColor"/></svg>'
VOICE_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 10v4M8 7v10M12 4v16M16 8v8M20 11v2"/></svg>'
FS_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>'

def fmt(s): return f"{s//60}:{s%60:02d}"

def session_player(s, r, heading="h2"):
    v = f"{r}assets/video/{s['clip']}"
    data = html.escape(json.dumps({"id": s["id"], "title": s["title"], "total": s["total"], "cues": s["cues"]}), quote=True)
    transcript = "".join(f"<li><span>{fmt(t)}</span>{html.escape(c)}</li>" for t, c in s["cues"])
    return f'''<article class="session reveal" id="session-{s['id']}" data-session="{data}" aria-labelledby="st-{s['id']}">
  <div class="player" role="group" aria-label="{html.escape(s['title'])} player">
    <video muted loop playsinline preload="none" poster="{v}-poster.webp" aria-label="{html.escape(s['alt'])}" width="1280" height="720">
      <source src="{v}.webm" type="video/webm"><source src="{v}.mp4" type="video/mp4">
    </video>
    <audio preload="none" src="{r}assets/audio/{s['id']}.mp3"></audio>
    <div class="player-veil" aria-hidden="true"></div>
    <p class="caption" aria-live="polite"></p>
    <button class="big-play" type="button" aria-label="Begin {html.escape(s['title'])}">{PLAY_ICON}<span>Begin · {s['mins']} min</span></button>
    <div class="player-bar">
      <button type="button" class="pbtn" data-play aria-label="Play" aria-pressed="false">{PLAY_ICON}</button>
      <input class="seek" type="range" min="0" max="{s['total']}" step="1" value="0" aria-label="Session position">
      <span class="ptime">0:00 / {fmt(s['total'])}</span>
      <button type="button" class="pbtn voice" data-voice aria-pressed="false" title="Spoken guidance">{VOICE_ICON}<span>Voice off</span></button>
      <button type="button" class="pbtn" data-fs aria-label="Full screen">{FS_ICON}</button>
    </div>
    <p class="sr-only" data-announce aria-live="polite"></p>
  </div>
  <div class="session-info">
    <span class="eyebrow">{s['kind']} · {s['mins']} minutes</span>
    <{heading} id="st-{s['id']}">{s['title']}</{heading}>
    <p>{s['desc']}</p>
    <details class="transcript"><summary>Read the guidance</summary><ol>{transcript}</ol></details>
  </div>
</article>'''

# ---------------------------------------------------------------- tools
def timer_tool():
    durs = "".join(f'<button type="button" data-min="{m}" aria-pressed="false">{m} min</button>' for m in (3, 5, 10, 15, 20))
    return f'''<div class="tool tool-timer" data-tool="timer">
  <div class="timer-face">
    <svg viewBox="0 0 200 200" aria-hidden="true"><defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e7b598"/><stop offset="1" stop-color="#a98bb8"/></linearGradient></defs>
      <circle cx="100" cy="100" r="92" class="ring-bg"/><circle cx="100" cy="100" r="92" class="ring-fill" stroke="url(#tg)" transform="rotate(-90 100 100)"/></svg>
    <div class="timer-read"><span class="timer-time" role="timer" aria-label="Time remaining">05:00</span><span class="timer-state">Ready</span></div>
  </div>
  <div class="timer-controls">
    <div class="chip-row" role="group" aria-label="Duration">{durs}<label class="custom-min"><span class="sr-only">Custom minutes</span><input data-custom type="number" min="1" max="120" inputmode="numeric" placeholder="Custom"></label></div>
    <div class="timer-opts">
      <label>Interval bell <select data-interval><option value="0">None</option><option value="1">Every minute</option><option value="2">Every 2 minutes</option><option value="5">Every 5 minutes</option></select></label>
      <button type="button" class="btn-link" data-test-bell>Hear the bell</button>
    </div>
    <div class="tool-actions"><button type="button" class="btn btn-primary" data-start aria-pressed="false">Begin</button><button type="button" class="btn btn-outline" data-reset>Reset</button></div>
    <p class="tool-note" data-log></p>
  </div>
  <p class="sr-only" data-announce aria-live="polite"></p>
</div>'''

SCAN = [("all", "Settle", "Lie down or sit with support. Take three slow breaths, letting each out-breath be a little longer than the last."),
        ("head", "Crown & forehead", "Bring your attention to the top of your head. Let the forehead smooth, as if someone had brushed it gently."),
        ("head", "Face & jaw", "Soften around the eyes. Let the jaw unclench, the lips part slightly, and the tongue rest."),
        ("neck shoulders", "Neck & shoulders", "Notice any lifting or bracing here. On the next out-breath, let the shoulders drop a little."),
        ("arms hands", "Arms & hands", "Feel the weight of your arms. Notice the palms, the fingers, any warmth or tingling at the fingertips."),
        ("chest", "Chest", "Feel the chest rise and fall. No need to change the breath; simply keep it company."),
        ("belly", "Belly", "Let the belly be soft and round. Notice it swelling gently with each in-breath."),
        ("hips", "Hips & lower back", "Sense where your body meets the surface beneath you. Let the hips grow heavy and wide."),
        ("legs", "Legs", "Move slowly down the thighs, the knees, the shins and calves. Let the legs be completely still."),
        ("feet", "Feet", "Notice the heels, the soles, each toe. Imagine tension draining out through the soles of the feet."),
        ("all", "Whole body", "Now feel the whole body at once, breathing and resting. Stay as long as you like.")]

FIGURE = '''<svg class="scan-figure" viewBox="0 0 200 420" role="img" aria-label="A simple outline of a human figure; the area currently in focus glows softly">
  <defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <radialGradient id="aura" cx="50%" cy="45%" r="55%"><stop offset="0" stop-color="#e7b598" stop-opacity=".28"/><stop offset="1" stop-color="#cfc3dc" stop-opacity="0"/></radialGradient></defs>
  <ellipse class="aura" cx="100" cy="210" rx="98" ry="205" fill="url(#aura)"/>
  <ellipse data-part="head" cx="100" cy="46" rx="24" ry="29"/>
  <rect data-part="neck" x="91" y="72" width="18" height="18" rx="6"/>
  <path data-part="shoulders" d="M62 97 Q100 82 138 97 L134 110 Q100 100 66 110 Z"/>
  <path data-part="chest" d="M66 110 Q100 100 134 110 L130 156 Q100 162 70 156 Z"/>
  <path data-part="belly" d="M70 156 Q100 162 130 156 L127 200 Q100 206 73 200 Z"/>
  <path data-part="hips" d="M73 200 Q100 206 127 200 L132 233 Q100 245 68 233 Z"/>
  <path data-part="arms" d="M62 97 Q49 101 47 118 L39 200 Q38 209 45 210 Q51 210 52 202 L62 126 L66 110 Z"/>
  <path data-part="arms" d="M138 97 Q151 101 153 118 L161 200 Q162 209 155 210 Q149 210 148 202 L138 126 L134 110 Z"/>
  <ellipse data-part="hands" cx="45" cy="224" rx="8" ry="12"/><ellipse data-part="hands" cx="155" cy="224" rx="8" ry="12"/>
  <path data-part="legs" d="M68 236 Q84 244 98 243 L96 318 L93 390 L79 390 L74 318 Z"/>
  <path data-part="legs" d="M132 236 Q116 244 102 243 L104 318 L107 390 L121 390 L126 318 Z"/>
  <ellipse data-part="feet" cx="85" cy="399" rx="12" ry="7"/><ellipse data-part="feet" cx="115" cy="399" rx="12" ry="7"/>
</svg>'''

def bodyscan_tool():
    lis = "".join(f'<li data-region="{reg}"><button type="button"><strong>{t}</strong><span>{d}</span></button></li>' for reg, t, d in SCAN)
    return f'''<div class="tool tool-scan" data-tool="bodyscan">
  <div class="scan-visual">{FIGURE}</div>
  <div class="scan-side">
    <div class="scan-panel" aria-live="polite"><span class="scan-num">1 / {len(SCAN)}</span><h3 class="scan-title">Settle</h3><p class="scan-text"></p><div class="scan-bar" aria-hidden="true"><span></span></div></div>
    <div class="tool-actions">
      <button type="button" class="btn btn-outline btn-icon" data-prev aria-label="Previous area">←</button>
      <button type="button" class="btn btn-primary" data-play aria-pressed="false">Begin</button>
      <button type="button" class="btn btn-outline btn-icon" data-next aria-label="Next area">→</button>
    </div>
    <div class="tool-opts">
      <label>Time per area <select data-pace><option value="20">20 seconds</option><option value="40" selected>40 seconds</option><option value="60">1 minute</option><option value="90">90 seconds</option></select></label>
      <label class="check"><input type="checkbox" data-voice> Read aloud</label>
    </div>
    <details class="scan-list"><summary>All {len(SCAN)} areas</summary><ol class="scan-steps">{lis}</ol></details>
  </div>
</div>'''

def grounding_tool():
    steps = "".join(f'<li><b>{n}</b>{s}</li>' for n, s in ((5, "see"), (4, "feel"), (3, "hear"), (2, "smell"), (1, "taste")))
    return f'''<div class="tool tool-ground" data-tool="grounding">
  <ol class="ground-steps" aria-label="Senses">{steps}</ol>
  <div class="ground-stage">
    <span class="ground-num" aria-hidden="true">5</span>
    <h3 class="ground-title">Five things you can see</h3>
    <p class="ground-hint"></p>
    <div class="ground-dots" aria-hidden="true"></div>
    <label class="sr-only" for="gnote">Optional note</label><input id="gnote" class="ground-note" type="text" autocomplete="off">
    <div class="tool-actions"><button type="button" class="btn btn-primary" data-notice>I noticed one</button><button type="button" class="btn btn-outline" data-gnext>Next sense →</button><button type="button" class="btn btn-primary" data-grestart hidden>Begin again</button></div>
  </div>
  <p class="sr-only" data-announce aria-live="polite"></p>
</div>'''

def kindness_tool():
    chips = '<button type="button" data-circle="journey" aria-pressed="true">Full journey</button>' + "".join(
        f'<button type="button" data-circle="{k}" aria-pressed="false">{n}</button>' for k, n in (("loved", "A loved one"), ("self", "Yourself"), ("neutral", "Someone neutral"), ("difficult", "Someone difficult"), ("all", "All beings")))
    return f'''<div class="tool tool-lk" data-tool="kindness">
  <div class="chip-row" role="group" aria-label="Who to offer kindness to">{chips}</div>
  <div class="lk-stage">
    <span class="lk-who">Five circles</span>
    <p class="lk-phrase" aria-live="polite">Five widening circles of kindness, beginning with someone you love.</p>
    <div class="lk-dots" aria-hidden="true"></div>
  </div>
  <div class="tool-actions"><button type="button" class="btn btn-primary" data-play aria-pressed="false">Begin</button><button type="button" class="btn btn-outline" data-next>Next phrase</button></div>
  <div class="tool-opts">
    <label>Each phrase <select data-pace><option value="6">6 seconds</option><option value="9" selected>9 seconds</option><option value="12">12 seconds</option></select></label>
    <label class="check"><input type="checkbox" data-voice> Read aloud</label>
  </div>
  <details class="lk-edit"><summary>Write your own phrases</summary>
    <p>One phrase per line, written to “you”. They are adapted automatically for yourself (“May I…”) and for all beings.</p>
    <label class="sr-only" for="lk-ta">Your phrases</label><textarea id="lk-ta" rows="4"></textarea>
    <div class="tool-actions"><button type="button" class="btn btn-outline btn-sm" data-save>Save phrases</button><button type="button" class="btn-link" data-default>Use the traditional ones</button><span class="tool-note" data-saved role="status"></span></div>
  </details>
</div>'''

def breathe_widget(extra=True):
    ex = '<button data-pattern="exhale" aria-pressed="false">Long exhale 4·6</button>' if extra else ''
    return f'''<div class="breath-stage" data-breathe aria-live="polite">
        <div class="breath-ring r2"></div><div class="breath-ring"></div>
        <div class="breath-circle"></div>
        <span class="breath-label">Ready</span>
        <span class="breath-count"></span>
      </div>
      <div class="breath-controls">
        <div class="pattern-select" role="group" aria-label="Breathing pattern">
          <button data-pattern="box" aria-pressed="true">Box 4·4·4·4</button>
          <button data-pattern="calm" aria-pressed="false">Calm 4·7·8</button>
          <button data-pattern="even" aria-pressed="false">Even 5·5</button>{ex}
        </div>
        <button class="btn btn-primary" data-breathe-toggle aria-pressed="false">Begin</button>
      </div>'''

TOOLS = {"timer": timer_tool, "bodyscan": bodyscan_tool, "grounding": grounding_tool, "kindness": kindness_tool}

def embed(name, r):
    """Markup for <!--tool:NAME--> placeholders inside posts."""
    if name == "breathe":
        return f'<div class="breathe breathe-embed">{breathe_widget()}</div>'
    if name.startswith("session:"):
        s = next(x for x in SESSIONS if x["id"] == name.split(":")[1])
        return f'<div class="embed-session">{session_player(s, r, heading="h3")}</div>'
    return f'<div class="embed-tool">{TOOLS[name]()}<p class="embed-more">More interactive practices on the <a href="{r}practice.html">Practice page</a>.</p></div>'
