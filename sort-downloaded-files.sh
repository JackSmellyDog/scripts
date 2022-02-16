#!/bin/sh

TARGET=~/Downloads
PROCESSED=~/Desktop/ 

move_to_depends_on_extension() {
    local current_path="$TARGET/$1"

    case "$1" in
    *.jpg) mv $current_path ~/Pictures/$1 ;;
    *.pgn) mv $current_path ~/Chess Games/$1 ;;
    *) : ;;
    esac
}

inotifywait -m -e create --format "%f" $TARGET | 
    while read FILENAME; do
        echo Detected $FILENAME, moving and zipping
        move_to_depends_on_extension $FILENAME
    done
