#!/usr/bin/env python3
"""Synthesize the ambient background music for each guided session -> src/assets/audio/<id>-music.mp3.
100% original: additive-synthesis pads (detuned soft harmonics with slow 'filter' movement), a low drone,
sparse singing-bowl strikes or felt-piano notes, and a synthetic reverb. No samples, no beat.
Deterministic (seeded). Needs numpy, scipy, ffmpeg.   python3 make_music.py"""
import subprocess, tempfile, json
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from practices import SESSIONS

SR = 44100
ROOT = Path(__file__).parent; OUT = ROOT / "src" / "assets" / "audio"; OUT.mkdir(parents=True, exist_ok=True)
def hz(n): return 440.0 * 2 ** ((n - 69) / 12)           # MIDI note -> Hz

# Per-session palette: chord progression (MIDI notes), seconds per chord, drone root, and accents.
PALETTE = {
 "breath":   dict(chords=[[50,57,62,66,69],[47,54,59,62,66],[43,50,55,59,62],[45,52,57,61,64]], hold=22, drone=50,
                  bright=0.68, bowls=dict(every=21, notes=[74,69,78]), piano=None, seed=1),          # D major, misty dawn
 "bodyscan": dict(chords=[[43,50,55,59,64],[48,55,60,64,67],[40,47,55,59,62],[45,52,57,60,64]], hold=26, drone=43,
                  bright=0.66, bowls=dict(every=40, notes=[67]), piano=dict(every=9, notes=[67,71,74,76,79,72]), seed=2),  # G, forest light
 "winddown": dict(chords=[[41,48,53,57,64],[38,45,50,53,60],[46,53,58,62,65],[43,50,55,58,65]], hold=28, drone=41,
                  bright=0.58, bowls=dict(every=30, notes=[65,60]), piano=None, seed=3),          # F, low and warm, candle
 "kindness": dict(chords=[[48,55,60,64,67],[45,52,57,60,64],[41,48,53,57,64],[43,50,55,59,62]], hold=24, drone=48,
                  bright=0.64, bowls=dict(every=34, notes=[72]), piano=dict(every=11, notes=[72,76,79,74,67]), seed=4),  # C, open sky
}

def soft_tone(f, n, rng, bright, t0=0):
    """A soft additive tone: harmonics rolling off fast, each with its own slow amplitude drift (= gentle filter movement)."""
    t = (np.arange(n) + t0) / SR; y = np.zeros(n)
    for h in range(1, 7):
        if f * h > 5000: break
        amp = (bright ** (h - 1)) / h
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * rng.uniform(0.01, 0.05) * t + rng.uniform(0, 6.28))
        y += amp * lfo * np.sin(2 * np.pi * f * h * t + rng.uniform(0, 6.28))
    return y

def pad(p, total, rng):
    L = np.zeros(int(total * SR)); R = np.zeros_like(L)
    hold, xf = p["hold"], 9.0                               # each chord fades in/out over 9 s, overlapping the next
    k, start = 0, -xf / 2
    while start < total:
        ch = p["chords"][k % len(p["chords"])]; a = max(0, start); b = min(total, start + hold + xf)
        n0, n1 = int(a * SR), int(b * SR); n = n1 - n0
        tt = np.arange(n) / SR + (a - start)
        env = np.clip(tt / xf, 0, 1) * np.clip((hold + xf - tt) / xf, 0, 1); env = env * env * (3 - 2 * env)  # smoothstep
        for i, note in enumerate(ch):
            for det in (-5, 0, 6):                         # three slightly detuned voices per note (cents)
                f = hz(note) * 2 ** (det / 1200); pan = rng.uniform(0.2, 0.8)
                g = (0.10 if i == 0 else 0.16) * (0.85 if det else 1.0) * (0.9 if note > 64 else 1.0)
                y = g * env * soft_tone(f, n, rng, p["bright"], n0)
                L[n0:n1] += y * np.sqrt(1 - pan); R[n0:n1] += y * np.sqrt(pan)
        k += 1; start += hold
    t = np.arange(len(L)) / SR                               # low drone (root + fifth), slowly breathing
    d = (0.08 * np.sin(2*np.pi*hz(p["drone"])*t) + 0.07*np.sin(2*np.pi*hz(p["drone"]+7)*t + 1) + 0.05*np.sin(2*np.pi*hz(p["drone"])*2.002*t)) \
        * (0.75 + 0.25 * np.sin(2 * np.pi * t / 23))
    return L + d, R + d

