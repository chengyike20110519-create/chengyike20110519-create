"""Check local image references in the profile README without fetching URLs."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


class ImageReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == 'img' and attributes.get('src'):
            self.urls.append(attributes['src'])
        if tag in {'source', 'img'} and attributes.get('srcset'):
            self.urls.extend(item.strip().split()[0]
                             for item in attributes['srcset'].split(',') if item.strip())


def check(readme):
    text = readme.read_text(encoding='utf-8')
    parser = ImageReferences()
    parser.feed(text)
    parser.urls.extend(re.findall(r'!\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+[^)]*)?\)', text))
    root = readme.parent.resolve()
    checked = set()
    errors = []
    for reference in parser.urls:
        url = urlsplit(reference)
        if url.scheme or url.netloc or not url.path:
            continue
        target = (root / unquote(url.path).lstrip('/')).resolve()
        if target in checked:
            continue
        checked.add(target)
        if not target.is_relative_to(root):
            errors.append(f'Image path escapes the repository: {reference}')
        elif not target.is_file():
            errors.append(f'Missing image: {reference}')
    return len(checked), errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('readme', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'README.md')
    args = parser.parse_args()
    try:
        count, errors = check(args.readme)
    except (OSError, UnicodeError) as error:
        parser.exit(1, f'Cannot read README: {error}\n')
    if errors:
        parser.exit(1, '\n'.join(errors) + '\n')
    print(f'Checked {count} local images; all references exist.')
