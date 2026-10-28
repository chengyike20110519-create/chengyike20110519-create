# Profile asset tools

Use Python 3.10 or newer. Run these commands from the repository root:

```sh
python -m pip install -r requirements-profile.txt
python scripts/build_motion_assets.py
```

Use `python3` instead of `python` if that is your system's Python 3 command.

The generator replaces the existing typing GIFs, still PNGs, divider and footer.
It does not create or restore portrait images. Each generated GIF is fully decoded
to check its frames before the command finishes.

## Fonts

The script tries Andale Mono on macOS, Consolas on Windows, then common Linux
monospace fonts. If none can be loaded, it uses Pillow's bundled font.
For consistent typography across machines, supply the same local font file:

```sh
PROFILE_FONT=/path/to/font.ttf python scripts/build_motion_assets.py
```

In Windows PowerShell:

```powershell
$env:PROFILE_FONT = 'C:\Windows\Fonts\consola.ttf'
python scripts/build_motion_assets.py
Remove-Item Env:PROFILE_FONT
```

An invalid explicit font path stops with an error instead of silently changing fonts.

## Verified environments

- macOS, Python 3.13, Pillow 12.3: default generation and bundled-font fallback checked.
- Native Windows and Linux execution still needs a contributor's verification.
