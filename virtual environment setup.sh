#!/bin/bash

# --- Virtual Environment Setup ---
echo "Creating Python virtual environment named 'recipe'..."
python3 -m venv recipe

# --- Activation ---
# Determine the correct activation script path based on the OS structure
# Linux/macOS uses recipe/bin/activate
# Git Bash on Windows uses recipe/Scripts/activate (though sometimes /bin/ also works)
if [ -f "recipe/bin/activate" ]; then
    echo "Activating virtual environment (Linux/macOS style)..."
    source recipe/bin/activate
elif [ -f "recipe/Scripts/activate" ]; then
    echo "Activating virtual environment (Windows/Git Bash style)..."
    source recipe/Scripts/activate
else
    echo "Error: Could not find 'activate' script in 'recipe/bin' or 'recipe/Scripts'."
    exit 1
fi

# --- Installation ---
echo "Installing required Python packages..."
# Use python3 -m pip to ensure the correct pip is used and upgrade it first.
python3 -m pip install --upgrade pip
# Install all packages in a single command.
python3 -m pip install fastapi uvicorn mysql-connector-python sqlalchemy

echo "Setup complete! The virtual environment is now active."
echo "To deactivate it, type 'deactivate'."