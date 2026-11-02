# Serverless profile-photo checker launch film

The 66-second film at the top of the [repository README](../../README.md), published at
https://andyyaro.github.io/serverless-profile-photo-checker/film.html. It shows how one photo
becomes one answer: a small client posts it to API Gateway, a Lambda asks Amazon Rekognition for
the faces, a one-face guard and a smile and open-eyes rule decide, and 14 Terraform resources
build it all. The project has no screen of its own, so the film is one board of its parts that the
camera glides across as the voice names each one. Every name, number and answer on it comes from
this repository's code at `fd8589e`.

[STORYBOARD.md](STORYBOARD.md) has the scenes, the look, the sound and every build step.
[FACTS.md](FACTS.md) has every claim in the film and where it comes from, and
[SPEC.md](SPEC.md) is the full brief it was built from, with every time and level.

## What is here

| Path | What it is |
|---|---|
| `index.html`, `compositions/` | The composition (HyperFrames 0.8.173, GSAP): one file per scene, plus the burned-in subtitles |
| `build.py` | Writes the scene windows and subtitles into the composition, and the captions file |
| `sound/` | The music edit (`music.py`), the mix (`mix.py`: narration, music and effects) and `picture_cues.py`, which puts each effect on its picture event |
| `sound/*.json`, `assets/vo.js`, `assets/timing.js`, `narration/words.json` | The bar grid, the scene windows, the picture cues and the narration's word times the scenes read. The build steps write them; they are kept so the picture renders without re-voicing |
| `narration/` | The script (`lines.json`), the script as voiced (`lines-tts.json`) and `pick.py`, which chooses the best take of each line and times its words |
| `research/` | The local checks behind the film's claims: `terraform validate`, `terraform graph`, and the real handler and client run with Rekognition stubbed (`harness/`) |
| `FACTS.md`, `SPEC.md` | Every line of narration and every on-screen claim with its source; the brief |
| `scripts/` | The HIG Native line icons and the script that writes them into `index.html` |
| `tools/fetch_vendor.sh` | Fetches GSAP at the pinned version and checks its SHA-256 |
| `deploy/film.html`, `deploy/index.html`, `deploy/mark.svg` | The watch page, a redirect to it from the site's root, and the film's mark |
| `assets/img/` | Smaller copies of the repository's two test photos, as the film shows them |
| `assets/brand/README.md` | Why there is no logo: the project has none, and the film's mark is made for the film only |
| `assets/audio/SOURCE.md` | Every third-party sound and the type in the film, with its licence and where it goes |

## What is not here, and why

The working folder for the film is about 70 MB. This folder keeps the source and leaves out
everything that is generated or that its licence does not let us hand on by itself:

- **Generated:** the narration takes and the chosen takes, the music edit, the voice alone, the
  mix, the snapshots and contact sheets, and the renders. The build steps make them again.
- **The full-size test photos:** they are `goodphoto.jpeg` and `badphoto.png` at the repository
  root, so they are not copied twice.
- **Third-party media:** the music ("Sweet September" by Arulo, Mixkit) and seven Mixkit sound
  effects. [assets/audio/SOURCE.md](assets/audio/SOURCE.md) lists each one with its licence and
  the path it goes to.
- **Libraries and fonts:** GSAP 3.14.2 is fetched by `tools/fetch_vendor.sh`. The type is SF Pro,
  Apple's system font, loaded from the Mac it renders on, so it is not in any folder here.

There are no screen recordings and no 3D models: the film is drawn entirely in HTML.

## Publishing

The MP4, its captions and its poster are assets of the
[`film-v1` release](https://github.com/andyyaro/serverless-profile-photo-checker/releases/tag/film-v1),
so the 10.9 MB film is not in the repository's history. The
[film page workflow](../../.github/workflows/film.yml) puts them on GitHub Pages with
`deploy/film.html`, `deploy/index.html` and `deploy/mark.svg`. It runs when anything in `deploy/`
changes on `main`. After replacing a release asset, run it by hand:

```sh
gh release upload film-v1 photo-checker-launch.mp4 --clobber
gh workflow run film.yml
```

## Credits

Narration: Kokoro-82M (Apache-2.0), voice af_heart. Music: "Sweet September" by Arulo (Mixkit).
Sound effects: Mixkit. Type: SF Pro. Icons: HIG Native line glyphs. The handler and client
scaffolding follow AWS's example "Analyzing images with an AWS Lambda function", and the film says
so on screen; the one-face check and the Smile and EyesOpen rule are this project's.
