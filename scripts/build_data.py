"""Build a normalized activity snapshot from the default catalog."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running the script directly from the repository root.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.activity_catalog import build_activity_summary, get_default_activities
from src.data_store import save_activity_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the generated extracurricular activity snapshot"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("data/activities.generated.json"),
        help="Path to write the generated snapshot",
    )
    args = parser.parse_args()

    activities = get_default_activities()
    summary = build_activity_summary(activities)
    output_path = save_activity_snapshot(activities, args.output)

    print("Activity snapshot built successfully")
    print(f"Output: {output_path}")
    print(f"Activities: {summary['activity_count']}")
    print(f"Participants: {summary['participant_count']}")
    print(f"Capacity: {summary['capacity_total']}")
    print(f"Spots left: {summary['spots_left']}")
    print(f"Full activities: {summary['full_activities']}")


if __name__ == "__main__":
    main()