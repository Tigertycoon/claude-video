"""Subtitle parsing used by URL captions and local sidecars."""
from __future__ import annotations

from pathlib import Path

import transcribe


def test_parse_subrip_sidecar(tmp_path: Path):
    subtitle = tmp_path / "clip.srt"
    subtitle.write_text(
        "1\n"
        "00:00:01,000 --> 00:00:02,500\n"
        "Hello <i>sidecar</i>.\n\n"
        "2\n"
        "00:00:03,000 --> 00:00:04,000\n"
        "Still local.\n\n",
        encoding="utf-8",
    )

    segments = transcribe.parse_subtitle(str(subtitle))

    assert segments == [
        {"start": 1.0, "end": 2.5, "text": "Hello sidecar."},
        {"start": 3.0, "end": 4.0, "text": "Still local."},
    ]


def test_parse_webvtt_without_hour_component(tmp_path: Path):
    subtitle = tmp_path / "clip.vtt"
    subtitle.write_text(
        "WEBVTT\n\n"
        "00:01.000 --> 00:02.000 align:start\n"
        "Short VTT timestamp.\n\n",
        encoding="utf-8",
    )

    segments = transcribe.parse_subtitle(str(subtitle))

    assert segments == [
        {"start": 1.0, "end": 2.0, "text": "Short VTT timestamp."},
    ]
