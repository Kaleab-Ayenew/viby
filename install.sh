#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 Installing Vity - AI Terminal Assistant${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo -e "${RED}❌ Python 3.9+ is required (found $python_version)${NC}"
    exit 1
fi

# Install pipx if not available
if ! command -v pipx &> /dev/null; then
    echo -e "${YELLOW}📦 Installing pipx...${NC}"
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install vity
echo -e "${YELLOW}📦 Installing vity...${NC}"
pipx install vity

# Install shell integration
echo -e "${YELLOW}🔧 Setting up shell integration...${NC}"
vity install

echo -e "${GREEN}✅ Vity installed successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. Get an OpenAI API key: https://platform.openai.com/api-keys"
echo "2. Run 'vity config' to set up your API key"
echo "3. Start a new terminal or run 'source ~/.bashrc'"
echo "4. Try: vity do 'find all python files'"
echo ""
echo "For help: vity --help" 