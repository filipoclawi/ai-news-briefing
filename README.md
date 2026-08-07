# AI Briefing

A static, privacy-safe archive of plain-language executive briefings distilled from the exact Gmail label `AI news`.

Live site: <https://filipoclawi.github.io/ai-news-briefing/>

## Editions

- **24–31 July 2026** — transition edition covering the day after the original briefing through the end of the first completed reporting week; six source issues considered, eight stories retained.
- **24 June–23 July 2026** — original edition, updated after one late recovery; seventeen source issues considered, ten stories retained.
- Future editions use a regular **Saturday–Friday** reporting window and are published on Friday evening.

The top-level URL always presents the latest edition. Earlier editions remain available through the edition navigation.

## Editorial method

- Every source issue in the frozen reporting-window set is considered.
- Repeated stories are merged and low-signal material is removed.
- Hyperbolic language is rewritten in plain English.
- Early, disputed, or company-reported claims are labelled.
- Clean public links are used instead of email tracking links.
- No email addresses, Gmail identifiers, recipient data, credentials, private attribution, or personalized links are published.
- Source emails are marked read and archived only after the corresponding public edition is deployed and verified; the `AI news` label is preserved.

## Local preview and checks

```bash
python3 tests/ui_smoke.py
```

The test covers the latest and archived editions, filters, clean links, privacy, desktop/mobile overflow, and browser console errors.
