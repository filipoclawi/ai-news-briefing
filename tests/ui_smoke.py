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
    assert page.title()=='AI Briefing — 7 August 2026'
    assert page.locator('.story[data-category]').count()==7
    assert page.locator('.signal').count()==5
    assert page.locator('.source-link').count()==9
    assert page.locator('.edition-nav [aria-current="page"]').text_content().strip()=='1–7 Aug'
    assert page.locator('.edition-nav a[href="editions/2026-07-31/"]').count()==1
    assert page.locator('.edition-nav a[href="editions/2026-07-23/"]').count()==1
    for label,expected in [('Science',1),('Models',1),('Security',1),('Agents',1),('Policy',1),('Infrastructure',2)]:
      page.get_by_role('button',name=label,exact=True).click()
      assert page.locator('.story[data-category]:visible').count()==expected,(label,page.locator('.story[data-category]:visible').count())
      assert page.locator('#result-count').text_content().strip()==f'{expected} {"story" if expected==1 else "stories"}'
    page.get_by_role('button',name='All',exact=True).click()
    assert page.locator('.story[data-category]:visible').count()==7
    hrefs=page.locator('.source-link').evaluate_all("els=>els.map(e=>e.href)")
    assert all(h.startswith('https://') for h in hrefs)
    assert not any('substack.com/redirect/' in h or '?' in h for h in hrefs)
    text=page.locator('body').inner_text().lower()
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}',text)
    assert not any(x in text for x in ['/home/','gmail','@icloud.com'])
    assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')
    page.screenshot(path=str(ROOT/'test-results-desktop.png'),full_page=True)

    archives=[
      ('2026-07-31','AI Briefing — 31 July 2026',8,'24–31 Jul'),
      ('2026-07-23','AI Briefing — 23 July 2026',10,'24 Jun–23 Jul')]
    for slug,title,count,current in archives:
      page.goto(f'http://127.0.0.1:8765/editions/{slug}/',wait_until='networkidle')
      page.wait_for_function("document.documentElement.dataset.ready === 'true'")
      assert page.title()==title
      assert page.locator('.story[data-category]').count()==count
      assert page.locator('.edition-nav [aria-current="page"]').text_content().strip()==current
      assert page.locator('.edition-nav a[href="../../"]').count()==1
      assert page.locator('.edition-nav a').count()==2
      assert page.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')
      if slug=='2026-07-23':
        assert '17 issues reviewed · 1 recovered' in page.locator('.utility').text_content()
        assert page.locator('.brief-box strong').text_content().strip()=='10 / 17'
        assert 'recovered after the original publication' in page.locator('.method').inner_text()
        archive_hrefs=page.locator('.source-link').evaluate_all("els=>els.map(e=>e.href)")
        assert all(h.startswith('https://') for h in archive_hrefs)
        assert not any('substack.com/redirect/' in h or '?' in h for h in archive_hrefs)
        archive_text=page.locator('body').inner_text().lower()
        assert not re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}',archive_text)
        assert not any(x in archive_text for x in ['/home/','gmail','@icloud.com'])
        page.screenshot(path=str(ROOT/'test-results-recovered-archive.png'),full_page=True)

    mobile=browser.new_page(viewport={'width':390,'height':844})
    mobile.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
    mobile.on('pageerror',lambda e: errors.append(str(e)))
    for path,count in [('',7),('editions/2026-07-31/',8),('editions/2026-07-23/',10)]:
      mobile.goto('http://127.0.0.1:8765/'+path,wait_until='networkidle')
      mobile.wait_for_function("document.documentElement.dataset.ready === 'true'")
      assert mobile.locator('.story[data-category]').count()==count
      assert mobile.locator('.edition-nav').count()==1
      assert mobile.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth')
    mobile.goto('http://127.0.0.1:8765',wait_until='networkidle')
    mobile.screenshot(path=str(ROOT/'test-results-mobile.png'),full_page=True)
    mobile.close(); browser.close()
    assert not errors,errors
  print('UI smoke passed: 3 editions, recovery metadata, exact filters, clean HTTPS links, desktop/mobile overflow, no console errors')
finally:
  server.terminate(); server.wait(timeout=5)
