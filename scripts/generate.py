#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.micro from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]

# micro group -> (fg role, bg role, attribute). For cursor-line and
# color-column, micro paints the foreground color as the line background.
GROUPS = {
    "default": ("ui.fg", "ui.bg", ""),
    "comment": ("syn.comment", None, "italic"),
    "identifier": ("syn.identifier", None, ""),
    "identifier.class": ("syn.type", None, ""),
    "identifier.var": ("syn.identifier", None, ""),
    "constant": ("syn.constant", None, ""),
    "constant.number": ("syn.number", None, ""),
    "constant.string": ("syn.string", None, ""),
    "constant.specialChar": ("syn.regex", None, ""),
    "symbol": ("syn.operator", None, ""),
    "symbol.brackets": ("syn.punct", None, ""),
    "symbol.tag": ("syn.fun", None, ""),
    "type": ("syn.type", None, ""),
    "type.keyword": ("syn.keyword", None, ""),
    "special": ("syn.special1", None, ""),
    "statement": ("syn.statement", None, ""),
    "preproc": ("syn.preproc", None, ""),
    "underlined": ("syn.special1", None, "underline"),
    "error": ("diag.error", None, "bold"),
    "todo": ("diag.warning", None, "bold"),
    "diff-added": ("vcs.added", None, ""),
    "diff-modified": ("vcs.changed", None, ""),
    "diff-deleted": ("vcs.removed", None, ""),
    "gutter-error": ("diag.error", None, ""),
    "gutter-warning": ("diag.warning", None, ""),
    "statusline": ("ui.fg_dim", "ui.bg_m3", ""),
    "tabbar": ("ui.fg_dim", "ui.bg_m3", ""),
    "indent-char": ("ui.whitespace", None, ""),
    "line-number": ("ui.nontext", None, ""),
    "current-line-number": ("diag.warning", None, "bold"),
    "cursor-line": ("ui.bg_p2", None, ""),
    "color-column": ("ui.bg_p1", None, ""),
}


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}


def theme(variant, colors):
    out = [f"# Kanagawa {variant.capitalize()}", "# https://github.com/kanagawa-community/micro", ""]
    for group, (fg, bg, attr) in GROUPS.items():
        value = ",".join(colors[r] for r in (fg, bg) if r)
        out.append(f'color-link {group} "{attr + " " if attr else ""}{value}"')
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.micro"
        out.parent.mkdir(exist_ok=True)
        out.write_text(theme(v, roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
