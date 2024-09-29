import re
import subprocess
import threading

def get_main_screen() -> str:
    output = subprocess.check_output(["bash", "-c", "xrandr --query | grep ' connected' | grep primary | awk '{print $1}'"])
    return output.decode().replace("\n", "")

def start_in_thread(target, daemon=True):
    """Helper to start any target function in a daemon thread."""
    thread = threading.Thread(target=target)
    thread.daemon = daemon
    thread.start()
    return thread

def current_vim_color_scheme() -> str:
    color: str = ""
    with open("/home/sky/.config/nvim/after/plugin/colors.lua") as f:
        last_line = f.readlines()[-1]
        color = re.findall(r'"[^"]+"', last_line)[0]
    return color.strip('"')
