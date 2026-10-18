from html.parser import HTMLParser
from pathlib import Path
class Checker(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=set();self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='a' and a.get('href','').startswith('#'):self.links.append(a['href'][1:])
c=Checker();c.feed(Path('index.html').read_text());missing=[x for x in c.links if x not in c.ids]
if missing:raise SystemExit('Broken anchors: '+', '.join(missing))
print('All internal anchors resolve: '+str(len(c.links)))
