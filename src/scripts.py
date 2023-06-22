import subprocess
import signal
import time

def end_dolphin():
    program = "dolphin"
    pids = subprocess.check_output(["pgrep", program]).splitlines()
    if len(pids) >= 2:
        pid = int(pids[1])
        child_pid = int(pids[0])
        os.kill(pid, signal.SIGTERM)

def poweroff():
    end_dolphin()
    time.sleep(10)
    subprocess.run(["/usr/bin/systemctl", "poweroff"], check=True)
    return 0

def reboot():
    end_dolphin()
    time.sleep(10)
    subprocess.run(["/usr/bin/systemctl", "reboot"], check=True)
    return 0
