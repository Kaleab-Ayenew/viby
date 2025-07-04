#!/bin/sh
set -e

# Colors for output (using printf for better compatibility)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

printf "${GREEN}🤖 Installing Vity - AI Terminal Assistant${NC}\n"

# Check if Python is available
if ! command -v python3 >/dev/null 2>&1; then
    printf "${RED}❌ Python 3 is required but not installed${NC}\n"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    printf "${RED}❌ Python 3.9+ is required (found $python_version)${NC}\n"
    exit 1
fi

# Install pipx if not available
if ! command -v pipx >/dev/null 2>&1; then
    printf "${YELLOW}📦 Installing pipx...${NC}\n"
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install vity
printf "${YELLOW}📦 Installing vity...${NC}\n"
pipx install vity

# Install shell integration
printf "${YELLOW}🔧 Setting up shell integration...${NC}\n"
vity install

printf "${GREEN}✅ Vity installed successfully!${NC}\n"
printf "\n"
printf "Next steps:\n"
printf "1. Get an OpenAI API key: https://platform.openai.com/api-keys\n"
printf "2. Run 'vity config' to set up your API key\n"
printf "3. Start a new terminal or run 'source ~/.bashrc'\n"
printf "4. Try: vity do 'find all python files'\n"
printf "\n"
printf "For help: vity --help\n"