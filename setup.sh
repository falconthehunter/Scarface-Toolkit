#!/usr/bin/env bash

# Colors
BLUE='\033[34;1m'
GREEN='\033[32;1m'
RED='\033[31;1m'
YELLOW='\033[33;1m'
CYAN='\033[36;1m'
RESET='\033[0m'

# Configuration
REQUIRED_DIRS=("scripts" "sites" "results")
PYTHON_DEPS=("flask" "requests" "termcolor" "bs4")

# Timed loading animation (3 seconds)
timed_loading() {
    local msg="$1"
    echo -ne "${CYAN}${msg} [                    ] 0%${RESET}"
    for i in {1..20}; do
        sleep 0.15
        echo -ne "\r${CYAN}${msg} ["
        for j in $(seq 1 $i); do echo -ne "▓"; done
        for j in $(seq $i 19); do echo -ne " "; done
        echo -ne "] $((i*5))%"
    done
    echo -e "${RESET}"
}

# Error handler
handle_error() {
    echo -e "\n${RED}✗ Error: $1${RESET}"
    echo -e "${YELLOW}Try manual installation:"
    echo -e "1. cd $(pwd)"
    echo -e "2. ln -sf \$PWD/scarface /usr/local/bin/scarface"
    echo -e "3. chmod +x scarface scripts/*.py${RESET}"
    exit 1
}

# Detect installation directory
detect_bin_dir() {
    if [ -n "$PREFIX" ] && [[ "$PREFIX" == *"com.termux"* ]]; then
        echo "$PREFIX/bin"  # Termux
    elif [ -d "/usr/local/bin" ]; then
        echo "/usr/local/bin"  # Linux/macOS
    elif [ -d "$HOME/.local/bin" ]; then
        echo "$HOME/.local/bin"  # User-space
    else
        echo "$HOME/bin"  # Fallback
    fi
}

# Verify Python environment
verify_python() {
    timed_loading "   Checking Python setup"
    if ! command -v python3 >/dev/null 2>&1; then
        handle_error "Python 3 not found"
    fi

    for dep in "${PYTHON_DEPS[@]}"; do
        if ! python3 -c "import $dep" 2>/dev/null; then
            echo -e "${YELLOW}▲ Installing $dep...${RESET}"
            pip3 install --user "$dep" || handle_error "Failed to install $dep"
        fi
    done
}

# Main installation
install_scarface() {
    clear
    echo -e "${BLUE}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
    echo -e "█ Scarface Environment Setup v3.0 █"
    echo -e "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀${RESET}"
    
    # Environment detection
    timed_loading "[1/6] Detecting OS environment"
    BIN_DIR=$(detect_bin_dir)
    echo -e "\n${GREEN}✓ Installation target: ${BIN_DIR}${RESET}"

    # Directory validation
    timed_loading "[2/6] Validating structure"
    for dir in "${REQUIRED_DIRS[@]}"; do
        [ -d "$dir" ] || handle_error "Missing directory: $dir"
    done

    # System linking
    timed_loading "[3/6] Creating system links"
    mkdir -p "$BIN_DIR" || handle_error "Can't create $BIN_DIR"
    ln -sf "$PWD/scarface" "$BIN_DIR/scarface" || handle_error "Symlink failed"

    # Permissions
    timed_loading "[4/6] Setting permissions"
    chmod +x scarface scripts/*.py || handle_error "Permission denied"

    # Python setup
    timed_loading "[5/6] Configuring Python"
    verify_python

    # Final check
    timed_loading "[6/6] Verifying installation"
    command -v scarface >/dev/null || handle_error "PATH configuration failed"

    echo -e "\n${GREEN}✓ Installation successful!${RESET}"
    echo -e "${YELLOW}Run anywhere: ${CYAN}scarface${RESET}"
}

# Execute installation
install_scarface
