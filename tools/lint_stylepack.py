#!/usr/bin/env python3
import argparse, sys, yaml, pathlib, re

def iter_files(root, exts=(".md",)):
    for p in pathlib.Path(root).rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            yield p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--style-pack", required=True, help="Path to style pack YAML")
    ap.add_argument("--paths", nargs="+", default=["docs","generated"])
    args = ap.parse_args()

    pack = yaml.safe_load(open(args.style_pack, "r", encoding="utf-8"))
    banned = pack.get("banned_phrases", [])
    if not banned:
        print("No banned phrases configured.")
        return 0
    banned_re = re.compile("|".join(re.escape(x) for x in banned))
    violations = []
    for path in args.paths:
        for f in iter_files(path):
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if banned_re.search(line):
                    violations.append(f"{f}:{i}: banned phrase")
    if violations:
        print("
".join(violations))
        print(f"Found {len(violations)} violations from style pack '{pack.get('id')}'.", file=sys.stderr)
        return 1
    print(f"No style-pack violations ({pack.get('id')}).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
