import os
from Xlib import display, X
import subprocess
import signal
import time

dolphin_process = None

def end_dolphin():
    print("Shutting down dolphin!")
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

def open_x11_application(application_command):
    print("Opening application: " + application_command)
    disp = display.Display(os.environ['DISPLAY'])
    print(disp)
    root = disp.screen().root

    win = root.create_window(
        0, 0, 1, 1,
        0,
        disp.screen().root_depth,
        X.InputOutput,
        X.CopyFromParent,
        event_mask=X.ExposureMask | X.KeyPressMask
    )

    win.map()

    while 1:
        event = disp.next_event()
        if event.type == X.Expose:
            break

    import subprocess
    subprocess.Popen(application_command, shell=True)

    disp.close()

    return ''

def open_and_run_dolphin():
    global dolphin_process

    if dolphin_process is not None and dolphin_process.poll() is None:
        return "Dolphin is already running"

    print('Opening dolphin!')
    dolphin_process = subprocess.Popen(["dolphin-emu"])
    dolphin_process.wait()

    print('Running dolphin command!')
    subprocess.run(["gamemoderun", "mangohud", "dolphin-emu", "-b", "-n", "0000000100000002"])
    return "Command executed successfully"