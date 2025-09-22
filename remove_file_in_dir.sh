#!/bin/bash
# Script to recursively delete all files named FILENAMERM inside DIRRM

# --- User-defined variables ---
# FILENAMERM="I125Beam_PHSP.phsp"   # name of the file to remove
FILENAMERM="Foci*"
DIRRM="./work" # directory where search and deletion will happen

# --- Safety checks ---
if [ -z "$FILENAMERM" ] || [ -z "$DIRRM" ]; then
    echo "Error: FILENAMERM and DIRRM must be set."
    exit 1
fi

if [ ! -d "$DIRRM" ]; then
    echo "Error: Directory $DIRRM does not exist."
    exit 1
fi

# --- Perform deletion ---
echo "Searching for files named '$FILENAMERM' inside '$DIRRM' ..."
find "$DIRRM" -type f -name "$FILENAMERM" -exec rm -v {} +

echo "Done."
