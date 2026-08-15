"""Generate browser locale payloads from data/i18n/<lang>.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "i18n"
OUT = ROOT / "assets" / "js"


def main():
    for source in sorted(SRC.glob("*.json")):
        data = json.loads(source.read_text(encoding="utf-8"))
        lang = data["lang"]
        target = OUT / f"locale.{lang}.generated.js"
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        target.write_text(
            "/* Generated from data/i18n/%s.json — do not edit by hand. */\n"
            "window.NexlunaLocale = %s;\n" % (source.name, payload),
            encoding="utf-8",
        )
        print(f"generated {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
