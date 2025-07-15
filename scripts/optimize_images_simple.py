#!/usr/bin/env python3
"""Simple image optimization - WebP conversion only."""

import subprocess
from pathlib import Path


def create_webp(input_path, output_path):
    """Create WebP version of image."""
    try:
        subprocess.run(
            ["cwebp", "-q", "85", "-m", "6", str(input_path), "-o", str(output_path)],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ WebP conversion failed: {e.stderr.decode()}")
        return False


def main():
    """Convert images to WebP format."""
    docs_dir = Path("docs")

    # Find all PNG images
    images = list(docs_dir.rglob("*.png"))

    if not images:
        print("No PNG images found.")
        return

    print(f"Found {len(images)} PNG images\n")

    for img_path in images:
        print(f"Processing: {img_path}")
        original_size = img_path.stat().st_size / 1024  # KB

        # Create WebP version
        webp_path = img_path.with_suffix(".webp")
        if create_webp(img_path, webp_path):
            webp_size = webp_path.stat().st_size / 1024  # KB
            reduction = (1 - webp_size / original_size) * 100
            print(
                f"  ✅ WebP created: {original_size:.1f}KB → {webp_size:.1f}KB ({reduction:.1f}% smaller)\n"
            )

    print("✅ WebP conversion complete!")


if __name__ == "__main__":
    main()
