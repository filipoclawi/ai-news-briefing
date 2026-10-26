#!/usr/bin/env python3
"""Deterministic local/live edition checks. BASE_URL selects a deployment."""
import functools, http.server, json, os, re, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'tests/editions.json').read_text())
server = None
base = os.environ.get('BASE_URL')
if not base:
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        errors = []
        for width in [1440, 390]:
            page = browser.new_page(viewport={'width': width, 'height': 900})
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            for path, expected in manifest.items():
                response = page.goto(base + path + '?verify=' + os.environ.get('VERIFY_BUILD', '20261002'), wait_until='networkidle')
                assert response.status == 200, path
                page.wait_for_function("document.documentElement.dataset.ready === 'true'")
                assert page.title() == expected['title'], path
                assert page.locator('.story[data-category]').count() == expected['stories'], path
                if path == 'editions/2026-10-02/index.html':
                    assert page.locator('.metric strong').all_text_contents() == ['3', '7', '5', '0']
                    assert page.locator('.method-list a').count() == 3
                    assert '22:31:29 CEST' in page.locator('.method-list').inner_text()
                    page.locator('[data-filter=all]').focus()
                    page.keyboard.press('Tab')
                    assert page.evaluate("document.activeElement.matches('button[data-filter]')")
                    page.keyboard.press('Enter')
                    assert page.evaluate("document.activeElement.getAttribute('aria-pressed')") == 'true'
                    page.locator('[data-filter=all]').click()
                if 'metrics' in expected:
                    assert page.locator('.metric strong').all_text_contents() == expected['metrics']
                    assert page.locator('.method-list a').count() == expected['sources']
                    assert expected['cutoff'] in page.locator('.method-list').inner_text()
                    method = page.locator('.method-list').inner_text()
                    german = expected.get('basis') == 'newsletter-de'
                    if german:
                        assert page.locator('html').get_attribute('lang') == 'de'
                        assert 'Auf Grundlage der Newsletter' in method
                        assert 'Keine unabhängige Verifikation' in method
                        assert 'Meldung' in (page.locator('#result-count').text_content() or '')
                        assert ('Woche bisher' in page.title()) == (expected['status'] == 'week-to-date')
                        assert 'lesezeit nicht angegeben' in page.locator('body').inner_text().lower()
                        assert 'Newsletter-Audio:' in method
                    else:
                        assert 'Email-only method' in method and 'no independent verification is claimed' in method
                        assert 'Completed week' in page.title()
                    issue_urls = set(page.locator('.method-list a').evaluate_all('els => els.map(e => e.href)'))
                    assert len(issue_urls) == expected['sources']
                    for card in page.locator('.story').all():
                        assert card.locator('.source-link').get_attribute('href') in issue_urls
                        assert ('Zum Newsletter' if german else 'Newsletter issue') in card.locator('.source-link').inner_text()
                        assert ('Lesezeit nicht angegeben' if german else '~1 min summary') in (card.locator('.story-date').text_content() or '')
                        date_box = card.locator('.story-date').bounding_box()
                        link_box = card.locator('.source-link').bounding_box()
                        card_box = card.bounding_box()
                        assert date_box and link_box and card_box
                        assert date_box['width'] >= 150
                        assert link_box['width'] <= card_box['width']
                    page.locator('[data-filter=all]').focus()
                    page.keyboard.press('Tab')
                    assert page.evaluate("document.activeElement.matches('button[data-filter]')")
                    page.keyboard.press('Enter')
                    assert page.evaluate("document.activeElement.getAttribute('aria-pressed')") == 'true'
                    page.locator('[data-filter=all]').click()
                assert page.locator('.edition-nav [aria-current=page]').count() == 1
                assert page.locator('.edition-nav a').count() == len(manifest) - 2
                assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth'), path
                for button in page.locator('button[data-filter]').all():
                    value = button.get_attribute('data-filter')
                    button.click()
                    count = expected['stories'] if value == 'all' else page.locator(f'.story[data-category="{value}"]').count()
                    assert page.locator('.story:visible').count() == count
                page.locator('[data-filter=all]').click()
                for href in page.locator('.source-link').evaluate_all('els => els.map(e => e.href)'):
                    assert href.startswith('https://') and '?' not in href and 'substack.com/redirect' not in href
                text = page.locator('body').inner_text()
                assert not re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}', text)
                assert not any(x in text.lower() for x in ['/home/', 'gmail', 'token.json'])
                for link in page.locator('.edition-nav a').all():
                    assert page.request.get(link.get_attribute('href') if link.get_attribute('href').startswith('http') else __import__('urllib.parse', fromlist=['urljoin']).urljoin(page.url, link.get_attribute('href'))).status == 200
                if path == 'index.html' or any(x in path for x in ['2026-08-28','2026-09-04','2026-09-11']):
                    page.screenshot(path=str(ROOT / f'test-results-{Path(path).parent.name}-{width}.png'), full_page=True)
            page.close()
        browser.close()
        assert not errors, errors
    for path in [ROOT/'index.html', *ROOT.glob('editions/*/index.html'), *ROOT.glob('assets/*')]:
        text = path.read_text()
        assert not re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}|/home/|substack.com/redirect|AIza[\w-]+|ghp_[\w]+', text), path
    print(f'PASS: {len(manifest)} pages, desktop/mobile, filters, navigation, privacy, clean source links, no console errors')
finally:
    if server:
        server.shutdown()
