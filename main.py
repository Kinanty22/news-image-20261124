#!/usr/bin/env python3
"""World in One Day: 24 November 2026.

Draws a newspaper front page summing up the world news of
Tuesday 24 November 2026, using only the Python 3 standard library,
and writes it deterministically to entry.png (1024x1024, < 1 MiB).

News (checked 24 Nov 2026 against Reuters, BBC, CNN, AP, WSJ,
The Times, BusinessWorld, via web search this session):
 1. KOREA, TUESDAY MORNING: Russian military planes entered the
    Korean air defence zone near Ulleung Island; Seoul scrambled
    fighter jets and briefly told islanders to take shelter. The
    alert was lifted in minutes; no airspace violation. Seoul
    will summon the Russian military attache to protest.
 2. MARKETS, TUESDAY: Asia rallied after Nvidia reinstated Jensen
    Huang as chief executive on Monday 23 Nov; Nvidia shares rose
    33%, Nasdaq +6%, S and P +4%. On Tuesday the Kospi rose 7.4%
    and Taiwan shares 9%; the dollar sat near a 20-month high.
 3. WAR AT SEA, CONFIRMED MONDAY 23 NOV: Ukraine says seven sea
    drones sank the Russian corvette Merkury at Benghazi, Libya,
    and hit the cargo ship MV Angara. A second Russian cargo ship,
    Sparta II, was hit in the Baltic Sea days earlier.
 4. USA-IRAN: President Trump told Fox News on Sunday 22 Nov the
    US could resume strikes on Iran in 2027 if no nuclear deal is
    reached, and that Iranian ships trying to break the US naval
    blockade would be sunk. Tehran says the blockade must be broken.
 5. CLIMATE: COP31 in Antalya, Turkiye ended on Sunday 22 Nov with
    no deal, the longest COP on record; the EU and 130 nations
    rejected a draft with no mention of fossil fuels. The UN chief
    called the outcome deeply disappointing.
 ALSO: Indonesia, 24 dead and about 30 missing after a candy
    factory fire in Cikande, Banten (fire Sat 21 Nov; toll
    confirmed Mon 23 Nov); Bangladesh to vaccinate 50 million
    children against typhoid; Thai-Cambodia border fighting on
    hold after a truce.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   (or /output in the grader)
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (16, 32, 64)
NAVY2 = (24, 48, 92)
GOLD = (198, 158, 40)
RED = (178, 34, 34)
DARKRED = (120, 20, 20)
ORANGE = (230, 120, 30)
YELLOW = (240, 200, 40)
GREY = (110, 110, 105)
LIGHTGREY = (225, 220, 208)
BLUE = (30, 90, 160)
SKY = (120, 180, 220)
GREEN = (28, 110, 55)
TEAL = (0, 120, 110)
WHITE = (255, 255, 255)
SEA = (40, 110, 150)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 integers, one per row, 5 bits (bit 4 = leftmost pixel).
# Written fresh for this entry from the standard letterforms.
_FONT = {
    'A': (14, 17, 17, 31, 17, 17, 17),
    'B': (30, 17, 17, 30, 17, 17, 30),
    'C': (14, 17, 16, 16, 16, 17, 14),
    'D': (30, 17, 17, 17, 17, 17, 30),
    'E': (31, 16, 16, 30, 16, 16, 31),
    'F': (31, 16, 16, 30, 16, 16, 16),
    'G': (14, 17, 16, 23, 17, 17, 15),
    'H': (17, 17, 17, 31, 17, 17, 17),
    'I': (14, 4, 4, 4, 4, 4, 14),
    'J': (7, 2, 2, 2, 2, 18, 12),
    'K': (17, 18, 20, 24, 20, 18, 17),
    'L': (16, 16, 16, 16, 16, 16, 31),
    'M': (17, 27, 21, 21, 17, 17, 17),
    'N': (17, 25, 21, 19, 17, 17, 17),
    'O': (14, 17, 17, 17, 17, 17, 14),
    'P': (30, 17, 17, 30, 16, 16, 16),
    'Q': (14, 17, 17, 17, 21, 18, 13),
    'R': (30, 17, 17, 30, 20, 18, 17),
    'S': (15, 16, 16, 14, 1, 1, 30),
    'T': (31, 4, 4, 4, 4, 4, 4),
    'U': (17, 17, 17, 17, 17, 17, 14),
    'V': (17, 17, 17, 17, 17, 10, 4),
    'W': (17, 17, 17, 21, 21, 27, 17),
    'X': (17, 17, 10, 4, 10, 17, 17),
    'Y': (17, 17, 10, 4, 4, 4, 4),
    'Z': (31, 1, 2, 4, 8, 16, 31),
    '0': (14, 17, 19, 21, 25, 17, 14),
    '1': (4, 12, 4, 4, 4, 4, 14),
    '2': (14, 17, 1, 6, 8, 16, 31),
    '3': (31, 2, 4, 2, 1, 17, 14),
    '4': (2, 6, 10, 18, 31, 2, 2),
    '5': (31, 16, 30, 1, 1, 17, 14),
    '6': (6, 8, 16, 30, 17, 17, 14),
    '7': (31, 1, 2, 4, 8, 8, 8),
    '8': (14, 17, 17, 14, 17, 17, 14),
    '9': (14, 17, 17, 15, 1, 2, 12),
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 12, 12),
    ',': (0, 0, 0, 0, 12, 4, 8),
    ':': (0, 12, 12, 0, 12, 12, 0),
    ';': (0, 12, 12, 0, 12, 4, 8),
    '-': (0, 0, 0, 14, 0, 0, 0),
    '!': (4, 4, 4, 4, 4, 0, 4),
    '?': (14, 17, 1, 6, 4, 0, 4),
    '%': (25, 26, 2, 4, 8, 11, 19),
    '+': (0, 4, 4, 31, 4, 4, 0),
    '/': (1, 2, 2, 4, 8, 8, 16),
    '(': (2, 4, 8, 8, 8, 4, 2),
    ')': (8, 4, 2, 2, 2, 4, 8),
    '&': (12, 18, 20, 8, 21, 18, 13),
    '$': (4, 15, 20, 14, 5, 30, 4),
    "'": (4, 4, 8, 0, 0, 0, 0),
    '"': (10, 10, 10, 0, 0, 0, 0),
    '=': (0, 0, 31, 0, 31, 0, 0),
    '>': (8, 4, 2, 1, 2, 4, 8),
    '<': (2, 4, 8, 16, 8, 4, 2),
    '*': (0, 21, 14, 31, 14, 21, 0),
}


def text_width(s, scale):
    return len(s) * 6 * scale - scale


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(bg * (w * h))

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            span = min(self.w, x + w) - max(0, x)
            if span > 0:
                self.buf[base:base + span * 3] = bytes(color) * span

    def frame(self, x, y, w, h, color, t=2):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def hline(self, x, y, w, color, t=1):
        self.rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.rect(x, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, t=2):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.rect(cx - dx, cy + dy, t, 1, color)
            self.rect(cx + dx - t + 1, cy + dy, t, 1, color)

    def poly(self, pts, color):
        # Scanline fill of a simple polygon.
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.rect(int(xs[i]), y, max(1, int(xs[i + 1]) - int(xs[i])), 1, color)

    def text(self, x, y, s, scale, color):
        for ci, ch in enumerate(s):
            glyph = _FONT.get(ch, _FONT[' '])
            ox = x + ci * 6 * scale
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits >> (4 - col) & 1:
                        self.rect(ox + col * scale, y + row * scale,
                                  scale, scale, color)

    def text_c(self, cx, y, s, scale, color):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, color)

    def para(self, x, y, lines, scale, color, lh):
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, scale, color)
        return y + len(lines) * lh


# ---------------------------------------------------------------- PNG encode
def encode_png(c):
    raw = bytearray()
    stride = c.w * 3
    for y in range(c.h):
        raw.append(0)
        raw += c.buf[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        out = struct.pack('>I', len(data)) + kind + data
        return out + struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = bytearray(b'\x89PNG\r\n\x1a\n')
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', c.w, c.h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    return bytes(png)

# ---------------------------------------------------------------- art
def draw_jet(c, x, y, s, color):
    # Simple side-view jet, nose pointing right, scaled by s.
    body = [(x, y + 6 * s), (x + 30 * s, y + 6 * s), (x + 44 * s, y + 9 * s),
            (x + 30 * s, y + 12 * s), (x, y + 12 * s)]
    c.poly(body, color)
    c.poly([(x + 8 * s, y + 6 * s), (x + 16 * s, y), (x + 20 * s, y),
            (x + 18 * s, y + 6 * s)], color)          # tail fin
    c.poly([(x + 14 * s, y + 12 * s), (x + 22 * s, y + 20 * s),
            (x + 26 * s, y + 20 * s), (x + 24 * s, y + 12 * s)], color)
    c.disc(x + 36 * s, y + 8 * s, 2 * s, WHITE)        # cockpit
    c.line(x - 4 * s, y + 9 * s, x - 12 * s, y + 9 * s, ORANGE, 2 * s)


def draw_alert_triangle(c, cx, cy, r, color):
    c.poly([(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)], color)
    c.poly([(cx, cy - r + 6), (cx + r - 6, cy + r - 4), (cx - r + 6, cy + r - 4)],
           (255, 255, 255))
    c.text(cx - 3, cy - 2, '!', 2, DARKRED)


def draw_ship(c, x, y, w, hull, deck):
    # Warship silhouette on the sea; x,y = top-left of hull box.
    c.poly([(x, y), (x + w, y), (x + w - 12, y + 18), (x + 12, y + 18)], hull)
    c.rect(x + w // 3, y - 16, w // 3, 16, deck)
    c.rect(x + w // 2 - 2, y - 30, 4, 16, deck)
    c.line(x + 6, y + 24, x + w - 6, y + 24, SEA, 2)
    c.line(x + 20, y + 30, x + w - 20, y + 30, SEA, 2)


def draw_blast(c, cx, cy, r):
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r // 2
        pts.append((cx + int(rr * math.cos(ang)), cy + int(rr * math.sin(ang))))
    c.poly(pts, ORANGE)
    c.disc(cx, cy, r // 2, YELLOW)
    c.disc(cx, cy, r // 4, WHITE)


def draw_tanker(c, x, y, w):
    c.rect(x, y, w, 16, INK)
    c.rect(x + 8, y - 14, 30, 14, INK)
    c.rect(x + w - 46, y - 22, 18, 22, DARKRED)
    c.rect(x + w - 50, y - 26, 26, 4, DARKRED)
    c.line(x - 6, y + 22, x + w + 6, y + 22, SEA, 2)
    c.line(x + 10, y + 28, x + w - 10, y + 28, SEA, 2)


def draw_globe(c, cx, cy, r):
    c.disc(cx, cy, r, SKY)
    c.ring(cx, cy, r, BLUE, 3)
    # crude continents: two dark blobs
    c.disc(cx - r // 3, cy - r // 4, r // 3, GREEN)
    c.disc(cx + r // 3, cy + r // 4, r // 4, GREEN)
    c.line(cx - r, cy, cx + r, cy, BLUE, 2)
    # the crack: a red zig-zag across the globe
    c.line(cx - r + 6, cy - r + 10, cx - 6, cy - 4, RED, 3)
    c.line(cx - 6, cy - 4, cx + 8, cy + 6, RED, 3)
    c.line(cx + 8, cy + 6, cx + r - 8, cy + r - 12, RED, 3)


def draw_chart(c, x, y, w, h):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, LIGHTGREY, 1)
    c.line(x + 8, y + h - 8, x + w - 8, y + h - 8, GREY, 1)
    c.line(x + 8, y + 8, x + 8, y + h - 8, GREY, 1)
    pts = [(x + 14, y + h - 20), (x + 60, y + h - 28), (x + 110, y + h - 24),
           (x + 160, y + h - 38), (x + 210, y + h - 44), (x + 260, y + h - 52),
           (x + w - 16, y + 10)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], GREEN, 3)
    tip = pts[-1]
    c.poly([(tip[0], tip[1] - 2), (tip[0] - 12, tip[1] + 2),
            (tip[0] - 2, tip[1] + 12)], GREEN)
    c.text(x + 16, y + 10, '+33%', 3, GREEN)


# ---------------------------------------------------------------- panels
def panel(c, x, y, w, h):
    c.rect(x, y, w, h, WHITE)
    c.frame(x, y, w, h, INK, 2)


def kicker(c, x, y, s, color):
    c.text(x, y, s, 2, color)


def draw_masthead(c):
    c.rect(0, 0, W, 116, NAVY)
    c.text_c(W // 2, 16, 'THE WORLD IN ONE DAY', 5, WHITE)
    c.text_c(W // 2, 62, 'TUESDAY 24 NOVEMBER 2026', 3, GOLD)
    c.hline(0, 112, W, GOLD, 4)
    c.text_c(W // 2, 126, 'FIVE STORIES THAT DEFINED TUESDAY - FROM SEOUL TO ANTALYA',
             2, NAVY)


def draw_lead_korea(c):
    x, y, w, h = 16, 152, 600, 288
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'KOREA - TUESDAY MORNING', RED)
    c.text(x + 16, y + 38, 'JETS SCRAMBLED AS', 4, NAVY)
    c.text(x + 16, y + 70, 'RUSSIAN PLANES', 4, NAVY)
    c.text(x + 16, y + 102, 'NEAR ULLEUNG ISLAND', 4, NAVY)
    body = [
        'RUSSIAN WARPLANES ENTERED',
        'THE KOREAN AIR DEFENCE',
        'ZONE OFF THE EAST COAST.',
        'SEOUL SCRAMBLED FIGHTER',
        'JETS AND BRIEFLY TOLD',
        'ULLEUNG ISLANDERS TO TAKE',
        'SHELTER. NO AIRSPACE',
        'VIOLATION. SEOUL WILL',
        'PROTEST TO MOSCOW.',
    ]
    c.para(x + 16, y + 146, body, 2, INK, 15)
    # art, right column: alert triangle above a jet over the sea
    draw_alert_triangle(c, x + 470, y + 180, 34, YELLOW)
    draw_jet(c, x + 380, y + 224, 2, NAVY)
    c.line(x + 380, y + 272, x + 590, y + 272, SEA, 2)
    c.line(x + 400, y + 280, x + 570, y + 280, SEA, 2)


def draw_markets(c):
    x, y, w, h = 628, 152, 380, 288
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'MARKETS - TUESDAY', RED)
    c.text(x + 16, y + 38, 'NVIDIA COMEBACK', 3, NAVY)
    c.text(x + 16, y + 62, 'LIFTS ASIA', 3, NAVY)
    body = [
        'NVIDIA REINSTATED JENSEN',
        'HUANG AS CHIEF. SHARES',
        'ROSE 33% ON MONDAY.',
        'TUESDAY, ASIA FOLLOWED:',
        'KOSPI +7.4%, TAIWAN +9%.',
        'NASDAQ +6%, S AND P +4%.',
        'DOLLAR NEAR 20-MONTH HIGH.',
    ]
    c.para(x + 16, y + 96, body, 2, INK, 15)
    draw_chart(c, x + 16, y + 208, w - 32, 64)

def draw_ukraine(c):
    x, y, w, h = 16, 452, 484, 248
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'WAR AT SEA - CONFIRMED MONDAY', RED)
    c.text(x + 16, y + 38, 'UKRAINE SINKS RUSSIAN', 3, NAVY)
    c.text(x + 16, y + 62, 'WARSHIP IN LIBYA', 3, NAVY)
    body = [
        'SEVEN SEA DRONES SANK',
        'THE CORVETTE MERKURY AT',
        'BENGHAZI, LIBYA. THE',
        'CARGO SHIP MV ANGARA WAS',
        'HIT TOO. A SECOND RUSSIAN',
        'CARGO SHIP WAS HIT IN',
        'THE BALTIC SEA.',
    ]
    c.para(x + 16, y + 94, body, 2, INK, 15)
    # art, right column: a burning ship on the sea
    draw_ship(c, x + 330, y + 150, 130, NAVY, NAVY2)
    draw_blast(c, x + 395, y + 128, 26)
    c.line(x + 320, y + 196, x + 470, y + 196, SEA, 2)
    c.line(x + 340, y + 204, x + 450, y + 204, SEA, 2)


def draw_iran(c):
    x, y, w, h = 512, 452, 496, 248
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'USA - IRAN', RED)
    c.text(x + 16, y + 38, 'DEAL BY NEW YEAR OR', 3, NAVY)
    c.text(x + 16, y + 62, 'STRIKES, SAYS TRUMP', 3, NAVY)
    body = [
        'PRESIDENT TRUMP SAID THE',
        'US COULD RESUME STRIKES',
        'ON IRAN IN 2027 IF NO',
        'NUCLEAR DEAL IS REACHED.',
        'SHIPS BREAKING THE US',
        'NAVAL BLOCKADE WOULD BE',
        'SUNK, HE SAID.',
    ]
    c.para(x + 16, y + 94, body, 2, INK, 15)
    # art, right column: a tanker stopped by a red blockade line
    draw_tanker(c, x + 330, y + 150, 140)
    c.line(x + 320, y + 116, x + 480, y + 116, RED, 3)
    c.text(x + 330, y + 92, 'BLOCKADE', 2, RED)
    c.line(x + 320, y + 196, x + 480, y + 196, SEA, 2)
    c.line(x + 340, y + 204, x + 460, y + 204, SEA, 2)


def draw_cop31(c):
    x, y, w, h = 16, 712, 600, 168
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'CLIMATE - ANTALYA, TURKIYE', RED)
    c.text(x + 16, y + 38, 'COP31 ENDS WITH NO DEAL', 3, NAVY)
    body = [
        'AFTER RECORD OVERTIME, THE EU AND',
        '130 NATIONS REJECTED A DRAFT WITH',
        'NO MENTION OF FOSSIL FUELS. THE UN',
        'CHIEF CALLED IT DEEPLY DISAPPOINTING.',
    ]
    c.para(x + 16, y + 74, body, 2, INK, 15)
    draw_globe(c, x + 520, y + 92, 52)


def draw_also(c):
    x, y, w, h = 628, 712, 380, 168
    panel(c, x, y, w, h)
    kicker(c, x + 16, y + 14, 'ALSO TODAY', RED)
    items = [
        ['INDONESIA: 24 DEAD, 30',
         'MISSING IN FACTORY FIRE.'],
        ['BANGLADESH: TYPHOID JABS',
         'FOR 50 MILLION CHILDREN.'],
        ['THAI-CAMBODIA: FIGHTING',
         'ON HOLD AFTER TRUCE.'],
    ]
    yy = y + 40
    for it in items:
        c.rect(x + 16, yy + 2, 8, 8, RED)
        c.para(x + 32, yy, it, 2, INK, 14)
        yy += 42


def draw_footer(c):
    c.hline(16, 892, W - 32, GOLD, 3)
    c.text_c(W // 2, 906, 'SOURCES: REUTERS, BBC, CNN, AP, WSJ, THE TIMES', 2, NAVY)
    c.text_c(W // 2, 928, 'ALL STORIES AS REPORTED ON TUESDAY 24 NOVEMBER 2026', 2, INK)
    c.text_c(W // 2, 950, 'DRAWN FROM REPORTS PUBLISHED ON THE DAY.', 2, GREY)


def main():
    c = Canvas(W, H, PAPER)
    draw_masthead(c)
    draw_lead_korea(c)
    draw_markets(c)
    draw_ukraine(c)
    draw_iran(c)
    draw_cop31(c)
    draw_also(c)
    draw_footer(c)
    out = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'entry.png'), 'wb') as f:
        f.write(encode_png(c))


if __name__ == '__main__':
    main()
