# Scripts Directory

This directory contains utility scripts for maintaining and developing the ESO Logs Python client.

## Scripts Overview

### 🔧 Core Development Scripts

#### `generate_client.sh`
Generates the GraphQL client code from the ESO Logs API schema.

**Usage:**
```bash
./scripts/generate_client.sh
```

**What it does:**
1. Downloads the latest GraphQL schema from ESO Logs API
2. Generates Python client code using `ariadne-codegen`
3. Applies post-processing via `post_codegen.py`
4. Updates the client with the latest API methods

**Requirements:**
- Valid ESO Logs API credentials in environment variables:
  - `ESOLOGS_ID`: Your client ID
  - `ESOLOGS_SECRET`: Your client secret

---

#### `post_codegen.py`
Post-processes the generated GraphQL client code to fix various issues and improve usability.

**Usage:**
```bash
python scripts/post_codegen.py
```

**What it does:**
1. Fixes import statements in generated files
2. Adds proper type annotations
3. Resolves naming conflicts
4. Ensures compatibility with the project structure

**Note:** This is automatically called by `generate_client.sh` and rarely needs to be run manually.

---

### 🛠️ Utility Scripts

#### `optimize_images.py`
Optimizes images in the documentation for better performance.

**Usage:**
```bash
python scripts/optimize_images.py
```

**What it does:**
1. Finds all PNG and JPEG images in the `docs/` directory
2. Creates backup copies (`.backup` extension)
3. Optimizes PNGs using `pngquant` (lossy) and `optipng` (lossless)
4. Creates WebP versions for modern browser support
5. Reports size savings and optimization statistics

**Requirements:**
```bash
# Ubuntu/Debian
sudo apt-get install -y pngquant optipng webp

# macOS
brew install pngquant optipng webp
```

**Features:**
- Automatic backup creation
- Special handling for favicons
- Detailed optimization report
- WebP generation for ~30-50% additional size savings

---

#### `quick_api_check.py`
Quick diagnostic tool to check if ESO Logs API endpoints are responding.

**Usage:**
```bash
python scripts/quick_api_check.py
```

**What it does:**
1. Tests connectivity to all major ESO Logs endpoints
2. Reports status for each endpoint (✅ OK, ❌ Down, ⏱️ Timeout)
3. Helps diagnose API availability issues

**Example output:**
```
ESO Logs Endpoint Status Check
==================================================
✅ Main Website      200 OK
✅ OAuth Token       401 (Auth required - endpoint is up)
✅ GraphQL Client    401 (Auth required - endpoint is up)
✅ GraphQL User      401 (Auth required - endpoint is up)
✅ API Docs          200 OK
==================================================
```

**Use cases:**
- Debugging authentication failures
- Checking if API is down
- Verifying network connectivity

---

## Development Workflow

### Regenerating the Client

When the ESO Logs API is updated:

1. Ensure your credentials are set:
   ```bash
   export ESOLOGS_ID="your-client-id"
   export ESOLOGS_SECRET="your-client-secret"
   ```

2. Run the generator:
   ```bash
   ./scripts/generate_client.sh
   ```

3. Review the changes and run tests:
   ```bash
   pytest tests/
   ```

### Optimizing Documentation Images

Before releasing new documentation:

1. Add your images to the `docs/` directory
2. Run the optimizer:
   ```bash
   python scripts/optimize_images.py
   ```
3. Commit both the optimized images and their `.webp` versions

### Troubleshooting API Issues

If you're experiencing API errors:

1. First check if the API is up:
   ```bash
   python scripts/quick_api_check.py
   ```

2. If endpoints show as down (502 errors), the API may be experiencing issues
3. Check https://twitter.com/esologs or https://status.esologs.com/ for updates

---

## Notes

- All scripts should be run from the project root directory
- Scripts use proper error handling and will report issues clearly
- Generated code should not be manually edited - changes will be overwritten
- Always test after regenerating the client
