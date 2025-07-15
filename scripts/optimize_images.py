#!/usr/bin/env python3
"""Optimize documentation images before build."""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def check_dependencies() -> bool:
    """Check if required tools are installed."""
    tools = ["pngquant", "optipng", "cwebp"]
    missing: List[str] = []

    for tool in tools:
        if shutil.which(tool) is None:
            missing.append(tool)

    if missing:
        print(f"❌ Missing required tools: {', '.join(missing)}")
        print("\nInstall with:")
        print("  Ubuntu/Debian: sudo apt-get install -y pngquant optipng webp")
        print("  macOS: brew install pngquant optipng webp")
        return False
    return True


def optimize_png(input_path: Path, output_path: Path) -> None:
    """Optimize PNG using pngquant and optipng."""
    temp_path = output_path.with_suffix(".temp.png")

    # First pass: pngquant (lossy)
    try:
        subprocess.run(
            [
                "pngquant",
                "--quality=85-95",
                "--speed",
                "3",
                "--output",
                str(temp_path),
                "--force",
                str(input_path),
            ],
            check=True,
            capture_output=True,
        )
        input_path = temp_path
    except subprocess.CalledProcessError as e:
        print(f"  ⚠️  pngquant failed for {input_path}, continuing with optipng")
        print(f"      Error: {e.stderr.decode()}")

    # Second pass: optipng (lossless)
    try:
        subprocess.run(
            [
                "optipng",
                "-o3",
                "-strip",
                "all",
                "-out",
                str(output_path),
                str(input_path),
            ],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"  ❌ optipng failed: {e.stderr.decode()}")
        shutil.copy2(input_path, output_path)

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


def create_webp(input_path: Path, output_path: Path) -> bool:
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


def optimize_favicon() -> None:
    """Special handling for favicon."""
    favicon_path = Path("docs/assets/favicon.ico")
    if not favicon_path.exists():
        print("⚠️  No favicon found at docs/assets/favicon.ico")
        return

    # Check size
    size_kb = favicon_path.stat().st_size / 1024
    print(f"\nFavicon size: {size_kb:.1f}KB")

    if size_kb > 50:  # 50KB is large for a favicon
        print("⚠️  Favicon is large. Consider creating a smaller version.")
        # Note: ICO optimization is complex, leaving as-is for now


def main() -> None:
    """Optimize all images in docs directory."""
    if not check_dependencies():
        sys.exit(1)

    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ docs directory not found!")
        sys.exit(1)

    # Find all images
    image_patterns = ["*.png", "*.jpg", "*.jpeg"]
    images: List[Path] = []
    for pattern in image_patterns:
        images.extend(docs_dir.rglob(pattern))

    if not images:
        print("No images found to optimize.")
        return

    print(f"Found {len(images)} images to optimize\n")

    total_original = 0.0
    total_optimized = 0.0
    total_webp = 0.0

    for img_path in images:
        print(f"Processing: {img_path}")
        original_size = img_path.stat().st_size / 1024  # KB
        total_original += original_size

        # Create backup
        backup_path = img_path.with_suffix(img_path.suffix + ".backup")
        if not backup_path.exists():
            shutil.copy2(img_path, backup_path)

        # Optimize based on type
        if img_path.suffix.lower() == ".png":
            optimize_png(img_path, img_path)

        # Create WebP version
        webp_path = img_path.with_suffix(".webp")
        if create_webp(img_path, webp_path):
            webp_size = webp_path.stat().st_size / 1024  # KB
            total_webp += webp_size
            print(f"  ✅ WebP created: {webp_size:.1f}KB")

        # Report results
        new_size = img_path.stat().st_size / 1024  # KB
        total_optimized += new_size

        reduction = (1 - new_size / original_size) * 100 if original_size > 0 else 0
        print(
            f"  ✅ Optimized: {original_size:.1f}KB → {new_size:.1f}KB ({reduction:.1f}% reduction)"
        )

        if webp_path.exists():
            webp_reduction = (
                (1 - webp_size / original_size) * 100 if original_size > 0 else 0
            )
            print(
                f"  ✅ WebP size: {webp_size:.1f}KB ({webp_reduction:.1f}% reduction vs original)\n"
            )
        else:
            print()

    # Handle favicon specially
    optimize_favicon()

    # Summary
    print("\n" + "=" * 50)
    print("OPTIMIZATION SUMMARY")
    print("=" * 50)
    print(f"Total original size: {total_original:.1f}KB")
    print(f"Total optimized size: {total_optimized:.1f}KB")
    print(f"Total reduction: {(1 - total_optimized/total_original) * 100:.1f}%")
    if total_webp > 0:
        print(f"Total WebP size: {total_webp:.1f}KB")
        print(
            f"WebP vs original: {(1 - total_webp/total_original) * 100:.1f}% reduction"
        )

    print("\n✅ Image optimization complete!")
    print("💡 Tip: To restore original images, rename .backup files")


if __name__ == "__main__":
    main()
