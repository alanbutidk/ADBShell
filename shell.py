import os
import subprocess as s
import sys
import platform
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

#Starting Info about shell:

print("ADBShell V1.1.0")
print("Made using python 3.13.7")
print("Type 'help' for commands if you are not knowing them!")


def printhelp():
    print("ADBShell V1.0.0")
    print("CSC Means Custom Shell Command")
    print("\nALL COMMANDS ARE ALMOST CASE-SENSETIVE. Commands are:"
        "\n\nhelp = Prints this help screen."
        "\n\nclear/cls = clears the screen."
        "\n\nversion = Prints the version of the SHELL, not adb or fastboot"
        "\n\nserver = enters the server menu, type exit to exit this menu or type start or stop to start/stop the daemon. \nor server start & server stop for no menu."
        "\n\nreboot = reboots the connected device."
        "\n\ncheck = gives the output for device is connected, offline, not connected, device name, device android version etc..."
        "\n\nbattery = outputs the current battery level."
        "\n\nshutdown = self-explanatory..."
        "\n\nfastboot connect = connects to fastboot/bootloader mode"
        "\n\nfastboot disconnect = launches disconnect fastboot ATTEMPT"
        "\n\nfastboot_d connect = sandbox fastboot connect."
        "\n\nfastboot_d disconnect = sandbox fastboot disconnect."
        "\n\nrecovery connect = connects to recovery mode."
        "\n\nrecovery disconnect = disconnects from recovery mode."
        "\n\nclear cache = clears the cache partition."
        "\n\nclear all = same as resetting phone from settings."
        "\n\nroot test = checks for root availiblity."
        "\n\nfastboot unlock = NO LOCKING AVAILIBLITY, Unlocks your bootloader if capable."
        "\n\ngive <FileName> <DeviceLocationToSaveTo> = give is adb push, \n\nfilename is the file on host & DeviceLocationToSaveTo is the location to save the file on the android device\n"
        "\n\ntake <DeviceLocationToTakeTo> <PathToSaveToOnHost> = take is adb pull, \n\nDeviceLocationToTakeTo is the location the file exists on the Android Device & PathToSaveToOnHost is to save onto on the PC/Host.")

#global var(s):

global VERSION
VERSION = "Stable, 1.1.0, Made on HOST: WINDOWS_10 x86_64 with MINGW64 LAYER POSIX, Target: Windows PE Executable Handleable versions (Win 7 <=)"

global filepath
filepath = Path(__file__).parent.resolve().as_posix()

global ext
ext = ".exe" if platform.system() == "Windows" else ""

global p
p = filepath + f"/adb{ext}"

global z
z = filepath + f"/fastboot{ext}"

#end of global vars

def run(cmd):
    return s.run(cmd, capture_output=True, text=True, shell=True).stdout.strip()

def sermenu():
    while True:
        seruser = input("Server Menu; 'start'/'stop': ")
        if seruser == "start": s.run(f"{p} start-server", shell=True); break
        elif seruser == "stop": s.run(f"{p} kill-server", shell=True); break
        elif seruser == "exit": break
#end of function

def unlockboot():
    while True:
        bootunlock = input("yes or no; incase-senstive: ")
        if bootunlock == "yes" or bootunlock == "Yes" or bootunlock == "YES":
            print("You have wished for the device doom, NOW THY SHALL SUFFER!!!!!!!!!!!")
            s.run(f"{p} reboot bootloader", shell=True)
            s.run(f"{z} unlock", shell=True)
        elif bootunlock == "no" or bootunlock == "No" or bootunlock == "NO":
            print("ok i wont doom ur phone!!!!!!!!!!!!!")
            break

def clearuser():
    while True:
        clruser = input("yes or no; incase-senstive: ")
        if clruser == "yes" or clruser == "Yes" or clruser == "YES": 
            print("YES IS DETECTED, ERASING ALL DATA...")
            s.run(f"{p} reboot bootloader", shell=True)
            s.run(f"{z} erase userdata", shell=True)
            continue
        elif clruser == "no" or clruser == "No" or clruser == "NO":
            print("no detected, not deleting ur device data from existence")
            break
        else: print("Wrong command, exiting this 'menu'..."); break

