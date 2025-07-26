import os

import xbmc


def remove_udevil_rules():
    # Define the path to the udevil rules file
    udevil_rules_path = "/storage/.config/udev.rules.d/95-udevil-mount.rules"

    # Check if the file exists
    if os.path.exists(udevil_rules_path):
        try:
            # Remove the file
            os.remove(udevil_rules_path)
        except Exception as e:
            xbmc.log(f"Failed to remove {udevil_rules_path}: {e}", level=xbmc.LOGERROR)
    else:
        xbmc.log(f"{udevil_rules_path} does not exist", level=xbmc.LOGINFO)
