from pathlib import Path
import os
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
ASSETS.mkdir(exist_ok=True)
PHRASES = ['Stay curious. Make it real.', 'From questions to working tools.', 'AI / Mathematical modeling / Web']

# Each GIF frame is flattened from a single text string, so unsupported SVG
# clipping or animation cannot reveal several overlapping slogans.
from PIL import Image, ImageDraw, ImageFont

def load_font():
    override = os.environ.get('PROFILE_FONT')
    if override:
        try:
            return ImageFont.truetype(override, 40)
        except OSError as error:
            raise SystemExit(f'Cannot load PROFILE_FONT: {override}') from error

    candidates = [
        '/System/Library/Fonts/Supplemental/Andale Mono.ttf',
        str(Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts' / 'consola.ttf'),
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf',
        'DejaVuSansMono.ttf',
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, 40)
        except OSError:
            continue
    return ImageFont.load_default(size=40)


FONT = load_font()
SIZE = (920, 84)
THEMES = {'light': ('#ffffff', '#0969da'), 'dark': ('#0d1117', '#79c0ff')}

def draw_frame(text, background, ink, cursor=True):
    frame = Image.new('RGB', SIZE, background)
    draw = ImageDraw.Draw(frame)
    draw.text((14, 58), text, font=FONT, fill=ink, anchor='ls')
    x = round(14 + draw.textlength(text, font=FONT))
    assert x + 6 < SIZE[0], 'Slogan exceeds available space'
    if cursor:
        draw.rectangle((x + 3, 20, x + 6, 63), fill=ink)
    return frame

# Start with a readable full slogan. During transitions only one prefix is drawn.
sequence = []
for index, phrase in enumerate(PHRASES):
    if index:
        sequence.extend((phrase[:n], 60, True) for n in range(1, len(phrase) + 1))
    for _ in range(3):
        sequence.extend([(phrase, 350, True), (phrase, 350, False)])
    sequence.extend((phrase[:n], 30, True) for n in range(len(phrase) - 1, -1, -1))
sequence.extend((PHRASES[0][:n], 60, True) for n in range(1, len(PHRASES[0])))

for theme, (background, ink) in THEMES.items():
    frames = [draw_frame(text, background, ink, cursor) for text, _, cursor in sequence]
    path = ASSETS / f'typing-{theme}.gif'
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=[duration for _, duration, _ in sequence],
                   loop=0, disposal=2, optimize=True)
    draw_frame(PHRASES[0], background, ink, cursor=False).save(ASSETS / f'typing-{theme}.png')
    with Image.open(path) as check:
        assert check.n_frames > 100 and check.size == SIZE
        for frame in range(check.n_frames):
            check.seek(frame)
            check.convert('RGB').load()
    print(path.name, path.stat().st_size, 'bytes')
(ASSETS / 'typing.svg').unlink(missing_ok=True)

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

for filename, content in [('divider.svg', divider), ('footer.svg', footer)]:
    ET.fromstring(content)
    (ASSETS / filename).write_text(content)
    print(filename, len(content.encode()), 'bytes')
