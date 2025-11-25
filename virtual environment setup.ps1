# Requires PowerShell 3.0 or later

# --- Virtual Environment Setup ---
Write-Host "Creating Python virtual environment named 'recipe'..."
python -m venv recipe

# --- Activation ---
# Note: For the activation to affect the current session, this script must be
# 'dot-sourced' when run.
$venvPath = ".\recipe\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."

    # Check if the execution policy allows running scripts.
    # Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned is often required.
    # The user should ensure their environment permits script execution.

    # This line *sources* the script into the current shell's scope.
    # Running this script directly (e.g., .\setup.ps1) WILL NOT activate the venv
    # in the calling terminal session due to PowerShell's scope rules.
    # The user must run it as: . .\setup.ps1 (Note the leading dot and space)
    & $venvPath

} else {
    Write-Host "Error: Could not find activation script at '$venvPath'." -ForegroundColor Red
    exit 1
}

# --- Installation ---
Write-Host "Installing required Python packages..."
# Use the activated python's pip module to ensure packages are installed in the venv
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn mysql-connector-python sqlalchemy

Write-Host "Setup complete! The virtual environment is now active." -ForegroundColor Green
Write-Host "NOTE: To deactivate it, type 'deactivate'."