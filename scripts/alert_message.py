#!/usr/bin/env python3
"""Turn the alert rows from take_alerts into a Telegram message.

Reads the JSON array on stdin, writes the message on stdout. Prints nothing if
there is nothing to report, so the workflow can skip sending."""
import json
import sys

KIND = {
    'daily_limit':    'hit the daily limit',
    'device_blocked': 'tried to use an extra device',
    'revoked':        'used a switched-off code',
    'expired':        'used an expired code',
}


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        return
    try:
        rows = json.loads(raw)
    except json.JSONDecodeError:
        sys.stderr.write('could not read the alert list: %s\n' % raw[:200])
        sys.exit(1)
    if not rows:
        return

    lines = ['*MCQ bank - %d alert(s)*' % len(rows), '']
    for r in rows:
        who = r.get('holder') or 'not assigned to anyone'
        when = (r.get('created_at') or '')[11:16]
        lines.append('`%s`  (%s)' % (r.get('code'), who))
        lines.append('%s' % KIND.get(r.get('kind'), r.get('kind') or 'alert'))
        if r.get('detail'):
            lines.append(r['detail'])
        lines.append('_at %s UTC_' % when)
        lines.append('')
    sys.stdout.write('\n'.join(lines))


if __name__ == '__main__':
    main()
