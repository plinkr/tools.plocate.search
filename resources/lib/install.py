import os
import shutil
import stat

from resources.config import script_path, plocate_path, updatedb_path, database_dir


def copy_and_modify_udevil_rules(path_to_script):
    # Define source and destination paths
    src = "/usr/lib/udev/rules.d/95-udevil-mount.rules"
    dst_dir = "/storage/.config/udev.rules.d/"
    dst = os.path.join(dst_dir, "95-udevil-mount.rules")

    # Ensure the destination directory exists
    os.makedirs(dst_dir, exist_ok=True)

    # Copy the file
    shutil.copy(src, dst)

    # Read the file and modify the specific line
    with open(dst, 'r') as file:
        lines = file.readlines()

    # Define the old and new lines
    old_line = ("ACTION==\"add\", PROGRAM=\"/usr/bin/sh -c '/usr/bin/grep -E ^/dev/%k\\  /proc/mounts || true'\", "
                "RESULT==\"\", RUN+=\"/usr/bin/systemctl restart udevil-mount@/dev/%k.service\"")
    new_line = (f"ACTION==\"add\", PROGRAM=\"/usr/bin/sh -c '/usr/bin/grep -E ^/dev/%k\\  /proc/mounts || true'\", "
                f"RESULT==\"\", RUN+=\"/usr/bin/systemctl restart udevil-mount@/dev/%k.service\", "
                f"RUN+=\"/usr/bin/systemd-run --on-active=1 /usr/bin/sh {path_to_script} /dev/%k\"")

    # Replace the line in the file
    with open(dst, 'w') as file:
        for line in lines:
            if old_line in line:
                file.write(new_line + '\n')
            else:
                file.write(line)


def make_binary_file_executable(path_to_binary_file):
    # Ensure the binary is executable
    st = os.stat(path_to_binary_file)
    os.chmod(path_to_binary_file, st.st_mode | stat.S_IEXEC)


def create_udev_rules_if_not_exists():
    # Check if the udev rules file exists
    if not os.path.exists("/storage/.config/udev.rules.d/95-udevil-mount.rules"):
        # If doesn't exist, call the function to create it
        copy_and_modify_udevil_rules(script_path)


def check_and_fix_executable_permission():
    """
    Checks the permission of the specified files and makes them executable if they are not.
    """
    # List of file paths to check and modify
    file_paths = [
        script_path,  # Path to the script file
        plocate_path,  # Path to the plocate binary file
        updatedb_path  # Path to the updatedb binary file
    ]

    # Iterate over each file path
    for file_path in file_paths:
        # Check if the file has the executable permission
        if not os.access(file_path, os.X_OK):
            # If not, make the file executable
            make_binary_file_executable(file_path)


def create_database_dir_if_not_exists():
    """
    Checks if the database directory exists and creates it if it does not.
    """
    if not os.path.exists(database_dir):
        os.makedirs(database_dir, exist_ok=True)
