"""Download all AoC puzzle inputs. Requires: pip install advent-of-code-data
Set AOC_SESSION env var to your adventofcode.com session cookie."""

from aocd import get_data
from pathlib import Path

for year in range(2018, 2021):
    for day in range(1, 26):
        out = Path(f"inputs/{year}/day{day:02d}.txt")
        if out.exists():
            continue
        try:
            data = get_data(year=year, day=day)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(data)
            print(f"✓ {year} day {day}")
        except Exception as e:
            print(f"✗ {year} day {day}: {e}")
