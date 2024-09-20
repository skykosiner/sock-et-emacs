import subprocess

def Get_main_screen() -> str:
    output = subprocess.check_output(["bash", "-c", "xrandr --query | grep ' connected' | grep primary | awk '{print $1}'"])
    return output.decode().replace("\n", "")
