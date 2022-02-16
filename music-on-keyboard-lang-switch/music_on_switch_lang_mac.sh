#!/bin/bash

readonly CHECK_INTERVAL_IN_SECONDS=0.1
readonly SECONDS_TO_PLAY_ANTHEM=5
readonly PATH_TO_ANTHEM_FILE="<PATH_TO_MP3_FILE>"
readonly MATCH_COUNTRY_REGEX=".*[Uu]krainian.*"


while true; do
	prev_lang=$current_lang
	current_lang=$(eval "defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources | egrep -w 'KeyboardLayout Name'")

	if [[ "$current_lang" =~ $MATCH_COUNTRY_REGEX ]]  && ! [[ "$prev_lang" =~ $MATCH_COUNTRY_REGEX ]]; then
		afplay -t $SECONDS_TO_PLAY_ANTHEM $PATH_TO_ANTHEM_FILE
	fi

	sleep $CHECK_INTERVAL_IN_SECONDS
done
