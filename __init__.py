name = "mac_scan"

from subprocess import Popen, PIPE # Used to run native OS commads in python wrapped subproccess
from sys import version_info # Used to check the Python-interpreter version at runtime
import time

# Declare batman interface

class mac_scan(object):

    def __init__(self, interface):
        self.interface = interface


#returns result of "sudo batctl n"

    def getBatinfo(self):
 
            
            scan_command = ['sudo','batctl','n']
            #print("ran batctl n")

            scan_process = Popen(scan_command, stdout=PIPE, stderr=PIPE)
            # Returns the 'success' and 'error' output.
            (raw_output, raw_error) = scan_process.communicate() 
            # Block all execution, until the scanning completes.
            scan_process.wait()
            # Returns all output in a dictionary.
            return {'output':raw_output,'error':raw_error}


    def getMacAddresses(self, raw_cell_string):
        raw_cells = raw_cell_string.split('wlan0') # Divide raw string into raw cells.
        raw_cells.pop(0) # Remove unneccesary "B.A.T.M.A.N." message.
        raw_cells.pop(0) # Remove first wlan0 message. 
        #print("formatting cells")
        #print(raw_cells)
        if(len(raw_cells) > 0): # Continue execution, if atleast one node is detected.
            # Iterate through nodes for parsing.
            # Array will hold all parsed cells as dictionaries.
            all_MAC_addresses = [cell.split()[0] for cell in raw_cells]
            #print("cells were formatted")
            # Return list of addresses
            return all_MAC_addresses
        else:
            print("No nodes detected.")
            return False


    def getAPinfo(self, sudo=False):
            # Unparsed access-point listing. AccessPoints are strings.
            raw_scan_output = self.getBatinfo()['output']
            if version_info.major == 3:
                raw_scan_output = raw_scan_output.decode('utf-8')
            # Parsed access-point listing. Access-points are dictionaries.
            print(raw_scan_output)
            #all_access_points = raw_scan_output
            all_access_points = self.getMacAddresses(raw_scan_output)
            # Checks if access-points were found.
            if all_access_points:
                    return all_access_points

            else:
                # No access-points were found. 
                return False

    def interferer(self):
        while True:
            macs = self.getAPinfo(sudo=True)
            if macs == False:
                print("waiting")
                time.sleep(1)
                continue
            else:
                for i in macs:
                    scan_command = ['sudo','batctl','throughputmeter', i]
                    print("ran throughputmeter on ", i)
                    scan_process = Popen(scan_command, stdout=PIPE, stderr=PIPE)
                scan_process.wait()
                print('\n \n \n \n')

