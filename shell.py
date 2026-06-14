import os
import subprocess as s
import sys
import platform
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# ANSI / VT color codes enable (smart trick isnt it?)
os.system("")

red  = "\x1b[31m"
ylw  = "\x1b[33m"
grn  = "\x1b[32m"
cyn  = "\x1b[36m"
wht  = "\x1b[97m"
bold = "\x1b[1m"
rst  = "\x1b[0m"

print(f"{bold}{wht}ADBShell v1.1.1{rst}")
print("Made using python 3.13.7")
print(f"Type {ylw}'help'{rst} for commands if you are not familiar with them.")


def printhelp():
    print(f"{bold}{wht}ADBShell v1.1.1{rst}")
    print("CSC Means Custom Shell Command")
    print(
        f"\n{ylw}ALL COMMANDS ARE ALMOST CASE-SENSITIVE. Commands are:"
        "\nhelp                        = Prints this help screen."
        "\nclear / cls                 = Clears the screen."
        "\nversion                     = Prints the version of the shell."
        "\nserver                      = Opens the server menu. Type 'start', 'stop', or 'exit'."
        "\nserver start / server stop  = Start or stop the ADB daemon directly."
        "\nreboot                      = Reboots the connected device."
        "\ncheck                       = Displays device connection status, model, Android version, etc."
        "\nbattery                     = Displays the current battery level."
        "\nshutdown                    = Powers off the connected device."
        "\nfastboot connect            = Reboots the device into bootloader (fastboot) mode."
        "\nfastboot disconnect         = Attempts to exit fastboot mode."
        "\nfastboot_d connect          = Reboots the device into fastbootd (userspace fastboot) mode."
        "\nfastboot_d disconnect       = Attempts to exit fastbootd mode."
        "\nrecovery connect            = Reboots the device into recovery mode."
        "\nrecovery disconnect         = Exits recovery mode."
        "\nclear cache                 = Clears the cache partition via fastboot."
        "\nclear all                   = Performs a full factory reset (wipes all user data)."
        "\nroot test                   = Checks whether root (su) access is available on the device."
        "\nfastboot unlock             = Unlocks the bootloader. This operation is destructive and irreversible on many devices."
        "\ngive <FileName> <DevicePath> = Pushes a file from the host to the specified path on the device (adb push)."
        f"\ntake <DevicePath> <HostPath> = Pulls a file from the device to the specified path on the host (adb pull).{rst}")


# Global variables

VERSION = "ADBShell v1.1.1"
if getattr(sys, 'frozen', False):
    filepath = Path(sys.executable).parent.resolve().as_posix()
else:
    filepath = Path(__file__).parent.resolve().as_posix()
ext = ".exe" if platform.system() == "Windows" else ""

p = filepath + f"/adb{ext}"

z = filepath + f"/fastboot{ext}"


def run(cmd_list, **kwargs):
    result = s.run(cmd_list, capture_output=True, text=True, **kwargs)
    return result.stdout.strip()


def sermenu():
    while True:
        seruser = input("Server Menu; \"start\" / \"stop\" / \"exit\": ").strip()
        if seruser == "start":
            s.run([p, "start-server"])
            print(f"{grn}ADB server started.{rst}")
            break
        elif seruser == "stop":
            s.run([p, "kill-server"])
            print(f"{ylw}ADB server stopped.{rst}")
            break
        elif seruser == "exit":
            break
        else:
            print(f"{ylw}Unrecognized input. Enter 'start', 'stop', or 'exit'.{rst}")


def unlockboot():
    while True:
        bootunlock = input("Confirm (yes / no): ").strip().lower()
        if bootunlock == "yes":
            print(f"\n{red}{bold}Confirmed. Rebooting to bootloader and issuing unlock command.{rst}")
            s.run([p, "reboot", "bootloader"])
            s.run([z, "flashing", "unlock"])
        elif bootunlock == "no":
            print(f"\n{ylw}Operation cancelled. No changes were made.{rst}")
            break
        else:
            print(f"{ylw}Invalid input. Enter 'yes' or 'no'.{rst}")


