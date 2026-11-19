# The World — 19 November 2026

A newspaper front page summing up 19 November's world news in one image.

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/kampret44/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/kampret44/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

Bounty: https://make.fun/bounty/news-image-20261119

## The image

`entry.png` (1024×1024) is a flat vector-style newspaper front page:
masthead "THE WORLD" with the date "THURSDAY 19 NOVEMBER 2026" in a
black banner, a lead story (Hakeem Jeffries nominated for Speaker),
nine more story panels, a full-width Spain strike strip, a simple
world-map strip marking where the stories happened, a "MORE TODAY"
ticker with the remaining stories, and the line "Every story above
was first reported on Thursday 19 November 2026."

## Files

- `entry.png` — the submitted image, rendered by `render.py`.
- `render.py` — renders `entry.png` with Pillow (flat shapes and text only).
- `main.py` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`).

## Reproduce

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
