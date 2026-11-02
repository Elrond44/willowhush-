#!/usr/bin/env python3
"""Render the guided-session narration to src/assets/audio/<id>-voice.mp3 with Kokoro-82M (offline, CPU, Apache-2.0).
Each caption is spoken (sentence by sentence, with natural pauses) starting 0.8 s after its cue time, and the
track is padded with silence to the session length, so the voice stays in sync with the on-screen captions.
Also writes narration_timing.json (speech start/end per cue), used by the player to duck the music under the voice.
Needs: pip install kokoro-onnx soundfile; kokoro-v1.0.onnx + voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases); ffmpeg.
  KOKORO_DIR=/workspace/kokoro python3 make_narration.py"""
import os, re, json, subprocess, tempfile
from pathlib import Path
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from practices import SESSIONS

KDIR = Path(os.environ.get("KOKORO_DIR", "."))
VOICE = os.environ.get("KOKORO_VOICE", "af_heart"); SPEED = float(os.environ.get("KOKORO_SPEED", "0.82"))
SENT_GAP, COMMA_GAP, LEAD = 1.05, 0.38, 0.8          # seconds of silence after a sentence / a comma clause; delay after the cue
ROOT = Path(__file__).parent; OUT = ROOT / "src" / "assets" / "audio"; OUT.mkdir(parents=True, exist_ok=True)
SR = 24000
k = Kokoro(str(KDIR / "kokoro-v1.0.onnx"), str(KDIR / "voices-v1.0.bin"))

def trim(a, th=0.003):
    idx = np.where(np.abs(a) > th)[0]
    return a[max(0, idx[0] - 1200): idx[-1] + 2400] if len(idx) else a

def sentences(text):
    out = []
    for x in (x for x in re.split(r'(?<=[.!?])\s+', text.strip()) if x):
        if out and len(out[-1].split()) < 3: out[-1] += " " + x      # keep one-word sentences ("Welcome.") with the next
        else: out.append(x)
    return out

def speak(text):
    """Synthesize one caption: split at sentence ends and commas (keeping the punctuation for natural intonation)."""
    parts = []
    for sent in sentences(text):
        clauses = [c for c in re.split(r'(?<=,)\s+', sent) if c]
        if any(len(c.split()) < 3 for c in clauses): clauses = [sent]      # don't chop very short clauses
        for ci, c in enumerate(clauses):
            a, sr = k.create(c, voice=VOICE, speed=SPEED, lang="en-us"); assert sr == SR
            a = trim(a)
            fade = int(0.01 * SR); a[:fade] *= np.linspace(0, 1, fade); a[-fade:] *= np.linspace(1, 0, fade)
            gap = COMMA_GAP if ci < len(clauses) - 1 else SENT_GAP
            parts += [a, np.zeros(int(gap * SR), np.float32)]
    return np.concatenate(parts[:-1]) if parts else np.zeros(1, np.float32)

timing = {}
for s in SESSIONS:
    track = np.zeros(int(s["total"] * SR), np.float32); spans = []
    for i, (t, text) in enumerate(s["cues"]):
        a = speak(text); start = t + LEAD
        nxt = s["cues"][i + 1][0] if i + 1 < len(s["cues"]) else s["total"]
        if start + len(a) / SR > nxt: print(f"  ! {s['id']} cue {i} overruns next cue by {start + len(a)/SR - nxt:.1f}s")
        n0 = int(start * SR); a = a[: len(track) - n0]; track[n0:n0 + len(a)] += a
        spans.append([round(start, 2), round(start + len(a) / SR, 2)])
    timing[s["id"]] = spans
    tmp = Path(tempfile.mkdtemp()) / "v.wav"; sf.write(tmp, track, SR)
    mp3 = OUT / f"{s['id']}-voice.mp3"
    # gentle polish: de-rumble, slight low-pass, a touch of room, then loudness-normalise to -16 LUFS (true peak -1.5 dB)
    af = (f"highpass=f=70,lowpass=f=9500,aecho=0.85:0.5:45|90:0.10|0.05,afade=t=out:st={s['total']-1.5}:d=1.5,"
          "loudnorm=I=-16:TP=-1.5:LRA=11")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af", af, "-ac", "1", "-ar", "24000",
                    "-c:a", "libmp3lame", "-b:a", "64k", str(mp3)], check=True)
    print("wrote", mp3, f"{mp3.stat().st_size // 1024} KB")
(ROOT / "narration_timing.json").write_text(json.dumps(timing, indent=1))
