# Joker
Joker is a simple program that can be run on a linux machine running the B.A.T.M.A.N mesh networking interface to create constant interference on the network. 

# Notes
* This program and the documentation was created with a secific use case in mind for a research project. Your use case may differ greatly. My setup was a fleet of ten raspberry pi Zeros running raspberry pi OS Buster and one pi 3B. They were set up  as a mesh netowrk using the  B.A.T.M.A.N advanced interface. One node is chosen as the broadcaster of interference while the rest recieve.

# Installation:
Download the two program files
* For all nodes
    - move SD card to pi 3, connect Ethernet, and boot
    - ssh in and change batman network name. Anything will work, it just has to be different from the two we will test and any nearby network. It also must be the same on all interference network nodes.
        - `sudo nano /etc/network/interfaces.d/wlan0`
     - If your hostname is the same as any other node on this new network don’t forget to change it.
     - Change name, save and transfer back to zero
* For the interference broadcaster
    - Follow steps above
      - switch python version
        - `sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10`
    		- copy __init__.py to the pi 3 using ssh and scp.
            - BE SURE IT IS PLACED IN 
               `/home/pi/.local/lib/python3.7/site-packages/mac_scan`
               - You may need to create all these directories after .local
               - if your python version is different, replace that part of the path.
         - copy interfere.py to the pi 3 using ssh and scp
          - Place it on the desktop ( /home/pi/Desktop)
         - Next we need to make the program run at startup. I had trouble with this step but found a workaround that I’ll explain below. I tried using rc.local and systemd but neither worked. Instead I added it to .bashrc and made the terminal run at startup. To do this, while SSHed in, do the following:
           - `sudo nano /home/pi/.bashrc`
             - add these two lines at the end
               - `echo running at boot`
               - `python /home/pi/Desktop/interfere.py`
           - `sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`
             - add this after the last line:
               - `lxterminal`
         - For some reason, batman stopped running for me at this stage. I found this workaround. Run the following on the pi 3:
           - `sudo rfkill unblock 0`
           - `sudo ifconfig wlan0 up`
         - reboot the pi 3 and make sure the terminal opens and the program is running

	Note: If you don’t have a screen, you can still test at this stage if you know the mac addresses of the other nodes on the network. You can get them by running sudo batctl n. Then, on the pi 3 you just set up, run sudo batctl throughputmeter MAC but replace MAC with one of the mac addresses. If the program is running fine, you should see “Cannot run two tests towards the same node”
        			▪ If no other nodes are set up, the output should look like this:
				
▪ If other nodes have been set up, it should show something like this:

    	◦ You should be able to transfer back to a zero now and it will run at startup

Hopefully this will work fine, if not, I am creating and uploading an image just in case this manual setup doesn’t work
