# Serverless profile-photo checker launch film: storyboard and build

66.3 s, 1920 × 1080, 30 fps (1,989 frames). H.264 with AAC at 256 kb/s; measured on the MP4:
-16.1 LUFS integrated, true peak -2.1 dBTP, loudness range 4.9 LU. Every claim in it and its
source is in [FACTS.md](FACTS.md); the brief, with every cue time, is [SPEC.md](SPEC.md).

## What is real and what is drawn

- **Real:** every name, number and code word on screen comes from this repository at `fd8589e`:
  `POST /friendly` on the REST API `my-api` (REGIONAL, stage `dev`, us-east-1), the Lambda
  `Detection_Lambda_Function`, `detect_faces` with `Attributes ALL`, the guard
  `len(FaceDetails) != 1`, the Smile and EyesOpen rule, the role and its four permissions, 14
  Terraform resources in 163 lines. The two photos are the repository's own test fixtures.
- **Run locally:** the answers on the board ("200 · Good Profile Photo", "200 · Bad Profile Photo",
  "400 · Please upload a picture with only one face") are the shapes the real handler returned
  when it was run with Rekognition stubbed, and `terraform validate` was run on a copy of the
  Terraform with no credentials ([research/](research/)).
- **Not claimed:** nothing was deployed and AWS was never called, so the film shows no
  Rekognition result, confidence or account number. The face attributes in the local runs came
  from the stub, so the film never says what Rekognition would make of the two photos: they stand
  for the README's fixture that should pass and the one that should fail, and the rule decides on
  screen.
- **Drawn:** the board itself, a diagram of the parts in HTML; the two-face card in the opening,
  two glyphs rather than a photo; and the mark on the title and end card, made for the film only
  (the project has no logo, see [assets/brand/README.md](assets/brand/README.md)).

## The film

| Time (s) | Scene | Narration | What you see |
|---|---|---|---|
| 0–9.5 | Hook | "One question: is this usable as a profile photo? And with two people in frame, which face is it about?" | goodphoto.jpeg in a white card; above it, under a small "One question", "Is this usable as a profile photo?" in bold, word by word. A second card with two person glyphs and "which face?" in grey. |
| 9.5–14.6 | Title | "This is the serverless profile-photo checker." | The mark pops on the music's drop with "serverless"; "Serverless profile-photo checker", then, silent, "AWS Lambda · API Gateway · Amazon Rekognition" and a chip, "InternPass research internship · June to July 2025". |
| 14.2–21.4 | The board: the request | "A small client encodes the photo and posts it to API Gateway. The gateway hands it to a Lambda function." | "From photo to answer", "POST /friendly · stage dev · us-east-1". The camera sweeps in to the `interact.py` card (base64, requests.post) with the two photos. A token travels the `POST /friendly` wire with "558,892 characters" (goodphoto.jpeg as base64) to API Gateway (REST API my-api · REGIONAL), then along `lambda:InvokeFunction` to the Lambda. |
| 21.4–31.4 | The faces | "It asks Amazon Rekognition to describe the faces it finds. Unless there is exactly one, it answers: please upload a picture with only one face." | A glide right: Rekognition (`detect_faces`, `Attributes ALL`) lights; a FaceDetails token comes back; the guard "Exactly one face?" with `len(FaceDetails) != 1`, and the red "400 · Please upload a picture with only one face". |
| 31.4–38.9 | The rule | "One face passes only if it's smiling and its eyes are open. Anything else comes back as a bad profile photo." | A glide down: "Smiling, eyes open?" with "Smile and EyesOpen · Value true"; goodphoto.jpeg gets the green "200 · Good Profile Photo" on "open", badphoto.png the orange "200 · Bad Profile Photo" on "bad". |
| 38.9–44.2 | The role | "Its role allows three log actions and read-only Rekognition, nothing else." | `Detection_Lambda_Function_Role`, dashed to the Lambda, with `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents` and `AmazonRekognitionReadOnlyAccess`; CloudWatch Logs lights. |
| 44.2–47.8 | The whole board | (none) | The camera pulls back to the whole architecture and holds; the answer returns to `interact.py`, whose card shows "Good Profile Photo". |
| 47.4–60.4 | Proof and credit | "Fourteen Terraform resources build all of it, and terraform validate passes. It builds on an AWS example, adding the one-face check and the photo rule." | "Infrastructure as code", "lambda.tf + apigw.tf · 163 lines". A big 14; lambda.tf (5 resources) and apigw.tf (9) with each resource type; "terraform validate · Success! The configuration is valid.". Then "Built on an AWS example": "Handler and client scaffolding: AWS's Rekognition + Lambda example" and "Added: the one-face check and the Smile + EyesOpen rule" (python/rekognition.py, lines 37-49). |
| 60.0–66.3 | End card | "Serverless profile-photo checker." | The mark, the name, "One face, smiling, eyes open." and "14 Terraform resources.", then github.com/andyyaro/serverless-profile-photo-checker on the track's final hit. The picture fades over the last second. |

## Look

