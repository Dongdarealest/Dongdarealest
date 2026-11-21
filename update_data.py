import json, math, urllib.request
from datetime import datetime, timezone, timedelta

USER = 'Dongdarealest'
VN = timezone(timedelta(hours=7))
SANS = "Inter, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
SERIF = "Georgia, 'Times New Roman', serif"

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'profile-data-updater'})
    return json.load(urllib.request.urlopen(req, timeout=25))

repos = get(f'https://api.github.com/users/{USER}/repos?per_page=100&type=owner')
projects = [r for r in repos if not r['fork'] and r['name'] != USER]

# ---- languages across all project repos ----
totals = {}
for r in projects:
    try:
        langs = get(r['languages_url'])
    except Exception:
        continue
    for k, v in langs.items():
        totals[k] = totals.get(k, 0) + v
grand = sum(totals.values())
top = sorted(totals.items(), key=lambda kv: -kv[1])[:6]
maxpct = top[0][1] / grand * 100
FREQS = ['31 Hz', '62 Hz', '250 Hz', '1 kHz', '4 kHz', '16 kHz']
bands = []
for i, (name, b) in enumerate(top):
    pct = b / grand * 100
    db = -12 + 24 * (pct / maxpct) ** 0.55
    bands.append((FREQS[i], name, pct, round(db, 1)))

# ---- animated EQ svg ----
def lerp(c1, c2, t):
    return tuple(round(a + (bb - a) * t) for a, bb in zip(c1, c2))

def hx(c):
    return '#%02X%02X%02X' % c

BOT, TOPC = (138, 109, 52), (232, 200, 122)
N = 24
SEG_TOP, SEG_H, SEG_GAP = 262, 17, 5
STEP = SEG_H + SEG_GAP
SEG_BOT = SEG_TOP + (N - 1) * STEP + SEG_H
W, H = 1760, 1060
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
o.append('<rect x="40" y="40" width="1680" height="980" rx="28" fill="#0D1117" stroke="#23272F" stroke-width="2"/>')
for sx, sy in [(76, 76), (1684, 76), (76, 984), (1684, 984)]:
    o.append(f'<circle cx="{sx}" cy="{sy}" r="10" fill="none" stroke="#3A4150" stroke-width="2"/>')
    o.append(f'<line x1="{sx - 6}" y1="{sy}" x2="{sx + 6}" y2="{sy}" stroke="#3A4150" stroke-width="2"/>')
o.append(f'<text x="110" y="122" font-family="{SANS}" font-size="40" font-weight="600" letter-spacing="14" fill="#F2EFE9">DONGDAREALEST</text>')
o.append(f'<text x="110" y="170" font-family="{SANS}" font-size="30" fill="#8A8680">profile, equalized</text>')
o.append(f'<text x="1650" y="122" text-anchor="end" font-family="{SANS}" font-size="25" letter-spacing="4" fill="#8A8680">DA LAT · NIGHT SESSION</text>')
o.append('<line x1="110" y1="208" x2="1650" y2="208" stroke="#23272F" stroke-width="2"/>')
pitch = 1540 / 6
for i, (freq, name, pct, db) in enumerate(bands):
    cx = 110 + pitch * (i + 0.5)
    lit = round((db + 12) / 24 * N)
    o.append(f'<text x="{cx}" y="240" text-anchor="middle" font-family="{MONO}" font-size="30" font-weight="600" fill="#E8C87A">{db:+.1f} dB</text>')
    rail_x = cx + 40
    o.append(f'<line x1="{rail_x}" y1="{SEG_TOP}" x2="{rail_x}" y2="{SEG_BOT}" stroke="#23272F" stroke-width="6"/>')
    for tick in range(5):
        ty = SEG_TOP + tick * (SEG_BOT - SEG_TOP) / 4
        o.append(f'<line x1="{rail_x + 10}" y1="{ty}" x2="{rail_x + 24}" y2="{ty}" stroke="#2A2F3A" stroke-width="3"/>')
    for j in range(N):
        y = SEG_TOP + j * STEP
        fb = N - 1 - j
        if fb < lit:
            color = hx(lerp(BOT, TOPC, fb / max(lit - 1, 1)))
            begin = 0.15 + i * 0.12 + fb * 0.045
            o.append(f'<rect x="{cx - 62}" y="{y}" width="46" height="{SEG_H}" rx="4" fill="{color}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.05s" fill="freeze"/></rect>')
        else:
            o.append(f'<rect x="{cx - 62}" y="{y}" width="46" height="{SEG_H}" rx="4" fill="#1A2029"/>')
    knob_cy = SEG_BOT - lit * STEP + STEP / 2
    o.append(f'<g><rect x="{rail_x - 33}" y="{knob_cy - 18}" width="66" height="36" rx="9" fill="#141A23" stroke="#A98B4F" stroke-width="2"/><line x1="{rail_x - 20}" y1="{knob_cy}" x2="{rail_x + 20}" y2="{knob_cy}" stroke="#F2EFE9" stroke-width="4"/><animateTransform attributeName="transform" type="translate" from="0 250" to="0 0" begin="{i * 0.12:.2f}s" dur="0.9s" fill="freeze"/></g>')
    o.append(f'<text x="{cx}" y="852" text-anchor="middle" font-family="{MONO}" font-size="26" fill="#8A8680">{freq}</text>')
    o.append(f'<text x="{cx}" y="898" text-anchor="middle" font-family="{SANS}" font-size="34" font-weight="600" fill="#F2EFE9">{name}</text>')
    o.append(f'<text x="{cx}" y="934" text-anchor="middle" font-family="{MONO}" font-size="25" fill="#8A8680">{pct:.1f}%</text>')
