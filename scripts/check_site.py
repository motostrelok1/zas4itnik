from pathlib import Path
from html.parser import HTMLParser
import re

html=Path("index.html").read_text()
js=Path("template.js").read_text()
css=Path("template.css").read_text()
class Html(HTMLParser):
    def __init__(self):
        super().__init__(); self.scripts=[]; self.styles=[]; self.ids=set()
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get("id"): self.ids.add(d["id"])
        if tag=="script" and d.get("src"): self.scripts.append(d["src"])
        if tag=="link" and d.get("rel")=="stylesheet": self.styles.append(d.get("href"))
p=Html();p.feed(html)
assert "app" in p.ids, "Missing app mount"
assert "./template.js" in p.scripts, "Missing app script"
assert "./template.css" in p.styles, "Missing stylesheet"
for required in ["hero","facts","cards","stages","catalog","groups","details","faq"]:
    assert f"id=\"{required}\"" in js, f"Missing section {required}"
for required in ["catalog-grid","show-more","bindTabs","aria-selected"]:
    assert required in js, f"Missing interaction {required}"
assert not re.search(r"<form\b|<img\b|<video\b",html+js,re.I), "Unexpected application form or image/video"
assert "@media" in css, "Missing responsive styling"
print("Root page, section coverage, adaptive CSS and interactions: OK")
