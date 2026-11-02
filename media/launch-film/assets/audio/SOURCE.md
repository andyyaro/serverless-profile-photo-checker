# Third-party sounds, pictures and type in the film

These are in the film but not in this repository. Their licences cover using them inside a film,
not handing the files on by themselves, so they are listed here instead. Download each one again
to the path shown to rebuild.

## Music

| Used as | Track | Licence | Put it at |
|---|---|---|---|
| The bed under the whole film, cut on its bar lines by `sound/music.py` | "Sweet September" by Arulo, Mixkit 282 | [Mixkit Stock Music Free License](https://mixkit.co/license/): free in any project, no credit required, not for use in a music-only track | `sound/track.mp3` |

## Sound effects

All from Mixkit, under the [Mixkit Sound Effects Free License](https://mixkit.co/license/).
The names are the ones `sound/mix.py` uses (`SFX`); each file goes in `sound/sfx-src/` as
`mixkit-<id>.mp3`. There are 47 in the film, one per picture event in `sound/picture-cues.json`.

| Name in `mix.py` | Mixkit id | What it marks |
|---|---|---|
| `pop` | 2357 | A part arriving or lighting up: a card, the mark's badge, the credit card; pitched down, the 400 refusal and nothing else |
| `tick` | 1120 | A step or a counter: a chip, a status dot and its word, a credit row, an end-card line |
| `whoosh_air` | 1492 | A token travelling along a wire on the board |
| `whoosh_wind` | 1465 | The camera gliding between close shots |
| `sweep` | 3115 | The two big camera moves: into the board, and the pull-back |
| `pop_hard` | 3005 | The soft hit on the mark at the drop, on the big 14 and on the mark at the end card |
| `riser` | 2408 | The swell into the drop |

## Voice

Kokoro-82M ([Apache-2.0](https://huggingface.co/hexgrad/Kokoro-82M)), voice af_heart, run
locally. The lines are `narration/lines-tts.json`; the audio is generated, so it is not kept.

## Type

SF Pro, Apple's system font, loaded through `local()` as the "HostUI" face in `index.html`. It is
not in this repository and has no download path here: the composition renders only on a Mac that
has it. Every word on screen is set in it, code words included; there is no monospace.

## Pictures

The two photos are the repository's own test fixtures, `goodphoto.jpeg` and `badphoto.png` at the
repository root (1024 × 1536, AI-generated: the shirt reads "AI GENERATED PIC"). The film uses
smaller copies of them, kept in `assets/img/`. The two-face card in the opening is a drawing made
of two glyphs, not a photo.

The icons are the HIG Native line glyphs (`scripts/vendor/hig-icons.js`), written into
`index.html` by `scripts/build-icons.mjs`. There are no AWS or Apple logos in the film.
