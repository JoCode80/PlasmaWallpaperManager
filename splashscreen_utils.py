import os
import subprocess
import shutil
import json
from PIL import Image, ImageFilter

def update_splashscreen_theme(image_path):
    # Paths
    config_file = os.path.expanduser("~/.config/ksplashrc")
    local_look_and_feel_dir = os.path.expanduser("~/.local/share/plasma/look-and-feel/")
    global_look_and_feel_dir = "/usr/share/plasma/look-and-feel/"
    custom_theme_name = "CustomTheme"

    # Read the current theme from the configuration file
    if not os.path.exists(config_file):
        print("Configuration file ksplashrc not found.")
        return False

    with open(config_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Theme="):
                current_theme = line.split("=")[1].strip()
                break
        else:
            print("No valid theme found in ksplashrc.")
            return False

    # Source and destination for copying the theme
    source_dir = os.path.join(local_look_and_feel_dir, current_theme)
    if not os.path.exists(source_dir):
        source_dir = os.path.join(global_look_and_feel_dir, current_theme)

    target_dir = os.path.join(local_look_and_feel_dir, custom_theme_name)

    # If the target directory already exists and the current theme is "CustomTheme", no copying is needed
    if current_theme == custom_theme_name and os.path.exists(target_dir):
        print("CustomTheme is already active. No copying required.")
    else:
        if not os.path.exists(source_dir):
            print(f"The current theme directory {source_dir} was not found.")
            return False

        # Create the target directory if it doesn't exist
        os.makedirs(local_look_and_feel_dir, exist_ok=True)

        # Copy the theme
        try:
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)  # Remove the old CustomTheme
            shutil.copytree(source_dir, target_dir)
            print(f"Theme successfully copied to {target_dir}.")
        except Exception as e:
            print(f"Error copying the theme: {e}")
            return False

    # Modify metadata.json
    if not modify_metadata_json():
        return False

    # Update the splashscreen background
    if not update_splashscreen_background(image_path):
        return False

    # Set the new theme in ksplashrc
    if not set_new_theme_in_config(config_file, custom_theme_name):
        return False

    print("Splashscreen theme successfully updated.")
    return True

def modify_metadata_json():
    # Path to the metadata.json file in the CustomTheme
    metadata_file = os.path.expanduser("~/.local/share/plasma/look-and-feel/CustomTheme/metadata.json")

    if not os.path.exists(metadata_file):
        print(f"The file {metadata_file} was not found.")
        return False

    # Open the file and load the contents
    with open(metadata_file, "r") as file:
        data = json.load(file)

    # Modify the content
    data["KPlugin"]["Authors"] = [{"Name": "NA"}]
    data["KPlugin"]["Description"] = "Custom Theme"
    data["KPlugin"]["Id"] = "CustomTheme"
    data["KPlugin"]["Name"] = "Custom Theme"
    data["KPlugin"]["Name[x-test]"] = "xxCustom Themexx"
    data["KPlugin"]["Website"] = "NA"

    # Save the changes
    try:
        with open(metadata_file, "w") as file:
            json.dump(data, file, indent=4)
        print("metadata.json successfully modified.")
        return True
    except Exception as e:
        print(f"Error saving the file: {e}")
        return False

def convert_to_png_with_pillow(image_path):
    # Destination paths for the PNG image
    png_image_path = os.path.expanduser("~/.local/share/plasma/look-and-feel/CustomTheme/contents/splash/images/background.png")
    preview_image_path = os.path.expanduser("~/.local/share/plasma/look-and-feel/CustomTheme/contents/previews/splash.png")

    try:
        # Open the image
        image = Image.open(image_path)

        # Apply a blur filter to the image
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))

        # Save the image as PNG (main image)
        blurred_image.save(png_image_path, format="PNG")
        print(f"Image successfully converted to PNG with Pillow and saved as {png_image_path}.")

        # Save the image as PNG (preview image)
        blurred_image.save(preview_image_path, format="PNG")
        print(f"Image also successfully saved as preview at {preview_image_path}.")

        return True

    except Exception as e:
        print(f"Error converting the image with Pillow: {e}")
        return False

def update_splashscreen_background(image_path):
    # First convert the image to PNG if necessary
    if not convert_to_png_with_pillow(image_path):
        return False  # If the conversion fails, abort the process

    # Note: No need to copy the original image again, as the conversion already created the target image
    print("The splashscreen background image has been successfully updated.")
    return True

def set_new_theme_in_config(config_file, theme_name):
    try:
        # Read the content of the configuration file
        with open(config_file, "r") as file:
            lines = file.readlines()

        # Set the new theme in the config file
        with open(config_file, "w") as file:
            for line in lines:
                if line.startswith("Theme="):
                    file.write(f"Theme={theme_name}\n")
                else:
                    file.write(line)

        print(f"The new theme '{theme_name}' has been set in {config_file}.")
        return True
    except Exception as e:
        print(f"Error setting the new theme: {e}")
        return False
