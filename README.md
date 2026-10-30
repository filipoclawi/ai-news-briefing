# AI Briefing

A static, privacy-safe archive of plain-language executive briefings distilled from the exact Gmail label `AI news`.

Live site: <https://filipoclawi.github.io/ai-news-briefing/>

## Editions

- **24.–30. Oktober 2026 — Freitagsausgabe, Woche bisher:** eine Newsletter-Ausgabe vom 24. Oktober, eine unverändert beibehaltene Forschungs-Kurzvorschau; keine neue Meldung. Redaktionell finalisiert zum Quellenstand 30. Oktober 2026, 22:31:16 CET. Das Kalenderfenster endet erst um Mitternacht; spätere Eingänge werden als Nachtrag ergänzt. Keine historischen Nachträge in diesem Lauf.
- **17.–23. Oktober 2026 — abgeschlossene Woche, Nachtrag:** zwei Newsletter-Ausgaben, acht technische und strategische Kurzanalysen. Alle achtzig zuvor veröffentlichten Karten bleiben in ihren Archiven erhalten.

`editions.json` hält den aktuellen Ausgabenstand, saubere Quellenadressen und stabile Karten-IDs fest. Bei der Freitagsaktualisierung werden vorhandene Quellen und Karten mit neuen Eingängen zusammengeführt: nach Quellenadresse und Karten-ID deduplizieren, niemals den Zwischenstand allein durch neue Eingänge ersetzen. Die aktuelle Wochenquelle bleibt bis zur verifizierten Finalisierung im Posteingang. Private Quellenbelege werden separat geführt und nicht veröffentlicht.

- **10–16 October 2026 (completed-week recovery)** — three source issues reviewed; twelve email-grounded stories. Reviewed 17 October, 09:47:08 CEST.
- **3–9 October 2026 (completed-week catch-up)** — two historical source issues recovered; eight email-grounded stories. Recovered on 17 October, filling the previously unpublished window. All sixty previously published story cards remain intact.

The 16 October run prepared local changes but did not publish; the recovery resumed that work, read all five source emails, and used their actual clean public issue links without requiring external article fetches.

- **26 September–2 October 2026 (week to date)** — three source issues reviewed, seven stories retained. Updated 2 October at the 22:31:29 CEST source cutoff; two additional current-week issues added five stories, with no historical recoveries in this update.

Recovered publication on 18 September 2026: 14 source issues, 10 historical; 11 new stories across four windows.

- **2026-09-18** — 4 source issues; 4 stories.
- **2026-09-11** — 2 source issues; 2 stories.
- **2026-09-04** — 4 source issues; 2 stories.
- **2026-08-28** — 4 source issues; 3 stories.

- **15–21 August 2026** — five source issues considered, eight stories retained.
- **8–14 August 2026** — catch-up edition assembled from four late-recovered source issues, seven stories retained.
- **1–7 August 2026** — six source issues considered, seven stories retained.
- **24–31 July 2026** — transition edition; six source issues considered, eight stories retained.
- **24 June–23 July 2026** — original edition, updated after one late recovery; seventeen source issues considered, ten stories retained.
- Future editions use a regular **Saturday–Friday** reporting window and are published on Friday evening.

The top-level URL always presents the latest edition. Earlier editions remain available through the edition navigation.

## Editorial method

- Every source issue in the frozen reporting-window set is considered.
- Repeated stories are merged and low-signal material is removed.
- Hyperbolische Sprache wird neutral zusammengefasst; neue Ausgaben erscheinen auf Deutsch, frühere Karten bleiben unverändert.
- Frühe, strittige und unternehmenseigene Angaben werden als berichtete Behauptungen gekennzeichnet.
- Clean public links are used instead of email tracking links.
- No email addresses, Gmail identifiers, recipient data, credentials, private attribution, or personalized links are published.
- Source emails are marked read and archived only after the corresponding public edition is deployed and verified; the `AI news` label is preserved.

## Local preview and checks

```bash
python3 tests/ui_smoke.py
```

The test covers the latest and archived editions, filters, clean links, privacy, desktop/mobile overflow, and browser console errors.
