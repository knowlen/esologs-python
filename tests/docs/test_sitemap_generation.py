"""Test sitemap.xml generation in MkDocs builds."""

import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest


class TestSitemapGeneration:
    """Test that MkDocs generates sitemap.xml correctly."""

    @pytest.mark.integration
    def test_mkdocs_generates_sitemap(self):
        """Test that MkDocs build generates a valid sitemap.xml file."""
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent

        # Use a temporary directory for the build
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run mkdocs build
            result = subprocess.run(
                ["mkdocs", "build", "--site-dir", temp_dir, "--clean"],
                cwd=project_root,
                capture_output=True,
                text=True,
            )

            # Check build succeeded
            assert result.returncode == 0, f"MkDocs build failed: {result.stderr}"

            # Check sitemap.xml exists
            sitemap_path = Path(temp_dir) / "sitemap.xml"
            assert sitemap_path.exists(), "sitemap.xml was not generated"

            # Validate sitemap content
            tree = ET.parse(sitemap_path)
            root = tree.getroot()

            # Check root element
            assert root.tag.endswith("urlset"), "Invalid sitemap root element"

            # Check namespace
            expected_ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
            assert expected_ns in root.tag, f"Missing sitemap namespace in {root.tag}"

            # Check for URL entries
            urls = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")
            assert len(urls) > 0, "No URLs found in sitemap"

            # Check each URL has required elements
            for url in urls:
                loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                assert loc is not None, "URL entry missing <loc> element"
                assert loc.text, "URL entry has empty <loc> element"
                assert loc.text.startswith(
                    "https://esologs-python.readthedocs.io"
                ), f"Invalid URL: {loc.text}"

            # Check specific pages are included
            url_texts = [
                url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
                for url in urls
            ]
            assert any(
                "https://esologs-python.readthedocs.io/" == url for url in url_texts
            ), "Home page not in sitemap"

    def test_mkdocs_site_url_configured(self):
        """Test that site_url is properly configured in mkdocs.yml."""
        mkdocs_path = Path(__file__).parent.parent.parent / "mkdocs.yml"
        content = mkdocs_path.read_text()

        # Parse for site_url
        site_url_line = None
        for line in content.split("\n"):
            if line.strip().startswith("site_url:"):
                site_url_line = line
                break

        assert site_url_line is not None, "site_url not found in mkdocs.yml"

        # Extract URL
        site_url = site_url_line.split(":", 1)[1].strip()
        assert site_url == "https://esologs-python.readthedocs.io/"

    @pytest.mark.integration
    def test_sitemap_xml_validation(self):
        """Test that generated sitemap.xml is valid XML and follows sitemap protocol."""
        project_root = Path(__file__).parent.parent.parent

        with tempfile.TemporaryDirectory() as temp_dir:
            # Build docs
            subprocess.run(
                ["mkdocs", "build", "--site-dir", temp_dir, "--clean"],
                cwd=project_root,
                capture_output=True,
            )

            sitemap_path = Path(temp_dir) / "sitemap.xml"
            if not sitemap_path.exists():
                pytest.skip("Sitemap not generated")

            # Read and validate XML structure
            with open(sitemap_path) as f:
                content = f.read()

            # Basic XML validation
            assert content.startswith("<?xml"), "Missing XML declaration"
            assert "<urlset" in content, "Missing urlset element"
            assert "</urlset>" in content, "Unclosed urlset element"

            # Check for sitemap namespace
            assert "xmlns" in content, "Missing namespace declaration"
            assert "sitemaps.org/schemas/sitemap" in content, "Missing sitemap schema"

            # Check structure
            assert "<url>" in content, "No URL entries found"
            assert "<loc>" in content, "No location elements found"

            # Count URLs
            url_count = content.count("<url>")
            loc_count = content.count("<loc>")
            assert url_count == loc_count, "Mismatch between url and loc elements"
            assert url_count > 5, f"Too few URLs in sitemap: {url_count}"
