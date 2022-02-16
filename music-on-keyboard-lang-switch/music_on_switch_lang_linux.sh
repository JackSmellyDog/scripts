#!/bin/bash

# The program which is used to get current language is 'xkblayout-state'.
# Its original repo: https://github.com/nonpop/xkblayout-state

readonly UA="ua"
readonly CHECK_INTERVAL_IN_SECONDS=0.1
readonly SECONDS_TO_PLAY=5
readonly PATH_TO_FILE="<PATH_TO_MP3_FILE>"

prev_lang=""
current_lang=""

while true; do
    prev_lang=$current_lang
    current_lang=$(eval "./xkblayout-state print \"%s\"")

    if [ "$current_lang" != "$prev_lang" ] && [ "$current_lang" = "$UA" ]; then
        ffplay -t $SECONDS_TO_PLAY $PATH_TO_FILE -nodisp -autoexit 2> /dev/null
    fi

    sleep $CHECK_INTERVAL_IN_SECONDS
done
