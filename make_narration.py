#!/usr/bin/env python3
"""Render the guided-session narration to src/assets/audio/<id>.mp3 with Piper TTS (offline neural voice).
Each caption is spoken at its cue time; the track is padded with silence to the session length,
so the audio stays in sync with the on-screen captions.
Needs: a Python env with `piper-tts`, the en_GB-cori-high voice (public-domain LibriVox data), and ffmpeg.
  PIPER=/workspace/ttsenv/bin/piper VOICE=/workspace/voices/en_GB-cori-high.onnx python3 make_narration.py"""
import os, subprocess, tempfile, wave
from pathlib import Path
from practices import SESSIONS

PIPER = os.environ.get("PIPER", "piper"); VOICE = os.environ.get("VOICE", "en_GB-cori-high.onnx")
OUT = Path(__file__).parent / "src" / "assets" / "audio"; OUT.mkdir(parents=True, exist_ok=True)

def dur(p):
    with wave.open(str(p)) as w: return w.getnframes() / w.getframerate()

for s in SESSIONS:
    tmp = Path(tempfile.mkdtemp()); inputs, filt = [], []
    for i, (t, text) in enumerate(s["cues"]):
        wav = tmp / f"{i}.wav"
        subprocess.run([PIPER, "-m", VOICE, "--length-scale", "1.18", "--sentence-silence", "0.6", "-f", str(wav)], input=text.encode(), check=True, capture_output=True)
        nxt = s["cues"][i+1][0] if i + 1 < len(s["cues"]) else s["total"]
        d = dur(wav)
        if t + 0.8 + d > nxt: print(f"  ! {s['id']} cue {i} ({d:.1f}s) overruns next cue by {t+0.8+d-nxt:.1f}s")
        inputs += ["-i", str(wav)]; ms = int((t + 0.8) * 1000)
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    n = len(s["cues"])
    fc = ";".join(filt) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,apad,atrim=0:{s['total']},afade=t=out:st={s['total']-2}:d=2,lowpass=f=7000,aecho=0.8:0.5:60:0.12,volume=1.1[out]"
    mp3 = OUT / f"{s['id']}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]", "-ac", "1", "-ar", "22050", "-c:a", "libmp3lame", "-b:a", "24k", str(mp3)], check=True)
    print("wrote", mp3, f"{mp3.stat().st_size//1024} KB")
