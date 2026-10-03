"""Response types for the GetYouTubeTranscript API.

These are ``TypedDict`` hints only: the client still returns plain dicts.
"""

from __future__ import annotations

from typing import List, TypedDict


class Segment(TypedDict):
    """One caption line, returned in ``segments`` when ``timestamps=True``."""

    start: float  # start time in seconds
    duration: float  # duration in seconds
    text: str


class _TranscriptRequired(TypedDict):
    video_id: str
    language_code: str
    title: str
    author_name: str
    author_url: str
    thumbnail_url: str
    transcript: str
    word_count: int


class TranscriptData(_TranscriptRequired, total=False):
    """Result of :meth:`Client.get_transcript`."""

    segments: List[Segment]  # present only when timestamps=True
