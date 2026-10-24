# SamuelArther/homebrew-tap

Formulae for my own tools, for Homebrew on macOS and Linux and for [brew-windows](https://github.com/SamuelArther/brew-windows) (Homebrew for Windows).

```
brew install samuelarther/tap/fetchart
```

Or tap it first, then install by name:

```
brew tap samuelarther/tap
brew install fetchart
```

| Formula | What it is |
|---|---|
| [fetchart](https://github.com/SamuelArther/fetchart) | Download game art, achievements, posters, album covers and more from the command line |
| [fetchamiibo](https://github.com/SamuelArther/fetchamiibo) | Download amiibo NFC dumps for a Flipper Zero, by name or by game and letter |

Taps and formulae work the way [Homebrew](https://brew.sh) defines them.

`fetchart` is bumped automatically: `.github/workflows/bump.yml` runs every few hours, and once a new release has both its PyPI sdist and its GitHub release exe, `scripts/bump_fetchart.py` rewrites the formula, commits it, and runs the tests.
