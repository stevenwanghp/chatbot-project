"""Fetch configured Syariah Court pages and save article content as Markdown."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from helper_functions.config import load_config

CONFIG = load_config()
ALLOWED_HOST = "syariahcourt.gov.sg"


def extract_article(html: str, page_url: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("main .page-structure-holder") or soup.find("main")
    if article is None:
        raise ValueError("Could not find the page's main article content")

    for element in article.select(
        "script, style, nav, footer, [role='navigation'], "
        ".breadcrumb, .chatbot, .cookie-banner"
    ):
        element.decompose()

    for heading in article.find_all(re.compile(r"^h[1-6]$")):
        if not heading.get_text(" ", strip=True):
            heading.decompose()

    for link in article.find_all("a", href=True):
        link["href"] = urljoin(page_url, link["href"])
    for image in article.find_all("img", src=True):
        image["src"] = urljoin(page_url, image["src"])

    title_element = article.find("h1") or soup.find("title")
    title = title_element.get_text(" ", strip=True) if title_element else page_url
    body = markdownify(
        str(article),
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
    )
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    if len(body) < 100:
        raise ValueError("Extracted page content is unexpectedly short")
    return title, body


def fetch_page(session: requests.Session, page_url: str) -> tuple[str, str]:
    parsed_url = urlparse(page_url)
    if parsed_url.scheme != "https" or parsed_url.hostname != ALLOWED_HOST:
        raise ValueError(f"URL is not on the allowed official host: {page_url}")

    response = session.get(page_url, timeout=30)
    response.raise_for_status()
    if urlparse(response.url).hostname != ALLOWED_HOST:
        raise ValueError(f"Page redirected away from the allowed host: {response.url}")
    return extract_article(response.text, page_url)


def output_path_for(page_url: str, output_dir: Path) -> Path:
    path = urlparse(page_url).path.strip("/")
    return output_dir / "web" / f"{path}.md"


def write_markdown(page_url: str, title: str, body: str, output_path: Path) -> None:
    metadata = {
        "source_type": "web",
        "source_url": page_url,
        "title": title,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "---\n"
        + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
        + "---\n\n"
        + f"# {title}\n\n{body}\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url",
        action="append",
        dest="urls",
        help="fetch one configured URL (repeatable); defaults to all configured pages",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / CONFIG["PROCESSED_DATA_DIRECTORY"],
        help=f"Markdown output directory (default: {CONFIG['PROCESSED_DATA_DIRECTORY']}/)",
    )
    args = parser.parse_args()

    configured_urls = CONFIG["WEB_SOURCE_URLS"]
    urls = args.urls or configured_urls
    unconfigured_urls = sorted(set(urls) - set(configured_urls))
    if unconfigured_urls:
        parser.error(f"URL is not in config.yaml allowlist: {unconfigured_urls[0]}")

    failed_urls = []
    with requests.Session() as session:
        session.headers.update(
            {"User-Agent": "AI-Bootcamp-RAG-Indexer/1.0 (official page ingestion)"}
        )
        for page_url in urls:
            try:
                title, body = fetch_page(session, page_url)
                output_path = output_path_for(page_url, args.output_dir)
                write_markdown(page_url, title, body, output_path)
                print(f"Fetched {title}: {output_path}")
            except (requests.RequestException, ValueError) as error:
                failed_urls.append(page_url)
                print(f"Failed to fetch {page_url}: {error}", file=sys.stderr)

    if failed_urls:
        print(f"Failed to fetch {len(failed_urls)} of {len(urls)} pages", file=sys.stderr)
        return 1
    print(f"Fetched {len(urls)} official pages into {args.output_dir / 'web'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())