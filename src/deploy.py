#!/usr/bin/env python3
"""Deploy ../site to Vercel using the REST API (no Node / Vercel CLI needed).

Token resolution order:  $VERCEL_TOKEN  ->  ~/.vercel_token  ->  ./.vercel_token
The token is never printed.

Usage:  python3 deploy.py [project-name] [--preview]      (default: flatfish-gnv)
"""
import os, sys, json, hashlib, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..'))   # the repo root is the site
SKIP_DIRS = {'.git', 'src', 'node_modules', '.vercel', '__pycache__', '.github'}
API  = 'https://api.vercel.com'

PROJECT = (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-')
           else 'flatfish-gnv')
TARGET  = 'staging' if '--preview' in sys.argv else 'production'


def token():
    t = os.environ.get('VERCEL_TOKEN', '').strip()
    if t:
        return t
    for p in (os.path.expanduser('~/.vercel_token'), os.path.join(HERE, '.vercel_token')):
        if os.path.exists(p):
            t = open(p, encoding='utf-8').read().strip()
            if t:
                return t
    sys.exit('No Vercel token found. Set $VERCEL_TOKEN or write it to ~/.vercel_token')


TOK = token()


def req(method, path, body=None, raw=None, extra=None):
    url = path if path.startswith('http') else API + path
    hdrs = {'Authorization': 'Bearer ' + TOK}
    if raw is not None:
        data = raw
        hdrs['Content-Length'] = str(len(raw))
    elif body is not None:
        data = json.dumps(body).encode()
        hdrs['Content-Type'] = 'application/json'
    else:
        data = None
    hdrs.update(extra or {})
    r = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode() or '{}')
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:900]
        sys.exit('\n%s %s -> HTTP %s\n%s' % (method, path, e.code, detail))


# ---- collect files -------------------------------------------------------
files, total = [], 0
for root, dirs, names in os.walk(SITE):
    dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS and not d.startswith('.')]
    for n in sorted(names):
        if n == '.DS_Store' or n.startswith('.'):
            continue
        full = os.path.join(root, n)
        rel = os.path.relpath(full, SITE).replace(os.sep, '/')
        blob = open(full, 'rb').read()
        files.append({'file': rel, 'sha': hashlib.sha1(blob).hexdigest(),
                      'size': len(blob), '_blob': blob})
        total += len(blob)

print('whoami ...', end=' ', flush=True)
me = req('GET', '/v2/user')
user = me.get('user', me)
print('%s (%s)' % (user.get('username') or user.get('name'), user.get('email')))
print('project : %s   target: %s' % (PROJECT, TARGET))
print('files   : %d  (%.1f KB)\n' % (len(files), total / 1024.0))

# ---- upload blobs -------------------------------------------------------
for i, f in enumerate(files, 1):
    req('POST', '/v2/files', raw=f['_blob'],
        extra={'x-vercel-digest': f['sha'], 'Content-Type': 'application/octet-stream'})
    print('  [%2d/%d] %-26s %7.1f KB  uploaded' % (i, len(files), f['file'], f['size'] / 1024.0))

# ---- create deployment --------------------------------------------------
payload = {
    'name': PROJECT,
    'target': TARGET,
    'files': [{'file': f['file'], 'sha': f['sha'], 'size': f['size']} for f in files],
    'projectSettings': {
        'framework': None, 'buildCommand': None, 'installCommand': None,
        'devCommand': None, 'outputDirectory': None,
    },
}
print('\ncreating deployment ...')
dep = req('POST', '/v13/deployments?skipAutoDetectionConfirmation=1', body=payload)
dep_id, url = dep['id'], dep['url']
print('  id  : %s\n  url : https://%s' % (dep_id, url))

# ---- poll ---------------------------------------------------------------
print('\nwaiting for READY', end='', flush=True)
state = dep.get('readyState') or dep.get('status')
for _ in range(100):
    if state in ('READY', 'ERROR', 'CANCELED'):
        break
    time.sleep(3)
    print('.', end='', flush=True)
    state = req('GET', '/v13/deployments/' + dep_id).get('readyState')
print('\n  state: %s' % state)

if state != 'READY':
    sys.exit('Deployment did not reach READY.')

# ---- resolve the stable production alias --------------------------------
info = req('GET', '/v13/deployments/' + dep_id)
aliases = info.get('alias') or []
print('\n' + '=' * 58)
print('LIVE:  https://%s' % url)
for a in aliases:
    print('       https://%s' % a)
print('=' * 58)
print('\nPages:')
for f in files:
    if f['file'].endswith('.html'):
        slug = '' if f['file'] == 'index.html' else '/' + f['file'][:-5]
        print('  https://%s%s' % (aliases[0] if aliases else url, slug))
