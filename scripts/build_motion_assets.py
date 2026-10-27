from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
ASSETS.mkdir(exist_ok=True)
TOTAL = 18
PHRASES = ['Stay curious. Make it real.', 'From questions to working tools.', 'AI / Mathematical modeling / Web']

def events(text, start):
    count = len(text)
    points = [(0, 0), (start, 0)]
    points += [(start + 1.8 * n / count, n * 12) for n in range(1, count + 1)]
    points.append((start + 4.25, count * 12))
    points += [(start + 4.25 + .65 * n / count, (count - n) * 12) for n in range(1, count + 1)]
    points.append((TOTAL, 0))
    return points

definitions = []
groups = []
for index, text in enumerate(PHRASES):
    start = index * 6 + .25
    points = events(text, start)
    times = ';'.join(f'{time / TOTAL:.6f}' for time, _ in points)
    widths = ';'.join(str(width) for _, width in points)
    cursor = ';'.join(str(width + 7) for _, width in points)
    definitions.append(f'''<clipPath id="line-{index}"><rect x="7" y="0" width="0" height="42"><animate attributeName="width" values="{widths}" keyTimes="{times}" calcMode="discrete" dur="18s" repeatCount="indefinite"/></rect></clipPath>''')
    groups.append(f'''<g class="animated">
  <text x="7" y="29" clip-path="url(#line-{index})">{escape(text)}</text>
  <g opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{start/TOTAL:.6f};{(start+4.9)/TOTAL:.6f};{(start+5.2)/TOTAL:.6f};1" calcMode="discrete" dur="18s" repeatCount="indefinite"/>
    <rect x="7" y="10" width="2" height="22"><animate attributeName="x" values="{cursor}" keyTimes="{times}" calcMode="discrete" dur="18s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.45;.5;1" calcMode="discrete" dur="1s" repeatCount="indefinite"/></rect>
  </g>
</g>''')

typing = f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="42" viewBox="0 0 460 42" role="img" aria-labelledby="title desc">
<title id="title">Stay curious. Make it real.</title>
<desc id="desc">Typing animation cycling through a personal motto, turning questions into tools, and AI, mathematical modeling and web development.</desc>
<style>
text,rect{{fill:#0969da}} text{{font:20px ui-monospace,SFMono-Regular,Consolas,monospace}} .static{{display:none}}
@media(prefers-color-scheme:dark){{text,rect{{fill:#79c0ff}}}}
@media(prefers-reduced-motion:reduce){{.animated{{display:none}}.static{{display:inline}}}}
</style>
<defs>{''.join(definitions)}</defs>
{''.join(groups)}
<text class="static" x="7" y="29">{escape(PHRASES[0])}</text>
</svg>
'''

divider = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="8" viewBox="0 0 1200 8" role="presentation">
<style>@media(prefers-reduced-motion:reduce){.animated{display:none}}</style>
<defs><linearGradient id="pulse"><stop stop-color="#6ca9ff" stop-opacity="0"/><stop offset=".7" stop-color="#6ca9ff" stop-opacity=".55"/><stop offset="1" stop-color="#79c0ff"/></linearGradient></defs>
<rect y="3" width="1200" height="2" rx="1" fill="#6ca9ff" opacity=".22"/>
<g class="animated"><rect x="-180" y="3" width="180" height="2" rx="1" fill="url(#pulse)"><animate attributeName="x" from="-180" to="1200" dur="6s" repeatCount="indefinite"/></rect>
<circle cx="0" cy="4" r="3" fill="#6ca9ff"><animate attributeName="cx" from="0" to="1200" dur="6s" repeatCount="indefinite"/></circle></g>
</svg>
'''

nodes = []
for index, (x, label) in enumerate([(80, 'ASK'), (427, 'BUILD'), (773, 'CHECK'), (1120, 'SHARE')]):
    nodes.append(f'''<g><circle cx="{x}" cy="29" r="6" class="node"/>
<circle class="animated ring" cx="{x}" cy="29" r="7" opacity="0"><animate attributeName="r" values="7;17" dur="2.4s" begin="{index*.6}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".45;0" dur="2.4s" begin="{index*.6}s" repeatCount="indefinite"/></circle>
<text x="{x}" y="66" text-anchor="middle">{label}</text></g>''')

footer = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="86" viewBox="0 0 1200 86" role="img" aria-labelledby="title desc">
<title id="title">Ask. Build. Check. Share.</title><desc id="desc">A gently animated blue light connects four steps in Yike's creative process.</desc>
<style>
:root{{--bg:#f6f8fa;--line:#d0d7de;--ink:#57606a;--accent:#0969da}} text{{font:16px ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:2px;fill:var(--ink)}} .node{{fill:var(--bg);stroke:var(--accent);stroke-width:2}} .ring{{fill:none;stroke:var(--accent);stroke-width:1.5}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0d1117;--line:#30363d;--ink:#a5b4c5;--accent:#79c0ff}}}}
@media(prefers-reduced-motion:reduce){{.animated{{display:none}}}}
</style>
<rect x=".5" y=".5" width="1199" height="85" rx="12" fill="var(--bg)" stroke="var(--line)"/>
<path d="M80 29H1120" stroke="var(--line)" stroke-width="1.5"/>
{''.join(nodes)}
<circle class="animated" r="3.5" fill="var(--accent)"><animateMotion path="M80 29H1120" dur="8s" repeatCount="indefinite"/></circle>
</svg>
'''

for filename, content in [('typing.svg', typing), ('divider.svg', divider), ('footer.svg', footer)]:
    ET.fromstring(content)
    (ASSETS / filename).write_text(content)
    print(filename, len(content.encode()), 'bytes')
