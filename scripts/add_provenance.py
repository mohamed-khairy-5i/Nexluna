#!/usr/bin/env python3
"""Add reviewed provenance metadata to the canonical Nexluna units source."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "units.json"
REVIEWED = "2026-08-15"
NIST = "https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors"
FEDDAN = "https://en.wikipedia.org/wiki/Feddan"

CATEGORY_META = {
    "length": ("SI-derived and customary length units", "international", "NIST SP 811 Appendix B; factors expressed against metre."),
    "weight": ("SI-derived and customary mass units", "international", "NIST SP 811 Appendix B; factors expressed against kilogram."),
    "area": ("SI-derived, customary, and Egyptian land-area units", "international / Egypt", "NIST SP 811 for international factors; Egyptian land-unit note below."),
    "volume": ("SI-derived and customary volume units", "international / US / UK", "NIST SP 811 and exact US/UK customary definitions."),
    "temperature": ("temperature scales", "international", "Exact Celsius, Fahrenheit, and Kelvin scale relations."),
    "data": ("decimal and IEC binary information units", "international", "Decimal factors are powers of 1000; binary factors are powers of 1024."),
    "speed": ("derived speed units", "international", "Factors are derived from exact length and time definitions."),
    "time": ("SI-derived and calendar-duration units", "international", "SI seconds for fixed durations; month/year are stated average durations."),
    "pressure": ("SI-derived and customary pressure units", "international", "NIST SP 811 Appendix B; factors expressed against pascal."),
    "energy": ("SI-derived and customary energy units", "international", "NIST SP 811 Appendix B; factors expressed against joule."),
    "power": ("SI-derived and customary power units", "international", "NIST SP 811 Appendix B; factors expressed against watt."),
    "angle": ("SI-derived and plane-angle units", "international", "Exact degree/radian relationships and named angular subdivisions."),
    "fuel": ("fuel economy units", "international / US / UK", "Derived from exact kilometre, mile, litre, US gallon, and UK gallon definitions."),
    "frequency": ("SI-derived frequency units", "international", "Factors expressed against hertz; rpm is cycles per minute."),
}

LOCAL_OVERRIDES = {
    ("area", "feddan"): ("Egyptian land area", "Egypt", "Egyptian feddan is treated as 4,200.833 m²; it is divided into 24 kirat.", FEDDAN),
    ("area", "kirat"): ("Egyptian land area", "Egypt", "Egyptian land kirat is 1/24 of a feddan, approximately 175.0347083333 m².", FEDDAN),
    ("area", "sahm"): ("Egyptian land area", "Egypt", "Egyptian land sahm is 1/24 of a kirat, approximately 7.2931128472 m².", FEDDAN),
    ("area", "dunam"): ("metric land area", "Levant / regional usage", "This dataset uses the metric dunam definition of exactly 1,000 m²; regional usage can vary and should be stated.", NIST),
    ("volume", "gal"): ("US customary volume", "United States", "US liquid gallon: exactly 3.785411784 litres.", NIST),
    ("volume", "galUK"): ("Imperial volume", "United Kingdom", "Imperial gallon: exactly 4.54609 litres.", NIST),
    ("fuel", "mpg"): ("US customary fuel economy", "United States", "Miles per US liquid gallon; converted through exact mile and gallon definitions.", NIST),
    ("fuel", "mpgUK"): ("Imperial fuel economy", "United Kingdom", "Miles per Imperial gallon; converted through exact mile and gallon definitions.", NIST),
}


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    for category, definition in data.items():
        system, region, notes = CATEGORY_META[category]
        definition["provenance"] = {
            "schema_version": "1.0",
            "system": system,
            "region": region,
            "source": NIST,
            "reviewed": REVIEWED,
            "notes": notes,
        }
        unit_provenance = {}
        for unit_id, unit_label in definition["units"]:
            unit_system, unit_region, unit_definition, source = LOCAL_OVERRIDES.get(
                (category, unit_id),
                (system, region, f"{unit_label}; factor is maintained in the canonical base table for {category}.", NIST),
            )
            unit_provenance[unit_id] = {
                "system": unit_system,
                "region": unit_region,
                "definition": unit_definition,
                "source": source,
                "reviewed": REVIEWED,
            }
        definition["unit_provenance"] = unit_provenance
    SOURCE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated provenance for {len(data)} categories and {sum(len(d['units']) for d in data.values())} units")


if __name__ == "__main__":
    main()

# Notes:
# - The Egyptian feddan source is a secondary reference and should be verified
#   against a local metrology authority before any legal/financial use.
# - Provenance documents definitions; it does not replace the deterministic
#   converter or imply that regional variants are interchangeable.
