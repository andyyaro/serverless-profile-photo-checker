"""Kokoro af_heart takes (serverless profile-photo checker). Choose the best take of each narration line and time its words.

    python3 narration/pick.py takes     (the folder of <id>.<k>.wav takes)

For every line in lines.json: transcribe each take (mlx-whisper, word timestamps), score it by how exactly the words
match the script (and, as a tie-break, closeness to the slot's length budget), trim silence, and keep the winner as
chosen/<id>.wav (narration/overrides.json can force a take: {"v02": "v02.2.wav"}). words.json gets each chosen line's words with times relative to the clip's start.
"""
import json, re, sys, difflib
from pathlib import Path
import numpy as np, soundfile as sf
import mlx_whisper

HERE = Path(__file__).resolve().parent
ASR = "mlx-community/whisper-large-v3-turbo"
# this script's spellings: the TTS text says "A.P.I.", "A.W.S." and "Recognition"; Whisper may write digits or split words
NUM = {"1": "one", "2": "two", "3": "three", "14": "fourteen"}
def norm(s):
    s = re.sub(r"\[([^\]]+)\]\(/[^)]*/\)", r"\1", s).lower()     # "[word](/phonemes/)" -> "word"
    s = s.replace("-", " ").replace("a.p.i.", "api").replace("a.w.s.", "aws")
    for a, b in [("rekognition", "recognition"), ("server less", "serverless"), ("terra form", "terraform"),
                 ("it's", "it is"), ("lamda", "lambda")]:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = re.sub(r"\ba p i\b", "api", re.sub(r"\ba w s\b", "aws", s))
    return " ".join(NUM.get(w, w) for w in s.split())



def respell(text, ws):
    """Give the timed words the script's own spellings (lines.json), so the scenes' W() cues and the subtitles read
    "Rekognition", "Fourteen", "read-only", "profile-photo". Whisper's "-only" style pieces are joined to the word
    before; then each script token takes as many heard words as spell it. Returns None if they do not line up."""
    key = lambda s: norm(s).replace(" ", "")
    heard = []
    for w in ws:
        if heard and w["w"].startswith("-"):
            heard[-1] = {"w": heard[-1]["w"] + w["w"], "t0": heard[-1]["t0"], "t1": w["t1"]}
        else:
            heard.append(dict(w))
    out, i = [], 0
    for tok in text.split():
        want, got, j = key(tok), "", i
        while j < len(heard) and len(got) < len(want):
            got += key(heard[j]["w"]); j += 1
        if got != want or j == i:
            return None
        out.append({"w": tok, "t0": heard[i]["t0"], "t1": heard[j - 1]["t1"]})
        i = j
    return out if i == len(heard) else None

def trim(y, sr, thr_db=-42, pad=0.06):
    env = np.abs(y)
    win = int(0.01 * sr)
    rms = np.sqrt(np.convolve(env ** 2, np.ones(win) / win, "same"))
    on = np.where(20 * np.log10(rms + 1e-9) > thr_db)[0]
    if not len(on):
        return y, 0.0
    a, b = max(0, on[0] - int(pad * sr)), min(len(y), on[-1] + int(pad * sr))
    return y[a:b], a / sr


def main():
    takes_dir = HERE / sys.argv[1]
    lines = json.loads((HERE / "lines.json").read_text())
    tts = json.loads((HERE / "lines-tts.json").read_text())
    out = HERE / "chosen"; out.mkdir(exist_ok=True)
    over = json.loads((HERE / "overrides.json").read_text()) if (HERE / "overrides.json").exists() else {}
    words_out, report = {}, []
    for key, text in lines.items():
        best = None
        cands = [takes_dir / over[key]] if key in over else sorted(takes_dir.glob(f"{key}.*.wav"))
        for f in cands:
            y, sr = sf.read(f)
            if y.ndim > 1: y = y.mean(1)
            y, cut = trim(y, sr)
            tmp = out / f"_{f.name}"; sf.write(tmp, y, sr)
            r = mlx_whisper.transcribe(str(tmp), path_or_hf_repo=ASR, language="en", word_timestamps=True)
            tmp.unlink()
            heard = " ".join(s["text"] for s in r["segments"]).strip()
            score = difflib.SequenceMatcher(None, norm(tts[key]).split(), norm(heard).split()).ratio()
            dur = len(y) / sr
            # words-per-second sanity: penalise very slow, draggy takes slightly
            wps = len(text.split()) / max(dur, 0.1)
            rank = score + (0.03 if f.name.endswith(".1.wav") else 0.0)
            ws = [{"w": w["word"].strip(), "t0": round(w["start"], 3), "t1": round(w["end"], 3)}
                  for s in r["segments"] for w in s.get("words", [])]
            if best is None or rank > best[0]:
                best = (rank, f.name, y, sr, heard, dur, ws, score)
        rank, name, y, sr, heard, dur, ws, score = best
        sf.write(out / f"{key}.wav", y, sr)
        ws = respell(text, ws) or (print(f"warning: {key} words keep Whisper's spelling", file=sys.stderr) or ws)
        words_out[key] = {"text": text, "dur": round(dur, 3), "take": name, "words": ws}
        report.append(f"{key} {name:10s} {dur:5.2f}s match={score:.2f}  heard: {heard}")
    (HERE / "words.json").write_text(json.dumps(words_out, indent=1))
    print("\n".join(report))


if __name__ == "__main__":
    main()
