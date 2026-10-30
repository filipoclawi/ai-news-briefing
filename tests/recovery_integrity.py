#!/usr/bin/env python3
"""Audit edition state and retained editorial coverage without private inputs."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Cards(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'article' and 'story' in (values.get('class') or '').split():
            self.ids.append(values.get('id'))

state = json.loads((ROOT / 'editions.json').read_text())
assert state['latest'] == '2026-10-30'
assert state['sourceCutoff'] == '2026-10-30T22:31:16+01:00'
assert len(state['editions']) == len(list((ROOT / 'editions').glob('*/index.html')))
by_date = {e['date']: e for e in state['editions']}
for date, stories, sources, status in [
    ('2026-10-23', 8, 2, 'completed'),
    ('2026-10-30', 1, 1, 'week-to-date'),
]:
    entry = by_date[date]
    assert (entry['stories'], len(entry['sources']), entry['status']) == (stories, sources, status)
    text = (ROOT / entry['path']).read_text()
    parser = Cards()
    parser.feed(text)
    assert set(parser.ids) == set(entry['storyIds'])
    assert len(parser.ids) == len(set(parser.ids)) == stories
    assert '<html lang="de">' in text
    assert 'Auf Grundlage der Newsletter' in text
    assert 'Lesezeit nicht angegeben' in text
    assert '~1 min' not in text
    for source in entry['sources']:
        assert source['url'].startswith('https://theinnermostloop.substack.com/p/')
        assert '?' not in source['url']
        assert set(source['storyIds']).issubset(parser.ids)
        assert source['url'] in text
    assert set(parser.ids) == {i for s in entry['sources'] for i in s['storyIds']}
root = (ROOT / 'index.html').read_text()
assert 'Woche bisher' in root and '30. Oktober 2026, 22:31:16 CET' in root
assert '24.–30. Oktober 2026' in root
assert '2026-10-30' in root
assert 'redaktionell finalisiert' in root and 'Kalenderfenster läuft bis Mitternacht' in root
assert by_date['2026-10-30']['fridayFinalized'] is True
assert by_date['2026-10-30']['finalizedThrough'] == state['sourceCutoff']
assert by_date['2026-10-30']['newStories'] == 0
assert by_date['2026-10-30']['retainedStories'] == 1

for path in [ROOT/'editions.json', ROOT/'README.md', ROOT/'index.html', *ROOT.glob('assets/*'), *ROOT.glob('editions/*/index.html')]:
    text = path.read_text()
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}|/home/|substack\.com/redirect|utm_|[?&](?:token|r|email|recipient)=|AIza[\w-]+|gh[pousr]_[\w]+', text, re.I), path
print('PASS: durable edition/source/story mapping, German email-only previews, honest current-week cutoff, public privacy')
