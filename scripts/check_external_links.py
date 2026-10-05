#!/usr/bin/env python3
"""Check external (http/https) links. Run on a schedule or by hand, NOT on every edit.

Classification (so that a temporary network problem is not reported as a broken link):
  OK            2xx, or 3xx that ends in 2xx
  BROKEN        404 / 410 after retries            -> fails the job (exit 1)
  RATE_LIMITED  429                                  -> warning
  FORBIDDEN     401 / 403 / 999 (the site refuses automatic access; check by hand) -> warning
  SERVER_ERROR  5xx                                  -> warning
  TIMEOUT       timeout, DNS or connection error     -> warning (retry later)
Only BROKEN fails. Every warning is printed so that nothing is hidden.
"""
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklib import ROOT, all_markdown_files, iter_links, is_external  # noqa: E402

UA = "Mozilla/5.0 (compatible; two-worlds-one-mind-linkcheck/1.1; +https://github.com/HomenSAI/two-worlds-one-mind)"


def classify(url):
    last = "TIMEOUT"
    for attempt in range(3):
        for method in ("HEAD", "GET"):
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    return "OK", r.status
            except urllib.error.HTTPError as e:
                if e.code in (405, 501) and method == "HEAD":
                    continue
                if e.code in (404, 410):
                    last = ("BROKEN", e.code)
                elif e.code == 429:
                    last = ("RATE_LIMITED", e.code)
                elif e.code in (401, 403, 999):
                    last = ("FORBIDDEN", e.code)
                elif e.code >= 500:
                    last = ("SERVER_ERROR", e.code)
                else:
                    last = ("SERVER_ERROR", e.code)
                break
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
                last = ("TIMEOUT", str(e)[:60])
                break
        time.sleep(2 * (attempt + 1))
        if isinstance(last, tuple) and last[0] in ("BROKEN", "FORBIDDEN"):
            if attempt >= 1:
                break
    return last if isinstance(last, tuple) else (last, "")


def main():
    urls = {}
    for md in all_markdown_files():
        text = md.read_text(encoding="utf-8")
        found = [h for _, h, _ in iter_links(text) if h and re.match(r"^https?://", h)]
        found += re.findall(r"<(https?://[^>\s]+)>", text)
        for u in found:
            urls.setdefault(u.split("#")[0], md.relative_to(ROOT).as_posix())
    results = {}
    for u in sorted(urls):
        if "github.com/HomenSAI/two-worlds-one-mind" in u and ("/releases/tag/v1.1" in u):
            results[u] = ("SKIPPED", "release not published yet")
            continue
        results[u] = classify(u)
        time.sleep(0.5)
    broken = [u for u, (c, _) in results.items() if c == "BROKEN"]
    for u, (c, d) in results.items():
        if c != "OK":
            print(f"{c:13} {d!s:>5}  {u}   (in {urls[u]})")
    counts = {}
    for c, _ in results.values():
        counts[c] = counts.get(c, 0) + 1
    print(f"EXTERNAL LINKS: {len(results)} unique URLs; " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    if broken:
        print(f"EXTERNAL LINKS: FAIL ({len(broken)} broken)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
