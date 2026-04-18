"""Persistence helpers for activity data snapshots."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from src.activity_catalog import build_activity_summary, get_default_activities


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
GENERATED_FILE = DATA_DIR / "activities.generated.json"


def _read_json_file(file_path: Path) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as file_handle:
        payload = json.load(file_handle)

    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {file_path}")

    return payload


def load_activities() -> Dict[str, Dict[str, Any]]:
    """Load the latest generated activity set, or fall back to the defaults."""

    if GENERATED_FILE.exists():
        payload = _read_json_file(GENERATED_FILE)
        activities = payload.get("activities", payload)
        if isinstance(activities, dict):
            return activities

    return get_default_activities()


def build_activity_snapshot(activities: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Create a normalized snapshot with aggregate metrics."""

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": build_activity_summary(activities),
        "activities": activities,
    }


def save_activity_snapshot(activities: Dict[str, Dict[str, Any]], output_path: Path | None = None) -> Path:
    """Persist a normalized activity snapshot to disk."""

    target_path = output_path or GENERATED_FILE
    target_path.parent.mkdir(parents=True, exist_ok=True)

    snapshot = build_activity_snapshot(activities)
    with open(target_path, "w", encoding="utf-8") as file_handle:
        json.dump(snapshot, file_handle, ensure_ascii=False, indent=2)

    return target_path