"""Cut "Sweet September" (Arulo, Mixkit 282, Mixkit Stock Music Free License) to the photo-checker film.

    python3 -I sound/music.py     # -> assets/audio/music.wav, sound/grid.json

The brief, 2026-11-01: "calm but not too calm". Sweet September is relaxed hip-hop/chillout, 98.7 s long.
Measured (librosa, 2026-11-01, sound stage): the beat tracker reads 101 BPM, but 101 does not fit the kicks, which
repeat every 3.158 s (5.33 beats at 101). It is 76.0 BPM in 4/4 with a half-time feel: snare on beats 2 and 4, kick
onsets at bar starts 12.638 + 3.15792 n to within a few ms through bar 28. Track bar n starts at 0.0063 + 3.15792 n.
  bars  0-3   0.00-12.64  intro, keys only (-21..-23 dB RMS): G | F | G | Gm/Eb (chroma)
  bar   4    12.64        THE DROP: kick and bass enter on the downbeat (-14 dB)
  bars  4-11 12.64-37.90  groove A (8 bars)
  bars 12-19 37.90-63.17  groove B, fuller (-12 dB, 8 bars)
  bar  20    63.17-66.32  half a bar of groove, then it thins (64.74)
  bars 21-23 66.32-75.80  breakdown (not used)
  bars 24-28 75.80-91.59  groove C; bar 28 (88.43) is the last full bar
  bar  29    91.59        the final hit; ring-out to 94.38, then silence

The edit (joins on bar lines, 20 ms crossfades):
  film  0.000- 3.158  track  0.006- 3.164  bar 0, the track's real opening (G)
  film  3.158- 9.474  track  6.322-12.638  bars 2-3: bar 1 (F) skipped, the join is G into G (chroma 0.93)
  film  9.474-60.007  track 12.638-63.171  the drop on "serverless", groove A, groove B from film 34.74, 16 bars
  film 60.007-66.30   track 88.428-...     the last full bar under the end card, the final hit at film 63.165,
                                           the track's own ring-out, a short fade on the last 0.35 s
So film bar k starts at 3.15792 k: the drop is film bar 3, the end card film bar 19, the final hit film bar 20.
"""
import json, subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
TRACK = ROOT / "sound/track.mp3"
SR, B0, BAR = 48000, 0.0063, 3.15792
tb = lambda n: B0 + n * BAR          # track bar n
fb = lambda k: k * BAR               # film bar k
SEGMENTS = [(0.0, tb(0)), (fb(1), tb(2)), (fb(3), tb(4)), (fb(19), tb(28))]   # (film start, track start)
DROP, GROOVE_B, END_CARD, FINAL_HIT = fb(3), fb(11), fb(19), fb(20)
FILM_END = 66.3
XF = 0.020


def main():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(TRACK), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    track = np.frombuffer(raw, np.float32).reshape(-1, 2).T.astype(np.float64)
    n = int(round(FILM_END * SR))
    out = np.zeros((2, n))
    x = int(XF * SR); ramp = np.linspace(0, 1, x)
    for k, (f0s, t0s) in enumerate(SEGMENTS):
        f0 = int(round(f0s * SR)); f1 = int(round(SEGMENTS[k + 1][0] * SR)) if k + 1 < len(SEGMENTS) else n
        t0 = int(round(t0s * SR))
        seg = track[:, t0: t0 + (f1 - f0)]
        seg = np.pad(seg, ((0, 0), (0, (f1 - f0) - seg.shape[1])))
        if k > 0:   # equal-gain crossfade over the 20 ms before the bar line: old segment out, new segment's lead-in in
            out[:, f0 - x: f0] = out[:, f0 - x: f0] * (1 - ramp) + track[:, t0 - x: t0] * ramp
        out[:, f0:f1] = seg
    fi = int(0.010 * SR); out[:, :fi] *= np.linspace(0, 1, fi)        # click guard only: the track starts on its own
    fo = int(0.35 * SR); out[:, -fo:] *= np.linspace(1, 0, fo) ** 2  # the ring-out is nearly gone by then
    import soundfile as sf
    (ROOT / "assets/audio").mkdir(parents=True, exist_ok=True)
    sf.write(ROOT / "assets/audio/music.wav", out.T.astype(np.float32), SR)
    grid = {"track": "Sweet September (Arulo, Mixkit 282)", "bpm": 76, "bar": BAR, "film_bar_k": "k * bar",
            "drop": round(DROP, 3), "groove_b": round(GROOVE_B, 3), "end_card": round(END_CARD, 3),
            "track_ending": round(END_CARD, 3), "final_hit": round(FINAL_HIT, 3), "duration": FILM_END,
            "segments": [[round(a, 3), round(b, 3)] for a, b in SEGMENTS]}
    (ROOT / "sound/grid.json").write_text(json.dumps(grid, indent=1))
    print(f"music.wav {FILM_END} s; drop {DROP:.3f}, groove B {GROOVE_B:.3f}, end card {END_CARD:.3f}, "
          f"final hit {FINAL_HIT:.3f}")


if __name__ == "__main__":
    main()
