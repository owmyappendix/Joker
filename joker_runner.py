import mac_scan
import time

#time.sleep(20)

interface = 'bat0'
mac_scanner = mac_scan.mac_scan(interface)
mac_scanner.interferer()


