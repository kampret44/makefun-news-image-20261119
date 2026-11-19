#!/usr/bin/env python3
"""Render entry.png — a one-page newspaper front page summing up
Thursday 19 November 2026. Flat vector-style art only, PIL only."""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

INK = (17, 17, 17)
PAPER = (251, 247, 236)
WHITE = (255, 255, 255)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
TEAL = (13, 115, 119)
GOLD = (176, 132, 24)
OCEAN = (205, 226, 240)
LAND = (232, 220, 192)
GREY = (90, 90, 90)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, max_w, fill=INK, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.12)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def panel(draw, box, tag, tag_color, headline, sub, hl_size=24, icon=None,
          sub_size=16):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=WHITE, outline=INK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 26], fill=tag_color)
    draw.text((x0 + 10, y0 + 4), tag, font=font(SANS_B, 15), fill=WHITE)
    if icon:
        icon(draw, x1 - 52, y0 + 34)
    max_w = (x1 - x0 - 20) - (56 if icon else 0)
    draw_wrapped(draw, (x0 + 10, y0 + 34), headline,
                 font(SANS_B, hl_size), max_w, leading=int(hl_size * 1.08))
    n_lines = len(wrap(draw, headline, font(SANS_B, hl_size), max_w))
    sub_y = y0 + 34 + n_lines * int(hl_size * 1.08) + 4
    if sub_y + sub_size < y1 - 4:
        draw_wrapped(draw, (x0 + 10, sub_y), sub,
                     font(SANS, sub_size), x1 - x0 - 20, fill=GREY,
                     leading=sub_size + 3)


# --- tiny flat icons (simple shapes, no faces/people) ---
def ic_dome(d, x, y):
    d.ellipse([x + 8, y + 2, x + 40, y + 22], fill=NAVY)
    d.rectangle([x + 2, y + 22, x + 46, y + 28], fill=NAVY)
    d.rectangle([x + 6, y + 28, x + 42, y + 40], fill=NAVY)
    for cx in (x + 10, x + 24, x + 38):
        d.rectangle([cx - 2, y + 30, cx + 2, y + 38], fill=WHITE)


def ic_flag(d, x, y):
    d.rectangle([x + 8, y + 2, x + 12, y + 42], fill=INK)
    d.polygon([(x + 12, y + 4), (x + 42, y + 10), (x + 12, y + 18)], fill=RED)


def ic_chart(d, x, y):
    for i, h in enumerate((14, 26, 38)):
        d.rectangle([x + 6 + i * 14, y + 42 - h, x + 16 + i * 14, y + 42],
                    fill=TEAL)
    d.line([(x + 2, y + 6), (x + 20, y + 18), (x + 34, y + 8), (x + 46, y + 2)],
           fill=RED, width=3)


def ic_rocket(d, x, y):
    d.polygon([(x + 24, y + 2), (x + 34, y + 22), (x + 14, y + 22)], fill=NAVY)
    d.ellipse([x + 19, y + 12, x + 29, y + 22], fill=WHITE)
    d.polygon([(x + 14, y + 22), (x + 8, y + 36), (x + 16, y + 28)], fill=RED)
    d.polygon([(x + 34, y + 22), (x + 40, y + 36), (x + 32, y + 28)], fill=RED)
    d.polygon([(x + 21, y + 30), (x + 27, y + 30), (x + 24, y + 42)], fill=GOLD)


def ic_game(d, x, y):
    d.rounded_rectangle([x + 2, y + 10, x + 46, y + 34], radius=10, fill=INK)
    d.line([(x + 12, y + 18), (x + 12, y + 28)], fill=WHITE, width=3)
    d.line([(x + 7, y + 23), (x + 17, y + 23)], fill=WHITE, width=3)
    d.ellipse([x + 30, y + 18, x + 36, y + 24], fill=RED)
    d.ellipse([x + 37, y + 23, x + 43, y + 29], fill=GOLD)


def ic_coin(d, x, y):
    d.ellipse([x + 6, y + 4, x + 42, y + 40], fill=GOLD, outline=INK, width=2)
    d.text((x + 17, y + 10), "€", font=font(SANS_B, 22), fill=WHITE)


def ic_drone(d, x, y):
    d.ellipse([x + 14, y + 14, x + 34, y + 30], fill=INK)
    for cx, cy in ((x + 8, y + 8), (x + 40, y + 8), (x + 8, y + 36), (x + 40, y + 36)):
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=INK, width=2)