o.append('<line x1="110" y1="962" x2="1650" y2="962" stroke="#23272F" stroke-width="2"/>')
o.append(f'<text x="880" y="1000" text-anchor="middle" font-family="{SANS}" font-size="24" fill="#8A8680">Levels measured from the real code across his repositories</text>')
o.append('</svg>')
open('eq.svg', 'w').write('\n'.join(o))
print('eq.svg regenerated:', [(b[1], b[2]) for b in bands])

# ---- projects panel ----
def rel(iso):
    t = datetime.fromisoformat(iso.replace('Z', '+00:00'))
    d = datetime.now(timezone.utc) - t
    if d.days <= 0:
        h = d.seconds // 3600
        return 'just now' if h == 0 else f'{h}h ago'
    if d.days == 1:
        return 'yesterday'
    if d.days < 30:
        return f'{d.days} days ago'
    return f'{d.days // 30} mo ago'

recent = sorted(projects, key=lambda r: r['pushed_at'], reverse=True)[:6]
ROW = 96
HH = 108 + ROW * len(recent) + 18
p = []
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="1760" height="{HH}" viewBox="0 0 1760 {HH}">')
p.append(f'<rect x="4" y="4" width="1752" height="{HH - 8}" rx="24" fill="#141414" stroke="#2A2A26" stroke-width="2"/>')
p.append(f'<text x="70" y="66" font-family="{SANS}" font-size="24" font-weight="600" letter-spacing="8" fill="#A98B4F">ON THE BENCH</text>')
upd = datetime.now(VN).strftime('%d/%m')
p.append(f'<text x="1690" y="66" text-anchor="end" font-family="{SANS}" font-size="22" fill="#8A8680">updated {upd}</text>')
for i, r in enumerate(recent):
    y0 = 108 + i * ROW
    if i:
        p.append(f'<line x1="70" y1="{y0 - 26}" x2="1690" y2="{y0 - 26}" stroke="#232320" stroke-width="1"/>')
    p.append(f'<text x="70" y="{y0 + 14}" font-family="{SERIF}" font-size="36" fill="#F2EFE9">{r["name"]}</text>')
    meta = (r['language'] or 'code') + ' · last push ' + rel(r['pushed_at'])
    p.append(f'<text x="1690" y="{y0 + 14}" text-anchor="end" font-family="{SANS}" font-size="24" fill="#8A8680">{meta}</text>')
    desc = (r['description'] or '').strip()
    if len(desc) > 88:
        desc = desc[:87] + '…'
    if desc:
        desc = desc.replace('&', '&amp;').replace('<', '&lt;')
        p.append(f'<text x="70" y="{y0 + 54}" font-family="{SANS}" font-size="23" fill="#8A8680">{desc}</text>')
p.append('</svg>')
open('projects.svg', 'w').write('\n'.join(p))
print('projects.svg regenerated:', [r['name'] for r in recent])
