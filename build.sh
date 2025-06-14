#!/bin/bash

GAME_NAME="Dont Get Caught"
MAIN_SCRIPT="main.py"
GAME_ICON="icon.ico"

# --- PyInstaller Command ---
echo ""
echo "Building ${GAME_NAME} with PyInstaller..."
echo ""

pyinstaller "${MAIN_SCRIPT}" \
    --noconsole \
    --name run \
    --onefile \
    --windowed \
    --icon="${GAME_ICON}" \


echo ""
echo "Copying assets to dist folder..."
echo ""

mkdir -p ./dist/src/assets
cp -r ./src/assets ./dist/src

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: PyInstaller build failed!"
    echo ""
else
    echo ""
    echo "PyInstaller build successful!"
    echo "Check the \"dist\" folder for your executable."
    echo ""
fi