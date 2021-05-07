#!/usr/bin/env bash
# source of script: https://github.com/clulab/tomcat-speech/blob/master/scripts/activate_virtualenv
# This script activates the virtual environment for the project
# creating it if it doesn't exist.
# Usage: ./activate_virtualenv

# Set the ROOT environment variable, assuming that the directory structure
# mirrors that of the git repository.
ROOT="$(cd "$( dirname "${BASH_SOURCE[0]}" )/../" >/dev/null 2>&1 && pwd)"
export ROOT

# Set path to the directory in which we want our virtual environment to live.
VENV_DIR="$ROOT"/.venv
if [[ ! -d "$VENV_DIR" ]]; then
    echo "We did not find the virtual environment directory ${VENV_DIR}."
    echo "Thus, we will create it now."
    python3 -m venv "$VENV_DIR"
fi
echo $VENV_DIR 
. "$VENV_DIR"/bin/activate
