import subprocess

THEME_NAME = "CustomTheme"
ORIGINAL_THEME = "/usr/share/sddm/themes/breath"
THEME_DIR = f"/usr/share/sddm/themes/{THEME_NAME}"
CONFIG_FILE = "/etc/sddm.conf.d/kde_settings.conf"

def create_and_activate_sddm_theme(image_path, password):
    metadata_file = f"{THEME_DIR}/metadata.desktop"

    try:
        # Create the theme directory with sudo
        subprocess.run(['sudo', '-S', 'mkdir', '-p', THEME_DIR], input=password + "\n", text=True, check=True)

        # Copy the files from the original theme to the new theme directory
        subprocess.run(['sudo', '-S', 'cp', '-r', f"{ORIGINAL_THEME}/.", THEME_DIR], input=password + "\n", text=True, check=True)

        # Generate the metadata.desktop content
        metadata_content = f"""[SddmGreeterTheme]
Name={THEME_NAME}
Description={THEME_NAME}
Comment=Custom SDDM Theme
Type=sddm-theme
Screenshot=background.png
MainScript=Main.qml
ConfigFile=theme.conf
Theme-Id={THEME_NAME}
QtVersion=6
"""

        # Write metadata to the file with sudo (using tee to redirect input to the file) and suppress output
        subprocess.run(['sudo', '-S', 'tee', metadata_file], input=metadata_content, text=True, check=True, stdout=subprocess.DEVNULL)

        # Copy the selected background image into the theme folder with sudo
        subprocess.run(['sudo', '-S', 'cp', image_path, f"{THEME_DIR}/background.png"], input=password + "\n", text=True, check=True)

        # Remove any user-specific configuration file and update the theme's background in the config
        subprocess.run(['sudo', 'rm', '-f', f"{THEME_DIR}/theme.conf.user"], check=True)
        subprocess.run(['sudo', 'sed', '-i', f"s|^background=.*|background={THEME_DIR}/background.png|", f"{THEME_DIR}/theme.conf"], check=True)

        # Update the system's SDDM configuration to use the new theme
        subprocess.run(['sudo', '-S', 'sed', '-i', f"s|^Current=.*|Current={THEME_NAME}|", CONFIG_FILE], input=password + "\n", text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating or activating the SDDM theme: {e}")
        return

    except Exception as e:
        print(f"Unexpected error: {e}")
