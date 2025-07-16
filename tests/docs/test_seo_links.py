"""Test SEO-related links and metadata."""

import re
from pathlib import Path


class TestSEOLinks:
    """Test that SEO-related links are valid."""

    def test_readme_external_links(self):
        """Test that all external links in README are properly formatted."""
        readme_path = Path(__file__).parent.parent.parent / "README.md"
        content = readme_path.read_text()

        # Find all markdown links
        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        links = link_pattern.findall(content)

        # Check that all links have valid format
        for text, url in links:
            assert text.strip(), f"Empty link text for URL: {url}"
            assert url.strip(), f"Empty URL for link text: {text}"

            # Check external links start with http
            # Skip anchors (#), absolute paths (/), and relative file paths
            if not any(
                url.startswith(prefix) for prefix in ["#", "/", "http://", "https://"]
            ):
                # This is likely a relative path - check it's not trying to be a URL
                if "." in url and not any(
                    url.endswith(ext)
                    for ext in [".md", ".py", ".txt", ".yml", ".toml", ".json"]
                ):
                    # Looks like a domain without protocol
                    raise AssertionError(f"URL missing protocol: {url}")

    def test_pypi_badge_exists(self):
        """Test that PyPI version badge exists in README."""
        readme_path = Path(__file__).parent.parent.parent / "README.md"
        content = readme_path.read_text()

        # Check for PyPI badge
        assert (
            "badge.fury.io/py/esologs-python" in content
        ), "PyPI version badge not found"

    def test_search_terms_format(self):
        """Test that search terms are properly formatted with commas."""
        readme_path = Path(__file__).parent.parent.parent / "README.md"
        content = readme_path.read_text()

        # Find search terms section
        search_section = content.split("## Search Terms")[-1]
        if search_section:
            # Get the first paragraph after the heading
            lines = search_section.strip().split("\n")
            if len(lines) > 1:
                search_terms_line = lines[1].strip()
                # Check that it contains commas
                assert (
                    "," in search_terms_line
                ), "Search terms should be comma-separated"
                # Check that it contains expected keywords
                assert "Elder Scrolls Online" in search_terms_line
                assert "ESO" in search_terms_line
                assert "Python" in search_terms_line

    def test_mkdocs_sitemap_config(self):
        """Test that site_url is configured for sitemap generation."""
        mkdocs_path = Path(__file__).parent.parent.parent / "mkdocs.yml"
        content = mkdocs_path.read_text()

        # Check for site_url which is required for sitemap generation
        assert "site_url:" in content, "site_url not configured (required for sitemap)"
        assert "esologs-python.readthedocs.io" in content, "Site URL should be set"

    def test_mkdocs_social_meta(self):
        """Test that OpenGraph meta tags are configured."""
        mkdocs_path = Path(__file__).parent.parent.parent / "mkdocs.yml"
        content = mkdocs_path.read_text()

        # Check for OpenGraph tags
        assert "og:title" in content, "OpenGraph title not configured"
        assert "og:description" in content, "OpenGraph description not configured"
        assert "og:type" in content, "OpenGraph type not configured"
        assert "twitter:card" in content, "Twitter card not configured"

    def test_robots_txt_exists(self):
        """Test that robots.txt exists for documentation."""
        robots_path = Path(__file__).parent.parent.parent / "docs" / "robots.txt"
        assert robots_path.exists(), "robots.txt not found in docs directory"

        content = robots_path.read_text()
        assert "User-agent:" in content, "User-agent directive missing"
        assert "Sitemap:" in content, "Sitemap directive missing"
        assert "esologs-python.readthedocs.io" in content, "Site URL missing"
