"""The photo-checker soundtrack: Kokoro af_heart, "Sweet September" (Arulo) as a quiet bed, and a few soft effects.

    python3 -I sound/mix.py

Inputs: assets/audio/music.wav + sound/grid.json (sound/music.py), narration/chosen/<id>.wav + narration/words.json
(narration/pick.py), sound/sfx-src/mixkit-<id>.mp3 (Mixkit free sound effects, same licence as the music).
Outputs:
- assets/audio/mix.wav: the soundtrack, -16 LUFS integrated, true peak under -1.5 dBTP.
- assets/audio/vo.wav: the voice alone (after its EQ and compression, before its gain).
- assets/vo.js: window.VO, each line's start/end and word times in film seconds (the script's spellings).
- assets/timing.js and sound/timing.json: window.TM, the scene windows and the music's cue points. Every scene
  reads its start from it, and build.py writes the same numbers into index.html.

Levels (the brief: "the sound should not be too loud, just present, the voice should be clear"):
- Speech at -16 LUFS, measured on the spoken stretches only (each line's start to end).
- The bed 9 dB under the speech (its integrated loudness over the film), ducked 4.5 dB more while she speaks
  (40 ms attack, 450 ms release), so about 13.5 dB under her while she talks.
- Effects: one per picture event in sound/picture-cues.json (sound/picture_cues.py mirrors the scenes' cue formulas).
  Each is levelled by measurement to 3-6 dB over the bed under it (K-weighted: the effect over 200 ms around its
  peak against the bed's 400 ms momentary level there), never closer than 3 dB under the voice, and placed so its
  peak lands one frame after its picture.
- The sum is levelled to -16 LUFS and limited; the report at the end re-measures every one of these numbers.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, soundfile as sf, librosa
from scipy.signal import lfilter

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
G = json.loads((ROOT / "sound/grid.json").read_text())
DROP, END_CARD, FINAL_HIT, DUR, BAR = G["drop"], G["end_card"], G["final_hit"], G["duration"], G["bar"]

# Each line's start in film seconds (film bar k starts at k * 3.15792 s; see sound/music.py).
#  hook   v01-v02 on the track's keys intro, breaths 0.79 / 0.85
#  title  v03 starts 0.53 s early so "serverless" (its "s" 0.47 s into the clip, the vowel 0.62) lands on the drop 9.474
#  board  v04-v10: breaths 0.57-0.75, the camera glides inside them; v08 placed so "open" (the green answer) lands
#         0.1 s after groove B enters (34.737); 3.4 s after v10 for the pull-back to the whole board
#  proof  v11-v12, then 1.8 s to read the credit before the end card
#  end    v13 on the track's last full bar (60.0); the final hit (63.158) is the URL's moment
SLOTS = {"v01": 1.60, "v02": 5.38, "v03": 8.95, "v04": 14.62, "v05": 19.10, "v06": 21.90, "v07": 26.25,
         "v08": 31.86, "v09": 35.85, "v10": 39.35, "v11": 47.95, "v12": 53.40, "v13": 60.55}
# Scene windows (film seconds), on the track's bar lines (and one half bar). A scene's window runs 0.4 s past the
# next one's start: its exit fades over the incoming scene. The hook clears by itself before the drop.
SCENES = {"s1": [0, round(3 * BAR, 3)],                        # hook        bars 0-2 (keys only)
          "s2": [round(3 * BAR, 3), round(4.5 * BAR + 0.4, 3)],   # title       the drop, 1.5 bars
          "s3": [round(4.5 * BAR, 3), round(15 * BAR + 0.4, 3)],  # board       b1-b4 + the pull-back, 10.5 bars
          "s4": [round(15 * BAR, 3), round(END_CARD + 0.4, 3)],   # proof       14 resources, validate, credit, 4 bars
          "s5": [END_CARD, DUR]}                                   # end card    the last full bar, the final hit, ring-out


def lufs(path):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summ = out[out.rfind("Summary:"):]
    i = float(summ.split("I:")[1].split("LUFS")[0])
    tp = float(summ.split("Peak:")[1].split("dBFS")[0]) if "Peak:" in summ else 0.0
    return i, tp


def lufs_of(y, tmp, name):
    y = np.asarray(y)
    sf.write(tmp / f"{name}.wav", (y.T if y.ndim == 2 else y).astype(np.float32), SR)
    return lufs(tmp / f"{name}.wav")[0]


def load(path, sr=SR):
    y, s = sf.read(path, always_2d=True)
    y = y.T.astype(np.float64)
    if s != sr:
        y = np.vstack([librosa.resample(ch, orig_sr=s, target_sr=sr) for ch in y])
    return y


def main():
    words = json.loads((ROOT / "narration/words.json").read_text())
    music = load(ROOT / "assets/audio/music.wav")
    n = music.shape[1]

    # ---------------------------------------------------------------- the voice
    vo = np.zeros(n)
    meta, prev_end = {}, 0.0
    for key, t0 in SLOTS.items():
        y = load(ROOT / f"narration/chosen/{key}.wav").mean(0)
        if t0 < prev_end + 0.3:
            print(f"warning: {key} starts {prev_end + 0.3 - t0:.2f} s too early (breath under 0.3 s)", file=sys.stderr)
        a = int(round(t0 * SR)); b = min(n, a + len(y))
        if b - a < len(y):
            print(f"warning: {key} runs past the end of the film", file=sys.stderr)
        vo[a:b] += y[: b - a]
        end = t0 + len(y) / SR
        meta[key] = {"start": round(t0, 3), "end": round(end, 3), "text": words[key]["text"],
                     "words": [{"w": w["w"], "t0": round(t0 + w["t0"], 3), "t1": round(t0 + w["t1"], 3)} for w in words[key]["words"]]}
        prev_end = end
    tmp = Path(tempfile.mkdtemp())
    sf.write(tmp / "vo_raw.wav", vo.astype(np.float32), SR)
    # Kokoro is clean and bright already: a high-pass, a touch of presence, light de-essing and compression
    chain = ("highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=1.5,equalizer=f=250:t=q:w=1.0:g=-1,"
             "deesser=i=0.2:f=0.5,acompressor=threshold=0.1:ratio=2.5:attack=10:release=150:makeup=1.3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "vo_raw.wav"), "-af", chain, "-ar", str(SR),
                    str(ROOT / "assets/audio/vo.wav")], check=True)
    vo = load(ROOT / "assets/audio/vo.wav").mean(0)[:n]
    vo = np.pad(vo, (0, n - len(vo)))
    speech = np.zeros(n, bool)
    for m in meta.values():
        speech[int(m["start"] * SR): int(m["end"] * SR)] = True
    # speech at -16 LUFS as it sits in the mix: measured as two identical channels (a mono file reads 3 dB lower)
    vo *= 10 ** ((-16 - lufs_of(np.vstack([vo, vo])[:, speech], tmp, "speech")) / 20)

    # ---------------------------------------------------------------- the bed: quieter, less boom, ducked by the voice
    sf.write(tmp / "m.wav", music.T.astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "m.wav"), "-af",
                    "bass=g=-4:f=110:w=0.7,equalizer=f=2500:t=q:w=1.5:g=-2", str(tmp / "m2.wav")], check=True)
    bed = load(tmp / "m2.wav")[:, :n]
    bed *= 10 ** ((-25 - lufs(tmp / "m2.wav")[0]) / 20)      # the bed 9 dB under the speech before ducking
    bed_open = bed.copy()
    # duck: -4.5 dB under the voice, 40 ms attack, 450 ms release (followed at 1 kHz, then interpolated)
    hop = SR // 1000
    env = np.sqrt(np.convolve(vo ** 2, np.ones(int(0.05 * SR)) / int(0.05 * SR), "same"))[::hop]
    on = (env > 10 ** (-45 / 20)).astype(float)
    g = np.empty(len(on)); state = 0.0
    att, rel = 1 - np.exp(-1 / (0.04 * 1000)), 1 - np.exp(-1 / (0.45 * 1000))
    for i, target in enumerate(on):
        state += (att if target > state else rel) * (target - state)
        g[i] = state
    g = np.interp(np.arange(n), np.arange(len(g)) * hop, g)
    bed *= 10 ** (-4.5 * g / 20)

    # ---------------------------------------------------------------- timing for the picture (and for picture_cues.py)
    (ROOT / "assets/vo.js").write_text("window.VO = " + json.dumps(meta) + ";\n")
    cues = {"mark_title": DROP, "groove_b": G["groove_b"], "mark_end": END_CARD,
            "end_line1": round(meta["v13"]["end"] + 0.25, 3), "end_line2": round(meta["v13"]["end"] + 0.6, 3),
            "url": FINAL_HIT}
    tm = {"drop": DROP, "end_card": END_CARD, "track_ending": G["track_ending"], "final_hit": FINAL_HIT,
          "duration": DUR, "bar": BAR, **SCENES, "cues": cues}
    (ROOT / "assets/timing.js").write_text("window.TM = " + json.dumps(tm) + ";\n")
    (ROOT / "sound/timing.json").write_text(json.dumps(tm, indent=1))
    subprocess.run([sys.executable, "-I", str(ROOT / "sound/picture_cues.py")], check=True)

    # ---------------------------------------------------------------- effects, levelled against the bed and the voice
    sfx = np.zeros((2, n))
    events = sfx_events(json.loads((ROOT / "sound/picture-cues.json").read_text()))
    vo_k = kpow(np.vstack([vo, vo]))
    bed_p, vo_s = Power(kpow(bed)), Power(vo_k, speech)
    speech_l = Power(vo_k).level(speech)
    placed = []
    for t, name, over, pitch, what in events:
        placed.append((t, name, what) + place(sfx, name, t, over, pitch, bed_p, vo_s, speech_l))

    # ---------------------------------------------------------------- sum, level, limit
    mix = bed + sfx + np.vstack([vo, vo])
    gm = 10 ** ((-16 - lufs_of(mix, tmp, "mix")) / 20)
    mix *= gm
    sf.write(tmp / "mix2.wav", mix.T.astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "mix2.wav"), "-af",
                    "alimiter=limit=0.76:attack=3:release=60:level=disabled", "-ar", str(SR),
                    str(ROOT / "assets/audio/mix.wav")], check=True)
    fi, tp = lufs(ROOT / "assets/audio/mix.wav")

    # ---------------------------------------------------------------- the report: every level re-measured on the result
    gap = ~speech; gap[: int(0.5 * SR)] = False
    v_speech = lufs_of(gm * np.vstack([vo, vo])[:, speech], tmp, "r1")
    b_under = lufs_of(gm * bed[:, speech], tmp, "r2")
    b_open_under = lufs_of(gm * bed_open[:, speech], tmp, "r3")
    b_gaps = lufs_of(gm * bed[:, gap], tmp, "r4")
    b_film = lufs_of(gm * bed_open, tmp, "r5")
    print(f"mix.wav {DUR} s: {fi:.1f} LUFS integrated, true peak {tp:.1f} dBTP; voice, bed and {len(placed)} effects")
    print(f"speech {v_speech:.1f} LUFS | bed over the film {b_film:.1f} ({v_speech - b_film:.1f} dB under the speech)"
          f" | bed under the speech, unducked {b_open_under:.1f}, ducked {b_under:.1f} ({v_speech - b_under:.1f} dB under)"
          f" | bed between lines {b_gaps:.1f}")
    print("lines: " + ", ".join(f"{k} {m['start']:.2f}-{m['end']:.2f}" for k, m in meta.items()))
    # each effect alone (as placed), then re-measured in the summed effects stem, so neighbours that overlap count
    sfx_p = Power(kpow(sfx))
    rows = []
    for t, name, what, pk, ob, uv in placed:
        c = int(round(pk * SR))
        e = sfx_p.at(c, 0.1)
        rows.append((t, name, ob, uv, e - bed_ref(bed_p, c), voice_ref(vo_s, c, speech_l) - e, what))
    print(f"effects ({len(rows)}), each alone: {min(r[2] for r in rows):.1f} to {max(r[2] for r in rows):.1f} dB over "
          f"the bed, at least {min(r[3] for r in rows):.1f} dB under the voice; with overlapping neighbours: up to "
          f"{max(r[4] for r in rows):.1f} dB over the bed, at least {min(r[5] for r in rows):.1f} dB under the voice")
    for t, name, ob, uv, ob2, uv2, what in rows:
        flag = "  <-- check" if not (2.95 <= ob <= 6.05) or ob2 > 6.55 or uv2 < 2.95 else ""
        print(f"  {t:6.2f}  {name:11s} +{ob:3.1f} over the bed ({ob2:+4.1f} summed), {uv:4.1f} under the voice"
              f" ({uv2:4.1f})  {what}{flag}")
    ks = list(meta)
    print("breaths: " + ", ".join(f"{ks[i]}>{ks[i + 1]} {meta[ks[i + 1]]['start'] - meta[ks[i]]['end']:.2f}"
                                  for i in range(len(ks) - 1)))
    shutil.rmtree(tmp, ignore_errors=True)   # about 100 MB of working files per run


SFX = {  # secure-data-hub's sound/sfx-src (Mixkit free sound effects), the same one vocabulary
    "pop": "mixkit-2357.mp3",          # soft pop: a part arriving or lighting up; at pitch 0.8 the low pop (refusal only)
    "tick": "mixkit-1120.mp3",         # tick: a step or a counter (a chip, a status dot + word, a row, an end line)
    "whoosh_air": "mixkit-1492.mp3",   # a token travelling along a wire
    "whoosh_wind": "mixkit-1465.mp3",  # the camera gliding between close shots
    "sweep": "mixkit-3115.mp3",        # the two big camera moves (into the board, the pull-back)
    "pop_hard": "mixkit-3005.mp3",     # the soft hit: the mark on the drop, the 14, the mark on the end card
    "riser": "mixkit-2408.mp3",        # swells into the drop
}
# picture kind -> (sound, dB over the bed, default pitch). sound/picture_cues.py names the kinds.
KINDS = {"pop": ("pop", 4.0, 1.0), "tick": ("tick", 4.0, 1.0), "whoosh": ("whoosh_air", 3.5, 1.1),
         "glide": ("whoosh_wind", 3.0, 1.0), "sweep": ("sweep", 4.5, 1.0), "lowpop": ("pop", 5.0, 0.8),
         "riser": ("riser", 3.0, 1.0), "hit": ("pop_hard", 4.5, 0.9)}
VOICE_MARGIN = 3.0   # an effect stays at least this far under the voice speaking around it (or the speech level)
_cache = {}

# K-weighting (ITU-R BS.1770 at 48 kHz): levels below are in LUFS-like units, comparable with the speech's -16
_KB1, _KA1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
_KB2, _KA2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]


def kpow(y):
    """K-weighted power per sample, summed over channels."""
    y = np.atleast_2d(y)
    z = lfilter(_KB2, _KA2, lfilter(_KB1, _KA1, y, axis=-1), axis=-1)
    return (z ** 2).sum(0)


class Power:
    """Window levels of a K-weighted power signal (cumulative sums, so each lookup is O(1)). With a mask, a window's
    level counts only the masked samples (the voice: what she says around a moment, not the pauses)."""
    def __init__(self, p, mask=None):
        self.p = p; self.c = np.concatenate([[0.0], np.cumsum(p if mask is None else p * mask)])
        self.k = np.concatenate([[0.0], np.cumsum(np.ones(len(p)) if mask is None else mask.astype(float))])

    def at(self, centre, half_s):
        h = int(half_s * SR); a = max(0, centre - h); b = min(len(self.p), centre + h)
        k = self.k[b] - self.k[a]
        return None if k < 1 else -0.691 + 10 * np.log10((self.c[b] - self.c[a]) / k + 1e-12)

    def level(self, mask):
        return -0.691 + 10 * np.log10(self.p[mask].mean() + 1e-12)


def bed_ref(bed_p, c):
    """The bed's level at sample c: the louder of its 400 ms momentary and 3 s short-term levels, so an effect in a
    pause between the intro's chords sits over the music's level in that bar, not over the silence."""
    return max(bed_p.at(c, 0.2), bed_p.at(c, 1.5))


def voice_ref(vo_s, c, speech_l):
    """The voice's level around sample c: her speech within 0.5 s (pauses not counted), else the film's speech level."""
    v = vo_s.at(c, 0.5)
    return speech_l if v is None or v < speech_l - 15 else v


def clip(name):
    if name not in _cache:
        y = load(ROOT / "sound/sfx-src" / SFX[name])
        if name == "riser":    # let it swell in from nothing (as secure-data-hub)
            f = int(1.2 * SR); y[:, :f] *= np.linspace(0, 1, f) ** 2
        _cache[name] = y
    return _cache[name]


def place(out, name, t, over_db, pitch, bed_p, vo_s, speech_l):
    """Put one effect in: its peak one frame after the picture at t, over_db over the bed there (K-weighted: the
    effect over 200 ms around its peak against bed_ref), capped VOICE_MARGIN under voice_ref.
    Returns (peak time, dB over the bed, dB under the voice), the effect alone."""
    y = clip(name)
    if pitch != 1.0:   # small pitch steps rotate repeated sounds (resampling also shortens or lengthens them)
        y = np.vstack([librosa.resample(ch, orig_sr=SR, target_sr=int(SR / pitch)) for ch in y])
    pk = int(np.argmax(np.convolve(np.abs(y).mean(0), np.ones(240) / 240, "same")))
    pad = int(0.2 * SR)                         # silence around the clip, so its 200 ms window is never cut short
    own = Power(kpow(np.pad(y, ((0, 0), (pad, pad))))).at(pk + pad, 0.1)
    c = int(round((t + 1 / 30) * SR))          # the peak lands one frame after the picture
    b_ref, v_ref = bed_ref(bed_p, c), voice_ref(vo_s, c, speech_l)
    target = min(b_ref + over_db, v_ref - VOICE_MARGIN)
    y = y * 10 ** ((target - own) / 20)
    a = c - pk
    s0 = max(0, -a); a = max(0, a)
    b = min(out.shape[1], a + y.shape[1] - s0)
    out[:, a:b] += y[:, s0: s0 + (b - a)]
    return (c / SR, target - b_ref, v_ref - target)


def sfx_events(cues):
    """(picture time, sound, dB over the bed, pitch, what) from sound/picture-cues.json. A whoosh or a glide peaks at
    the fastest point of its move: a token (sound/picture_cues.py: 12 % linear, then power1.inOut) at 0.56 of its
    travel, a camera glide (power2.inOut) at half way."""
    e = []
    for c in cues:
        name, over, pitch = KINDS[c["kind"]]
        over = c.get("over", over)              # a few coinciding events are set lower in picture_cues.py
        t = c["t"]
        if c["kind"] == "whoosh": t += 0.56 * c["d"]
        if c["kind"] == "glide": t += 0.5 * c["d"]
        e.append((t, name, over, c.get("pitch", pitch), c["what"]))
    return e


if __name__ == "__main__":
    main()
