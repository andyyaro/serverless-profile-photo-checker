# Serverless profile-photo checker launch film: SPEC

```text
GOAL:    a cloud engineer understands, in about a minute, how one photo becomes one answer: a small client posts
         it to API Gateway, a Lambda asks Amazon Rekognition for the faces, a one-face guard and a smile + open-eyes
         rule decide, and 14 Terraform resources (with a role that allows only logs and read-only Rekognition)
         build it all. Built during the InternPass cloud research internship (June to July 2025), on top of AWS's
         published Rekognition + Lambda example, credited on screen.
OUTPUT:  HyperFrames 0.8.173, 1920 x 1080, 30 fps, 66.3 s (1989 frames), burned-in subtitles.
         renders/photo-checker-v1.mp4.
SOUND:   "Sweet September" (Arulo, Mixkit 282, Mixkit Stock Music Free License), sound/track.mp3, 98.7 s.
         Measured (librosa, sound stage, 2026-11-01): 76.0 BPM, 4/4, half-time feel. The beat tracker reads 101
         (and read 152 in research); neither fits the kicks, which repeat every 3.158 s (5.33 beats at 101). Kick
         onsets at bar starts 12.638 + 3.15792 n to within a few ms through bar 28; snare on beats 2 and 4.
         Track bar n = 0.0063 + 3.15792 n.
           intro (keys, no drums)   0.00 - 12.64   bars 0-3, chords G | F | G | Gm/Eb (chroma)
           DROP                     12.638         kick + bass enter on the downbeat (bar 4)
           groove A                 12.64 - 37.90  bars 4-11, -14 dB RMS
           groove B (fuller)        37.90 - 63.17  bars 12-19, -12 dB (about 2 dB up); a pickup kick 0.12 s
                                                   before each downbeat
           bar 20                   63.17 - 66.32  half a bar of groove, thins from 64.74
           breakdown                66.32 - 75.80  bars 21-23 (not used)
           groove C                 75.80 - 91.59  bars 24-28; last full bar 88.43 - 91.59
           final hit + ring-out     91.59 - 94.38  (attack from 91.40), then silence
         THE EDIT (sound/music.py, sound/grid.json; joins on bar lines, 20 ms crossfades, no added clicks: the
         jumps at each join equal the source's at the same points):
           film  0.000 -  3.158   track  0.006 -  3.164   bar 0, the track's real opening (G)
           film  3.158 -  9.474   track  6.322 - 12.638   bars 2-3; bar 1 (F) skipped, G joins G (chroma 0.93)
           film  9.474 - 60.000   track 12.638 - 63.171   DROP on "serverless"; groove A; groove B from 34.737
           film 60.000 - 66.300   track 88.428 - ...      the last full bar under the end card, the final hit
                                                          at 63.158, the track's own ring-out to 65.95, 0.35 s fade
         Film bar k starts at k x 3.15792 s: the drop is bar 3, groove B bar 11, the end card bar 19, the final
         hit bar 20. The hook is short (two lines), so bar 1 goes and the drop comes at 9.474, not 12.64; the
         voice runs to 58.2, so all 16 bars of grooves A + B play before the end card.
         Voice Kokoro af_heart, all 13 lines the speed 1.0 take, every word matched (Whisper large-v3-turbo,
         match 1.00; narration/words.json carries the script's spellings: Rekognition, Fourteen, read-only).
         Lines (film s): v01 1.60-4.59, v02 5.38-8.10, v03 8.95-11.25 ("serverless" on the drop: its "s" at 9.42,
         the vowel 9.57), v04 14.62-18.49, v05 19.10-21.22, v06 21.90-25.63, v07 26.25-31.29, v08 31.86-35.24
         ("open" at 34.84, 0.1 s after groove B), v09 35.85-38.60, v10 39.35-43.97, v11 47.95-52.64, v12
         53.40-58.20, v13 60.55-62.36. Breaths 0.57-0.85 s; longer, picture-only gaps after v03 (3.4 s: stack
         + chip), v10 (4.0 s: the pull-back) and v12 (1.8 s on the credit before the end card).
         Levels (sound/mix.py prints them, re-measured on the result; finish stage): master -16.1 LUFS integrated,
         true peak -2.1 dBTP; speech -15.3 LUFS in the master (set to -16, then the master's gain: the gaps are
         bed only); the bed 9.0 dB under the speech over the film and 13.3 dB under while she speaks (ducked
         4.5 dB, 40 ms attack, 450 ms release). The voice is measured as the two identical channels it plays as.
         Effects (finish stage): 47, one per picture event in sound/picture-cues.json (sound/picture_cues.py
         mirrors the scenes' cue formulas; mix.py runs it). secure-data-hub's vocabulary and files
         (sound/sfx-src, Mixkit free sound effects):
           soft pop (2357)         a part arriving or lighting up (cards, the marks' badges, the credit card)  15
           tick (1120)             a step or a counter (chips, status dots + words, credit rows, end lines)    17
           whoosh_air (1492)       a token travelling a wire; peaks at the token's fastest point              5
           whoosh_wind (1465)      the camera gliding between close shots (b2, b3, b4); peaks half way        3
           sweep (3115)            the two big camera moves (into the board, the pull-back)                   2
           low pop (2357 at 0.8)   ONLY the refusal: the 400 "only one face" answer (as secure-data-hub)      1
           riser (2408)            swells into the drop                                                       1
           soft hit (3005)         the mark on the drop, the big 14, the mark on the end card                 3
         Each sound's peak lands one frame after its picture. Each is levelled by measurement, K-weighted: the
         effect over 200 ms around its peak sits 3-5 dB over the bed there (the louder of the bed's 400 ms and
         3 s levels, so the intro's pauses between chords do not count as the bed), and at least 3 dB under the
         voice (her speech within 0.5 s, else the film's speech level). Where two land together (the drop's
         riser + hit, the request token + API Gateway, the b4 glide + the role card) each is set to +3 to +3.5,
         and their sum peaks at +6.2 dB over the bed. The URL lands on the track's own final hit, no effect.
LOOK:    Reference: the CERFODES architecture video, in Andy's HIG Native design system (an unofficial web
         design system that follows Apple's HIG; tokens from its tokens.json). The project has no brand (assets/brand/
         README.md), so the look is HIG Native defaults. Taken from CERFODES:
           ground   grouped-background-primary #f2f2f7; zones fill-quaternary rgba(116,116,128,.08), radius 26
           cards    white (background-primary), radius 16-20 on the board, 22-26 for big cards; NO shadows;
                    a 44-52 px rounded tile (radius 11-13) in a system colour with a white 24x24 line glyph from
                    the HIG Native icon set (copy CERFODES source/scripts/vendor/hig-icons.js + build-icons.mjs,
                    sprite between HF:ICONS markers), a bold title (600, 22-31 px), a grey secondary line
           grey     label-secondary #68686d (video legibility, as CERFODES), never the HIG rgba value
           status   dot + word, always both: green #34c759 "Good Profile Photo", orange #ff8d28 "Bad Profile
                    Photo", red #ff383c only the 400 refusal; gray #8e8e93 neutral
           colours  tiles: client gray, API Gateway system-indigo #6155f5 (globe), Lambda system-blue #0088ff
                    (gearshape), Rekognition system-teal #00c3d0 (eye), guard and rule gray (person.crop.circle,
                    checkmark.circle), role gray (lock), logs gray (text.alignleft), Terraform indigo
                    (square.3.layers.3d.top.filled). No AWS service logos.
           chips    capsules in fill-tertiary rgba(118,118,128,.12), 18-20 px Medium: code words live here, in
                    the system face (detect_faces, Attributes ALL, POST /friendly)
           wires    system-gray #8e8e93, 2.5-3 px, round caps, small filled arrowheads; edge labels 17-19 px
                    Medium label-secondary; dashed wires for "assumed by" / policy links
           titles   section title top left: "Bold title" 46 px 700 + grey subtitle 26 px on the same baseline
           type     the system face exactly as CERFODES: @font-face "HostUI" src local("SF Pro"),
                    local("SF Pro Display"), local(".SF NS"); --font-ui: "HostUI", -apple-system, ... sans-serif.
                    NO monospace (never --font-mono, never SFNSMono), no caps kickers, so no Montserrat.
                    Verify in the first snapshot that SF Pro rendered (not Inter).
           subs     burned-in subtitles: a dark pill rgba(0,0,0,.74), radius 18, 38/47 px Medium white, bottom
                    30 px, max 1240 px, at most 2 lines of 42 characters; the band y >= 936 stays free (the board
                    is masked to y < ~930 through every camera move). Lines shown big on screen (v03, v13) are not
                    subtitled.
           mark     no project logo: a film-only tile (system-blue rounded square, white person.crop.circle, small
                    green checkmark.circle.fill badge) for the title and the end card.
           photos   the repo's own fixtures (assets/repo/goodphoto.jpeg, badphoto.png, 1024 x 1536, AI-generated:
                    the shirt reads "AI GENERATED PIC"; keep that text visible) inside white cards, radius 16.
MOTION:  CERFODES grammar, calm. Cues by word through window.VO and the W() helper (secure-data-hub pattern).
         Cards pop (opacity 0, y 18, scale 0.96 -> 1, back.out(1.5), 0.6 s). Skeleton placeholders: card shapes
         arrive faint (opacity 0.5) and fill in on the narrated word (content rises 10 px, a 1.035 nudge). Wires
         draw by stroke-dashoffset (0.25-0.5 s, power2.inOut), the arrowhead last. Status dots slide in from x -8
         0.45 s after their card. One token at a time travels a wire, drawn under the cards. One big board: the
         camera glides (power2.inOut, 1.1-1.5 s) and zooms (close shots >= 1.55) across it, then pulls back to
         the whole architecture at 1.0, where secondary lines fold away (titles, status words and chips stay).
         Scene exits fade 0.4 s, overlapping the next scene by 0.4 s. No shake, no flood, one thing at a time.
SHOTS:   (sound stage, 2026-11-01: windows = sound/timing.json SCENES, which run 0.4 s past the next start for the
         exit fade; cue words from window.VO, times below are film seconds)
         s1 hook     0-9.474      the keys intro (film bars 0-2). A white card with goodphoto.jpeg from ~0.3; beside
                                  it, bold, word by word: "Is this usable as a profile photo?" (v01 1.60-4.59, "is"
                                  2.52 ... "photo" 3.98). On v02 (5.38-8.10) a second card arrives on "two people"
                                  (5.70): a skeleton with two person.crop.circle glyphs (schematic, not a photo) and
                                  "● which face?" on "which face" (6.88; gray: orange is kept for "Bad Profile
                                  Photo"). Both clear 8.9-9.3, under "This is the".
         s2 title    9.474-14.211 the DROP (bar 3): the mark pops on 9.474 with "serverless"; the wordmark
                                  "Serverless profile-photo checker" (v03 8.95-11.25);
                                  then, silent, "AWS Lambda · API Gateway · Amazon Rekognition" in grey and a chip
                                  [calendar] "InternPass research internship · June to July 2025" (~11.6 and ~12.3,
                                  silent; read until the board comes in on the half bar 14.211).
         s3 board    14.211-47.369 ONE persistent composition ("From photo to answer", subtitle "POST /friendly ·
                                  stage dev · us-east-1"). Camera path:
           b1 request  14.2-21.4    (sweep in at 14.211) close on the client ("client" 15.00): interact.py card
                                  (chips base64, requests.post) with the two fixture thumbnails; the wire to API
                                  Gateway draws, label POST /friendly; a token {"image": "..."} travels it with a
                                  chip "558,892 characters" (goodphoto.jpeg as base64) (v04 14.62-18.49; "API
                                  Gateway" 17.42). API Gateway card: REST API my-api · REGIONAL. v05 (19.10-21.22,
                                  "Lambda" 20.34): the wire to the Lambda card (Detection_Lambda_Function,
                                  rekognition.lambda_handler), edge label lambda:InvokeFunction.
           b2 faces    21.4-31.4    glide right (21.3-22.6): Rekognition card (detect_faces · Attributes ALL) lights
                                  on "Rekognition" (v06 21.90-25.63, 22.84); on "faces" (24.56) a
                                  FaceDetails token comes back; the guard card "Exactly one face?" with the code
                                  chip len(FaceDetails) != 1; the two-face schematic goes in and the red answer
                                  lights: "● 400 · Please upload a picture with only one face" (v07 26.25-31.29:
                                  "exactly one" 26.93, "please upload" 28.77; low pop).
           b3 rule     31.4-38.9    glide down (31.3-32.6; review: framed at 1.5 so the whole Lambda zone fits): rule card "Smiling, eyes open?" with chip Smile and
                                  EyesOpen · Value true. goodphoto.jpeg -> "● Good Profile Photo" (green) on "open"
                                  (v08 31.86-35.24: "smiling" 33.50, "open" 34.84; groove B enters at 34.737);
                                  badphoto.png -> "● Bad Profile Photo" (orange) on "bad" (v09 35.85-38.60, 37.33).
                                  The answer token returns to interact.py, whose card prints "Good Profile Photo".
           b4 role     38.9-44.2    glide to the role card Detection_Lambda_Function_Role, dashed to the Lambda:
                                  chips logs:CreateLogGroup · logs:CreateLogStream · logs:PutLogEvents and
                                  AmazonRekognitionReadOnlyAccess (v10 39.35-43.97: "three log actions" 40.23,
                                  "read-only Rekognition" 41.71); the CloudWatch Logs card (errors logged
                                  with the function ARN) lights.
           wide        44.2-47.8    pull back (sweep, ~44.3-45.7) to the whole board at 1.0 and hold, no voice.
         s4 proof    47.369-60.0  "Infrastructure as code" / "lambda.tf + apigw.tf · 163 lines". A big 14, then
                                  two grouped cards fill in as skeletons: Function (5) aws_iam_role, aws_iam_policy,
                                  aws_iam_role_policy_attachment x2, aws_lambda_function; API (9) rest_api, resource,
                                  method, integration, method_response, integration_response, deployment, stage,
                                  aws_lambda_permission. Status row "● terraform validate · Success! The
                                  configuration is valid." (v11 47.95-52.64: "Fourteen" 47.95, "validate" 51.49).
                                  Then the credit, two rows with icons (v12 53.40-58.20: "AWS example" 54.16,
                                  "one-face check" 56.26), held to 60.0:
                                  [doc] "Handler and client scaffolding: AWS's Rekognition + Lambda example"
                                  [checkmark.circle] "Added: the one-face check and the Smile + EyesOpen rule".
         s5 end      60.0-66.3    on the track's last full bar (bar 19): the mark pops on 60.0; "Serverless
                                  profile-photo checker" (v13 60.55-62.36); two lines with icons (TM.cues 62.61,
                                  62.96, a tick each): [person.crop.circle] "One face, smiling, eyes open." and
                                  [square.3.layers.3d.top.filled] "14 Terraform resources." ; the URL in grey:
                                  github.com/andyyaro/serverless-profile-photo-checker on the track's final hit
                                  (63.158). The ring-out ends 65.95; fade the picture over the last 1.0 s (65.3-66.3).
OBJECTS: real code and real outputs only (FACTS.md has every source):
         python/rekognition.py: lambda_handler, event['image'] base64 -> {'Bytes': ...},
           rekognition.detect_faces(Image=image, Attributes=['ALL']), len(FaceDetails) != 1 -> ValueError
           'Please upload a picture with only one face', Smile['Value'] and EyesOpen['Value'] -> 'Good Profile
           Photo' else 'Bad Profile Photo'; responses {"statusCode": 200, "body": "\"Good Profile Photo\""} and
           {"statusCode": 400, "body": {"Error": "ValueError", "ErrorMessage": "Please upload a picture with only
           one face"}} (research/handler-run.txt); errors logged as "Error function <function ARN>: <message>".
         interact.py: python interact.py <url> <image>; prints "Good Profile Photo" (with its JSON quotes), or
           "Error: 400" + "Message: {...}" (research/cli-run.txt).
         apigw.tf: REST API my-api (REGIONAL), resource /friendly, POST, authorization NONE, integration type AWS,
           stage dev, AllowExecutionFromAPIGateway (lambda:InvokeFunction, apigateway.amazonaws.com), output
           deployment_invoke_url, redeploy trigger sha1 + create_before_destroy (optional detail, not spoken).
         lambda.tf: provider aws us-east-1, Detection_Lambda_Function (rekognition.lambda_handler, python3.8),
           Detection_Lambda_Function_Role (trust lambda.amazonaws.com), the logs policy (3 actions),
           AmazonRekognitionReadOnlyAccess.
         14 resources / 163 lines; terraform validate "Success! The configuration is valid." (research/
         terraform-validate.txt). Fixtures goodphoto.jpeg / badphoto.png and "558,892 characters".
         Never shown: a measured Rekognition result or confidence (Rekognition was never called), any AWS account
         number, the quotes-service/ folder or the RKE2 cluster (a different piece of work).
ARCH:    the board's 13 parts and their arrows (all names from the repo):
          1 goodphoto.jpeg / badphoto.png (fixtures)    ->  2 interact.py (client, Dockerfile python:3.9-slim)
          2 interact.py  --POST /friendly {"image": base64}-->  3 API Gateway REST API my-api (REGIONAL, stage dev)
          3 my-api  --integration type AWS · lambda:InvokeFunction (AllowExecutionFromAPIGateway)-->
          4 Lambda Detection_Lambda_Function (rekognition.lambda_handler)
          4 Lambda  --detect_faces · Attributes ALL-->  5 Amazon Rekognition
          5 Rekognition  --FaceDetails-->  6 guard: exactly one face?
          6 guard  --not 1-->  7 400 ValueError "Please upload a picture with only one face"
          6 guard  --1 face-->  8 rule: Smile and EyesOpen Value true?
          8 rule  -->  9 200 "Good Profile Photo"  |  10 200 "Bad Profile Photo"   (answer returns to 2)
         11 Detection_Lambda_Function_Role  ··assumed by··>  4 Lambda   (trust lambda.amazonaws.com)
         11 role  ··policy··>  12 logs policy (CreateLogGroup, CreateLogStream, PutLogEvents)  -> CloudWatch Logs
         11 role  ··policy··>  13 AmazonRekognitionReadOnlyAccess (AWS-managed)  -> 5 Rekognition
          4 Lambda  --logger.error(function ARN)-->  CloudWatch Logs
         Terraform (lambda.tf + apigw.tf) provisions 3, 4, 11, 12, 13 and the API chain: 14 resources.
BANNED:  monospace fonts (grep mono|Mono|monospace|Courier|Menlo|Consolas|ui-monospace before every snapshot);
         em dashes and en-dash separators on screen; caps kickers; the Huly look; Orkestra's dark Linear look;
         Provalume's Biennale paper; Secure Data Hub's navy/Geist look; drop shadows; three feature cards in a row;
         a logo docked in a corner; AWS or Apple logos; screen shake; a flood of tokens; "least-privilege",
         "deployed", "live" or any claim the repo cannot back; invented confidences, users or results.
QA:      1.0, 4.2, 7.4, 9.0, 10.4, 13.2, 16.2, 18.2, 20.9, 23.4, 30.8, 35.4, 38.2, 42.6, 46.6, 49.5, 52.3, 57.9,
         61.5, 63.8, 65.6.
```
