
import json, re, urllib.request
from datetime import datetime, timezone, timedelta
VN = timezone(timedelta(hours=7))
def fmt(ev, limit=5):
    lines = []
    for e in ev:
        t = datetime.fromisoformat(e['created_at'].replace('Z', '+00:00')).astimezone(VN)
        when = t.strftime('%d/%m')
        full = e['repo']['name']; repo = full.split('/')[1]
        link = '[' + repo + '](https://github.com/' + full + ')'
        typ, p = e['type'], e.get('payload', {})
        if typ == 'PushEvent':
            n = len(p.get('commits', [])) or p.get('size', 1)
            lines.append('- Pushed ' + str(n) + ' commit' + ('s' if n != 1 else '') + ' to ' + link + ' · ' + when)
        elif typ == 'PullRequestEvent':
            pr = p.get('pull_request', {})
            act = 'Merged' if pr.get('merged') else str(p.get('action', 'opened')).capitalize()
            lines.append('- ' + act + ' pull request #' + str(p.get('number')) + ' in ' + link + ' · ' + when)
        elif typ == 'CreateEvent':
            lines.append('- Created ' + str(p.get('ref_type', 'repository')) + ' in ' + link + ' · ' + when)
        elif typ == 'WatchEvent':
            lines.append('- Starred ' + link + ' · ' + when)
        elif typ == 'ForkEvent':
            lines.append('- Forked ' + link + ' · ' + when)
        elif typ == 'ReleaseEvent':
            lines.append('- Released in ' + link + ' · ' + when)
        elif typ == 'IssuesEvent':
            lines.append('- ' + str(p.get('action', 'updated')).capitalize() + ' an issue in ' + link + ' · ' + when)
        if len(lines) >= limit: break
    return '\n'.join(lines) if lines else '- Quiet lately. Building in private.'
ev = json.load(urllib.request.urlopen('https://api.github.com/users/Dongdarealest/events/public?per_page=30'))
body = fmt(ev)
src = open('README.md', encoding='utf-8').read()
new = re.sub(r'<!--ACTIVITY:START-->.*<!--ACTIVITY:END-->', '<!--ACTIVITY:START-->\n' + body + '\n<!--ACTIVITY:END-->', src, flags=re.S)
if new != src:
    open('README.md', 'w', encoding='utf-8').write(new)
    print('activity updated')
else:
    print('activity unchanged')
