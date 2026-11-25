#!/usr/bin/env python3
"""Draw the atlas entry image for news-image-20261125.

One PNG, 1024x1024: masthead, KPI strip, region bars, a UTC timeline,
15 illustrated panels for the day's top stories, a numbered pin map,
a digest of the remaining stories, and a DATE CHECK box naming the
stories discarded as other days' news. All story data lives in
SOURCES.md; every story here was reported on 25 November 2026.

Run:  python3 draw.py   ->  writes entry.png beside this file.
Uses only Pillow (build-time tool; the shipped program is main.ts).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (28, 30, 38)
MUTE = (96, 98, 108)
RED = (179, 57, 47)
BLUE = (36, 86, 166)
GOLD = (178, 132, 16)
TEAL = (18, 116, 110)
CARD = (255, 253, 247)
LINE = (196, 188, 168)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def wrap(s, font, width):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- masthead
text(16, 8, "THE WORLD IN ONE DAY", f(FB, 37))
text(16, 52, "Wednesday 25 November 2026  ·  Morning edition  ·  All times UTC  ·  One day, one picture", f(FR, 13), MUTE)
d.line([16, 74, 1008, 74], fill=INK, width=3)
d.line([16, 79, 1008, 79], fill=INK, width=1)

# ---------------------------------------------------------------- KPI strip
kpis = [
    ("36", "DATED STORIES"),
    ("8", "REGIONS COVERED"),
    ("00:18", "UTC · SHENZHOU-24 UP"),
    ("-5.3%", "SEOUL AT WORST POINT"),
    ("72", "ORANGUTANS RESCUED"),
    ("$120M", "CUBS SIGN MVP SATO"),
]
kx, kw = 16, (1024 - 32 - 5 * 6) // 6
for i, (num, lab) in enumerate(kpis):
    x = kx + i * (kw + 6)
    rect(x, 86, x + kw, 124, fill=CARD, outline=LINE)
    text(x + kw / 2, 90, num, f(FB, 19), RED if i in (3,) else INK, "ma")
    text(x + kw / 2, 113, lab, f(FB, 8), MUTE, "ma")

# ---------------------------------------------------------------- region bars
regions = [
    ("EAST & SE ASIA", 9), ("EUROPE", 6), ("MIDDLE EAST", 5), ("AFRICA", 5),
    ("OCEANIA", 4), ("NORTH AMERICA", 3), ("SOUTH ASIA", 2), ("LATIN AMERICA", 2),
]
text(16, 132, "STORIES BY REGION", f(FB, 10), MUTE)
for i, (name, n) in enumerate(regions):
    col, row = i % 4, i // 4
    x = 16 + col * 250
    y = 148 + row * 17
    text(x, y, name, f(FB, 9))
    bx = x + 118
    rect(bx, y + 1, bx + 90, y + 10, fill=(226, 219, 198))
    rect(bx, y + 1, bx + 90 * n / 9, y + 10, fill=BLUE)
    text(bx + 96, y, str(n), f(FB, 10), RED)

# ---------------------------------------------------------------- panels
panels = [
    ("rocket", "SHENZHOU-24 LIFTS OFF",
     "First foreign astronaut flies to China's Tiangong station"),
    ("chart", "ASIA STOCKS SLIDE",
     "Seoul off as much as 5.3% as tariff fears bite"),
    ("flags", "AUSTRALIA SIGNS SOLOMON PACT",
     "Canberra becomes defence partner of choice"),
    ("drone", "RUSSIAN DRONE CROSSES POLAND",
     "Chancellor Merz pledges Berlin's complete support"),
    ("tower", "KYIV TOWER STRIKE TOLL 11",
     "Rescuers search the rubble of a Kyiv-region block"),
    ("ship", "UKRAINE SINKS RUSSIAN SHIP",
     "Warship struck in Benghazi harbour, Libya"),
    ("gavel", "SHANGHAI CHIEF UNDER PROBE",
     "Politburo member Chen Jining faces graft inquiry"),
    ("cross", "WHO EVACUATES EBOLA HOSPITAL",
     "Health staff flee fighting in Ituri, DR Congo"),
    ("pump", "BAGHDAD MOVES ON KURDISH OIL",
     "Federal forces ordered to seize the oilfields"),
    ("car", "CAR BOMB INJURES 23",
     "Blast in Colombia; dozens more treated"),
    ("train", "SEOUL METRO STRIKE OFF",
     "Last-minute wage deal averts a shutdown"),
    ("palm", "FIJI DECLARES DISASTER",
     "El Nino dry spell grips the islands"),
    ("cricket", "ENGLAND LEVEL T20 SERIES",
     "Eight-wicket win over Australia levels it 1-1"),
    ("baseball", "CUBS LAND SATO FOR $120M",
     "Japanese MVP Teruaki Sato signs for six years"),
    ("tree", "72 ORANGUTANS RESCUED",
     "Wildfires drive apes from Borneo's forests"),
]


def icon(kind, cx, cy):
    """Tiny pictograms, drawn in a ~64x52 box centred at (cx, cy)."""
    if kind == "rocket":
        d.polygon([(cx, cy - 24), (cx + 10, cy + 6), (cx - 10, cy + 6)], fill=RED)
        d.polygon([(cx - 10, cy + 2), (cx - 18, cy + 16), (cx - 8, cy + 12)], fill=GOLD)
        d.polygon([(cx + 10, cy + 2), (cx + 18, cy + 16), (cx + 8, cy + 12)], fill=GOLD)
        d.ellipse([cx - 4, cy - 12, cx + 4, cy - 4], fill=(255, 255, 255))
        d.polygon([(cx - 4, cy + 14), (cx + 4, cy + 14), (cx, cy + 24)], fill=GOLD)
    elif kind == "chart":
        pts = [(cx - 26, cy - 14), (cx - 10, cy - 4), (cx + 2, cy - 10), (cx + 14, cy + 6), (cx + 26, cy + 14)]
        d.line(pts, fill=RED, width=4)
        d.polygon([(cx + 26, cy + 14), (cx + 16, cy + 13), (cx + 24, cy + 4)], fill=RED)
        d.line([cx - 28, cy + 20, cx + 28, cy + 20], fill=MUTE, width=2)
    elif kind == "flags":
        d.line([cx - 14, cy - 22, cx - 14, cy + 20], fill=INK, width=3)
        d.line([cx + 14, cy - 22, cx + 14, cy + 20], fill=INK, width=3)
        d.polygon([(cx - 14, cy - 22), (cx + 2, cy - 17), (cx - 14, cy - 11)], fill=BLUE)
        d.polygon([(cx + 14, cy - 22), (cx + 30, cy - 17), (cx + 14, cy - 11)], fill=RED)
    elif kind == "drone":
        for dx, dy in [(-18, -14), (18, -14), (-18, 14), (18, 14)]:
            d.ellipse([cx + dx - 8, cy + dy - 3, cx + dx + 8, cy + dy + 3], outline=INK, width=2)
            d.line([cx, cy, cx + dx, cy + dy], fill=INK, width=2)
        d.rectangle([cx - 9, cy - 6, cx + 9, cy + 6], fill=TEAL)
    elif kind == "tower":
        rect(cx - 14, cy - 24, cx + 14, cy + 22, fill=(150, 148, 140))
        for r in range(4):
            for c in range(2):
                rect(cx - 9 + c * 11, cy - 18 + r * 11, cx - 3 + c * 11, cy - 11 + r * 11, fill=(250, 230, 150))
        d.polygon([(cx + 2, cy - 24), (cx + 16, cy - 8), (cx + 6, cy - 4)], fill=RED)
    elif kind == "ship":
        d.polygon([(cx - 28, cy + 4), (cx + 28, cy + 4), (cx + 18, cy + 18), (cx - 18, cy + 18)], fill=INK)
        rect(cx - 6, cy - 14, cx + 12, cy + 4, fill=(150, 148, 140))
        d.line([cx - 16, cy - 20, cx - 16, cy + 4], fill=INK, width=3)
        d.line([cx - 30, cy + 22, cx + 30, cy + 22], fill=BLUE, width=3)
    elif kind == "gavel":
        d.line([cx - 16, cy + 16, cx + 8, cy - 8], fill=GOLD, width=5)
        d.rectangle([cx + 2, cy - 20, cx + 22, cy - 10], fill=INK)
        d.rectangle([cx + 6, cy - 4, cx + 26, cy + 6], fill=INK)
        d.line([cx - 24, cy + 21, cx + 8, cy + 21], fill=INK, width=3)
    elif kind == "cross":
        rect(cx - 7, cy - 22, cx + 7, cy + 22, fill=RED)
        rect(cx - 22, cy - 7, cx + 22, cy + 7, fill=RED)
    elif kind == "pump":
        d.polygon([(cx - 24, cy + 20), (cx - 6, cy - 12), (cx + 20, cy - 2), (cx + 24, cy + 4), (cx + 2, cy + 2), (cx - 12, cy + 20)], fill=INK)
        d.ellipse([cx + 16, cy - 14, cx + 28, cy - 2], outline=INK, width=3)
        d.line([cx - 28, cy + 22, cx + 28, cy + 22], fill=INK, width=3)
    elif kind == "car":
        d.polygon([(cx - 26, cy + 8), (cx - 16, cy - 8), (cx + 12, cy - 8), (cx + 24, cy + 8)], fill=BLUE)
        rect(cx - 28, cy + 8, cx + 28, cy + 16, fill=INK)
        d.ellipse([cx - 18, cy + 12, cx - 6, cy + 24], fill=INK)
        d.ellipse([cx + 8, cy + 12, cx + 20, cy + 24], fill=INK)
        for a in range(0, 360, 45):
            import math
            x2 = cx + 34 * math.cos(math.radians(a))
            y2 = cy - 16 + 34 * math.sin(math.radians(a))
            d.line([cx, cy - 16, x2, y2], fill=GOLD, width=2)
    elif kind == "train":
        rect(cx - 16, cy - 22, cx + 16, cy + 12, fill=TEAL)
        rect(cx - 11, cy - 16, cx + 11, cy - 4, fill=(220, 240, 245))
        d.ellipse([cx - 10, cy + 4, cx - 3, cy + 11], fill=(255, 255, 160))
        d.ellipse([cx + 3, cy + 4, cx + 10, cy + 11], fill=(255, 255, 160))
        d.line([cx - 8, cy + 12, cx - 16, cy + 22], fill=INK, width=3)
        d.line([cx + 8, cy + 12, cx + 16, cy + 22], fill=INK, width=3)
    elif kind == "palm":
        d.arc([cx - 6, cy - 6, cx + 26, cy + 24], start=270, end=360, fill=TEAL, width=4)
        for a in range(5):
            import math
            ang = math.radians(180 + a * 40)
            d.line([cx + 8, cy - 4, cx + 8 + 22 * math.cos(ang), cy - 4 + 14 * math.sin(ang)], fill=TEAL, width=3)
        d.ellipse([cx - 26, cy - 22, cx - 6, cy - 2], fill=GOLD)
    elif kind == "cricket":
        d.line([cx - 4, cy - 22, cx + 10, cy + 14], fill=GOLD, width=7)
        d.ellipse([cx - 20, cy + 8, cx - 6, cy + 22], fill=RED)
    elif kind == "baseball":
        d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(252, 252, 250), outline=INK, width=2)
        d.arc([cx - 26, cy - 14, cx - 2, cy + 14], start=300, end=60, fill=RED, width=2)
        d.arc([cx + 2, cy - 14, cx + 26, cy + 14], start=120, end=240, fill=RED, width=2)
    elif kind == "tree":
        d.polygon([(cx, cy - 24), (cx + 16, cy + 2), (cx + 6, cy + 2), (cx + 18, cy + 14), (cx - 18, cy + 14), (cx - 6, cy + 2), (cx - 16, cy + 2)], fill=TEAL)
        rect(cx - 3, cy + 14, cx + 3, cy + 24, fill=(120, 84, 40))
        d.polygon([(cx + 12, cy + 24), (cx + 18, cy + 8), (cx + 24, cy + 24)], fill=RED)


px0, py0, pw, ph, gap = 16, 188, 194, 148, 5
for i, (kind, head, sub) in enumerate(panels):
    col, row = i % 5, i // 5
    x = px0 + col * (pw + gap)
    y = py0 + row * (ph + gap)
    rect(x, y, x + pw, y + ph, fill=CARD, outline=LINE)
    d.ellipse([x + 6, y + 6, x + 24, y + 24], fill=RED)
    text(x + 15, y + 8, str(i + 1), f(FB, 11), (255, 255, 255), "ma")
    icon(kind, x + pw / 2, y + 46)
    ly = y + 80
    for ln in wrap(head, f(FB, 11), pw - 14):
        text(x + 7, ly, ln, f(FB, 11))
        ly += 14
    for ln in wrap(sub, f(FR, 9), pw - 14):
        text(x + 7, ly + 2, ln, f(FR, 9), MUTE)
        ly += 12

# ---------------------------------------------------------------- timeline
ty = 648
text(16, ty, "THE DAY IN UTC", f(FB, 12))
d.line([16, ty + 20, 1008, ty + 20], fill=INK, width=2)
tl = [
    ("00:09", "Israeli fire in S. Lebanon"),
    ("00:18", "Shenzhou-24 lifts off"),
    ("00:37", "Seoul strike averted"),
    ("00:38", "US tariffs; Sato deal"),
    ("00:43", "Solomon treaty signed"),
    ("01:15", "Shenzhou in orbit"),
    ("01:20", "Fiji disaster declared"),
]
for i, (t, lab) in enumerate(tl):
    x = 30 + i * 140
    anch, ax = "ma", x
    if i == 0:
        anch, ax = "la", 16
    if i == len(tl) - 1:
        anch, ax = "ra", 1008
    d.ellipse([x - 4, ty + 16, x + 4, ty + 24], fill=RED)
    text(ax, ty + 28, t, f(FB, 11), RED, anch)
    for j, ln in enumerate(wrap(lab, f(FR, 9), 128)):
        text(ax, ty + 44 + j * 11, ln, f(FR, 9), INK, anch)

# ---------------------------------------------------------------- map + digest
my = 724
text(16, my, "WHERE IT HAPPENED — SCHEMATIC MAP, PINS MATCH PANEL NUMBERS", f(FB, 10), MUTE)
land = [
    "                                                                ",
    "      #######            #####   ######### ######               ",
    "    ###########         ##################################      ",
    "   #############       ####################################     ",
    "    ##########        ############################  ####        ",
    "     ########          ########################     ###         ",
    "      ######            #####################                   ",
    "       #####             ##################        ##           ",
    "       ####               ################        ####          ",
    "       ###                 ##############         ######        ",
    "       ##                   ############           ####         ",
    "      ###                    ##########                          ",
    "      ##                      ########            ##             ",
    "                                                                ",
]
mw = 470
cell = mw / 64
for r, rowstr in enumerate(land):
    for c, ch in enumerate(rowstr):
        if ch == "#":
            rect(16 + c * cell, my + 16 + r * 11, 16 + (c + 1) * cell - 1, my + 16 + (r + 1) * 11 - 1, fill=(214, 205, 178))
pins = {  # panel number -> (col, row) on the schematic map
    1: (47, 3), 2: (50, 3), 3: (58, 10), 4: (30, 2), 5: (33, 3), 6: (29, 6),
    7: (48, 4), 8: (30, 8), 9: (36, 5), 10: (9, 8), 11: (51, 4), 12: (61, 11),
    13: (56, 10), 14: (10, 3), 15: (50, 8),
}
for n, (c, r) in pins.items():
    x = 16 + c * cell + cell / 2
    y = my + 16 + r * 11 + 5
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=RED)
    text(x, y - 6, str(n), f(FB, 9), (255, 255, 255), "ma")

dx = 506
text(dx, my, "THE REST OF THE DAY — DIGEST", f(FB, 10), MUTE)
digest = [
    "Naver pledges $743M logistics build-out to 2030 (Seoul)",
    "Xiamen Airlines orders 50 Boeing 737-8 jets",
    "Singapore backs ICJ ruling on Myanmar genocide",
    "North Korea envoy touts closer ties in Beijing",
    "BJP and Akali Dal reunite for Punjab 2027 polls",
    "Bangladesh opens investment office in Guangzhou",
    "EU caps hybrid car imports from China from Dec 1",
    "EU states split over ETS2 carbon-market start",
    "EU and Mauritania renew their fishing protocol",
    "Britain sanctions Houthis and four officials",
    "Israeli strike kills top Hamas security figure",
    "Iran pharmacies shut as medicine shortage bites",
    "Gunmen hold dozens in a Cartagena supermarket",
    "Storms threaten US Thanksgiving travel plans",
    "Nigerian emir suspended over assault allegation",
    "Cameroon separatist leader in a Norway court",
    "Rebels pull back from DR Congo towns",
    "Sudan RSF commander defects from the militia",
    "US readies new tariffs on 16 trade partners",
    "Australia inflation tops forecasts in October",
]
ly = my + 16
for ln in digest:
    text(dx, ly, "· " + ln, f(FR, 10))
    ly += 10.6

# ---------------------------------------------------------------- date check
by = 968
rect(16, by, 1008, 1006, fill=(252, 246, 232), outline=RED, width=2)
text(24, by + 5, "DATE CHECK", f(FB, 11), RED)
dc = ("Read and discarded as other days' news: Hormuz tanker-mine claims (IRGC statements, 23-24 Nov) · "
      "CIA-ODNI breach (first reported 24 Nov) · Huawei verdict in New York (24 Nov) · Senegal's AFCON title "
      "restored by CAS (24 Nov) · Real Madrid 5-1 PSV (played 24 Nov) · Belgian strike grounds flights (23 Nov) · "
      "BepiColombo reaches Mercury (22 Nov) · GTA VI launch (19 Nov).")
for i, ln in enumerate(wrap(dc, f(FR, 9), 850)):
    text(130, by + 5 + i * 11, ln, f(FR, 9))

text(16, 1010, "Sources: Reuters, AP, CNN, BBC, Xinhua, Al Jazeera, Korea Times, Bernama — all dated 25 Nov 2026. Detail in SOURCES.md.", f(FR, 8), MUTE)

img.save("entry.png", optimize=True)
print("wrote entry.png")
