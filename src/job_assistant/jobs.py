"""Job fetching from Adzuna and JSearch, with dedupe into SQLite."""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass

import httpx

from .config import Settings
from .storage import get_conn

log = logging.getLogger(__name__)

ADZUNA_URL = "https://api.adzuna.com/v1/api/jobs/us/search/{page}"
JSEARCH_URL = "https://api.openwebninja.com/jsearch/search-v2"


@dataclass
class Job:
    id: str
    title: str
    company: str
    location: str
    salary: str
    description: str
    url: str
    source: str


def _job_id(source: str, raw_id: str) -> str:
    return hashlib.sha1(f"{source}:{raw_id}".encode()).hexdigest()[:16]


def _location_params(settings: Settings) -> dict:
    if settings.location_mode == "remote":
        return {"what": "remote "}
    if settings.location_mode == "specific" and settings.location:
        return {"where": settings.location}
    return {}


def fetch_adzuna(settings: Settings, keywords: str, count: int = 20) -> list[Job]:
    if not (settings.adzuna_app_id and settings.adzuna_app_key):
        log.warning("Adzuna credentials missing; skipping")
        return []
    params = {
        "app_id": settings.adzuna_app_id,
        "app_key": settings.adzuna_app_key,
        "what": keywords,
        "results_per_page": min(count, 50),
        "content-type": "application/json",
    }
    if settings.location_mode == "specific" and settings.location:
        params["where"] = settings.location
    if settings.location_mode == "remote":
        params["what"] = f"{keywords} remote"

    try:
        r = httpx.get(ADZUNA_URL.format(page=1), params=params, timeout=30)
        r.raise_for_status()
        results = r.json().get("results", [])
    except httpx.HTTPError as e:
        log.error("Adzuna fetch failed: %s", e)
        return []

    jobs = []
    for j in results:
        salary = ""
        if j.get("salary_min") and j.get("salary_max"):
            salary = f"${j['salary_min']:,.0f} - ${j['salary_max']:,.0f}"
        jobs.append(Job(
            id=_job_id("adzuna", str(j.get("id", ""))),
            title=j.get("title", ""),
            company=j.get("company", {}).get("display_name", ""),
            location=j.get("location", {}).get("display_name", ""),
            salary=salary,
            description=j.get("description", ""),
            url=j.get("redirect_url", ""),
            source="adzuna",
        ))
    return jobs


def fetch_jsearch(settings: Settings, keywords: str, count: int = 20) -> list[Job]:
    if not settings.jsearch_api_key:
        log.warning("JSearch API key missing; skipping")
        return []
    query = keywords
    if settings.location_mode == "remote":
        query += " remote"
    elif settings.location_mode == "specific" and settings.location:
        query += f" in {settings.location}"

    try:
        r = httpx.get(
            JSEARCH_URL,
            params={"query": query, "num_pages": 1},
            headers={"x-api-key": settings.jsearch_api_key},
            timeout=30,
        )
        r.raise_for_status()
        items = r.json().get("data", [])
    except httpx.HTTPError as e:
        log.error("JSearch fetch failed: %s", e)
        return []

    jobs = []
    for j in items[:count]:
        salary = j.get("job_salary_string") or ""
        jobs.append(Job(
            id=_job_id("jsearch", str(j.get("job_id", ""))),
            title=j.get("job_title", ""),
            company=j.get("employer_name", ""),
            location=j.get("job_location", ""),
            salary=salary,
            description=j.get("job_description", ""),
            url=j.get("job_apply_link", "") or j.get("job_google_link", ""),
            source="jsearch",
        ))
    return jobs


def save_jobs(jobs: list[Job]) -> int:
    conn = get_conn()
    new = 0
    with conn:
        for j in jobs:
            cur = conn.execute(
                """INSERT OR IGNORE INTO jobs (id, title, company, location, salary, description, url, source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (j.id, j.title, j.company, j.location, j.salary, j.description, j.url, j.source),
            )
            new += cur.rowcount
    conn.close()
    return new


def search(settings: Settings, keywords: str, count: int = 20) -> tuple[int, int]:
    """Fetch from all sources, dedupe, store. Returns (total_found, new_saved)."""
    jobs = fetch_adzuna(settings, keywords, count) + fetch_jsearch(settings, keywords, count)
    seen: set[str] = set()
    unique = []
    for j in jobs:
        if j.id not in seen:
            seen.add(j.id)
            unique.append(j)
    return len(unique), save_jobs(unique)
