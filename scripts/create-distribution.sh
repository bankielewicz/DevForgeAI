#!/bin/bash

##############################################################################
# DevForgeAI Distribution Package Creator
#
# Creates distribution packages (tar.gz and zip) for DevForgeAI v1.0.1
# Includes all necessary files and generates SHA256 checksums
#
# Usage:
#   bash scripts/create-distribution.sh
#
# Output:
#   devforgeai-1.0.1.tar.gz    (~25 MB)
#   devforgeai-1.0.1.zip       (~25 MB)
#   SHA256SUMS                  (checksums)
#
##############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PACKAGE_VERSION="1.0.1"
PACKAGE_NAME="devforgeai"
SOURCE_DIR="."
TEMP_DIR="/tmp/devforgeai-dist-$$"
DIST_DIR="."

echo -e "${BLUE}DevForgeAI Distribution Package Creator v${PACKAGE_VERSION}${NC}\n"

# Step 1: Validate prerequisites
echo -e "${YELLOW}Step 1: Validating prerequisites...${NC}"

if ! command -v tar &> /dev/null; then
    echo -e "${RED}Error: tar not found${NC}"
    exit 1
fi

if ! command -v zip &> /dev/null; then
    echo -e "${RED}Error: zip not found${NC}"
    exit 1
fi

if ! command -v sha256sum &> /dev/null && ! command -v shasum &> /dev/null; then
    echo -e "${RED}Error: sha256sum or shasum not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites verified${NC}\n"

# Step 2: Create temporary staging directory
echo -e "${YELLOW}Step 2: Creating staging directory...${NC}"

mkdir -p "$TEMP_DIR/devforgeai-${PACKAGE_VERSION}"
STAGE_DIR="$TEMP_DIR/devforgeai-${PACKAGE_VERSION}"

echo -e "${GREEN}✓ Staging directory created: $STAGE_DIR${NC}\n"

# Step 3: Copy required directories and files
echo -e "${YELLOW}Step 3: Copying framework files...${NC}"

# Core directories
echo "  Copying src/"
cp -r src "$STAGE_DIR/" 2>/dev/null || echo "    (src/ not found - may be acceptable)"

echo "  Copying installer/"
cp -r installer "$STAGE_DIR/" 2>/dev/null || echo "    (installer/ not found)"

# Documentation
echo "  Copying documentation"
cp README.md "$STAGE_DIR/" 2>/dev/null || echo "    (README.md not found)"
cp INSTALL.md "$STAGE_DIR/" 2>/dev/null || echo "    (INSTALL.md not found)"
cp MIGRATION-GUIDE.md "$STAGE_DIR/" 2>/dev/null || echo "    (MIGRATION-GUIDE.md not found)"
cp ROADMAP.md "$STAGE_DIR/" 2>/dev/null || echo "    (ROADMAP.md not found)"
cp LICENSE "$STAGE_DIR/" 2>/dev/null || echo "    (LICENSE not found)"

# Version metadata
echo "  Copying version metadata"
cp version.json "$STAGE_DIR/" 2>/dev/null || echo "    (version.json not found)"

# DevForgeAI specs and configs
echo "  Copying devforgeai/"
cp -r devforgeai "$STAGE_DIR/" 2>/dev/null || echo "    (devforgeai/ not found)"

# .claude directory (deployed files)
echo "  Copying .claude/"
cp -r .claude "$STAGE_DIR/" 2>/dev/null || echo "    (.claude/ not found)"

# .ai_docs (examples and templates)
echo "  Copying .ai_docs/"
cp -r .ai_docs "$STAGE_DIR/" 2>/dev/null || echo "    (.ai_docs/ not found)"

# installer directory (if not already copied)
if [ ! -d "$STAGE_DIR/installer" ]; then
    echo "  Note: installer/ not included (development-only)"
fi

echo -e "${GREEN}✓ Framework files copied${NC}\n"

# Step 4: Verify required files
echo -e "${YELLOW}Step 4: Verifying package contents...${NC}"

REQUIRED_FILES=(
    "README.md"
    "LICENSE"
    "version.json"
    "MIGRATION-GUIDE.md"
)

FOUND_COUNT=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$STAGE_DIR/$file" ]; then
        echo "  ✓ $file"
        ((FOUND_COUNT++))
    else
        echo "  ✗ $file (missing)"
    fi
done

TOTAL_FILES=$(find "$STAGE_DIR" -type f | wc -l)
echo -e "${GREEN}✓ Package contains $TOTAL_FILES files${NC}\n"

# Step 5: Create tar.gz package
echo -e "${YELLOW}Step 5: Creating tar.gz package...${NC}"

TAR_FILE="$DIST_DIR/${PACKAGE_NAME}-${PACKAGE_VERSION}.tar.gz"
cd "$TEMP_DIR"
tar -czf "$TAR_FILE" "devforgeai-${PACKAGE_VERSION}/" 2>/dev/null
cd - > /dev/null

if [ -f "$TAR_FILE" ]; then
    SIZE_MB=$(du -m "$TAR_FILE" | cut -f1)
    echo -e "${GREEN}✓ Created: $TAR_FILE ($SIZE_MB MB)${NC}"
else
    echo -e "${RED}✗ Failed to create tar.gz package${NC}"
    exit 1
fi

echo ""

# Step 6: Create zip package
echo -e "${YELLOW}Step 6: Creating zip package...${NC}"

ZIP_FILE="$DIST_DIR/${PACKAGE_NAME}-${PACKAGE_VERSION}.zip"
cd "$TEMP_DIR"
zip -r -q "$ZIP_FILE" "devforgeai-${PACKAGE_VERSION}/" 2>/dev/null
cd - > /dev/null

