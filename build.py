#!/usr/bin/env python3
"""Regenerate the ready-to-publish homepage after editing content.json."""
import html
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "content.json").read_text())
p = data["profile"]
esc = html.escape
styles_version = hashlib.sha256((ROOT / "styles.css").read_bytes()).hexdigest()[:10]


def paper(item, published=False):
    title = esc(item["title"])
    if item["url"]:
        title = f'<a href="{esc(item["url"], quote=True)}">{title}</a>'
    metadata = [f'with {esc(item["coauthors"])}'] if item["coauthors"] else []
    if not published and item["year"]:
        metadata.append(f'<span class="paper-year">{esc(item["year"])}</span>')
    author = '<p class="authors">' + '<span class="citation-separator"> · </span>'.join(metadata) + '</p>' if metadata else ""
    citation = ""
    if published:
        citation = f'<p class="citation"><em>{esc(item["journal"])}</em>'
        if item["citation"]:
            citation += f'<span class="citation-separator"> · </span>{esc(item["citation"])}'
        citation += '</p>'
    summary = f'<p class="paper-summary">{esc(item["summary"])}</p>' if item.get("summary") else ""
    return f'''        <li class="paper{' publication' if published else ''}">
          <article>
            <div class="paper-content">
              <h3>{title}</h3>
              {author}
              {citation}
              {summary}
            </div>
          </article>
        </li>'''


working = "\n".join(paper(x) for x in data["working_papers"])
publications = "\n".join(paper(x, True) for x in data["publications"])
person = {"@context": "https://schema.org", "@type": "Person", "name": p["name"],
          "jobTitle": p["chair"], "email": p["email"],
          "affiliation": {"@type": "Organization", "name": p["university"]},
          "sameAs": [p["faculty"], p["ssrn"]]}
page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(p['name'])}, {esc(p['chair'])} at the McCombs School of Business, The University of Texas at Austin. Working papers, publications, and curriculum vitae.">
  <meta name="theme-color" content="#faf9f6">
  <meta property="og:title" content="Volker Laux | The University of Texas at Austin">
  <meta property="og:description" content="Working papers, publications, and curriculum vitae. {esc(p['chair'])}, McCombs School of Business.">
  <meta property="og:type" content="website">
  <title>Volker Laux | The University of Texas at Austin</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css?v={styles_version}">
  <script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>
  <script defer src="site.js"></script>
  <script defer src="analytics.js"></script>
</head>
<body id="top">
  <a class="skip-link" href="#main">Skip to research</a>
  <div class="page-width site-layout">
  <aside class="profile-panel" aria-label="Profile and navigation">
  <header class="profile-header">
    <div class="profile">
      <img class="portrait" src="{esc(p['photo'])}" alt="{esc(p['name'])}" width="540" height="540" fetchpriority="high">
      <div class="profile-text">
        <h1>{esc(p['name'])}</h1>
        <p class="chair"><strong>{esc(p['chair'])}</strong></p>
        <p class="affiliation"><a href="{esc(p['department_url'])}">{esc(p['department'])}</a><br>
          <a href="https://www.mccombs.utexas.edu/">{esc(p['school'])}</a><br>
          <a href="https://www.utexas.edu/">{esc(p['university'])}</a></p>
        <p class="contact"><a href="mailto:{esc(p['email'], quote=True)}">{esc(p['email'])}</a></p>
        <div class="profile-links">
          <a class="profile-link primary" href="{esc(p['cv'])}">Curriculum vitae <span aria-hidden="true">↗</span></a>
          <a class="profile-link" href="{esc(p['faculty'])}">Faculty profile <span aria-hidden="true">↗</span></a>
          <a class="profile-link" href="{esc(p['ssrn'])}">SSRN <span aria-hidden="true">↗</span></a>
        </div>
      </div>
    </div>
  </header>
  <nav class="section-nav" aria-label="Research sections">
    <div class="nav-inner">
      <a href="#working-papers" aria-current="location">Working papers</a>
      <a href="#publications">Publications</a>
    </div>
  </nav>
  </aside>
  <main id="main">
    <section id="working-papers" class="research-section" aria-labelledby="working-title">
      <div class="section-heading">
        <h2 id="working-title">Working papers</h2>
      </div>
      <ol class="paper-list working-list">
{working}
      </ol>
    </section>
    <section id="publications" class="research-section" aria-labelledby="publications-title">
      <div class="section-heading">
        <h2 id="publications-title">Publications</h2>
      </div>
      <ol class="paper-list publication-list">
{publications}
      </ol>
    </section>
  </main>
  </div>
  <footer class="site-footer">
    <div class="page-width footer-inner">
      <p>Volker Laux <span aria-hidden="true">·</span> McCombs School of Business</p>
      <a href="#top">Back to top <span aria-hidden="true">↑</span></a>
    </div>
  </footer>
</body>
</html>
'''
(ROOT / "index.html").write_text("\n".join(line.rstrip() for line in page.splitlines()) + "\n")
settings = json.dumps(data["analytics"], indent=2)
# Embed configuration so opening the local HTML file never requires a fetch.
(ROOT / "analytics.js").write_text('''/* Existing Google Analytics property. Local previews never send traffic. */
(() => {
  "use strict";
  const settings = ''' + settings + ''';
  const host = window.location.hostname;
  const isPreview = new URLSearchParams(window.location.search).has("preview");
  if (window.location.protocol !== "https:" || isPreview ||
      !settings.production_hosts.includes(host) ||
      !/^G-[A-Z0-9]+$/.test(settings.measurement_id)) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", settings.measurement_id);
  const tag = document.createElement("script");
  tag.async = true;
  tag.src = "https://www.googletagmanager.com/gtag/js?id=" + settings.measurement_id;
  document.head.appendChild(tag);
})();
''')
print(f"Built index.html: {len(data['working_papers'])} working papers, {len(data['publications'])} publications.")
