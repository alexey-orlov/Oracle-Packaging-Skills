#!/usr/bin/env python3
"""install_fonts.py — put the practice's brand fonts on this machine, for the current user.

    shared/tools/py shared/tools/install_fonts.py            # install what is not there yet
    shared/tools/py shared/tools/install_fonts.py --check    # report only, exit 1 when any is missing
    shared/tools/py shared/tools/install_fonts.py --from <dir>

The fonts ship in the oracle-packs plugin at `<plugin root>/fonts/` (licensed to the practice;
see the README there). This copies them into the per-user font folder:

    macOS    ~/Library/Fonts
    Windows  %LOCALAPPDATA%\\Microsoft\\Windows\\Fonts, registered under
             HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts (no admin rights needed)
    Linux    ~/.local/share/fonts, then `fc-cache -f` when fontconfig is present

Nothing system-wide is touched. Installing changes only what a render shows: the builders'
text-fit estimate reads the files from the plugin folder directly, so fit is exact without it.

Exit 0 installed or already present · 1 --check found a face missing · 2 no fonts folder.
Standard library only.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

FACES = {
    "Azurio-Regular.otf": "Azurio",
    "Azurio-Semibold.otf": "Azurio Semibold",
    "ReplicaLLTT-Regular.ttf": "Replica LL TT",
    "ReplicaLLTT-Bold.ttf": "Replica LL TT Bold",
}

HERE = Path(__file__).resolve().parent


def shipped_dir(override: str | None) -> Path | None:
    """The plugin's fonts folder: <plugin root>/fonts, two levels above shared/tools."""
    candidates = [Path(override)] if override else []
    root = HERE.parents[1]
    candidates += [root / "fonts", root / "plugins" / "oracle-packs" / "fonts"]
    for c in candidates:
        if c.is_dir() and any((c / name).is_file() for name in FACES):
            return c
    # A folder that exists but holds no files yet (the files are added by hand): still a
    # place to report against, so --check can say what is installed and what is not.
    for c in candidates:
        if c.is_dir():
            return c
    return None


def user_font_dir() -> Path:
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Fonts"
    if sys.platform.startswith("win"):
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / "Microsoft" / "Windows" / "Fonts"
    return Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share") / "fonts"


def already_installed(name: str, target: Path) -> bool:
    """Present in the user folder, or (macOS) in the managed system set the practice pushes."""
    if (target / name).is_file():
        return True
    stem = Path(name).stem
    roots = [target]
    if sys.platform == "darwin":
        roots += [Path("/Library/Fonts/Managed"), Path("/Library/Fonts")]
    for root in roots:
        if root.is_dir() and any(p.name.startswith(stem) for p in root.iterdir()):
            return True
    return False


def register_windows(path: Path, face: str) -> None:
    import winreg  # Windows only

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows NT\CurrentVersion\Fonts", 0, winreg.KEY_SET_VALUE)
    kind = "OpenType" if path.suffix.lower() == ".otf" else "TrueType"
    winreg.SetValueEx(key, f"{face} ({kind})", 0, winreg.REG_SZ, str(path))
    winreg.CloseKey(key)


def main() -> int:
    ap = argparse.ArgumentParser(description="Install the practice's brand fonts for the current user.")
    ap.add_argument("--from", dest="src", help="folder holding the font files (default: the plugin's fonts/)")
    ap.add_argument("--check", action="store_true", help="report only; exit 1 when a face is missing")
    args = ap.parse_args()

    src = shipped_dir(args.src)
    if src is None:
        print("install_fonts: no fonts folder found — the oracle-packs plugin ships them at "
              "<plugin root>/fonts/; pass --from <dir> to point at a copy.", file=sys.stderr)
        return 2
    target = user_font_dir()
    missing, installed = [], []
    for name, face in FACES.items():
        if already_installed(name, target):
            continue
        if not (src / name).is_file():
            missing.append(f"{face}: {name} is not in {src}")
            continue
        if args.check:
            missing.append(f"{face}: not installed")
            continue
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / name, target / name)
        if sys.platform.startswith("win"):
            try:
                register_windows(target / name, face)
            except Exception as exc:  # noqa: BLE001 — the copy is done; say what is left
                print(f"install_fonts: copied {name} but could not register it ({exc}); "
                      f"double-click the file in {target} once.", file=sys.stderr)
        installed.append(face)
    if installed and not sys.platform.startswith("win") and sys.platform != "darwin" and shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f"], capture_output=True)
    for line in missing:
        print("install_fonts: " + line, file=sys.stderr)
    if args.check:
        print("install_fonts: " + ("every face is installed" if not missing else f"{len(missing)} face(s) missing"))
        return 1 if missing else 0
    print("install_fonts: " + (f"installed {', '.join(installed)} into {target}" if installed
                               else "every face was already installed"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
