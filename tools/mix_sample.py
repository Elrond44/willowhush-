#!/usr/bin/env python3
"""Premix voice + music for a session the same way the player does (music at 0.8 gain, ducked to x0.63 while the
voice speaks), e.g. for listening samples:  python3 tools/mix_sample.py breath 0 40 out.mp3"""
import sys, json, subprocess
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent; A = ROOT / "src" / "assets" / "audio"; SR = 44100
VOL, DUCK = 0.8, 0.63
def load(f, ch):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"],
                                        capture_output=True, check=True).stdout, np.float32).reshape(-1, ch).T
def mix(sid):
    v = load(A / f"{sid}-voice.mp3", 1)[0]; m = load(A / f"{sid}-music.mp3", 2)
    n = min(len(v), m.shape[1]); v, m = v[:n], m[:, :n]
    target = np.full(n, VOL)
    for a, b in json.loads((ROOT / "narration_timing.json").read_text())[sid]:
        target[int(max(0, a - 0.3) * SR): int((b + 0.6) * SR)] = VOL * DUCK
    g = np.empty(n); k = 1 - np.exp(-1 / (0.4 * SR)); x = VOL            # one-pole smoothing, like setTargetAtTime(…, 0.4)
    for i0 in range(0, n, 441):                                          # 10 ms control rate
        x += (target[i0] - x) * (1 - np.exp(-441 / (0.4 * SR))); g[i0:i0 + 441] = x
    return m * g + v, v, m * g
if __name__ == "__main__":
    sid, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    y, _, _ = mix(sid); y = y * 0.89; y = y[:, int(t0 * SR): int(t1 * SR)]
    fade = int(1.5 * SR); y[:, -fade:] *= np.linspace(1, 0, fade); y[:, :int(0.3*SR)] *= np.linspace(0, 1, int(0.3*SR))
    print("peak", 20 * np.log10(np.abs(y).max()))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "libmp3lame", "-b:a", "128k", out],
                   input=np.ascontiguousarray(y.T).astype(np.float32).tobytes(), check=True)
