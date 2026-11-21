"""Render the profile README cards (Hotel noir).

    python scripts/build.py          # every card
    python scripts/build.py live     # music + stats (workflow, 14:00)
    python scripts/build.py music    # music only (workflow, 00:00)
Music: first five tracks of the public YouTube Music playlist (reorder the playlist to change them).
Stats: GitHub GraphQL, needs GITHUB_TOKEN (or GH_TOKEN) in the environment.
SVGs are shown through <img>, so photos and covers are inlined as data URIs and only system fonts are used.
"""
import base64, hashlib, io, json, os, re, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from html import escape

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
USER = "dev1ce2004"
PLAYLIST = "PLiWZPK0CLhRHQuAbRyUZhf0jjJZUrZ5Td"

BG, OX, CREAM, BRASS, DIM = "#0B0A09", "#7A1F1F", "#EDE3D1", "#B08D57", "#8C8273"
SERIF = "Georgia,'Times New Roman',serif"
MONO = "ui-monospace,Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

GRAIN = """<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 .93  0 0 0 0 .89  0 0 0 0 .82  0 0 0 .55 0"/></filter>"""


def write(name, svg):
    with open(os.path.join(A, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)


def data_uri(raw, mime="image/jpeg"):
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def t(s):
    return escape(s, quote=True)


def clip(s, n):
    return s if len(s) <= n else s[: n - 1] + "…"


def fetch(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "profile-readme", **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def card(W, H, inner, title):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>{t(title)}</title>
<defs>{GRAIN}<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<linearGradient id="g" x1="0" x2="1"><stop stop-color="{OX}" stop-opacity=".35"/><stop offset=".55" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#g)"/>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".09"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{BRASS}" stroke-opacity=".35"/>
{inner}
</g>
</svg>"""


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1200, 560
    photo = data_uri(open(os.path.join(A, "hero-plane.jpg"), "rb").read())
    write("hero.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>dev1ce — Tin Šolić</title>
<defs>{GRAIN}
<radialGradient id="vig" cx=".55" cy=".55" r=".75"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>
<linearGradient id="bot" x2="0" y2="1"><stop offset=".55" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".9"/></linearGradient>
<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<image href="{photo}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{W}" height="{H}" fill="{OX}" opacity=".10" style="mix-blend-mode:multiply"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/><rect width="{W}" height="{H}" fill="url(#bot)"/>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".16"/>
<text x="48" y="470" fill="{CREAM}" font-family="{SERIF}" font-style="italic" font-size="104" letter-spacing="-1">dev1ce</text>
<path d="M52 492H300" stroke="{BRASS}" stroke-width="1.5"/>
<text x="52" y="520" fill="{CREAM}" fill-opacity=".78" font-family="{MONO}" font-size="13" letter-spacing="4">TIN ŠOLIĆ — SOFTWARE, MOSTLY · SPLIT, HR</text>
<text x="1152" y="520" text-anchor="end" fill="{BRASS}" font-family="{MONO}" font-size="12" letter-spacing="3">UNTITLED (AIRPLANE)</text>
</g>
</svg>""")


# ---------------------------------------------------------------- wall labels
def label(name, title, year, medium, lines, credit):
    W, H = 590, 300
    body = "".join(f'<text x="40" y="{176+i*26}" fill="#2A2420" font-family="{SERIF}" font-size="18">{t(l)}</text>'
                   for i, l in enumerate(lines))
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>{t(title)}, {year}. {t(medium)}.</title>
<defs>{GRAIN}<filter id="sh" x="-5%" y="-5%" width="110%" height="120%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity=".55"/></filter></defs>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="3" fill="{CREAM}" filter="url(#sh)"/>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="3" filter="url(#grain)" opacity=".10"/>
<text x="40" y="58" fill="#2A2420" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="2">DEV1CE</text>
<text x="40" y="76" fill="#6B6157" font-family="{SANS}" font-size="12">Croatian, b. 2004</text>
<text x="40" y="114" fill="#16120F" font-family="{SERIF}" font-size="28"><tspan font-style="italic">{t(title)}</tspan>, {year}</text>
<text x="40" y="140" fill="#6B6157" font-family="{SANS}" font-size="13">{t(medium)}</text>
{body}
<path d="M40 250H{W-40}" stroke="#C9BDA8"/>
<text x="40" y="270" fill="{OX}" font-family="{MONO}" font-size="11" letter-spacing="2">{t(credit)}</text>
<text x="{W-40}" y="270" text-anchor="end" fill="{OX}" font-family="{MONO}" font-size="11" letter-spacing="2">VIEW ↗</text>
</svg>""")


def labels():
    label("label-mcdm-arena.svg", "MCDM Arena", 2026, "Python, TypeScript, pysc2, StarCraft II",
          ["Eleven decision methods and learning bots fight it out.",
           "Every move is recorded, ranked and explained."],
          "WINDOWS · RELEASES ON GITHUB")
    label("label-mark.svg", "Arena Shooter (mark)", 2026, "C, SDL3",
          ["Endless waves. A dash, a reload, a leaderboard.",
           "Arcade, sincerely."],
          "WINDOWS · SOURCE ON GITHUB")


# ---------------------------------------------------------------- music
NOISE = re.compile(r"\s*[\(\[][^\)\]]*(official|audio|video|lyric|visuali[sz]er|hq|hd|version)[^\)\]]*[\)\]]"
                   r"|\s*\bHQ Audio\b|\s*\bHD\b", re.I)


def tidy(title, author):
    """YouTube titles to (artist, song). '- Topic' channels already carry the artist."""
    title = NOISE.sub("", title).strip(" ~-")
    if author.endswith(" - Topic"):
        return author[: -len(" - Topic")], title
    m = re.match(r"(.+?)\s+[~\-–]\s+(.+)", title)
    return (m.group(1).strip(), m.group(2).strip(" ~")) if m else (author, title)


def cover(video_id):
    """Square album art: Topic videos centre the square cover in the 16:9 frame."""
    try:
        im = Image.open(io.BytesIO(fetch(f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"))).convert("RGB")
        im = im.crop((105, 45, 375, 315)).resize((160, 160), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=80)
        return data_uri(buf.getvalue())
    except Exception as e:
        print("cover failed:", video_id, e, file=sys.stderr)
        return None


def playlist(n=5):
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    root = ET.fromstring(fetch(f"https://www.youtube.com/feeds/videos.xml?playlist_id={PLAYLIST}"))
    out = []
    for e in root.findall("a:entry", ns)[:n]:
        artist, song = tidy(e.findtext("a:title", "", ns), e.findtext("a:author/a:name", "", ns))
        out.append({"artist": artist, "title": song, "cover": cover(e.findtext("yt:videoId", "", ns))})
    return out


def music():
    tracks = playlist()
    head = tracks[0]
    W, H = 1200, 330

    def art(x, y, s, tr, i):
        if tr["cover"]:
            return f'<image href="{tr["cover"]}" x="{x}" y="{y}" width="{s}" height="{s}" preserveAspectRatio="xMidYMid slice"/>'
        fill = OX if i % 2 == 0 else "#3A2A22"
        return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{fill}"/>'
                f'<text x="{x+s/2}" y="{y+s*0.66}" text-anchor="middle" fill="{CREAM}" font-family="{SERIF}" '
                f'font-style="italic" font-size="{s*0.5:.0f}">{t(tr["artist"][:1])}</text>')

    eq = "".join(
        f'<rect x="{i*7}" y="0" width="4" height="18" rx="1.5" fill="{BRASS}">'
        f'<animate attributeName="height" values="{v}" dur="{d}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="{";".join(str(18-int(n)) for n in v.split(";"))}" dur="{d}s" repeatCount="indefinite"/></rect>'
        for i, (v, d) in enumerate([("6;18;9;15;6", 1.1), ("16;7;18;5;16", .9), ("9;15;4;18;9", 1.3), ("12;5;14;8;12", 1.0)]))

    rows = "".join(
        f'<text x="640" y="{64+i*58+30}" fill="{BRASS}" font-family="{MONO}" font-size="13">{i+2:02d}</text>'
        + art(680, 64 + i * 58 + 6, 40, tr, i + 1) +
        f'<text x="736" y="{64+i*58+23}" fill="{CREAM}" font-family="{SERIF}" font-size="18">{t(clip(tr["title"], 38))}</text>'
        f'<text x="736" y="{64+i*58+42}" fill="{DIM}" font-family="{SANS}" font-size="13">{t(clip(tr["artist"], 44))}</text>'
        for i, tr in enumerate(tracks[1:5]))

    inner = f"""<text x="40" y="48" fill="{BRASS}" font-family="{MONO}" font-size="12" letter-spacing="4">SIDE A — ON REPEAT</text>
{art(40, 74, 168, head, 0)}
<text x="232" y="100" fill="{CREAM}" fill-opacity=".7" font-family="{MONO}" font-size="12" letter-spacing="3">01</text>
<text x="232" y="150" fill="{CREAM}" font-family="{SERIF}" font-style="italic" font-size="34">{t(clip(head["title"], 22))}</text>
<text x="232" y="182" fill="{CREAM}" fill-opacity=".75" font-family="{SANS}" font-size="16">{t(clip(head["artist"], 34))}</text>
<g transform="translate(232 206)">{eq}</g>
<path d="M608 64V292" stroke="{BRASS}" stroke-opacity=".3"/>
{rows}
<text x="40" y="296" fill="{DIM}" font-family="{MONO}" font-size="11" letter-spacing="3">dev1ce.radio · YOUTUBE MUSIC ↗</text>"""
    write("now-playing.svg", card(W, H, inner, f"On repeat: {head['artist']} — {head['title']}"))
    print("music:", " | ".join(f"{x['artist']} / {x['title']}" for x in tracks))


# ---------------------------------------------------------------- stats
QUERY = """query($u:String!){user(login:$u){createdAt
 contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}
 repositories(ownerAffiliations:OWNER,first:100,isFork:false,privacy:PUBLIC){totalCount
  nodes{languages(first:10){edges{size node{name}}}}}}}"""


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    i = len(counts) - 1
    if counts and counts[i] == 0:  # today not over yet
        i -= 1
    cur = 0
    while i >= 0 and counts[i]:
        cur += 1; i -= 1
    return cur, longest


def stats():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("stats skipped: no GITHUB_TOKEN", file=sys.stderr); return
    body = json.dumps({"query": QUERY, "variables": {"u": USER}}).encode()
    u = json.loads(fetch("https://api.github.com/graphql", body, {"Authorization": f"bearer {token}"}))["data"]["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    cur, longest = streaks(days)

    langs = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    shades = [OX, BRASS, CREAM, "#5A3A2E", DIM]

    W, H = 1200, 310
    figs = "".join(
        f'<text x="{40+i*200}" y="118" fill="{CREAM}" font-family="{SERIF}" font-style="italic" font-size="54">{v}</text>'
        f'<text x="{42+i*200}" y="144" fill="{DIM}" font-family="{MONO}" font-size="11" letter-spacing="3">{k}</text>'
        for i, (v, k) in enumerate([(cal["totalContributions"], "CONTRIBUTIONS"), (cur, "DAY STREAK"), (longest, "LONGEST")]))

    heat = ["#1A1714", "#3B1A16", "#5A1F1B", OX, BRASS]
    peak = max((d["contributionCount"] for d in days), default=0) or 1
    cells = []
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            c = d["contributionCount"]
            lvl = 0 if c == 0 else min(4, 1 + int(3 * c / peak))
            wd = (date.fromisoformat(d["date"]).weekday() + 1) % 7  # Sunday first, like GitHub
            cells.append(f'<rect x="{40+wi*12}" y="{172+wd*12}" width="9" height="9" rx="1.5" fill="{heat[lvl]}"/>')

    x, bar = 760, []
    for i, (name, size) in enumerate(top):
        w = 400 * size / total
        bar.append(f'<rect x="{x:.1f}" y="92" width="{max(w-2,1):.1f}" height="8" fill="{shades[i]}"/>'); x += w
    legend = "".join(
        f'<rect x="760" y="{126+i*28}" width="10" height="10" fill="{shades[i]}"/>'
        f'<text x="782" y="{136+i*28}" fill="{CREAM}" font-family="{SERIF}" font-size="17">{t(n)}</text>'
        f'<text x="1160" y="{136+i*28}" text-anchor="end" fill="{DIM}" font-family="{MONO}" font-size="12">{100*s/total:.1f}%</text>'
        for i, (n, s) in enumerate(top))

    since = u["createdAt"][:4]
    inner = f"""<text x="40" y="48" fill="{BRASS}" font-family="{MONO}" font-size="12" letter-spacing="4">ANNUAL REPORT — LAST 12 MONTHS</text>
{figs}
{''.join(cells)}
<path d="M720 40V280" stroke="{BRASS}" stroke-opacity=".3"/>
<text x="760" y="70" fill="{BRASS}" font-family="{MONO}" font-size="12" letter-spacing="4">MEDIUM, BY WEIGHT</text>
{''.join(bar)}
{legend}
<text x="1160" y="48" text-anchor="end" fill="{DIM}" font-family="{MONO}" font-size="11" letter-spacing="3">SINCE {since} · {u["repositories"]["totalCount"]} PUBLIC WORKS</text>"""
    write("stats.svg", card(W, H, inner,
                            f"{cal['totalContributions']} contributions in the last year, {cur}-day streak, longest {longest}."))
    print("stats:", cal["totalContributions"], cur, longest, top)


def stamp_readme():
    """Append ?v=<content hash> to each card URL so browsers and GitHub's cache fetch new versions."""
    path = os.path.join(ROOT, "README.md")
    md = open(path, encoding="utf-8").read()
    def sub(m):
        f = os.path.join(A, m.group(1))
        v = hashlib.sha1(open(f, "rb").read()).hexdigest()[:8] if os.path.exists(f) else None
        return f'assets/{m.group(1)}?v={v}"' if v else m.group(0)
    new = re.sub(r'assets/([\w.-]+\.svg)(?:\?v=\w+)?"', sub, md)
    if new != md:
        open(path, "w", encoding="utf-8", newline="\n").write(new)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "all":
        hero(); labels()
    music()
    if mode != "music":
        stats()
    stamp_readme()
