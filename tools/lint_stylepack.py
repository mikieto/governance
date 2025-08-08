#!/usr/bin/env python3
# Lints docs according to a "style pack" YAML.
# Safe-by-default: prints a JSON report; exits 1 only if style says so.
import argparse, sys, json, re, pathlib, subprocess

try:
  import yaml  # type: ignore
except Exception:
  subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pyyaml"], check=False)
  import yaml  # type: ignore

ROOT = pathlib.Path(__file__).resolve().parents[1]  # repo root (governance/)
DEFAULT_STYLE = ROOT / "policy" / "lint" / "style_book.yaml"

def load_style_pack(path: pathlib.Path) -> dict:
  try:
    with open(path, "r", encoding="utf-8") as f:
      return yaml.safe_load(f) or {}
  except FileNotFoundError:
    print(f"::warning:: style pack not found: {path}")
    return {}

def iter_files(paths):
  exts = {".md", ".qmd", ".mdx"}
  for p in paths:
    pth = pathlib.Path(p)
    if pth.is_file():
      if pth.suffix.lower() in exts:
        yield str(pth)
    elif pth.is_dir():
      for fp in pth.rglob("*"):
        if fp.suffix.lower() in exts:
          yield str(fp)

def load_banned(style: dict) -> set[str]:
  banned: set[str] = set(style.get("banned_phrases", []) or [])
  bf = style.get("banned_phrases_file")
  if bf:
    bfp = pathlib.Path(bf)
    if not bfp.is_absolute():
      bfp = ROOT / bfp
    if bfp.exists():
      for line in bfp.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
          banned.add(s)
  return banned

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--style-pack", required=False, default=str(DEFAULT_STYLE))
  ap.add_argument("--paths", nargs="+", required=True)
  args = ap.parse_args()

  style_path = pathlib.Path(args.style_pack)
  if not style_path.is_absolute():
    style_path = ROOT / style_path
  style = load_style_pack(style_path)

  files = list(iter_files(args.paths))
  banned = load_banned(style)
  violations = []

  for fp in files:
    txt = pathlib.Path(fp).read_text(encoding="utf-8", errors="ignore")
    # 1) banned phrases
    for phrase in banned:
      if phrase and phrase in txt:
        violations.append({"file": fp, "type": "banned_phrase", "detail": phrase})
    # 2) optional: require H1
    if style.get("require_h1", False):
      if not re.search(r"(?m)^\s*#\s+\S+", txt):
        violations.append({"file": fp, "type": "missing_h1"})

  report = {"checked": len(files), "violations": violations}
  print(json.dumps(report, ensure_ascii=False, indent=2))

  if violations and style.get("fail_on_violation", False):
    sys.exit(1)

if __name__ == "__main__":
  main()