def checksl():
    dsc = s.run(f"{p} devices", capture_output=True, text=True, shell=True)
    output = dsc.stdout.strip().splitlines()
    serial, status = "Unknown", "Not Connected"
    for line in output[1:]:
        if "\t" in line:
            serial, status = line.split("\t")

    print("CSC 'check' called")
    with ThreadPoolExecutor(max_workers=5) as ex:
        f_ver     = ex.submit(run, f"{p} version")
        f_release = ex.submit(run, f"{p} shell getprop ro.build.version.release")
        f_sdk     = ex.submit(run, f"{p} shell getprop ro.build.version.sdk")
        f_model   = ex.submit(run, f"{p} shell getprop ro.product.model")
        f_devname = ex.submit(run, f"{p} shell settings get global device_name")

    print("\nAdb version: ", f_ver.result())
    print("\nDevice Serial: ", serial)
    print("\nDevice Connection Status: ", status)
    print("\nAndroid version (Found through ADB SHELL): ", f_release.result())
    print("\nAndroid SDK Version (also found through adb shell getprop): ", f_sdk.result())
    print("\nDevice Name: ", f_model.result())
    print("\nUser Defined Device name: ", f_devname.result())
#end of function


while True:
    user = input(">>> ")
    if user == "help": printhelp(); continue
    elif user == "clear": os.system("cls") if os.name == "nt" else os.system("clear"); continue
    elif user == "cls": os.system("cls") if os.name == "nt" else os.system("clear"); continue
    elif user == "version": print(f"Details/Version of the shell is currently: {VERSION}"); continue
    elif user == "exit": sys.exit(1); print("Shell Exited"); continue
    elif user == "jajajajaj": print("jajajajaj"); continue
    elif user == "what": print("what do you mean what? (not being rude)"); continue
    elif user == "source code": print("idk where is the src code, probably at https://github.com/alanbutidk/ADBShell"); continue
    elif user == "server": sermenu(); continue
    elif user == "server start": s.run(f"{p} start-server", shell=True); continue
    elif user == "server stop": s.run(f"{p} kill-server", shell=True); continue
    elif user == "reboot": s.run(f"{p} reboot", shell=True); continue
    elif user == "check": checksl(); continue
    elif user == "battery":
        batlvl = s.run(f"{p} dumpsys battery | grep level", shell=True, capture_output=True, text=True).stdout.strip()
        if "level:" in batlvl:
            print(f"Current level from adb shell: {batlvl}")
        continue
    elif user == "shutdown": s.run(f"{p} shell svc power shutdown", shell=True); continue
    elif user == "fastboot connect": s.run(f"{p} reboot bootloader", shell=True); continue
    elif user == "fastboot disconnect":
        print("If the device is stuck on fastboot, please try doing volume button combos like: power + vol up, or power + vol down, \nif this doesnt work. TRY GOING ON YOUR PHONES COMPANYS PAGE OR GOOGLE TO CHECK FOR THE KEYCOMBO OR EXIT COMBO\n, DONT PANIC IF IT DOESNT WORK, KEEP IT ON TILL BATTERY IS 0% AND IT WILL REBOOT TO NORMAL ONCE CHARGED")
        s.run(f"{z} reboot", shell=True)
        continue
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
        s.run(f"{p} shell su -c 'rm -rf /cache/*'", shell=True)
        continue
    elif user == "fastboot unlock":
        print("Reminder that fastboot unlock is NOT RECOMMEND for users that are trying to act like a cool hacker boy, THAT IS LARPING... /nIf you're playing around and entered this command, it can BRICK (Kill your device from ever working) your device!, do you wish to continue?")
        unlockboot()
        continue
    elif "give" in user:
            givelist = user.split()
            s.run(f"{p} push {givelist[1:]} {givelist[2:]}", shell=True, text=True)
    elif "take" in user:
        takelist = user.split()
        s.run(f"{p} pull {takelist[1:]} {takelist[2:]}", shell=True, text=True)
    elif user == "":
        print("Empty command :)")
    else:
        print("Unknown Command recieved!")
        print("\nType 'help' for commands...")
        print("or maybe im not smart enough? :)")
        continue