"""Render the profile README cards (Hotel noir).

    python scripts/build.py          # all static cards + music card
    python scripts/build.py music    # music card only (used by the workflow)

The music card reads Last.fm when LASTFM_USER and LASTFM_API_KEY are set,
otherwise it falls back to the curated SIDE A list below.
SVGs are shown through <img>, so everything (photo, covers) is inlined as data URIs
and only system fonts are used.
"""
import base64, io, json, os, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")

BG, OX, CREAM, BRASS, DIM = "#0B0A09", "#7A1F1F", "#EDE3D1", "#B08D57", "#8C8273"
SERIF = "Georgia,'Times New Roman',serif"
MONO = "ui-monospace,Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

GRAIN = """<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 .93  0 0 0 0 .89  0 0 0 0 .82  0 0 0 .55 0"/></filter>"""

CURATED = [  # SIDE A, from the stories
    ("Lana Del Rey", "Interlude – The Trio"),
    ("She Wants Revenge", "Tear You Apart"),
    ("Ethel Cain", "Michelle Pfeiffer (feat. lil aaron)"),
    ("PureSnow", "One Shot"),
    ("Charli xcx", "Wink Wink"),
]


def write(name, svg):
    with open(os.path.join(A, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


def data_uri(path_or_bytes, mime="image/jpeg"):
    raw = path_or_bytes if isinstance(path_or_bytes, bytes) else open(path_or_bytes, "rb").read()
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def t(s):
    return escape(s, quote=True)


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1200, 560
    segs, gap, x0 = 6, 8, 32
    sw = (W - 2 * x0 - gap * (segs - 1)) / segs
    bars = []
    for i in range(segs):
        x = x0 + i * (sw + gap)
        bars.append(f'<rect x="{x:.1f}" y="22" width="{sw:.1f}" height="3" rx="1.5" fill="{CREAM}" opacity=".28"/>')
        if i < 2:
            bars.append(f'<rect x="{x:.1f}" y="22" width="{sw:.1f}" height="3" rx="1.5" fill="{CREAM}"/>')
        elif i == 2:
            bars.append(f'<rect x="{x:.1f}" y="22" width="0" height="3" rx="1.5" fill="{CREAM}">'
                        f'<animate attributeName="width" from="0" to="{sw:.1f}" dur="9s" repeatCount="indefinite"/></rect>')
    eq = "".join(
        f'<rect x="{i*4}" y="0" width="2.4" height="11" rx="1" fill="{CREAM}">'
        f'<animate attributeName="height" values="{v}" dur="{d}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="{";".join(str(11-int(n)) for n in v.split(";"))}" dur="{d}s" repeatCount="indefinite"/></rect>'
        for i, (v, d) in enumerate([("4;11;6;9;4", 1.1), ("10;5;11;3;10", .9), ("6;9;3;11;6", 1.3)]))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>dev1ce — Tin Šolić</title>
<defs>{GRAIN}
<radialGradient id="vig" cx=".55" cy=".55" r=".75"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>
<linearGradient id="top" x2="0" y2="1"><stop stop-color="#000" stop-opacity=".55"/><stop offset=".3" stop-color="#000" stop-opacity="0"/></linearGradient>
<linearGradient id="bot" x2="0" y2="1"><stop offset=".55" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".9"/></linearGradient>
<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<image href="{data_uri(os.path.join(A, 'hero-plane.jpg'))}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{W}" height="{H}" fill="{OX}" opacity=".10" style="mix-blend-mode:multiply"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/><rect width="{W}" height="{H}" fill="url(#top)"/><rect width="{W}" height="{H}" fill="url(#bot)"/>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".16"/>
{''.join(bars)}
<g transform="translate(32 44)">
  <circle cx="20" cy="20" r="20" fill="{BG}" stroke="{BRASS}" stroke-width="1.5"/>
  <text x="20" y="27" text-anchor="middle" fill="{CREAM}" font-family="{SERIF}" font-style="italic" font-size="20">d</text>
  <text x="54" y="17" fill="{CREAM}" font-family="{SANS}" font-size="15" font-weight="600">dev1ce2004 <tspan fill="{CREAM}" fill-opacity=".6" font-weight="400"> 107w</tspan></text>
  <g transform="translate(54 26)">{eq}</g>
  <text x="70" y="37" fill="{CREAM}" font-family="{SANS}" font-size="13"><tspan font-weight="600">Lana Del Rey</tspan> · Interlude – The Trio</text>
</g>
<g transform="translate(1084 52)" fill="{CREAM}">
  <path d="M0 6h5l6-5v18l-6-5H0z"/><path d="M15 6l8 8M23 6l-8 8" stroke="{CREAM}" stroke-width="2"/>
  <rect x="40" y="2" width="4" height="16" rx="1"/><rect x="49" y="2" width="4" height="16" rx="1"/>
  <circle cx="68" cy="10" r="2.4"/><circle cx="76" cy="10" r="2.4"/><circle cx="84" cy="10" r="2.4"/>
</g>
<text x="48" y="470" fill="{CREAM}" font-family="{SERIF}" font-style="italic" font-size="104" letter-spacing="-1">dev1ce</text>
<path d="M52 492H300" stroke="{BRASS}" stroke-width="1.5"/>
<text x="52" y="520" fill="{CREAM}" fill-opacity=".78" font-family="{MONO}" font-size="13" letter-spacing="4">TIN ŠOLIĆ — SOFTWARE, MOSTLY · SPLIT, HR</text>
<text x="1152" y="520" text-anchor="end" fill="{BRASS}" font-family="{MONO}" font-size="12" letter-spacing="3">UNTITLED (AIRPLANE)</text>
</g>
</svg>"""
    write("hero.svg", svg)


# ---------------------------------------------------------------- statement
def statement():
    W, H = 1200, 132
    write("statement.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>Statement: dev1ce builds decision engines and small games. Computer science at FESB, Split.</title>
<defs>{GRAIN}</defs>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/><rect width="{W}" height="{H}" rx="14" filter="url(#grain)" opacity=".08"/>
<rect x="32" y="30" width="3" height="72" fill="{OX}"/>
<text x="56" y="52" fill="{BRASS}" font-family="{MONO}" font-size="12" letter-spacing="4">ARTIST STATEMENT</text>
<text x="56" y="84" fill="{CREAM}" font-family="{SERIF}" font-style="italic" font-size="25">Builds decision engines and small games, between espressos. Computer science at FESB, Split.</text>
<text x="56" y="110" fill="{DIM}" font-family="{MONO}" font-size="12" letter-spacing="3">MEDIUM — PYTHON · TYPESCRIPT · C · C++ · SDL3 · PYSC2</text>
</svg>""")


# ---------------------------------------------------------------- wall labels
def label(name, artist, title, year, medium, lines, credit):
    W, H = 590, 300
    body = "".join(f'<text x="40" y="{176+i*26}" fill="#2A2420" font-family="{SERIF}" font-size="18">{t(l)}</text>'
                   for i, l in enumerate(lines))
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>{t(title)}, {year}. {t(medium)}.</title>
<defs>{GRAIN}<filter id="sh" x="-5%" y="-5%" width="110%" height="120%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity=".55"/></filter></defs>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="3" fill="{CREAM}" filter="url(#sh)"/>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="3" filter="url(#grain)" opacity=".10"/>
<text x="40" y="58" fill="#2A2420" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="2">{t(artist.upper())}</text>
<text x="40" y="76" fill="#6B6157" font-family="{SANS}" font-size="12">Croatian, b. 2004</text>
<text x="40" y="114" fill="#16120F" font-family="{SERIF}" font-size="28"><tspan font-style="italic">{t(title)}</tspan>, {year}</text>
<text x="40" y="140" fill="#6B6157" font-family="{SANS}" font-size="13">{t(medium)}</text>
{body}
<path d="M40 250H{W-40}" stroke="#C9BDA8"/>
<text x="40" y="270" fill="{OX}" font-family="{MONO}" font-size="11" letter-spacing="2">{t(credit)}</text>
<text x="{W-40}" y="270" text-anchor="end" fill="{OX}" font-family="{MONO}" font-size="11" letter-spacing="2">VIEW ↗</text>
</svg>""")


def labels():
    label("label-mcdm-arena.svg", "dev1ce", "MCDM Arena", 2026, "Python, TypeScript, pysc2, StarCraft II",
          ["Eleven decision methods and learning bots fight it out.",
           "Every move is recorded, ranked and explained."],
          "WINDOWS · RELEASES ON GITHUB")
    label("label-mark.svg", "dev1ce", "Arena Shooter (mark)", 2026, "C, SDL3",
          ["Endless waves. A dash, a reload, a leaderboard.",
           "Arcade, sincerely."],
          "WINDOWS · SOURCE ON GITHUB")


# ---------------------------------------------------------------- music
def lastfm(user, key):
    q = urllib.parse.urlencode({"method": "user.getrecenttracks", "user": user, "api_key": key,
                                "format": "json", "limit": 5})
    with urllib.request.urlopen(f"https://ws.audioscrobbler.com/2.0/?{q}", timeout=20) as r:
        items = json.load(r)["recenttracks"]["track"]
    out = []
    for it in items[:5]:
        img = next((i["#text"] for i in it.get("image", []) if i["size"] == "medium" and i["#text"]), None)
        out.append({"artist": it["artist"]["#text"], "title": it["name"], "img": img,
                    "now": it.get("@attr", {}).get("nowplaying") == "true",
                    "uts": int(it["date"]["uts"]) if "date" in it else None})
    return out


def cover(url):
    try:
        from PIL import Image
        with urllib.request.urlopen(url, timeout=15) as r:
            im = Image.open(io.BytesIO(r.read())).convert("RGB").resize((96, 96))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=80)
        return data_uri(buf.getvalue())
    except Exception:
        return None


def clip(s, n):
    return s if len(s) <= n else s[: n - 1] + "…"


def music():
    user, key = os.environ.get("LASTFM_USER"), os.environ.get("LASTFM_API_KEY")
    tracks = lastfm(user, key) if user and key else None
    if tracks:
        head = tracks[0]
        if head["now"]:
            status = "NOW PLAYING"
        else:
            when = datetime.fromtimestamp(head["uts"], timezone.utc).strftime("%d %b %Y").upper()
            status = f"LAST PLAYED · {when}"
        side = "SIDE A — LIVE FROM LAST.FM"
    else:
        tracks = [{"artist": a, "title": s, "img": None, "now": False} for a, s in CURATED]
        head, status, side = tracks[0], "ON REPEAT", "SIDE A — CURATED"

    W, H = 1200, 330
    def art(x, y, s, tr, i):
        uri = cover(tr["img"]) if tr.get("img") else None
        if uri:
            return f'<image href="{uri}" x="{x}" y="{y}" width="{s}" height="{s}" preserveAspectRatio="xMidYMid slice"/>'
        fill = OX if i % 2 == 0 else "#3A2A22"
        return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{fill}"/>'
                f'<text x="{x+s/2}" y="{y+s*0.66}" text-anchor="middle" fill="{CREAM}" font-family="{SERIF}" '
                f'font-style="italic" font-size="{s*0.5:.0f}">{t(tr["artist"][0])}</text>')

    eq = "".join(
        f'<rect x="{i*7}" y="0" width="4" height="18" rx="1.5" fill="{BRASS}">'
        f'<animate attributeName="height" values="{v}" dur="{d}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="{";".join(str(18-int(n)) for n in v.split(";"))}" dur="{d}s" repeatCount="indefinite"/></rect>'
        for i, (v, d) in enumerate([("6;18;9;15;6", 1.1), ("16;7;18;5;16", .9), ("9;15;4;18;9", 1.3), ("12;5;14;8;12", 1.0)]))

    rows = []
    for i, tr in enumerate(tracks[1:5]):
        y = 64 + i * 58
        rows.append(f'<text x="640" y="{y+30}" fill="{BRASS}" font-family="{MONO}" font-size="13">{i+2:02d}</text>'
                    + art(680, y + 6, 40, tr, i + 1) +
                    f'<text x="736" y="{y+23}" fill="{CREAM}" font-family="{SERIF}" font-size="18">{t(clip(tr["title"], 38))}</text>'
                    f'<text x="736" y="{y+42}" fill="{DIM}" font-family="{SANS}" font-size="13">{t(clip(tr["artist"], 44))}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>{t(status.title())}: {t(head["artist"])} — {t(head["title"])}</title>
<defs>{GRAIN}<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<linearGradient id="g" x1="0" x2="1"><stop stop-color="{OX}" stop-opacity=".35"/><stop offset=".55" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#g)"/>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".09"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{BRASS}" stroke-opacity=".35"/>
<text x="40" y="48" fill="{BRASS}" font-family="{MONO}" font-size="12" letter-spacing="4">{t(side)}</text>
{art(40, 74, 168, head, 0)}
<text x="232" y="100" fill="{CREAM}" fill-opacity=".7" font-family="{MONO}" font-size="12" letter-spacing="3">01 · {t(status)}</text>
<text x="232" y="150" fill="{CREAM}" font-family="{SERIF}" font-style="italic" font-size="34">{t(clip(head["title"], 22))}</text>
<text x="232" y="182" fill="{CREAM}" fill-opacity=".75" font-family="{SANS}" font-size="16">{t(clip(head["artist"], 34))}</text>
<g transform="translate(232 206)">{eq}</g>
<path d="M608 64V292" stroke="{BRASS}" stroke-opacity=".3"/>
{''.join(rows)}
<text x="40" y="296" fill="{DIM}" font-family="{MONO}" font-size="11" letter-spacing="3">dev1ce.radio · YOUTUBE MUSIC ↗</text>
</g>
</svg>"""
    write("now-playing.svg", svg)
    print("music:", status, "-", head["artist"], "/", head["title"])


if __name__ == "__main__":
    if sys.argv[1:] == ["music"]:
        music()
    else:
        hero(); statement(); labels(); music()