def bowl(f, dur, rng):
    """Singing bowl: inharmonic partials (1, 2.76, 5.4, 8.93) each a beating pair, soft mallet attack, long decay."""
    t = np.arange(int(dur * SR)) / SR; y = np.zeros_like(t)
    for r, g, d in ((1, 1, 9), (2.76, 0.4, 6), (5.4, 0.14, 3.5), (8.93, 0.05, 2)):
        for beat in (0, rng.uniform(0.6, 1.4)):
            y += 0.5 * g * np.exp(-t / d * 1.0) * np.sin(2 * np.pi * (f * r + beat) * t + rng.uniform(0, 6.28))
    return y * np.clip(t / 0.04, 0, 1)

def felt_piano(f, dur, rng):
    t = np.arange(int(dur * SR)) / SR; y = np.zeros_like(t)
    for h, g in ((1, 1), (2, 0.35), (3, 0.12), (4, 0.05)):
        y += g * np.exp(-t * (0.7 + 0.9 * h)) * np.sin(2 * np.pi * f * h * 1.0004 ** h * t)
    return y * np.clip(t / 0.012, 0, 1)

def reverb(x, rng, secs=5.5):
    n = int(secs * SR); t = np.arange(n) / SR
    out = []
    for ch in range(2):                                     # decorrelated L/R noise tails, darker as they decay
        ir = rng.standard_normal(n) * np.exp(-t / (secs / 6.9))
        ir = sosfilt(butter(2, 3500, fs=SR, output="sos"), ir); ir /= np.sqrt(np.sum(ir ** 2))
        out.append(fftconvolve(x[ch], ir)[: x.shape[1]])
    return np.array(out)

def render(sid, total):
    p = PALETTE[sid]; rng = np.random.default_rng(p["seed"])
    L, R = pad(p, total, rng)
    acc = np.zeros((2, len(L)))
    def place(y, at, pan, gain):
        n0 = int(at * SR); y = y[: len(L) - n0]
        acc[0, n0:n0+len(y)] += gain * y * np.sqrt(1 - pan); acc[1, n0:n0+len(y)] += gain * y * np.sqrt(pan)
    b = p["bowls"]; at, i = 6.0, 0
    while at < total - 12:
        place(bowl(hz(b["notes"][i % len(b["notes"])]), 12, rng), at, rng.uniform(0.3, 0.7), 0.16); i += 1
        at += b["every"] + rng.uniform(-3, 3)
    if p["piano"]:
        pp = p["piano"]; at, i = 12.0, 0
        while at < total - 8:
            place(felt_piano(hz(pp["notes"][i % len(pp["notes"])]), 7, rng), at, rng.uniform(0.25, 0.75), 0.13); i += 1
            at += pp["every"] + rng.uniform(-2.5, 2.5)
    dry = np.array([L, R]) + acc
    dry = sosfilt(butter(2, 80, "highpass", fs=SR, output="sos"), dry)        # no sub rumble
    dry = sosfilt(butter(2, 7000, fs=SR, output="sos"), dry)                    # nothing sharp up top
    wet = reverb(dry, rng)
    mix = 0.55 * dry + 0.75 * wet
    t = np.arange(mix.shape[1]) / SR
    mix *= np.clip(t / 6, 0, 1) * np.clip((total - t) / 8, 0, 1)               # 6 s fade in, 8 s fade out
    return (mix / np.max(np.abs(mix)) * 0.5).astype(np.float32)

def loudnorm(src, dst, target=-28.0):
    """Two-pass EBU R128 normalisation (linear), true peak <= -3 dBTP, then 96 kbps stereo mp3."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"loudnorm=I={target}:TP=-3:LRA=20:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"): r.rindex("}") + 1])
    af = (f"loudnorm=I={target}:TP=-3:LRA=20:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ar", "44100", "-ac", "2", "-c:a", "libmp3lame", "-b:a", "96k", dst], check=True)

if __name__ == "__main__":
    import soundfile as sf, sys
    for s in SESSIONS:
        if len(sys.argv) > 1:     # quick preview: python3 make_music.py 60  -> first 60 s of each to /tmp
            sf.write(f"/tmp/{s['id']}-preview.wav", render(s["id"], float(sys.argv[1])).T, SR); continue
        wav = Path(tempfile.mkdtemp()) / "m.wav"; sf.write(wav, render(s["id"], s["total"]).T, SR, subtype="FLOAT")
        mp3 = OUT / f"{s['id']}-music.mp3"; loudnorm(str(wav), str(mp3))
        print("wrote", mp3, f"{mp3.stat().st_size // 1024} KB")
