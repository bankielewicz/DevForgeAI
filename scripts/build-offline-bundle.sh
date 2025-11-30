#!/bin/bash
# STORY-069: Build Offline Installation Bundle
#
# This script creates a complete offline installation bundle containing:
# - Framework files from src/claude/ and src/devforgeai/
# - Python wheel files for devforgeai CLI
# - SHA256 checksums manifest (checksums.json)
# - Version metadata (version.json)
#
# Output: bundled/ directory ready for NPM package distribution
#
# Usage:
#   bash scripts/build-offline-bundle.sh
#
# Requirements:
#   - Python 3.8+ (for wheel building)
#   - pip with wheel package installed
#   - jq (for JSON manipulation)

set -e  # Exit on error
set -u  # Exit on undefined variable

# Constants
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUNDLED_DIR="$PROJECT_ROOT/bundled"
SRC_DIR="$PROJECT_ROOT/src"
PYTHON_CLI_DIR="$PROJECT_ROOT/.claude/scripts"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Building offline installation bundle...${NC}"

# Clean existing bundle
if [ -d "$BUNDLED_DIR" ]; then
    echo "Removing existing bundled/ directory..."
    rm -rf "$BUNDLED_DIR"
fi

# Create bundled directory structure
echo "Creating bundle directory structure..."
mkdir -p "$BUNDLED_DIR/claude"
mkdir -p "$BUNDLED_DIR/devforgeai"
mkdir -p "$BUNDLED_DIR/python-cli/wheels"

# Copy framework files from src/
echo "Copying .claude/ framework files..."
if [ -d "$SRC_DIR/claude" ]; then
    cp -r "$SRC_DIR/claude/"* "$BUNDLED_DIR/claude/"
else
    echo -e "${YELLOW}Warning: $SRC_DIR/claude not found, using operational .claude/${NC}"
    cp -r "$PROJECT_ROOT/.claude/"* "$BUNDLED_DIR/claude/"
fi

# Remove development/cache files from bundle
echo "Cleaning up development files from bundle..."
find "$BUNDLED_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$BUNDLED_DIR" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find "$BUNDLED_DIR" -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
find "$BUNDLED_DIR" -type d -name ".git" -exec rm -rf {} + 2>/dev/null || true
find "$BUNDLED_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$BUNDLED_DIR" -type f -name ".coverage" -delete 2>/dev/null || true
find "$BUNDLED_DIR" -type f -name "coverage.json" -delete 2>/dev/null || true
find "$BUNDLED_DIR" -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
find "$BUNDLED_DIR" -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find "$BUNDLED_DIR" -type d -name "build" -exec rm -rf {} + 2>/dev/null || true

echo "Copying .devforgeai/ framework files..."
if [ -d "$SRC_DIR/devforgeai" ]; then
    cp -r "$SRC_DIR/devforgeai/"* "$BUNDLED_DIR/devforgeai/"
else
    echo -e "${YELLOW}Warning: $SRC_DIR/devforgeai not found, using operational .devforgeai/${NC}"
    # Copy only essential directories (exclude operational files)
    mkdir -p "$BUNDLED_DIR/devforgeai/context"
    mkdir -p "$BUNDLED_DIR/devforgeai/protocols"
    mkdir -p "$BUNDLED_DIR/devforgeai/specs"

    if [ -d "$PROJECT_ROOT/.devforgeai/context" ]; then
        cp -r "$PROJECT_ROOT/.devforgeai/context/"* "$BUNDLED_DIR/devforgeai/context/" 2>/dev/null || true
    fi
    if [ -d "$PROJECT_ROOT/.devforgeai/protocols" ]; then
        cp -r "$PROJECT_ROOT/.devforgeai/protocols/"* "$BUNDLED_DIR/devforgeai/protocols/" 2>/dev/null || true
    fi
    if [ -d "$PROJECT_ROOT/.devforgeai/specs" ]; then
        cp -r "$PROJECT_ROOT/.devforgeai/specs/"*.md "$BUNDLED_DIR/devforgeai/specs/" 2>/dev/null || true
    fi
fi

# Copy CLAUDE.md template
echo "Copying CLAUDE.md template..."
if [ -f "$SRC_DIR/CLAUDE.md" ]; then
    cp "$SRC_DIR/CLAUDE.md" "$BUNDLED_DIR/CLAUDE.md"
