"""Interview helpers: schedule, list upcoming, .ics export, launch reminder."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from .config import DATA_DIR
from .storage import get_conn


def schedule_interview(application_id: int, when: datetime, kind: str, link: str = "", notes: str = "") -> None:
    conn = get_conn()
    with conn:
        conn.execute(
            "INSERT INTO interviews (application_id, scheduled_at, kind, link, notes) VALUES (?, ?, ?, ?, ?)",
            (application_id, when.isoformat(timespec="minutes"), kind, link, notes),
        )
        conn.execute("UPDATE applications SET status='interview_scheduled' WHERE id=?", (application_id,))
    conn.close()


def upcoming_interviews(within_hours: int = 48) -> list[dict]:
    conn = get_conn()
    now = datetime.now()
    horizon = now + timedelta(hours=within_hours)
    rows = conn.execute(
        """SELECT i.id, i.scheduled_at, i.kind, i.link, i.notes, j.title, j.company
           FROM interviews i
           JOIN applications a ON a.id = i.application_id
           LEFT JOIN jobs j ON j.id = a.job_id
           WHERE i.scheduled_at >= ? AND i.scheduled_at <= ?
           ORDER BY i.scheduled_at""",
        (now.isoformat(timespec="minutes"), horizon.isoformat(timespec="minutes")),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def export_ics(out_path: Path | None = None) -> Path:
    out_path = out_path or (DATA_DIR / "interviews.ics")
    conn = get_conn()
    rows = conn.execute(
        """SELECT i.scheduled_at, i.kind, i.link, i.notes, j.title, j.company
           FROM interviews i
           JOIN applications a ON a.id = i.application_id
           LEFT JOIN jobs j ON j.id = a.job_id
           ORDER BY i.scheduled_at"""
    ).fetchall()
    conn.close()
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//JobAssistant//EN"]
    for r in rows:
        try:
            dt = datetime.fromisoformat(r["scheduled_at"])
        except ValueError:
            continue
        stamp = dt.strftime("%Y%m%dT%H%M%S")
        title = f"{r['kind']} interview — {r['title']} @ {r['company']}"
        lines += [
            "BEGIN:VEVENT",
            f"DTSTART:{stamp}",
            f"DTEND:{(dt + timedelta(minutes=45)).strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{r['notes'] or ''} {r['link'] or ''}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\r\n".join(lines), encoding="utf-8")
    return out_path


def reminder_text() -> str:
    upcoming = upcoming_interviews(within_hours=24)
    if not upcoming:
        return ""
    lines = ["Upcoming interviews (next 24h):"]
    for r in upcoming:
        lines.append(f"• {r['scheduled_at']} — {r['title']} @ {r['company']} ({r['kind']})")
    return "\n".join(lines)
