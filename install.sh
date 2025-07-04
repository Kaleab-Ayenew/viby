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

# Check if pip is available, install if not
if ! python3 -m pip --version >/dev/null 2>&1; then
    printf "${YELLOW}📦 Installing pip...${NC}\n"
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y python3-pip
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y python3-pip
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y python3-pip
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -S --noconfirm python-pip
    else
        printf "${RED}❌ Could not install pip automatically. Please install pip manually and try again.${NC}\n"
        exit 1
    fi
fi

# Install pipx if not available
if ! command -v pipx >/dev/null 2>&1; then
    printf "${YELLOW}📦 Installing pipx...${NC}\n"
    
    # Try package manager first (recommended approach for externally managed environments)
    if command -v apt >/dev/null 2>&1; then
        if sudo apt update && sudo apt install -y pipx 2>/dev/null; then
            printf "${GREEN}✅ pipx installed via apt${NC}\n"
        else
            printf "${YELLOW}⚠️  apt install failed, trying pip...${NC}\n"
            install_pipx_via_pip
        fi
    elif command -v yum >/dev/null 2>&1; then
        if sudo yum install -y pipx 2>/dev/null; then
            printf "${GREEN}✅ pipx installed via yum${NC}\n"
        else
            install_pipx_via_pip
        fi
    elif command -v dnf >/dev/null 2>&1; then
        if sudo dnf install -y pipx 2>/dev/null; then
            printf "${GREEN}✅ pipx installed via dnf${NC}\n"
        else
            install_pipx_via_pip
        fi
    elif command -v pacman >/dev/null 2>&1; then
        if sudo pacman -S --noconfirm python-pipx 2>/dev/null; then
            printf "${GREEN}✅ pipx installed via pacman${NC}\n"
        else
            install_pipx_via_pip
        fi
    else
        install_pipx_via_pip
    fi
    
    # Ensure pipx is in PATH
    if command -v pipx >/dev/null 2>&1; then
        pipx ensurepath 2>/dev/null || true
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi

# Function to install pipx via pip with error handling
install_pipx_via_pip() {
    if python3 -m pip install --user pipx 2>/dev/null; then
        printf "${GREEN}✅ pipx installed via pip${NC}\n"
    else
        # Handle externally managed environment error
        printf "${YELLOW}⚠️  pip install failed (externally managed environment)${NC}\n"
        printf "${YELLOW}Trying alternative methods...${NC}\n"
        
        # Try with --break-system-packages flag as last resort
        if python3 -m pip install --user pipx --break-system-packages 2>/dev/null; then
            printf "${GREEN}✅ pipx installed via pip (with --break-system-packages)${NC}\n"
        else
            printf "${RED}❌ Failed to install pipx automatically${NC}\n"
            printf "${RED}Please install pipx manually:${NC}\n"
            printf "  Ubuntu/Debian: sudo apt install pipx\n"
            printf "  Or create a virtual environment and install there\n"
            exit 1
        fi
    fi
}

# Install vity
printf "${YELLOW}📦 Installing vity...${NC}\n"

# Check if vity is already installed
if pipx list 2>/dev/null | grep -q "package vity"; then
    printf "${YELLOW}🔄 Vity is already installed. Upgrading to latest version...${NC}\n"
    pipx upgrade vity
    VITY_ACTION="upgraded"
else
    printf "${YELLOW}🆕 Installing vity for the first time...${NC}\n"
    pipx install vity
    VITY_ACTION="installed"
fi

# Ensure PATH includes pipx binaries
export PATH="$HOME/.local/bin:$PATH"

# Make sure pipx path is set up
pipx ensurepath >/dev/null 2>&1 || true

# Reload shell configuration to pick up PATH changes
source ~/.bashrc 2>/dev/null || true

# Install or update shell integration
printf "${YELLOW}🔧 Setting up shell integration...${NC}\n"
if [ "$VITY_ACTION" = "upgraded" ]; then
    printf "${YELLOW}🔄 Updating shell integration to latest version...${NC}\n"
    vity reinstall
else
    printf "${YELLOW}🆕 Installing shell integration...${NC}\n"
    vity install
fi

printf "${GREEN}✅ Vity ${VITY_ACTION} successfully!${NC}\n"
printf "\n"
if [ "$VITY_ACTION" = "upgraded" ]; then
    printf "${GREEN}🎉 Update complete!${NC}\n"
    printf "• Vity package upgraded to latest version\n"
    printf "• Shell integration updated with latest features\n"
    printf "• Terminal title fix applied\n"
    printf "\n"
    printf "Changes take effect immediately!\n"
else
    printf "Next steps:\n"
    printf "1. Get an OpenAI API key: https://platform.openai.com/api-keys\n"
    printf "2. Run 'vity config' to set up your API key\n"
    printf "3. Start a new terminal or run 'source ~/.bashrc'\n"
    printf "4. Try: vity do 'find all python files'\n"
fi
printf "\n"
printf "For help: vity --help\n"