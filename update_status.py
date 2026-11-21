
import json, re, urllib.request
from datetime import datetime, timezone, timedelta
codes = {0:'clear sky',1:'mostly clear',2:'partly cloudy',3:'overcast',45:'fog',48:'fog',51:'light drizzle',53:'drizzle',55:'drizzle',61:'light rain',63:'rain',65:'heavy rain',80:'light showers',81:'showers',82:'heavy showers',95:'thunderstorm'}
w = json.load(urllib.request.urlopen('https://api.open-meteo.com/v1/forecast?latitude=11.9404&longitude=108.4583&current=temperature_2m,weather_code&timezone=Asia%2FHo_Chi_Minh'))
cur = w['current']
desc = codes.get(cur['weather_code'], 'mountain weather')
last = 'recently'
try:
    ev = json.load(urllib.request.urlopen('https://api.github.com/users/Dongdarealest/events/public?per_page=10'))
    for e in ev:
        if e['type'] == 'PushEvent':
            t = datetime.fromisoformat(e['created_at'].replace('Z','+00:00')).astimezone(timezone(timedelta(hours=7)))
            last = t.strftime('%H:%M') + ' to ' + e['repo']['name'].split('/')[1]
            break
except Exception:
    pass
line = '<p align="center"><sub>Da Lat now: ' + str(cur['temperature_2m']) + '°C, ' + desc + ' · Last push ' + last + ' · Currently building TubeEQ and Sai Đâu Sửa Đó</sub></p>'
src = open('README.md', encoding='utf-8').read()
new = re.sub(r'<!--STATUS:START-->.*<!--STATUS:END-->', '<!--STATUS:START-->
' + line + '
<!--STATUS:END-->', src, flags=re.S)
if new != src:
    open('README.md', 'w', encoding='utf-8').write(new)
    print('status updated')
else:
    print('status unchanged')
