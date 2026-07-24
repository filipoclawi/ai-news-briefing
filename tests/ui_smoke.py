#!/usr/bin/env python3
import re, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
server=subprocess.Popen([sys.executable,'-m','http.server','8765'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
  time.sleep(1)
  with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    errors=[]
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.goto('http://127.0.0.1:8765',wait_until='networkidle')
    page.wait_for_function("document.documentElement.dataset.ready === 'true'")
    assert page.title()=='AI Briefing — 23 July 2026'
    assert page.locator('.story[data-category]').count()==10
    assert page.locator('.signal').count()==5
    assert page.locator('.source-link').count()>=18
    for label,expected in [('Security',2),('Models',1),('Agents',2),('Science',2),('Policy & legal',2),('Infrastructure',1)]:
      page.get_by_role('button',name=label,exact=True).click()
      assert page.locator('.story[data-category]:visible').count()==expected,(label,page.locator('.story[data-category]:visible').count())
    page.get_by_role('button',name='All',exact=True).click()
    assert page.locator('.story[data-category]:visible').count()==10
    hrefs=page.locator('.source-link').evaluate_all("els=>els.map(e=>e.href)")
    assert all(h.startswith('https://') for h in hrefs)
    assert not any('substack.com/redirect/' in h or '?j=' in h for h in hrefs)
    text=page.locator('body').inner_text().lower()
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}',text)
    assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')
    page.screenshot(path=str(ROOT/'test-results-desktop.png'),full_page=True)
    mobile=browser.new_page(viewport={'width':390,'height':844})
    mobile.goto('http://127.0.0.1:8765',wait_until='networkidle')
    mobile.wait_for_function("document.documentElement.dataset.ready === 'true'")
    assert mobile.locator('.story[data-category]').count()==10
    assert mobile.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')
    mobile.screenshot(path=str(ROOT/'test-results-mobile.png'),full_page=True)
    mobile.close();browser.close()
    assert not errors,errors
  print('UI smoke passed: 10 stories, filters, safe links, desktop/mobile, no console errors')
finally:
  server.terminate();server.wait(timeout=5)