def clearuser():
    while True:
        try:
            clruser = input("Confirm (yes / no): ").strip().lower()
            if clruser == "yes":
                print(f"\n{red}{bold}Confirmed. Rebooting to bootloader and erasing user data.{rst}")
                s.run([p, "reboot", "bootloader"])
                s.run([z, "erase", "userdata"])
                break
            elif clruser == "no":
                print(f"\n{ylw}Operation cancelled. No changes were made.{rst}")
                break
            else:
                print(f"{ylw}Invalid input. Exiting.{rst}")
                break
        except (ValueError, OSError):
            print(f"\n{red}A ValueError or OSError occurred. Exiting.{rst}")


def checksl():
    dsc = s.run([p, "devices"], capture_output=True, text=True)
    output = dsc.stdout.strip().splitlines()
    serial, status = "Unknown", "Not Connected"
    for line in output[1:]:
        if "\t" in line:
            serial, status = line.split("\t", 1)

    print(f"{cyn}CSC 'check' called{rst}")
    with ThreadPoolExecutor(max_workers=5) as ex:
        f_ver     = ex.submit(run, [p, "version"])
        f_release = ex.submit(run, [p, "shell", "getprop", "ro.build.version.release"])
        f_sdk     = ex.submit(run, [p, "shell", "getprop", "ro.build.version.sdk"])
        f_model   = ex.submit(run, [p, "shell", "getprop", "ro.product.model"])
        f_devname = ex.submit(run, [p, "shell", "settings", "get", "global", "device_name"])

    print(f"\n{wht}ADB version:{rst}                   ", f_ver.result())
    print(f"\n{wht}Device serial:{rst}                 ", serial)
    print(f"\n{wht}Device connection status:{rst}      ", status)
    print(f"\n{wht}Android version:{rst}               ", f_release.result())
    print(f"\n{wht}Android SDK version:{rst}           ", f_sdk.result())
    print(f"\n{wht}Device model:{rst}                  ", f_model.result())
    print(f"\n{wht}User-defined device name:{rst}      ", f_devname.result())


