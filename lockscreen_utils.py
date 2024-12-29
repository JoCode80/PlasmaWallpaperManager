import os

def update_lockscreen_background(image_path):
    # Define the path to the configuration file for the lock screen
    config_path = os.path.expanduser("~/.config/kscreenlockerrc")

    # Check if the configuration file exists
    if not os.path.exists(config_path):
        print(f"Configuration file {config_path} not found.")
        return False

    try:
        # Read the current configuration file
        with open(config_path, 'r') as file:
            lines = file.readlines()

        # Write the new image path into the configuration file
        with open(config_path, 'w') as file:
            for line in lines:
                if line.startswith("Image="):
                    file.write(f"Image={image_path}\n")
                elif line.startswith("PreviewImage="):
                    file.write(f"PreviewImage={image_path}\n")
                else:
                    file.write(line)

        # Return True if the update was successful
        return True
    except Exception as e:
        # Handle any exceptions and print an error message
        print(f"Error updating the file {config_path}: {e}")
        return False
