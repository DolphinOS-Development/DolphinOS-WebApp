import os

def poweroff():
    os.system("systemctl poweroff")
    return 0

def reboot():
    os.system("systemctl reboot")
    return 0
