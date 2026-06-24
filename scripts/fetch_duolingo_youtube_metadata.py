"""Collect public Duolingo YouTube short-form metadata with yt-dlp.

This script extracts public metadata only. It does not download videos, access
private analytics, collect ad performance data, or make sales/conversion claims.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

try:
    import yt_dlp
except ImportError as error:
    raise SystemExit(
        "yt-dlp is not installed. Install it with: python -m pip install yt-dlp"
    ) from error


DEFAULT_URLS = ["https://www.youtube.com/@duolingo/shorts"]
MAX_RESULTS = 30
SHORT_FORM_MAX_SECONDS = 180
ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT_DIR / "data" / "duolingo_youtube_shorts.csv"

CSV_COLUMNS = [
    "video_id",
    "title",
    "published_at",
    "video_url",
    "view_count",
    "like_count",
    "comment_count",
    "duration",
    "description",
    "content_pillar",
    "hook_type",
    "engagement_proxy",
]

CONTENT_PILLARS = {
    "Mascot Personality Content": [
        "duo",
        "owl",
        "mascot",
        "lily",
        "zari",
        "eddy",
        "lin",
        "bear",
        "character",
        "bird",
    ],
    "Trend-Jacking / Meme Content": [
        "meme",
        "trend",
        "viral",
        "pov",
        "when you",
        "me when",
        "sound",
        "relatable",
        "challenge",
    ],
    "Language Learning Reminder Content": [
        "streak",
        "practice",
        "lesson",
        "study",
        "reminder",
        "learn",
        "language",
        "spanish",
        "french",
        "japanese",
        "english",
    ],
    "Product Feature / App Usage Content": [
        "app",
        "feature",
        "course",
        "duolingo max",
        "super duolingo",
        "music",
        "math",
        "english test",
        "score",
        "xp",
    ],
    "Community Interaction Content": [
        "comment",
        "reply",
        "asked",
        "fan",
        "community",
        "users",
        "followers",
        "tag",
        "stitch",
        "duet",
    ],
}

HOOK_TYPES = {
    "Humor": [
        "funny",
        "joke",
        "lol",
        "comedy",
        "chaos",
        "unhinged",
        "threat",
    ],
    "Meme / Trend": [
        "meme",
        "trend",
        "viral",
        "pov",
        "when you",
        "me when",
        "sound",
        "challenge",
    ],
    "Character-driven": [
        "duo",
        "owl",
        "mascot",
        "lily",
        "zari",
        "eddy",
        "lin",
        "character",
        "bird",
    ],
    "Product Reminder": [
        "streak",
        "lesson",
        "practice",
        "app",
        "duolingo",
        "reminder",
        "xp",
    ],
    "Educational": [
        "learn",
        "how to",
        "tips",
        "language",
        "spanish",
        "french",
        "japanese",
        "english",
        "grammar",
        "vocab",
    ],
}


def main() -> None:
    urls = sys.argv[1:] or DEFAULT_URLS
    rows = collect_metadata(urls)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows[:MAX_RESULTS])

    print(f"Saved {min(len(rows), MAX_RESULTS)} rows to {OUTPUT_PATH}")


def collect_metadata(urls: list[str]) -> list[dict[str, str]]:
    """Extract public video metadata from channel tabs or video URLs."""

    ydl_options = {
        "extract_flat": False,
        "ignoreerrors": True,
        "playlistend": 80,
        "quiet": True,
        "skip_download": True,
    }
    rows: list[dict[str, str]] = []
    seen_video_ids: set[str] = set()

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        for url in urls:
            info = ydl.extract_info(url, download=False)
            for video in iter_videos(info):
                if len(rows) >= MAX_RESULTS:
                    return rows

                video_id = str(video.get("id") or "")
                if not video_id or video_id in seen_video_ids:
                    continue

                if not appears_to_be_short(video, source_url=url):
                    continue

                seen_video_ids.add(video_id)
                rows.append(build_row(video))

    return rows


def iter_videos(info: dict | None):
    """Yield video dictionaries from either a single video or playlist result."""

    if not info:
        return

    entries = info.get("entries")
    if entries is None:
        yield info
        return

    for entry in entries:
        if not entry:
            continue
        nested_entries = entry.get("entries") if isinstance(entry, dict) else None
        if nested_entries:
            yield from iter_videos(entry)
        else:
            yield entry


def build_row(video: dict) -> dict[str, str]:
    title = clean_text(video.get("title"))
    description = clean_text(video.get("description"))
    video_id = str(video.get("id") or "")
    view_count = parse_int(video.get("view_count"))
    like_count = parse_int(video.get("like_count"))
    comment_count = parse_int(video.get("comment_count"))
    duration = parse_int(video.get("duration"))
    text = f"{title} {description}"

    return {
        "video_id": video_id,
        "title": title,
        "published_at": format_published_at(video),
        "video_url": canonical_video_url(video, video_id),
        "view_count": blank_if_none(view_count),
        "like_count": blank_if_none(like_count),
        "comment_count": blank_if_none(comment_count),
        "duration": blank_if_none(duration),
        "description": description,
        "content_pillar": classify_text(text, CONTENT_PILLARS, "Other"),
        "hook_type": classify_text(text, HOOK_TYPES, "Other"),
        "engagement_proxy": calculate_engagement_proxy(like_count, comment_count, view_count),
    }


def appears_to_be_short(video: dict, source_url: str) -> bool:
    title = clean_text(video.get("title")).lower()
    description = clean_text(video.get("description")).lower()
    webpage_url = clean_text(video.get("webpage_url")).lower()
    original_url = clean_text(video.get("original_url")).lower()
    source = source_url.lower()
    duration = parse_int(video.get("duration"))
    combined_text = f"{title} {description} {webpage_url} {original_url} {source}"
    short_markers = ["/shorts/", "#shorts", "youtube shorts", "shorts", "short-form"]

    if any(marker in combined_text for marker in short_markers):
        return True

    return duration is not None and 0 < duration <= SHORT_FORM_MAX_SECONDS


def classify_text(text: str, categories: dict[str, list[str]], fallback: str) -> str:
    normalized = text.lower()
    best_category = fallback
    best_score = 0

    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in normalized)
        if score > best_score:
            best_category = category
            best_score = score

    return best_category


def calculate_engagement_proxy(
    like_count: int | None, comment_count: int | None, view_count: int | None
) -> str:
    if not view_count:
        return ""

    likes = like_count or 0
    comments = comment_count or 0
    return f"{(likes + comments) / view_count:.6f}"


def format_published_at(video: dict) -> str:
    upload_date = clean_text(video.get("upload_date"))
    if re.fullmatch(r"\d{8}", upload_date):
        return f"{upload_date[0:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    timestamp = parse_int(video.get("timestamp"))
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()

    release_timestamp = parse_int(video.get("release_timestamp"))
    if release_timestamp:
        return datetime.fromtimestamp(release_timestamp, tz=timezone.utc).date().isoformat()

    return ""


def canonical_video_url(video: dict, video_id: str) -> str:
    webpage_url = clean_text(video.get("webpage_url"))
    if "/shorts/" in webpage_url:
        return webpage_url
    if video_id:
        return f"https://www.youtube.com/shorts/{video_id}"
    return webpage_url


def parse_int(value) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def blank_if_none(value: int | None) -> str:
    return "" if value is None else str(value)


def clean_text(value) -> str:
    if value is None:
        return ""
    return str(value).replace("\r", " ").replace("\n", " ").strip()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Canceled.")
