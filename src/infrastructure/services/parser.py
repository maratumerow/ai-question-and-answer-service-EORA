import logging
import uuid
from datetime import UTC, datetime
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from src.domain.entities import Source
from src.domain.services.content_parsing import ContentParsingServiceInterface

logger = logging.getLogger(__name__)


class HTTPContentParsingService(ContentParsingServiceInterface):
    """HTTP-based implementation of ContentParsingService."""

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            },
        )

    async def parse_url(self, url: str) -> Source | None:
        """Parse content from URL."""
        if not url or not url.strip():
            logger.warning("Empty URL provided")
            return None

        try:
            logger.debug("Parsing URL: %s", url)

            response = await self.client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title_tag = soup.find("title")
            title = (
                title_tag.get_text().strip()
                if title_tag
                else urlparse(url).path
            )

            # Extract main content
            content = self._extract_content(soup)

            # Generate ID from URL
            source_id = uuid.uuid5(uuid.NAMESPACE_URL, url)

            source = Source(
                id=source_id,
                url=url,
                title=title,
                content=content,
                created_at=datetime.now(UTC),
            )

            logger.debug("Successfully parsed %s", url)
            return source

        except httpx.HTTPStatusError as e:
            if e.response.status_code in {404, 403, 410}:
                # Expected errors - page not found, forbidden, gone
                logger.info(
                    "Page not accessible: %s (status %d)",
                    url,
                    e.response.status_code,
                )
            else:
                # Unexpected HTTP errors
                logger.warning("HTTP error for %s: %s", url, e)
            return None

        except httpx.TimeoutException:
            logger.warning("Timeout while parsing %s", url)
            return None

        except httpx.ConnectError as e:
            logger.warning("Connection error for %s: %s", url, e)
            return None

        except httpx.RequestError as e:
            logger.warning("Request error for %s: %s", url, e)
            return None

        except Exception as e:
            logger.error("Unexpected error parsing %s: %s", url, e)
            return None

    async def parse_urls(self, urls: list[str]) -> list[Source]:
        """Parse content from multiple URLs."""
        if not urls:
            return []

        logger.info("Parsing %d URLs", len(urls))

        sources: list[Source] = []

        for url in urls:
            source = await self.parse_url(url)
            if source:
                sources.append(source)

        logger.info(
            "Successfully parsed %d out of %d URLs (failed: %d)",
            len(sources),
            len(urls),
            len(urls) - len(sources),
        )
        return sources

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from HTML."""
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        # Try to find main content areas
        content_selectors = [
            ".tn-atom",
        ]

        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                return "\n".join(el.get_text(strip=True) for el in elements)

        # If no specific content found, use body
        body = soup.find("body")
        if body:
            text = body.get_text(strip=True)
            return text[:5000] if text else ""

        return ""
