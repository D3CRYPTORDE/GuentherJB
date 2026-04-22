# sloof — iOS 26.1 Kernel Exploit

**CVE-2026-20700: Dyld Trust Error**

<p align="center">
  <img src="https://img.shields.io/badge/iOS-26.1-green" alt="iOS 26.1">
  <img src="https://img.shields.io/badge/Exploit-sloof-blue" alt="sloof">
  <img src="https://img.shields.io/badge/Version-1.0.0-red" alt="v1.0.0">
</p>

## ⚠️ WARNING

**This tool is for educational and research purposes only.** Using this exploit on devices you do not own is illegal and violates the DMCA. The maintainers of this project are not responsible for any damage caused by misuse of this tool.

---

## 📱 Supported Devices

| Device | Model Number | Chipset |
|--------|--------------|---------|
| iPhone 16 Pro | iPhone16,1 | A18 Pro |
| iPhone 16 Pro Max | iPhone16,2 | A18 Pro |
| iPhone 16 | iPhone16,3 | A18 |
| iPhone 16 Plus | iPhone16,4 | A18 |
| iPad Pro 13" (M4) | iPad14,3 | M4 |
| iPad Pro 11" (M4) | iPad14,4 | M4 |

**Required iOS Version: iOS 26.1 ONLY**

> ⚠️ This exploit **ONLY** works on iOS 26.2. Apple patched CVE-2026-4812 in iOS 26.3. 

---

## 🔧 Requirements

### macOS/Linux

```bash
# Python 3.9+
python3 --version

# Install dependencies
pip3 install -r requirements.txt

# Clone usbmuxd (required for USB exploitation)
git clone https://github.com/libimobiledevice/usbmuxd.git
cd usbmuxd
./autogen.sh
make
sudo make install
```

### Windows

```powershell
# Install Python 3.9+ from python.org
# Install Visual Studio Build Tools with C++ support

# Install dependencies
pip install -r requirements.txt

# Install libusb (via Zadig or native Windows driver)
```

---

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/d3cryptorde/guentherjb.git
cd sloof
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and adjust as needed:

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings:

```bash
# Exploit Configuration
SLOOF_CHAIN=0xdeadbeef
CORE_SECURITY_BYPASS=1
AMFI_PATCH_LEVEL=3
SANDBOX_ESCAPE=1
SEP_PATCH=0

# Device Configuration
DEVICE_UDID=auto
FORCE_DFU_MODE=0

# Debug Options
VERBOSE_LOGGING=0
DEBUG_OUTPUT=0
```

### 4. Run Setup Script

```bash
chmod +x install.sh
./install.sh
```

---

## 🔌 Device Preparation

### Enter DFU Mode

For the exploit to work, your device must be in DFU mode:

1. Connect your device to your computer
2. Turn off the device
3. Press and hold the Side button for 3 seconds
4. While holding Side, press and hold Volume Down for 10 seconds
5. Release Side but continue holding Volume Down for 5 more seconds
6. Your device should now be in DFU mode (black screen)

### macOS

```bash
# Check device in DFU mode
idevice_id -l
```

### Windows

Use iTunes or check Device Manager for "Apple Device (DFU Mode)"

---

## 🚀 Running the Exploit

### Basic Usage

```bash
python3 jailbreak.py
```

### Advanced Usage

```bash
# With custom environment
SLOOF_CHAIN=0xcafebabe python3 jailbreak.py

# Verbose mode
VERBOSE_LOGGING=1 python3 jailbreak.py

# Force DFU mode check
FORCE_DFU_MODE=1 python3 jailbreak.py
```

---

## 📋 Exploit Process

The sloof exploit performs the following steps:

```
[1] Device Detection
    ├── Identify device model
    └── Check iOS version (MUST be 26.1)

[2] Exploit Chain Initialization
    ├── Load ROP gadgets
    ├── Build kernel payload
    └── Initialize PAC keys

[3] Kernel Exploitation
    ├── Trigger CVE-2026-4812
    ├── Execute ROP chain
    └── Achieve arbitrary read/write

[4] Patches Application
    ├── AMFI bypass
    ├── Sandbox escape
    ├── SEPOS patch
    └── dyld injection

[5] Jailbreak Finalization
    ├── Mount root filesystem
    ├── Install Cydia/ Zebra
    └── Set up SSH access
```

---

## 🔬 Technical Details

### CVE-2026-4812: Core Security Error

**Description:** A critical memory corruption vulnerability in the iOS kernel allows arbitrary code execution with kernel privileges.

**Affected Versions:** iOS 26.0 - 26.1

**Patched In:** iOS 26.2

**CVSS Score:** 9.8 (Critical)

### Exploit Mechanism

The sloof exploit uses a multi-stage approach:

1. **Stage 1:** USB exploit triggers initial kernel read/write
2. **Stage 2:** ROP chain constructs arbitrary kernel primitive
3. **Stage 3:** Kernel patcher applies AMFI, Sandbox, and SEP bypasses
4. **Stage 4:** Tethered boot payload injection via iBoot

### Key Components

| Component | Description |
|-----------|-------------|
| `jailbreak.py` | Main exploit script |
| `exploit.bin.hex` | Encoded kernel payload |
| `install.sh` | Platform-specific setup |
| `.env` | Configuration file |

---

## 🐛 Troubleshooting

### "Device not supported"

- Ensure your device is in the supported list
- Check your device model: Settings → General → About

### "iOS version not supported"

- This exploit only works on **iOS 26.1**
- Check iOS version: Settings → General → About → Version

### "USB device not detected"

- Try a different USB cable (original Apple cable recommended)
- Try a different USB port (USB 2.0 preferred)
- On Windows, install Apple USB drivers

### "Exploit failed at stage X"

- Ensure device is in DFU mode
- Try running as administrator/root
- Check verbose logs with `VERBOSE_LOGGING=1`

### "Python module not found"

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📄 License

This project is for educational purposes only. Use at your own risk.

---

## 🙏 Acknowledgments

- Apple's Security Team (for finding and patching the vulnerability)
- Checkra1n team (for inspiration)
- unc0ver team (for methodology)
- All iOS jailbreak community members

---

## 📞 Contact

For issues and contributions, please open an issue on GitHub.

**Note:** This is a proof-of-concept exploit. It may not work on all devices or iOS versions.
