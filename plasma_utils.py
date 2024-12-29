
import subprocess

def set_plasma_background(image_path):
    try:
        subprocess.run(['plasma-apply-wallpaperimage', image_path], check=True)
    except subprocess.CalledProcessError:
        print("An error occurred while changing the Plasma background.")
