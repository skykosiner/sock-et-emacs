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
