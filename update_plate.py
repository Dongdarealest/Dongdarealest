
import json, urllib.request
from datetime import datetime, timezone, timedelta
VN = timezone(timedelta(hours=7))
WMO = {0: 'clear sky', 1: 'mostly clear', 2: 'partly cloudy', 3: 'overcast', 45: 'fog', 48: 'fog',
       51: 'light drizzle', 53: 'drizzle', 55: 'drizzle', 61: 'light rain', 63: 'rain', 65: 'heavy rain',
       71: 'light snow', 73: 'snow', 75: 'heavy snow', 80: 'showers', 81: 'showers', 82: 'heavy showers',
       95: 'thunderstorm', 96: 'thunderstorm', 99: 'thunderstorm'}
try:
    w = json.load(urllib.request.urlopen('https://api.open-meteo.com/v1/forecast?latitude=11.9404&longitude=108.4583&current=temperature_2m,weather_code', timeout=20))['current']
    temp = f"{w['temperature_2m']:.0f}"
    cond = WMO.get(w['weather_code'], '')
except Exception:
    temp, cond = '--', ''
try:
    ev = json.load(urllib.request.urlopen('https://api.github.com/users/Dongdarealest/events/public?per_page=100', timeout=20))
except Exception:
    ev = []
now = datetime.now(VN)
last = 'no pushes yet'
week = 0
for e in ev:
    t = datetime.fromisoformat(e['created_at'].replace('Z', '+00:00')).astimezone(VN)
    if e['type'] == 'PushEvent':
        if last == 'no pushes yet':
            last = f"Last push {t.strftime('%H:%M')} to {e['repo']['name'].split('/')[1]}"
        if (now - t).days < 7:
            week += 1
line1 = f"NIGHT SESSION · DA LAT {temp}°C" + (f" · {cond.upper()}" if cond else '')
line2 = f"{last} · {week} pushes this week"
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1760" height="230" viewBox="0 0 1760 230">
<style>.dot {{ animation: pulse 2.2s ease-in-out infinite; }} @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.2; }} 100% {{ opacity: 1; }} }}</style>
<rect x="4" y="4" width="1752" height="222" rx="24" fill="#141414" stroke="#2A2A26" stroke-width="2"/>
<circle class="dot" cx="92" cy="115" r="14" fill="#A98B4F"/>
<text x="140" y="104" font-family="Inter, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="35" font-weight="600" letter-spacing="6" fill="#F2EFE9">{line1}</text>
<text x="140" y="158" font-family="Inter, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="27" fill="#8A8680">{line2}</text>
</svg>
"""
open('plate.svg', 'w').write(svg)
print('plate:', line1, '|', line2)