elif [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
    cp "$PROJECT_ROOT/CLAUDE.md" "$BUNDLED_DIR/CLAUDE.md"
else
    echo -e "${RED}Error: CLAUDE.md not found${NC}"
    exit 1
fi

# Copy README.md
echo "Copying README.md..."
if [ -f "$PROJECT_ROOT/README.md" ]; then
    cp "$PROJECT_ROOT/README.md" "$BUNDLED_DIR/README.md"
fi

# Build Python wheel files
echo "Building Python CLI wheel files..."
if command -v python3 &> /dev/null; then
    if [ -d "$PYTHON_CLI_DIR" ]; then
        cd "$PYTHON_CLI_DIR"

        # Build wheel for devforgeai CLI
        if [ -f "setup.py" ]; then
            echo "Building devforgeai wheel..."
            python3 setup.py bdist_wheel --dist-dir "$BUNDLED_DIR/python-cli/wheels/" 2>/dev/null || {
                echo -e "${YELLOW}Warning: Failed to build wheel via setup.py, trying pip...${NC}"
                pip3 wheel . --no-deps --wheel-dir "$BUNDLED_DIR/python-cli/wheels/" 2>/dev/null || {
                    echo -e "${RED}Error: Failed to build Python wheel${NC}"
                    # Continue anyway - Python CLI is optional
                }
            }
        fi

        cd "$PROJECT_ROOT"
    fi
else
    echo -e "${YELLOW}Warning: Python 3 not available, skipping wheel build${NC}"
fi

# Copy version.json
echo "Copying version metadata..."
if [ -f "$SRC_DIR/devforgeai/version.json" ]; then
    cp "$SRC_DIR/devforgeai/version.json" "$BUNDLED_DIR/version.json"
else
    # Create default version.json
    echo '{
  "version": "1.0.0",
  "released_at": "2025-11-29T00:00:00Z",
  "schema_version": "1.0"
}' > "$BUNDLED_DIR/version.json"
fi

# Generate checksums.json
echo "Generating SHA256 checksums manifest..."
cd "$BUNDLED_DIR"

# Create checksums.json
echo "{" > checksums.json

# Find all files and calculate SHA256
first_entry=true
while IFS= read -r -d '' file; do
    # Skip checksums.json itself
    if [[ "$file" == "./checksums.json" ]]; then
        continue
    fi

    # Calculate SHA256
    if command -v sha256sum &> /dev/null; then
        hash=$(sha256sum "$file" | awk '{print $1}')
    elif command -v shasum &> /dev/null; then
        hash=$(shasum -a 256 "$file" | awk '{print $1}')
    else
        echo -e "${RED}Error: No SHA256 utility found (sha256sum or shasum)${NC}"
        exit 1
    fi

    # Get relative path (remove leading ./)
    relative_path="${file#./}"

    # Add entry to checksums.json (with comma separator except for first entry)
    if [ "$first_entry" = true ]; then
        echo "  \"$relative_path\": \"$hash\"" >> checksums.json
        first_entry=false
    else
        # Append comma to previous line and add new entry
        sed -i '$ s/$/,/' checksums.json
        echo "  \"$relative_path\": \"$hash\"" >> checksums.json
    fi
done < <(find . -type f -print0 | sort -z)

echo "}" >> checksums.json

cd "$PROJECT_ROOT"

# Verify bundle structure
echo "Verifying bundle structure..."
bundle_file_count=$(find "$BUNDLED_DIR" -type f | wc -l)
echo "  Files bundled: $bundle_file_count"

if [ $bundle_file_count -lt 200 ]; then
    echo -e "${YELLOW}Warning: Only $bundle_file_count files bundled (expected ≥200)${NC}"
fi

# Measure bundle size
echo "Measuring bundle size..."
if command -v du &> /dev/null; then
    # Uncompressed size
    uncompressed_kb=$(du -sk "$BUNDLED_DIR" | awk '{print $1}')
    uncompressed_mb=$((uncompressed_kb / 1024))
    echo "  Uncompressed: ${uncompressed_mb} MB"

    if [ $uncompressed_mb -gt 150 ]; then
        echo -e "${YELLOW}Warning: Uncompressed size ${uncompressed_mb} MB exceeds 150 MB limit${NC}"
    fi

    # Compressed size estimate (tar.gz)
    if command -v tar &> /dev/null && command -v gzip &> /dev/null; then
        temp_archive="/tmp/devforgeai-bundle-test.tar.gz"
        tar -czf "$temp_archive" -C "$PROJECT_ROOT" "bundled/" 2>/dev/null
        compressed_kb=$(du -k "$temp_archive" | awk '{print $1}')
        compressed_mb=$((compressed_kb / 1024))
        echo "  Compressed (tar.gz): ${compressed_mb} MB"
        rm -f "$temp_archive"

        if [ $compressed_mb -gt 60 ]; then
            echo -e "${YELLOW}Warning: Compressed size ${compressed_mb} MB exceeds 60 MB limit${NC}"
        fi
    fi
fi

echo -e "${GREEN}✓ Offline bundle created successfully: $BUNDLED_DIR${NC}"
echo ""
echo "Bundle contents:"
echo "  - claude/         Framework files"
echo "  - devforgeai/     Configuration templates"
echo "  - python-cli/     Python CLI wheels (optional)"
echo "  - checksums.json  SHA256 integrity manifest"
echo "  - version.json    Version metadata"
echo "  - CLAUDE.md       Installation template"
echo ""
echo "Next steps:"
echo "  1. Review bundled/ directory"
echo "  2. Run tests: npm test"
echo "  3. Package for NPM: npm pack"
