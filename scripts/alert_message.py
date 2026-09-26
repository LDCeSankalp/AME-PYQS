#!/usr/bin/env python3
"""Turn the alert rows from take_alerts into the daily Telegram message.

Reads the JSON array on stdin, writes the message on stdout. With no alerts it
writes a one-line "all quiet" note, so a missing message means the check itself
did not run. Prints nothing only if the database gave no answer at all."""
import json
import sys
from datetime import datetime, timedelta

KIND = {
    'daily_limit':    'hit the daily limit',
    'device_blocked': 'tried to use an extra device',
    'revoked':        'used a switched-off code',
    'expired':        'used an expired code',
    'report':         'reported a mistake',
}


def ist(stamp):
    """'2026-09-24T06:40:12.3+00:00' -> '24 Sep 12:10 IST'"""
    try:
        t = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        return (t + timedelta(hours=5, minutes=30)).strftime('%d %b %H:%M') + ' IST'
    except (ValueError, AttributeError):
        return stamp or ''


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
        sys.stdout.write('*MCQ bank - daily check*\nNo alerts since the last check.')
        return

    lines = ['*MCQ bank - daily check: %d alert(s)*' % len(rows), '']
    for r in rows:
        who = r.get('holder') or 'not assigned to anyone'
        lines.append('`%s`  (%s)' % (r.get('code'), who))
        lines.append('%s' % KIND.get(r.get('kind'), r.get('kind') or 'alert'))
        if r.get('detail'):
            lines.append(r['detail'])
        lines.append('_%s_' % ist(r.get('created_at')))
        lines.append('')
    sys.stdout.write('\n'.join(lines))


if __name__ == '__main__':
    main()