def ic_fence(d, x, y):
    for i in range(5):
        d.line([(x + 4 + i * 10, y + 6), (x + 4 + i * 10, y + 40)], fill=INK, width=3)
    d.line([(x + 2, y + 14), (x + 46, y + 14)], fill=RED, width=3)
    d.line([(x + 2, y + 30), (x + 46, y + 30)], fill=RED, width=3)


def ic_crowd(d, x, y):
    for cx, cy, r in ((x + 12, y + 14, 7), (x + 36, y + 14, 7), (x + 24, y + 10, 8)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    for cx in (x + 12, x + 36, x + 24):
        d.pieslice([cx - 11, y + 24, cx + 11, y + 44], 180, 360, fill=TEAL)


def ic_factory(d, x, y):
    d.rectangle([x + 4, y + 18, x + 44, y + 42], fill=NAVY)
    d.rectangle([x + 8, y + 6, x + 14, y + 18], fill=INK)
    d.rectangle([x + 18, y + 2, x + 24, y + 18], fill=INK)
    for cx in (x + 12, x + 24, x + 36):
        d.rectangle([cx - 3, y + 26, cx + 3, y + 34], fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top strip
    d.text((24, 10), "VOL. I — No. 323", font=font(SANS, 15), fill=GREY)
    d.text((W - 24 - d.textlength("PRICE: FREE", font=font(SANS, 15)), 10),
           "PRICE: FREE", font=font(SANS, 15), fill=GREY)
    d.line([(24, 32), (1000, 32)], fill=INK, width=2)

    # masthead
    mast = "THE WORLD"
    mf = font(SERIF_B, 108)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 36), mast, font=mf, fill=INK)
    sub = "ONE DAY  •  ONE PLANET  •  EVERY STORY THAT MATTERED"
    sf = font(SANS, 17)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 148), sub, font=sf, fill=GREY)
    d.line([(24, 172), (1000, 172)], fill=INK, width=2)

    # date banner — huge and unmistakable
    d.rectangle([24, 180, 1000, 228], fill=INK)
    d.rectangle([24, 180, 40, 228], fill=RED)
    d.rectangle([984, 180, 1000, 228], fill=RED)
    date = "THURSDAY 19 NOVEMBER 2026"
    df = font(SANS_B, 38)
    d.text(((W - d.textlength(date, font=df)) / 2, 190), date, font=df, fill=WHITE)

    # ---- lead story ----
    lead = (24, 240, 624, 408)
    d.rectangle(lead, fill=WHITE, outline=INK, width=2)
    d.rectangle([24, 240, 624, 266], fill=RED)
    d.text((34, 244), "USA  •  HISTORY IN THE MAKING", font=font(SANS_B, 15), fill=WHITE)
    lead_hl = "JEFFRIES TO MAKE HISTORY AS FIRST BLACK SPEAKER"
    lead_f = font(SANS_B, 36)
    n_lead = len(wrap(d, lead_hl, lead_f, 580))
    draw_wrapped(d, (34, 276), lead_hl, lead_f, 580, leading=40)
    draw_wrapped(d, (34, 276 + n_lead * 40 + 8),
                 "Democrats nominate Hakeem Jeffries for Speaker of the US House.",
                 font(SANS, 17), 580, fill=GREY, leading=20)

    # ---- right column: Trump + Anthropic (no icons: room for headline + sub) ----
    panel(d, (640, 240, 1000, 320), "CHINA  •  APEC", NAVY,
          "TRUMP LANDS IN SHENZHEN", "Trilateral talks with Xi and Putin.",
          hl_size=20, sub_size=14)
    panel(d, (640, 328, 1000, 408), "TECH  •  MARKETS", TEAL,
          "ANTHROPIC IPO: $81.3BN, BIGGEST EVER",
          "Record listing tops the all-time IPO table.",
          hl_size=20, sub_size=14)

    # ---- grid, 3 x 2 ----
    panel(d, (24, 420, 336, 546), "SPACE", NAVY,
          "VOYAGER 1: ONE LIGHT-DAY FROM HOME",
          "50 years after launch, the NASA probe keeps going.",
          hl_size=22, icon=ic_rocket)
    panel(d, (356, 420, 668, 546), "GAMES", RED,
          "GTA VI ROLLS OUT WORLDWIDE",
          "Rockstar's blockbuster begins its global launch.",
          hl_size=22, icon=ic_game)
    panel(d, (688, 420, 1000, 546), "EUROPE  •  UKRAINE", GOLD,
          "EU PLANS €45BN LOAN FOR UKRAINE",
          "Repaid after Russia pays reparations.",
          hl_size=22, icon=ic_coin)
    panel(d, (24, 556, 336, 682), "WAR  •  TALKS", INK,
          "DRONE WAR AS PEACE TALKS OPEN",
          "Crimean Bridge hit for a third time this week.",
          hl_size=22, icon=ic_drone)
    panel(d, (356, 556, 668, 682), "EUROPE", NAVY,
          "ESTONIA TO SHUT BORDER WITH RUSSIA",
          "Closure planned from December.",
          hl_size=22, icon=ic_fence)
    panel(d, (688, 556, 1000, 682), "CZECHIA", TEAL,
          "PRAGUE MARCHES FOR FREE MEDIA",
          "Hundreds of thousands demand independence.",
          hl_size=22, icon=ic_crowd)

    # ---- wide strip: Spain strike ----
    d.rectangle([24, 694, 1000, 776], fill=WHITE, outline=INK, width=2)
    d.rectangle([24, 694, 1000, 720], fill=INK)
    d.text((34, 698), "SPAIN", font=font(SANS_B, 15), fill=WHITE)
    d.text((34, 726), "GENERAL STRIKE GRIPS SPAIN",
           font=font(SANS_B, 28), fill=INK)
    d.text((560, 732), "Ports and factories disrupted nationwide.",
           font=font(SANS, 17), fill=GREY)
    ic_factory(d, 928, 728)

    # ---- world map strip ----
    d.rectangle([24, 788, 1000, 900], fill=OCEAN, outline=INK, width=2)
    d.text((34, 794), "WHERE IT HAPPENED", font=font(SANS_B, 15), fill=NAVY)
    # simplified continents (flat blobs)
    d.polygon([(60, 860), (150, 812), (250, 820), (280, 850), (220, 878),
               (140, 880), (80, 872)], fill=LAND)          # N America
    d.polygon([(270, 868), (300, 850), (330, 868), (310, 888), (285, 886)],
              fill=LAND)                                    # S America
    d.polygon([(470, 830), (520, 812), (560, 826), (545, 852), (500, 856),
               (475, 846)], fill=LAND)                      # Europe
    d.polygon([(560, 828), (640, 810), (720, 818), (700, 858), (620, 868),
               (575, 852)], fill=LAND)                      # Asia
    d.polygon([(500, 862), (540, 858), (555, 878), (520, 890), (495, 880)],
              fill=LAND)                                    # Africa
    d.polygon([(820, 868), (880, 862), (900, 880), (850, 890)], fill=LAND)  # Oceania
    markers = {  # number: (x, y, label)
        1: (150, 838, "Washington"), 2: (665, 838, "Shenzhen"),
        3: (105, 845, "San Francisco"), 4: (930, 802, "Voyager 1"),
        5: (480, 838, "London"), 6: (498, 824, "Brussels"),
        7: (560, 838, "Crimea"), 8: (530, 816, "Tallinn"),
        9: (514, 848, "Prague"), 10: (470, 856, "Madrid"),
    }
    for n, (mx, my, _lab) in markers.items():
        d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=RED, outline=WHITE, width=2)
        d.text((mx - 4, my - 8), str(n), font=font(SANS_B, 11), fill=WHITE)
    d.text((838, 798), "VOYAGER 1", font=font(SANS_B, 12), fill=NAVY)

    # ---- MORE TODAY ticker ----
    d.rectangle([24, 912, 1000, 976], fill=WHITE, outline=INK, width=2)
    d.rectangle([24, 912, 168, 976], fill=RED)
    d.text((34, 930), "MORE TODAY", font=font(SANS_B, 19), fill=WHITE)
    ticker = ("India–Japan 2+2 talks open in Tokyo  •  Cyclone Akvan nears Odisha  •  "
              "ICJ to rule on Rohingya case  •  US–Venezuela restore military ties  •  "
              "North Korea fires missiles  •  Canada sanctions settlers  •  "
              "Stacy Keach dies, 85  •  World COPD Day")
    draw_wrapped(d, (180, 918), ticker, font(SANS_B, 15), 808, leading=19)

    # ---- footer: line to the reader ----
    foot = "Every story above was first reported on Thursday 19 November 2026."
    ff = font(SERIF_I, 20)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 986), foot, font=ff, fill=INK)
    d.line([(24, 1014), (1000, 1014)], fill=INK, width=1)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
