#!/usr/bin/env python3
"""
sloof - iOS 26.1 Kernel Exploit
CVE-2026-20700: Dyld Trust Error
WARNING: For educational/research purposes only
"""
import os
import sys
import time
import base64
import binascii
from typing import Dict, List

class Colors:
    GREEN = '\033[1;32m'
    RED = '\033[1;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    MAGENTA = '\033[1;35m'
    RESET = '\033[0m'
    
    @staticmethod
    def info(msg):
        print(f"{Colors.GREEN}[+] {msg}{Colors.RESET}")
        time.sleep(0.2)
    
    @staticmethod
    def step(msg):
        print(f"{Colors.CYAN}[*] {msg}{Colors.RESET}")
        time.sleep(0.2)
    
    @staticmethod
    def warn(msg):
        print(f"{Colors.YELLOW}[!] {msg}{Colors.RESET}")
        time.sleep(0.3)
    
    @staticmethod
    def error(msg):
        print(f"{Colors.RED}[!] {msg}{Colors.RESET}")
        time.sleep(0.5)

class DeviceInfo:
    DEVICES = {
        'iPhone16,1': 'iPhone 16 Pro',
        'iPhone16,2': 'iPhone 16 Pro Max',
        'iPhone16,3': 'iPhone 16',
        'iPhone16,4': 'iPhone 16 Plus',
        'iPad14,3': 'iPad Pro 13" M4',
        'iPad14,4': 'iPad Pro 11" M4',
    }
    
    IOS_VERSIONS = {
        'iOS 26.1': '26.1.0-26A349',
        'iOS 26.2': '26.2.0-26B146'
    }
    
    @staticmethod
    def get_device_name(model: str) -> str:
        return DeviceInfo.DEVICES.get(model, 'Unknown Device')
    
    @staticmethod
    def get_ios_build(ios: str) -> str:
        return DeviceInfo.IOS_VERSIONS.get(ios, 'Unknown')

def print_header():
    print(f"""
{Colors.CYAN}    ███╗   ███╗ ██████╗ ███╗   ██╗███████╗██╗  ██╗██╗     ███████╗███████╗
    ████╗ ████║██╔═══██╗████╗  ██║██╔════╝╚██╗██╔╝██║     ██╔════╝██╔════╝
    ██╔████╔██║██║   ██║██╔██╗ ██║█████╗   ╚███╔╝ ██║     █████╗  ███████╗
    ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══╝   ██╔██╗ ██║     ██╔══╝  ╚════██║
    ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████╗██╔╝╚██╗███████╗███████╗███████║
    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝{Colors.RESET}
""")

def print_ascii_art():
    print(f"""
{Colors.MAGENTA}    ██████╗ ██╗  ██╗██╗   ██╗███████╗██╗  ██╗    ███████╗ ██████╗ ██████╗ ██╗██╗   ██╗███████╗
    ██╔══██╗██║  ██║╚██╗ ██╔╝██╔════╝██║  ██║    ██╔════╝██╔═══██╗██╔══██╗██║██║   ██║██╔════╝
    ██████╔╝███████║ ╚████╔╝ ███████╗███████║    █████╗  ██║   ██║██████╔╝██║██║   ██║█████╗  
    ██╔═══╝ ██╔══██║  ╚██╔╝  ╚════██║██╔══██║    ██╔══╝  ██║   ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  
    ██║     ██║  ██║   ██║   ███████║██║  ██║    ███████╗╚██████╔╝██║  ██║██║ ╚████╔╝ ███████╗
    ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  {Colors.RESET}
""")

def show_warning():
    print(f"\n{Colors.RED}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                    ⚠️  WARNING  ⚠️                        ║")
    print("╠═══════════════════════════════════════════════════════════════╣")
    print("║  CVE-2026-20700: Dyld Trust Error                          ║")
    print("║  This vulnerability allows kernel code execution!             ║")
    print("║  Apple patched this in iOS 26.3 - USE AT YOUR OWN RISK       ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    Colors.error("Vulnerable iOS Version DETECTED")
    time.sleep(1)

def get_device_info() -> Dict[str, str]:
    print("\n" + "="*60)
    Colors.step("Detecting connected iOS device...")
    time.sleep(1.5)
    
    print(f"\n{Colors.CYAN}[INPUT] Please enter your device model (e.g., iPhone16,1): {Colors.RESET}", end="")
    device = input().strip()
    
    print(f"{Colors.CYAN}[INPUT] Please enter iOS version (e.g., iOS 26.1): {Colors.RESET}", end="")
    ios = input().strip()
    
    return {'device': device, 'ios': ios}

def init_exploit_chain():
    Colors.step("Initializing exploit chain...")
    rop_gadgets = [
        "0x180040000", "0x180040004", "0x180040008", "0x18004000C",
        "0x180040010", "0x180040014", "0x180040018", "0x18004001C",
    ]
    
    chain = []
    for gadget in rop_gadgets:
        addr = int(gadget.replace('0x', ''), 16)
        chain.append(addr)
    
    result = 0x15000000
    for i, v in enumerate(chain):
        result ^= (v << (i % 8))
    
    Colors.info(f"ROP chain constructed: 0x{result:x}")
    time.sleep(0.5)

def load_offsets():
    Colors.step("Loading kernel offsets...")
    time.sleep(0.8)
    
    offsets = {
        'kernel_base': 0xfffffff007004000,
        'kernel_slide': 0x1000,
        'vm_kernel_addr': 0xfffffff007560000,
        'kernel_task': 0xfffffff007560048,
    }
    
    for name, offset in offsets.items():
        Colors.info(f"{name}: 0x{offset:x}")
    
    time.sleep(0.5)

def apply_patches():
    Colors.step("Patching AMFI (Apple Mobile File Integrity)...")
    time.sleep(0.6)
    Colors.info("AMFI patch applied: code signing enforcement disabled")
    time.sleep(0.3)
    
    Colors.step("Patching Sandbox...")
    time.sleep(0.6)
    Colors.info("Sandbox patch applied: full root access granted")
    time.sleep(0.3)
    
    Colors.step("Patching SEPOS (Secure Enclave Processor)...")
    time.sleep(0.6)
    Colors.info("SEP patch applied: SEP boot chain bypassed")
    time.sleep(0.3)
    
    Colors.step("Patching dyld (dynamic linker)...")
    time.sleep(0.6)
    Colors.info("dyld patch applied: custom dylib injection enabled")
    time.sleep(0.3)
    
    Colors.step("Bypassing PAC (Pointer Authentication Code)...")
    time.sleep(0.6)
    Colors.info("PAC bypass: using_keys(APIA, APDA)")
    time.sleep(0.3)

def load_kexts():
    Colors.step("Loading kext (kernel extensions)...")
    
    kexts = [
        ("com.apple.iokit.IOMobileGraphicsFamily", "0x18a00000"),
        ("com.apple.kpi.bsd", "0x18a01000"),
        ("com.apple.kpi.iokit", "0x18a02000"),
        ("com.apple.kpi.mach", "0x18a03000"),
    ]
    
    for name, addr in kexts:
        time.sleep(0.4)
        Colors.info(f"Loaded {name} @ {addr}")

def inject_payload():
    Colors.step("Injecting exploit payload...")
    
    payload = [
        0xD28014D2,  # mov x18, #0xA6
        0xD2801DC2,  # mov x2, #0xEE
        0xD65F03C0,  # ret
    ]
    
    Colors.info("Payload buffer allocated at 0x1800C0000")
    time.sleep(0.4)
    Colors.info(f"Writing {len(payload)} instructions...")
    time.sleep(0.4)
    Colors.info("Jumping to exploit code...")

def show_success():
    print(f"\n{Colors.GREEN}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║              🎉 JAILBREAK SUCCESSFUL 🎉                      ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    Colors.info("Exploit: sloof (CVE-2026-4812)")
    Colors.info("iOS Version: 26.1.0-26A349")
    Colors.info("Device: iPhone 16 Pro")
    Colors.info("Build: 26A349")
    Colors.info("Jailbreak Type: Tethered")
    Colors.info("Root Access: ✓")
    Colors.info("Sandbox Disabled: ✓")
    Colors.info("AMFI Bypassed: ✓")

def finalize():
    print(f"\n{Colors.CYAN}")
    print("="*60)
    Colors.step("Finalizing installation...")
    
    # Progress bar
    for i in range(101):
        sys.stdout.write(f"\r[{i:3d}%] {'█' * (i // 2)}{'░' * (50 - i // 2)}")
        sys.stdout.flush()
        time.sleep(0.02)
    print()
    print(f"{Colors.RESET}")
    time.sleep(1)

def wait_enter():
    print(f"\n{Colors.YELLOW}")
    print("="*60)
    print("Press ENTER to finalize the jailbreak...")
    print("="*60 + f"{Colors.RESET}")
    input()

def reveal_april_fools():
    # Decode Easter eggs
    easter_name = base64.b64decode("c2xvb2Y=").decode()  # "sloof"
    easter_msg = base64.b64decode("QXByaWwgRm9vbHMhISE=").decode()  # "April Fools!!!"
    
    time.sleep(1)
    print(f"\n{Colors.MAGENTA}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                     You got Fooled                               ║")
    print("╠═══════════════════════════════════════════════════════════════╣")
    print("║  This is a FAKE jailbreak! There is no working Jailbreak in 2026!                   ║")
    print("╠═══════════════════════════════════════════════════════════════╣")
    print(f"║  Exploit Name: {easter_name:<47}║")
    print(f"║  Secret Message: {easter_msg:<40}║")
    print("╠═══════════════════════════════════════════════════════════════╣")
    print("║  iOS 26.1 isnt jailbreakable (it's 2026, not 2024!)           ║")                ║")
    print("║  This was a joke - don't try this on a real device!           ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    time.sleep(1)
    Colors.info("Thanks for playing! Have a great Day! 🎉")

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print_header()
    print_ascii_art()
    
    Colors.step("sloof v1.0.0 - iOS 26.1- iOS 26.2 Kernel Exploit")
    Colors.step("CVE-2026-20700 Dyld Trust Error")
    print()
    
    if not show_warning():
        return
    
    info = get_device_info()
    
    if info['device'] not in DeviceInfo.DEVICES:
        Colors.error(f"Device {info['device']} not supported!")
        Colors.step("Supported devices: iPhone 16 series, iPad Pro M4")
        return
    
    if info['ios'] != "iOS 26.1":
        Colors.warn(f"iOS {info['ios']} not supported! This exploit ONLY works on iOS 26.1")
        Colors.step("Apple fixed CVE-2026-4812 in iOS 26.2")
        return
    
    device_name = DeviceInfo.get_device_name(info['device'])
    Colors.info(f"Device detected: {device_name}")
    Colors.info(f"iOS version: {info['ios']} ({DeviceInfo.get_ios_build(info['ios'])})")
    
    time.sleep(1)
    print()
    
    init_exploit_chain()
    load_offsets()
    apply_patches()
    load_kexts()
    inject_payload()
    show_success()
    finalize()
    wait_enter()
    reveal_april_fools()

if __name__ == "__main__":
    main()
