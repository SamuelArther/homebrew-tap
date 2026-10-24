#!/usr/bin/env python3
"""Bump Formula/fetchart.rb to the latest fetchart release.

The formula is only bumped once BOTH the PyPI sdist (macOS/Linux) and the
GitHub release exe (brew-windows) exist for the new version. Every url and
sha256 in the formula is rewritten.

Usage:
    bump_fetchart.py [FORMULA] [--version X.Y.Z] [--dry-run]

Writes `bumped=true|false` and `version=...` to $GITHUB_OUTPUT when set.
Uses $GH_TOKEN / $GITHUB_TOKEN for the GitHub API when available.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

REPO = "SamuelArther/fetchart"
PACKAGE = "fetchart"
EXE_ASSET = "fetchart-windows.exe"

URL_RE = re.compile(r'^(\s*)url "([^"]+)"')
SHA_RE = re.compile(r'^(\s*)sha256 "([0-9a-f]{64})"')
EXE_URL_RE = re.compile(r"^https://github\.com/[^/]+/[^/]+/releases/download/v([^/]+)/" + re.escape(EXE_ASSET) + "$")
SDIST_URL_RE = re.compile(r"^https://files\.pythonhosted\.org/packages/.+/" + re.escape(PACKAGE) + r"-([^/]+)\.tar\.gz$")


def http_get(url, accept=None, auth=False):
    req = urllib.request.Request(url, headers={"User-Agent": "homebrew-tap-bump"})
    if accept:
        req.add_header("Accept", accept)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if auth and token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def get_json(url, auth=False):
    try:
        return json.loads(http_get(url, "application/json", auth))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def vtuple(v):
    return tuple(int(p) if p.isdigit() else p for p in re.split(r"[.\-]", v))


def latest_github_version():
    rel = get_json(f"https://api.github.com/repos/{REPO}/releases/latest", auth=True)
    if not rel:
        return None
    return rel["tag_name"].lstrip("v")


def release_exe(version):
    """Return (url, sha256) of the release exe, or None if it isn't published yet."""
    rel = get_json(f"https://api.github.com/repos/{REPO}/releases/tags/v{version}", auth=True)
    if not rel:
        return None
    for asset in rel.get("assets", []):
        if asset["name"] == EXE_ASSET and asset.get("state", "uploaded") == "uploaded":
            url = asset["browser_download_url"]
            digest = asset.get("digest") or ""
            if digest.startswith("sha256:"):
                return url, digest.split(":", 1)[1]
            return url, hashlib.sha256(http_get(url)).hexdigest()
    return None


def pypi_sdist(version):
    """Return (url, sha256) of the PyPI sdist, or None if it isn't published yet."""
    data = get_json(f"https://pypi.org/pypi/{PACKAGE}/{version}/json")
    if not data:
        return None
    for f in data.get("urls", []):
        if f["packagetype"] == "sdist" and not f.get("yanked"):
            return f["url"], f["digests"]["sha256"]
    return None


def current_version(text):
    for line in text.splitlines():
        m = URL_RE.match(line)
        if m:
            u = EXE_URL_RE.match(m.group(2))
            if u:
                return u.group(1)
    raise SystemExit("could not find the release exe url in the formula")


def rewrite(text, exe, sdist):
    """Replace every url and the sha256 that follows it. Fails loudly on an unexpected layout."""
    lines = text.splitlines(keepends=True)
    pending = None  # sha256 expected for the next sha256 line
    counts = {"exe": 0, "sdist": 0}
    for i, line in enumerate(lines):
        m = URL_RE.match(line)
        if m:
            if pending:
                raise SystemExit(f"line {i + 1}: url without a following sha256")
            indent, url = m.groups()
            if EXE_URL_RE.match(url):
                kind, (new_url, new_sha) = "exe", exe
            elif SDIST_URL_RE.match(url):
                kind, (new_url, new_sha) = "sdist", sdist
            else:
                # Other urls (e.g. livecheck) carry no sha256 and are left alone.
                continue
            counts[kind] += 1
            lines[i] = line.replace(f'url "{url}"', f'url "{new_url}"', 1)
            pending = new_sha
            continue
        m = SHA_RE.match(line)
        if m and pending:
            lines[i] = line.replace(m.group(2), pending, 1)
            pending = None
    if pending:
        raise SystemExit("url without a following sha256 at end of file")
    if counts["exe"] != 1 or counts["sdist"] < 1:
        raise SystemExit(f"unexpected formula layout: {counts}")
    return "".join(lines)


def set_output(**kw):
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            for k, v in kw.items():
                f.write(f"{k}={v}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("formula", nargs="?", default="Formula/fetchart.rb")
    ap.add_argument("--version", help="target version (default: latest GitHub release)")
    ap.add_argument("--dry-run", action="store_true", help="print the new formula instead of writing it")
    args = ap.parse_args()

    with open(args.formula, encoding="utf-8", newline="") as f:
        text = f.read()
    cur = current_version(text)
    target = args.version or latest_github_version()
    print(f"formula: {cur}  latest release: {target}")

    if not target or vtuple(target) <= vtuple(cur):
        print("up to date")
        set_output(bumped="false", version=cur)
        return 0

    exe = release_exe(target)
    sdist = pypi_sdist(target)
    if not exe or not sdist:
        print(f"{target} not fully published yet (exe: {bool(exe)}, sdist: {bool(sdist)}); skipping")
        set_output(bumped="false", version=cur)
        return 0

    new = rewrite(text, exe, sdist)
    if args.dry_run:
        sys.stdout.write(new)
    else:
        with open(args.formula, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print(f"bumped {cur} -> {target}")
    print(f"  exe:   {exe[0]} {exe[1]}")
    print(f"  sdist: {sdist[0]} {sdist[1]}")
    set_output(bumped="true", version=target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
