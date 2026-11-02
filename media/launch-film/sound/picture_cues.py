"""The picture's event times, for the sound effects.

    python3 -I sound/picture_cues.py        # writes sound/picture-cues.json (sound/mix.py runs it for you)

The scenes time every entrance from window.VO (the W() helper) and window.TM; this script applies the same formulas to
assets/vo.js and sound/timing.json, so the list follows a re-voiced or re-slotted line exactly as the picture does.
If a scene's cue formula changes in compositions/*.html, change it here too (each entry names its scene and element).

Kinds, in secure-data-hub's one vocabulary (sound/mix.py maps each kind to its sound and level):
  pop     a part arriving or lighting up (a card, the mark's badge)
  tick    a step or a counter (a chip, a status dot + word, a credit row, an end-card line)
  whoosh  a token travelling a wire (t = when it starts to move, d = how long)
  glide   the camera gliding between two close shots (t = start, d = how long)
  sweep   the two big camera moves (into the board, the pull-back to the whole board)
  lowpop  ONLY a refusal: the 400 "only one face" answer
  riser   swells into the drop
  hit     a soft hit: the mark on the drop, the 14 landing, the mark on the end card
t is the picture's moment (the start of its tween); mix.py puts each sound's peak one frame after it (for whoosh and
glide: one frame after the fastest point of the move). "pitch" is optional (repeated ticks step up). "over" (dB over
the bed) is set only where two sounds land together, so their sum stays within about 6 dB of the bed.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TM = json.loads((ROOT / "sound/timing.json").read_text())
vo = (ROOT / "assets/vo.js").read_text()
VO = json.loads(vo[vo.index("{"): vo.rindex("}") + 1])
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def W(k, w, nth=0):
    """Film seconds of a word, as the scenes' W() finds it (exact match first, then prefix)."""
    alts = w.split("|")
    for exact in (True, False):
        c = 0
        for x in VO[k]["words"]:
            t = norm(x["w"])
            if any(t == a if exact else t.startswith(a) for a in alts):
                if c == nth:
                    return x["t0"]
                c += 1
    return VO[k]["start"]


E = []


def add(t, kind, what, d=None, pitch=None, over=None):
    E.append({"t": round(t, 3), "kind": kind, "what": what, **({"d": d} if d else {}), **({"pitch": pitch} if pitch else {}),
              **({"over": over} if over else {})})


