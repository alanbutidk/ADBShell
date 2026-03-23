import subprocess as s
import platform
from pathlib import Path

def printhelp():
	print("ADBShell V1.0.0")
	print("CSC Means Custom Shell Command")
	print("\nALL COMMANDS ARE CASE-SENSETIVE. Commands are:"
		"\nhelp = Prints this help screen."
		"\nserver = enters the server menu, type exit to exit this menu or type start or stop to start/stop the daemon."
		"\nreboot = reboots the connected device."
		"\ncheck = gives the output for device is connected, offline, not connected, device name, device android version etc..."
		"\nbattery = outputs the current battery level."
		"\nshutdown = self-explanatory..."
		"\nfastboot connect = connects to fastboot/bootloader mode"
		"\nfastboot disconnect = launches disconnect fastboot ATTEMPT"
		"\ndriver = tests ADB/USB/Google/OEM drivers."
		"\nfastboot_d connect = sandbox fastboot connect."
		"\nfastboot_d disconnect = sandbox fastboot disconnect."
		"\nrecovery connect = connects to recovery mode."
		"\nrecovery disconnect = disconnects from recovery mode."
		"\nclear cache = clears the cache partition."
		"\nclear all = same as resetting phone from settings."
		"\nroot test = checks for root availiblity."
		"\nfastboot unlock = NO LOCKING AVAILIBLITY, Unlocks your bootloader if capable.")

global filepath
filepath = Path(__file__).parent.resolve().as_posix()

global ext
ext = ".exe" if platform.system() == "Windows" else ""

global p
p = filepath + f"/adb{ext}"

global z
z = filepath + f"/fastboot{ext}"

def sermenu():
	while True:
		seruser = input("Server Menu; 'start'/'stop': ")
		if seruser == "start": s.run(f"{p} start-server", shell=True)
		elif seruser == "stop": s.run(f"{p} kill-server", shell=True)
		elif seruser == "exit": break
#end of function

def clearuser():
	while True:
		clruser = input("yes or no; case-sensetive: ")
		if clruser == "yes": print("YES IS DETECTED, ERASING ALL DATA..."); s.run(f"{p} reboot bootloader", shell=True); s.run(f"{z} erase userdata", shell=True); continue
		else:
			break
#end of function

def checksl():
	dsc = s.run(f"{p} devices", capture_output=True, text=True, shell=True)
	output = dsc.stdout.strip().splitlines()
	serial, status = "Unknown", "Not Connected"
	for line in output[1:]:
		if "\t" in line:
			serial, status = line.split("\t")
	print("CSC 'check' called")
	print("\nAdb version: ", s.run(f"{p} version", capture_output=True, text=True, shell=True).stdout)
	print("\nDevice Serial: ", serial)
	print("\nDevice Connection Status: ", status)
	print("\nAndroid version (Found through ADB SHELL): ", s.run(f"{p} shell getprop ro.build.version.release", capture_output=True, text=True, shell=True).stdout)
	print("\nAndroid SDK Version (also found through adb shell getprop): ", s.run(f"{p} shell getprop ro.build.version.sdk", capture_output=True, text=True, shell=True).stdout)
	print("\nDevice Name: ", s.run(f"{p} shell getprop ro.product.model", capture_output=True, text=True, shell=True).stdout)
	print("\nUser Defined Device name: ", s.run(f"{p} shell settings get global device_name", capture_output=True, text=True, shell=True).stdout)
#end of function


while True:
	user = input(">>> ")
	if user == "help": printhelp(); continue
	elif user == "exit": exit("Shell Exited")
	elif user == "server": sermenu(); continue
	elif user == "reboot": s.run(f"{p} reboot", shell=True); continue
	elif user == "check": checksl(); continue
	elif user == "battery": s.run(f"{p} shell cmd battery get level", shell=True); continue
	elif user == "shutdown": s.run(f"{p} shell svc power shutdown", shell=True); continue
	elif user == "fastboot connect": s.run(f"{p} reboot bootloader", shell=True); continue
	elif user == "fastboot disconnect":
		print("If the device is stuck on fastboot, please try doing vol button combos like: power + vol up, or power + vol down, \nif this doesnt work. TRY GOING ON YOUR PHONES COMPANYS PAGE OR GOOGLE TO CHECK FOR THE KEYCOMBO OR EXIT COMBO\n, DONT PANIC IF IT DOESNT WORK, KEEP IT ON TILL BATTERY IS 0% AND IT WILL REBOOT TO NORMAL ONCE CHARGED")
		s.run(f"{z} reboot", shell=True)
		continue
	elif user == "driver": print("This is not currently made, dev is working on it for cross-platform without external help..."); continue
	elif user == "fastboot_d connect": s.run(f"{p} reboot fastboot", shell=True); continue
	elif user == "fastboot_d disconnect": print("If the device is stuck on fastbootd without this command working, use vol buttons to navigate through the options and press the option which is related to reboot and shutdown, and then press the power button.\n OR WAIT TILL BATTERY IS 0% THEN CHARGE IT AND THEN OPEN IT AND IT WILL BOOT CORRECTLY"); s.run(f"{z} reboot", shell=True); print("IF THIS TAKES YOU TO BOOTLOADER MODE (FASTBOOT MODE), DO FASTBOOT DISCONNECT command OR USE VOL COMBOS..."); continue
	elif user == "recovery connect": s.run(f"{p} reboot recovery", shell=True); continue
	elif user == "recovery disconnect": print("One way to disconnect is to navigate through the recovery menu and press reboot or shutdown options..."); s.run(f"{p} reboot", shell=True); continue
	elif user == "clear cache": print("This will reboot to bootloader as only rooted devices are able to clear cache while normally working\n, if you have root access (su), then do: 'root clear cache' in the shell..."); s.run(f"{p} reboot fastboot", shell=True); s.run(f"{z} erase cache", shell=True); s.run(f"{z} reboot", shell=True); continue
	elif user == "clear all": print("WARNING: THIS WILL RESET YOUR PHONE, MEANING IT WILL COMPLETELY WIPE YOUR DATA. IF YOU WISH TO PROCEED, TYPE YES, ELSE NO!!!!!"); clearuser()
	elif user == "root test":
		su = s.run(f"{p} shell su -c whoami", capture_output=True, text=True, shell=True)
		if "root" in su.stdout: print("Device has su/root access right now..."); continue
		else: print("No su/root found on the device..."); continue
	elif user == "root clear cache":
		su = s.run(f"{p} shell su -c whoami", capture_output=True, text=True, shell=True)
		if "root" in su.stdout: s.run(f"{p} shell su -c 'rm -rf /cache/*'", shell=True); continue
		else: continue
	elif user == "fastboot unlock":
		print("Still in the makings...")
		continue
	else:
		continue
