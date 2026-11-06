"""Rewrite the 'Latest on dylanlewis.au' list in README.md.

Reads the site's sitemap (project pages come newest first) and each page's
og:title and og:description. Standard library only.
"""
import html, re, sys, urllib.request

SITE = "https://dylanlewis.au"
COUNT = 4
START, END = "<!-- LATEST:START -->", "<!-- LATEST:END -->"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dylannnnn111-profile-readme"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def meta(page, prop):
    m = re.search(r'<meta[^>]+property="%s"[^>]+content="([^"]*)"' % re.escape(prop), page)
    return html.unescape(m.group(1)).strip() if m else ""


def main():
    urls = re.findall(r"<loc>([^<]+/projects/[^<]+)</loc>", get(SITE + "/sitemap.xml"))[:COUNT]
    if not urls:
        sys.exit("no project pages in sitemap")
    lines = []
    for u in urls:
        page = get(u)
        title = meta(page, "og:title") or u.rsplit("/", 1)[-1]
        desc = meta(page, "og:description")
        lines.append(f"- [{title}]({u})" + (f" - {desc}" if desc else ""))
    readme = open("README.md", encoding="utf-8").read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END),
                 START + "\n" + "\n".join(lines) + "\n" + END, readme, flags=re.S)
    if new != readme:
        open("README.md", "w", encoding="utf-8").write(new)
        print("updated")
    else:
        print("no change")


if __name__ == "__main__":
    main()
