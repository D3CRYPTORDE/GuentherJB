#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${MAGENTA}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ███╗   ███╗ ██████╗ ███╗   ██╗███████╗██╗  ██╗██╗     ███████╗███████╗ ║
║    ████╗ ████║██╔═══██╗████╗  ██║██╔════╝╚██╗██╔╝██║     ██╔════╝██╔════╝ ║
║    ██╔████╔██║██║   ██║██╔██╗ ██║█████╗   ╚███╔╝ ██║     █████╗  ███████╗ ║
║    ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══╝   ██╔██╗ ██║     ██╔══╝  ╚════██║ ║
║    ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████╗██╔╝╚██╗███████╗███████╗███████║ ║
║    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ║
║                                                               ║
║          iOS 26.1 Kernel Exploit Installer                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "MSYS" || "$OSTYPE" == "CYGWIN"* || "$OSTYPE" == "MINGW"* ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

check_python() {
    echo -e "${CYAN}[*] Checking Python installation...${NC}"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        echo -e "${GREEN}[+] Python found: $PYTHON_VERSION${NC}"
        
        if [[ $PYTHON_MAJOR -lt 3 ]] || ([[ $PYTHON_MAJOR -eq 3 ]] && [[ $PYTHON_MINOR -lt 9 ]]); then
            echo -e "${RED}[!] Python 3.9+ is required${NC}"
            exit 1
        fi
    else
        echo -e "${RED}[!] Python 3 not found. Please install Python 3.9 or later.${NC}"
        
        OS=$(detect_os)
        if [[ "$OS" == "macos" ]]; then
            echo -e "${YELLOW}[*] On macOS, you can install Python using Homebrew:${NC}"
            echo -e "${YELLOW}    brew install python3${NC}"
        elif [[ "$OS" == "linux" ]]; then
            echo -e "${YELLOW}[*] On Linux, use your package manager:${NC}"
            echo -e "${YELLOW}    sudo apt-get install python3 python3-pip  (Debian/Ubuntu)${NC}"
            echo -e "${YELLOW}    sudo dnf install python3 python3-pip    (Fedora)${NC}"
        fi
        exit 1
    fi
}

check_pip() {
    echo -e "${CYAN}[*] Checking pip installation...${NC}"
    
    if python3 -m pip --version &> /dev/null; then
        PIP_VERSION=$(python3 -m pip --version | awk '{print $2}')
        echo -e "${GREEN}[+] pip found: $PIP_VERSION${NC}"
    else
        echo -e "${RED}[!] pip not found. Installing...${NC}"
        
        OS=$(detect_os)
        if [[ "$OS" == "macos" ]]; then
            python3 -m ensurepip --default-pip
        elif [[ "$OS" == "linux" ]]; then
            sudo apt-get install python3-pip
        fi
    fi
}

create_virtualenv() {
    echo -e "${CYAN}[*] Setting up virtual environment...${NC}"
    
    if [ -d "venv" ]; then
        echo -e "${YELLOW}[!] Virtual environment already exists. Removing...${NC}"
        rm -rf venv
    fi
    
    python3 -m venv venv
    
    if [[ "$OS" == "macos" ]] || [[ "$OS" == "linux" ]]; then
        source venv/bin/activate
    else
        source venv/Scripts/activate
    fi
    
    echo -e "${GREEN}[+] Virtual environment created${NC}"
}

install_dependencies() {
    echo -e "${CYAN}[*] Installing Python dependencies...${NC}"
    
    pip install --upgrade pip --quiet
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt --quiet
        echo -e "${GREEN}[+] Dependencies installed${NC}"
    else
        echo -e "${RED}[!] requirements.txt not found${NC}"
    fi
}

generate_keys() {
    echo -e "${CYAN}[*] Generating encryption keys...${NC}"
    
    if [ ! -d "keys" ]; then
        mkdir -p keys
    fi
    
    openssl rand -base64 32 > keys/sloof.key 2>/dev/null || python3 -c "import os; print(os.urandom(32).hex())" > keys/sloof.key
    
    echo -e "${GREEN}[+] Keys generated in keys/sloof.key${NC}"
}