- **Style:** an architecture film, like the CERFODES architecture video: one big board of the
  parts, a camera that glides and zooms across it as the voice names each one, then pulls back to
  the whole. Cards fill in on their word, wires draw, and one token at a time travels a wire.
- **Design system:** HIG Native's light tokens, as CERFODES uses them: the grouped background
  #f2f2f7, white cards with no shadows, line glyphs in system-colour tiles (API Gateway indigo
  #6155f5, the Lambda blue #0088ff, Rekognition teal #00c3d0, the rest grey), thin grey wires
  with small edge labels, and status as a dot plus a word: green #34c759 for "Good Profile Photo",
  orange #ff8d28 for "Bad Profile Photo", red #ff383c only for the 400 refusal.
- **Brand:** none; the project has no logo or colours. The mark is a system-blue tile with a
  white person glyph and a small green check badge, made for the film only (`deploy/mark.svg`).
- **Type:** SF Pro throughout, code words included, loaded through `local()`. No monospace, no
  caps kickers and no em dashes on screen. Subtitles are burned in on a dark pill; the lines shown
  big on screen are not subtitled.

## Sound

- **Voice:** Kokoro-82M, voice af_heart, 13 lines and 131 words, the speed 1.0 take of each,
  matching the script word for word. "API", "AWS" and "Rekognition" are spelled for the voice in
  `narration/lines-tts.json`; `narration/words.json` keeps the script's spellings so the scenes
  find their cue words.
- **Music:** "Sweet September" by Arulo (Mixkit 282), 76 BPM, cut on its bar lines by
  `sound/music.py`: the track's real opening, bar 1 skipped so the drop lands at 9.474 s on
  "serverless", grooves A and B under the board and the proof (groove B enters at 34.737 s, just
  before "open"), and the track's last full bar, final hit and ring-out under the end card. The
  URL lands on the final hit at 63.158 s.
- **Effects:** 47 soft Mixkit interface sounds, one per picture event (`sound/picture_cues.py`
  works them out from the same word times the scenes use): pops for parts arriving, ticks for
  steps, an air whoosh for each token, a wind whoosh for each glide, a sweep for the two big
  camera moves, and a low pop only for the 400 refusal. Each peaks one frame after its picture,
  3 to 5 dB over the bed and at least 3 dB under the voice. The list is in
  [assets/audio/SOURCE.md](assets/audio/SOURCE.md).
- **Levels:** speech set to -16 LUFS, the bed 9 dB under it and ducked 4.5 dB more while the voice
  speaks; master -16.1 LUFS, true peak -2.1 dBTP.

## Build

Get the inputs first: `tools/fetch_vendor.sh` for GSAP, then the music and effects listed in
[assets/audio/SOURCE.md](assets/audio/SOURCE.md). The render needs a Mac with SF Pro. The Python
steps need numpy, soundfile, scipy, librosa and mlx-whisper.

```sh
tools/fetch_vendor.sh
# Voice each line of narration/lines-tts.json with Kokoro-82M (af_heart) at speeds 1.0 and 1.06,
# as narration/takes/<id>.<k>.wav
python3 -I narration/pick.py takes           # best take per line, words.json
python3 -I sound/music.py                    # assets/audio/music.wav, sound/grid.json
python3 -I sound/mix.py                      # vo.js, timing.js, picture-cues.json, mix.wav
python3 -I build.py                          # scene windows, subtitles, the .vtt
node scripts/build-icons.mjs .               # only when the glyph list changes
npx --yes hyperframes@0.8.173 lint && npx --yes hyperframes@0.8.173 check
npx --yes hyperframes@0.8.173 render -o renders/raw.mp4 --fps 30
ffmpeg -y -i renders/raw.mp4 -i assets/audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k \
  -shortest -movflags +faststart renders/photo-checker-v1.mp4
```

The ffmpeg step puts the exact mix back on the picture, so the film's AAC is encoded once,
straight from `mix.wav`. The scenes find their cue words by text in `window.VO`, so a re-voiced
line re-times the picture by itself, and `sound/picture_cues.py` applies the same formulas for the
effects. If a scene's cue formula changes, change it in `picture_cues.py` as well.

## The README preview

`docs/assets/readme/photo-checker-in-action.webp` is the middle of the board, 22.6–38.6 s of the
film: Rekognition describes the faces, the one-face guard answers 400, and the rule gives
goodphoto.jpeg "Good Profile Photo" and badphoto.png "Bad Profile Photo". It is 1200 px wide,
15 fps, 1.0 MB. A keyframe every 6 to 12 frames and `-exact` keep lossy WebP from leaving faint
seams in the flat white cards where only part of the frame changes.

```sh
mkdir -p preview
ffmpeg -ss 22.6 -i renders/photo-checker-v1.mp4 -t 16 \
  -vf "fps=15,scale=1200:676:flags=lanczos" preview/f%03d.png
img2webp -loop 0 -kmax 12 -kmin 6 -lossy -q 90 -m 6 -d 67 -exact preview/f*.png \
  -o ../../docs/assets/readme/photo-checker-in-action.webp
```