# Main loop
try:
    while True:
        user = input(">>> ").strip()

        if user == "help":
            printhelp()

        elif user in ("clear", "cls"):
            s.run(["cls" if os.name == "nt" else "clear"], shell=True)

        elif user == "version":
            print(f"{cyn}Shell version: {VERSION}{rst}")

        elif user == "exit":
            print("Shell exited.")
            sys.exit(0)

        elif user == "server":
            sermenu()

        elif user == "server start":
            s.run([p, "start-server"])
            print(f"{grn}ADB server started.{rst}")

        elif user == "server stop":
            s.run([p, "kill-server"])
            print(f"{ylw}ADB server stopped.{rst}")

        elif user == "reboot":
            s.run([p, "reboot"])

        elif user == "check":
            checksl()

        elif user == "battery":
            batlvl = s.run([p, "shell", "dumpsys", "battery"], capture_output=True, text=True).stdout
            for line in batlvl.splitlines():
                if "level:" in line:
                    print(f"{grn}Current battery level: {line.strip()}{rst}")
                    break

        elif user == "shutdown":
            s.run([p, "shell", "svc", "power", "shutdown"])

        elif user == "fastboot connect":
            s.run([p, "reboot", "bootloader"])

        elif user == "fastboot disconnect":
            print(
                f"{ylw}{bold}NOTICE:{rst} If the device does not respond to this command, use the hardware key combination "
                "specified in your device manufacturer's documentation to exit fastboot mode manually. "
                "If no combination is effective, allow the battery to fully discharge. "
                "The device will boot normally once power is restored."
            )
            s.run([z, "reboot"])

        elif user == "fastboot_d connect":
            s.run([p, "reboot", "fastboot"])

        elif user == "fastboot_d disconnect":
            print(
                f"{ylw}{bold}NOTICE:{rst} If this command does not exit fastbootd, use the hardware volume keys "
                "to navigate to the reboot or shutdown option in the menu and confirm with the power button. "
                "If the device remains unresponsive, allow the battery to discharge fully. "
                "The device will boot normally once power is restored. "
                f"{ylw}If the device returns to standard fastboot mode, run 'fastboot disconnect' or use the appropriate key combination.{rst}"
            )
            s.run([z, "reboot"])

        elif user == "recovery connect":
            s.run([p, "reboot", "recovery"])

        elif user == "recovery disconnect":
            print(
                f"{cyn}Navigate to the reboot or shutdown option within the recovery menu to exit recovery mode.{rst}"
            )
            s.run([p, "reboot"])

        elif user == "clear cache":
            print(
                f"{ylw}{bold}NOTICE:{rst} Clearing the cache partition requires a reboot to bootloader. "
                "Devices without root access must use fastboot for this operation. "
                "To clear cache while the device is running, use the 'root clear cache' command if root access is available."
            )
            s.run([p, "reboot", "fastboot"])
            s.run([z, "erase", "cache"])
            s.run([z, "reboot"])

        elif user == "clear all":
            print(
                f"\n{red}{bold}WARNING: DESTRUCTIVE OPERATION{rst}\n"
                f"{red}This command will perform a complete factory reset, permanently erasing all user data, "
                "applications, and settings on the connected device. This action cannot be undone.\n"
                f"Ensure all critical data has been backed up before proceeding.{rst}\n"
            )
            clearuser()

        elif user == "root test":
            su = s.run([p, "shell", "su", "-c", "whoami"], capture_output=True, text=True)
            if "root" in su.stdout:
                print(f"{grn}Root (su) access is available on this device.{rst}")
            else:
                print(f"{ylw}Root (su) access was not detected on this device.{rst}")

        elif user == "root clear cache":
            su = s.run([p, "shell", "su", "-c", "whoami"], capture_output=True, text=True)
            if "root" in su.stdout:
                s.run([p, "shell", "su", "-c", "rm -rf /cache/*"])
                print(f"{grn}Cache cleared via root.{rst}")
            else:
                print(f"{red}Root access is required to perform this operation.{rst}")

        elif user == "fastboot unlock":
            print(
                f"\n{red}{bold}WARNING: DESTRUCTIVE OPERATION{rst}\n"
                f"{red}Unlocking the bootloader will trigger a factory reset on most devices, permanently erasing all user data. "
                "On some devices this action is irreversible and may void the manufacturer warranty. "
                "Certain devices do not support bootloader unlocking and may become inoperable if this command is issued. "
                "This tool does not provide a re-lock option.\n"
                f"Ensure all critical data has been backed up and that your device supports this operation before proceeding.{rst}\n"
            )
            unlockboot()

        elif user.startswith("give "):
            parts = user.split()
            if len(parts) >= 3:
                s.run([p, "push", parts[1], parts[2]])
            else:
                print(f"{ylw}Usage: give <FileName> <DevicePath>{rst}")

        elif user.startswith("take "):
            parts = user.split()
            if len(parts) >= 3:
                s.run([p, "pull", parts[1], parts[2]])
            else:
                print(f"{ylw}Usage: take <DevicePath> <HostPath>{rst}")

        elif user == "":
            print(f"{ylw}No command entered.{rst}")

        else:
            print(f"{red}Unrecognized command.{rst}")
            print("Type 'help' for a list of available commands.")
except KeyboardInterrupt:
    print(f"{red}Stopped operation without closing server. Please close server if you are exiting!{rst}")
except (OSError, FileNotFoundError):
    print(f"{red}Couldn't resolve file or internal OSError!{rst}")
