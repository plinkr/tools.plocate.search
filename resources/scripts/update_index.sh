#!/usr/bin/sh

DEVICE=$1

# Ignore partitions belonging to the same SD, e.g., if using multiboot on your RPi
case "$DEVICE" in
    "/dev/mmcblk0"*)
        exit 0 ;;
esac

# Get the mount point by reading /proc/mounts
MOUNT_POINT=$(grep "$DEVICE" /proc/mounts | awk '{print $2}')

# Get the UUID of the partition
UUID=$(blkid -s UUID -o value "$DEVICE")

# Database path
DB_PATH="/storage/.kodi/addons/tools.plocate.search/resources/databases/${UUID}.db"

# Execute updatedb
if [ -n "$MOUNT_POINT" ]; then
    /storage/.kodi/addons/tools.plocate.search/resources/lib/updatedb --require-visibility no --output "$DB_PATH" --database-root "$MOUNT_POINT"
fi

exit 0
