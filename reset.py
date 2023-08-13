import subprocess
import os

# Expanding the ~ to the full path of the user's home directory
plist_path = os.path.expanduser("~/Library/LaunchAgents/PLISTFILENAME")

subprocess.run(["launchctl", "unload", plist_path])
subprocess.run(["launchctl", "load", plist_path])