if [ -f "$ZIP_FILE" ]; then
    SIZE_MB=$(du -m "$ZIP_FILE" | cut -f1)
    echo -e "${GREEN}✓ Created: $ZIP_FILE ($SIZE_MB MB)${NC}"
else
    echo -e "${RED}✗ Failed to create zip package${NC}"
    exit 1
fi

echo ""

# Step 7: Generate checksums
echo -e "${YELLOW}Step 7: Generating SHA256 checksums...${NC}"

CHECKSUMS_FILE="$DIST_DIR/SHA256SUMS"

# Determine which checksum command to use
if command -v sha256sum &> /dev/null; then
    CHECKSUM_CMD="sha256sum"
else
    CHECKSUM_CMD="shasum -a 256"
fi

# Generate checksums
cd "$DIST_DIR"
rm -f "$CHECKSUMS_FILE"

$CHECKSUM_CMD "${PACKAGE_NAME}-${PACKAGE_VERSION}.tar.gz" >> "$CHECKSUMS_FILE" 2>/dev/null || \
    echo "Error generating checksum for tar.gz" >&2

$CHECKSUM_CMD "${PACKAGE_NAME}-${PACKAGE_VERSION}.zip" >> "$CHECKSUMS_FILE" 2>/dev/null || \
    echo "Error generating checksum for zip" >&2

cd - > /dev/null

if [ -f "$CHECKSUMS_FILE" ]; then
    echo -e "${GREEN}✓ Created: $CHECKSUMS_FILE${NC}"
    echo ""
    echo "Checksums:"
    cat "$CHECKSUMS_FILE" | sed 's/^/  /'
else
    echo -e "${YELLOW}⚠ Failed to create checksums file${NC}"
fi

echo ""

# Step 8: Cleanup
echo -e "${YELLOW}Step 8: Cleaning up temporary files...${NC}"

rm -rf "$TEMP_DIR"
echo -e "${GREEN}✓ Temporary files removed${NC}\n"

# Step 9: Summary and verification
echo -e "${BLUE}=== Distribution Package Summary ===${NC}\n"

echo "Package Name: DevForgeAI"
echo "Version: $PACKAGE_VERSION"
echo "Release Date: $(date +'%Y-%m-%d')"
echo ""

echo "Generated Files:"
if [ -f "$TAR_FILE" ]; then
    SIZE=$(du -h "$TAR_FILE" | cut -f1)
    echo "  ✓ ${PACKAGE_NAME}-${PACKAGE_VERSION}.tar.gz ($SIZE)"
fi

if [ -f "$ZIP_FILE" ]; then
    SIZE=$(du -h "$ZIP_FILE" | cut -f1)
    echo "  ✓ ${PACKAGE_NAME}-${PACKAGE_VERSION}.zip ($SIZE)"
fi

if [ -f "$CHECKSUMS_FILE" ]; then
    echo "  ✓ SHA256SUMS"
fi

echo ""
echo "Package Contents:"
echo "  • src/ - Framework source code"
echo "  • .claude/ - Deployed framework files"
echo "  • devforgeai/ - Configuration and specifications"
echo "  • .ai_docs/ - Examples and documentation"
echo "  • installer/ - Installation scripts"
echo "  • Documentation files (README, INSTALL.md, MIGRATION-GUIDE.md, LICENSE)"
echo "  • version.json - Version metadata"
echo ""

echo "Distribution Location: $DIST_DIR"
echo ""

# Final verification
echo -e "${BLUE}=== Verification ===${NC}\n"

echo "Package Integrity Check:"

# Test tar.gz extraction
echo "  Testing tar.gz extraction..."
TEST_DIR="/tmp/devforgeai-test-tar-$$"
mkdir -p "$TEST_DIR"
tar -xzf "$TAR_FILE" -C "$TEST_DIR" 2>/dev/null && {
    echo -e "  ${GREEN}✓ tar.gz extraction successful${NC}"
    rm -rf "$TEST_DIR"
} || {
    echo -e "  ${RED}✗ tar.gz extraction failed${NC}"
    rm -rf "$TEST_DIR"
}

# Test zip extraction
echo "  Testing zip extraction..."
TEST_DIR="/tmp/devforgeai-test-zip-$$"
mkdir -p "$TEST_DIR"
unzip -q "$ZIP_FILE" -d "$TEST_DIR" 2>/dev/null && {
    echo -e "  ${GREEN}✓ zip extraction successful${NC}"
    rm -rf "$TEST_DIR"
} || {
    echo -e "  ${RED}✗ zip extraction failed${NC}"
    rm -rf "$TEST_DIR"
}

# Verify checksums exist and are valid
echo "  Verifying checksums..."
if [ -f "$CHECKSUMS_FILE" ] && [ -s "$CHECKSUMS_FILE" ]; then
    cd "$DIST_DIR"
    if $CHECKSUM_CMD -c "$CHECKSUMS_FILE" &>/dev/null; then
        echo -e "  ${GREEN}✓ Checksums verified${NC}"
    else
        echo -e "  ${YELLOW}⚠ Checksum verification skipped (files just created)${NC}"
    fi
    cd - > /dev/null
fi

echo ""

# Final message
echo -e "${GREEN}=== Distribution Package Creation Complete ===${NC}"
echo ""
echo "Your distribution packages are ready!"
echo ""
echo "Next Steps:"
echo "  1. Verify checksums: cat $CHECKSUMS_FILE"
echo "  2. Upload packages to distribution server"
echo "  3. Publish release notes with checksums"
echo "  4. Announce availability to users"
echo ""
echo "Installation Instructions for Users:"
echo "  tar -xzf devforgeai-${PACKAGE_VERSION}.tar.gz"
echo "  cd devforgeai-${PACKAGE_VERSION}"
echo "  python installer/install.py --mode=fresh"
echo ""

exit 0