patch_usbmuxd() {
    echo -e "${CYAN}[*] Checking usbmuxd...${NC}"
    
    OS=$(detect_os)
    
    if [[ "$OS" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            if ! command -v usbmuxd &> /dev/null; then
                echo -e "${YELLOW}[!] usbmuxd not found. Installing via Homebrew...${NC}"
                brew install usbmuxd || echo -e "${YELLOW}[!] Could not install usbmuxd${NC}"
            else
                echo -e "${GREEN}[+] usbmuxd already installed${NC}"
            fi
        else
            echo -e "${YELLOW}[!] Homebrew not found. Skipping usbmuxd.${NC}"
        fi
    elif [[ "$OS" == "linux" ]]; then
        if ! command -v usbmuxd &> /dev/null; then
            echo -e "${YELLOW}[!] usbmuxd not found. Attempting to install...${NC}"
            sudo apt-get install usbmuxd 2>/dev/null || echo -e "${YELLOW}[!] Could not install usbmuxd${NC}"
        else
            echo -e "${GREEN}[+] usbmuxd already installed${NC}"
        fi
    fi
}

setup_environment() {
    echo -e "${CYAN}[*] Setting up environment configuration...${NC}"
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo -e "${GREEN}[+] Created .env from example${NC}"
        else
            cat > .env << 'EOF'
SLOOF_CHAIN=0xdeadbeef
CORE_SECURITY_BYPASS=1
AMFI_PATCH_LEVEL=3
SANDBOX_ESCAPE=1
SEP_PATCH=0
DEVICE_UDID=auto
FORCE_DFU_MODE=0
VERBOSE_LOGGING=0
DEBUG_OUTPUT=0
EOF
            echo -e "${GREEN}[+] Created .env configuration file${NC}"
        fi
    else
        echo -e "${YELLOW}[!] .env already exists${NC}"
    fi
}

download_payload() {
    echo -e "${CYAN}[*] Verifying exploit payload...${NC}"
    
    if [ -f "exploit.bin.hex" ]; then
        FILE_SIZE=$(wc -c < "exploit.bin.hex")
        echo -e "${GREEN}[+] Exploit payload found (${FILE_SIZE} bytes)${NC}"
    else
        echo -e "${RED}[!] exploit.bin.hex not found!${NC}"
    fi
}

run_installer() {
    echo -e "\n${MAGENTA}[════════════════════════════════════════════════════════════]${NC}"
    echo -e "${MAGENTA}                    INSTALLATION COMPLETE                       ${NC}"
    echo -e "${MAGENTA}[════════════════════════════════════════════════════════════]${NC}\n"
    
    echo -e "${GREEN}[+] To activate the virtual environment, run:${NC}"
    
    if [[ "$OS" == "macos" ]] || [[ "$OS" == "linux" ]]; then
        echo -e "${CYAN}    source venv/bin/activate${NC}"
    else
        echo -e "${CYAN}    venv\\Scripts\\activate${NC}"
    fi
    
    echo -e "\n${GREEN}[+] To run the exploit, use:${NC}"
    echo -e "${CYAN}    python3 jailbreak.py${NC}"
    
    echo -e "\n${YELLOW}[!] IMPORTANT:${NC}"
    echo -e "${YELLOW}    - Your device must be in DFU mode${NC}"
    echo -e "${YELLOW}    - This exploit ONLY works on iOS 26.1${NC}"
    echo -e "${YELLOW}    - Use at your own risk!${NC}\n"
}

progress_bar() {
    local current=$1
    local total=$2
    local prefix=${3:-Progress}
    local suffix=${4:-complete}
    local width=40
    
    let percent=(current*100/total)
    let filled=(width*current/total)
    let empty=(width-filled)
    
    printf "\r${CYAN}${prefix}: [${GREEN}"
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    printf "${CYAN}] ${percent}%% ${suffix}${NC}"
}

main() {
    OS=$(detect_os)
    
    echo -e "${BOLD}Detected OS: ${GREEN}$OS${NC}\n"
    
    check_python
    sleep 0.5
    
    check_pip
    sleep 0.5
    
    total_steps=6
    current=0
    
    echo ""
    for step in $(seq 1 $total_steps); do
        case $step in
            1) create_virtualenv ;;
            2) install_dependencies ;;
            3) generate_keys ;;
            4) patch_usbmuxd ;;
            5) setup_environment ;;
            6) download_payload ;;
        esac
        current=$step
        progress_bar $current $total_steps "Setting up"
        sleep 0.3
    done
    
    echo ""
    run_installer
}

main "$@"
