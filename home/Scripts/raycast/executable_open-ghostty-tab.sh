#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Open Ghostty Tab
# @raycast.mode silent
# @raycast.packageName Ghostty
# @raycast.icon 👻
# @raycast.description Launch Ghostty, or add a tab in your home folder if it is already running.

# Sending a folder during launch can create a second tab after the startup tab.
/usr/bin/pgrep -x ghostty >/dev/null
ghostty_status=$?

case "$ghostty_status" in
  0) exec /usr/bin/open -a /Applications/Ghostty.app "$HOME" ;;
  1) exec /usr/bin/open -a /Applications/Ghostty.app ;;
  *) echo "Could not check whether Ghostty is running." >&2; exit "$ghostty_status" ;;
esac