# s1-hook (scene starts at 0)
add(TM["s1"][0] + 0.3, "pop", "s1 photo card (goodphoto.jpeg)")
add(W("v02", "two") + 0.1, "pop", "s1 two-face schematic card")
add(W("v02", "which"), "tick", "s1 status: which face?")
# s2-title: the riser swells into the drop, the mark lands on it, its badge follows; the internship chip is silent text
add(TM["cues"]["mark_title"], "riser", "s2 the drop (riser into it)", over=3.0)
add(TM["cues"]["mark_title"], "hit", "s2 the mark lands on the drop", over=3.0)
add(TM["cues"]["mark_title"] + 0.45, "pop", "s2 the mark's checkmark badge", pitch=1.12)
add(VO["v03"]["end"] + 1.05, "tick", "s2 chip: InternPass research internship")
# s3-board
s3 = TM["s3"][0]
add(s3 + 0.3, "sweep", "s3 camera sweeps into the board")
add(W("v04", "client"), "pop", "s3 interact.py card lights")
add(W("v04", "encodes"), "tick", "s3 chip base64")
add(W("v04", "posts"), "tick", "s3 chip requests.post", pitch=1.05)
add(W("v04", "posts") + 0.25, "whoosh", "s3 token {image} client -> API Gateway", 0.95, over=3.0)
add(W("v04", "api"), "pop", "s3 API Gateway card lights", over=3.5)
add(W("v05", "hands") + 0.3, "whoosh", "s3 token API Gateway -> Lambda (with the glide right)", 0.6)
add(W("v05", "lambda"), "pop", "s3 Lambda function lights")
add(VO["v05"]["end"] + 0.1, "glide", "s3 camera glides right to Rekognition (b2)", 1.3)
add(W("v06", "asks") + 0.25, "whoosh", "s3 token Lambda -> Rekognition", 0.55)
add(W("v06", "rekognition"), "pop", "s3 Amazon Rekognition card lights")
add(W("v06", "faces") + 0.1, "whoosh", "s3 token FaceDetails (two faces) -> guard", 0.9)
add(W("v07", "exactly"), "pop", "s3 guard card lights: Exactly one face?")
add(W("v07", "please"), "lowpop", "s3 status: 400 · Please upload a picture with only one face")
add(VO["v07"]["end"] + 0.05, "glide", "s3 camera glides down to the rule (b3)", 1.3)
add(W("v08", "passes"), "pop", "s3 rule card lights: Smiling, eyes open?")
add(W("v08", "smiling"), "tick", "s3 chip Smile and EyesOpen · Value true")
add(W("v08", "open"), "tick", "s3 status: 200 · Good Profile Photo", pitch=1.06)
add(W("v09", "bad"), "tick", "s3 status: 200 · Bad Profile Photo", pitch=0.95)
add(VO["v09"]["end"] + 0.25, "glide", "s3 camera glides to the role (b4)", 1.3)
add(W("v10", "role"), "pop", "s3 role card lights (as the b4 glide arrives)", over=3.0)
for i in range(3):
    add(W("v10", "three") + i * 0.14, "tick", f"s3 role chip {i + 1} (log action)", pitch=(1.0, 1.05, 1.1)[i])
add(W("v10", "actions"), "pop", "s3 CloudWatch Logs card lights", pitch=1.06)
add(W("v10", "readonly"), "tick", "s3 role chip AmazonRekognitionReadOnlyAccess", pitch=1.15)
w0 = VO["v10"]["end"]
add(w0 + 0.3, "sweep", "s3 pull-back to the whole board (power2.inOut from v10's end, under way)")
add(w0 + 1.25, "whoosh", "s3 answer token returns Lambda -> API Gateway -> client", 1.12)
add(w0 + 1.25 + 1.15, "tick", 's3 client status: "Good Profile Photo"', pitch=1.06)
# s4-proof
add(W("v11", "fourteen") - 0.05, "hit", "s4 the big 14 lands")
add(W("v11", "terraform") + 0.1, "pop", "s4 lambda.tf card fills in")
add(W("v11", "resources"), "pop", "s4 apigw.tf card fills in", pitch=1.06)
add(W("v11", "validate") - 0.1, "tick", "s4 status: terraform validate")
add(VO["v12"]["start"] - 0.55 + 0.45, "pop", "s4 the credit card arrives")
add(W("v12", "aws") - 0.1, "tick", "s4 credit row 1 (AWS example)")
add(W("v12", "oneface") - 0.1, "tick", "s4 credit row 2 (added)", pitch=1.06)
# s5-end: the mark on the track's last full bar, its badge, the two lines; the URL lands on the track's final hit (no effect)
add(TM["cues"]["mark_end"], "hit", "s5 the mark lands on the end card")
add(TM["cues"]["mark_end"] + 0.4, "pop", "s5 the mark's checkmark badge", pitch=1.12)
add(TM["cues"]["end_line1"], "tick", "s5 end line 1: One face, smiling, eyes open.")
add(TM["cues"]["end_line2"], "tick", "s5 end line 2: 14 Terraform resources.", pitch=1.06)

E.sort(key=lambda e: e["t"])
(ROOT / "sound/picture-cues.json").write_text(json.dumps(E, indent=1, ensure_ascii=False) + "\n")
counts = {k: sum(e["kind"] == k for e in E) for k in ("pop", "tick", "whoosh", "glide", "sweep", "lowpop", "riser", "hit")}
print(f"sound/picture-cues.json: {len(E)} events", counts)
