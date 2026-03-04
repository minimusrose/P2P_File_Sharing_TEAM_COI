@echo off
echo ============================================
echo    Installation P2P File Sharing
echo ============================================
echo.

REM 1. Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans PATH
    echo.
    echo Telechargez Python 3.9+ depuis: https://www.python.org/downloads/
    echo Cochez "Add Python to PATH" pendant l'installation !
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
python --version

REM 2. Verifier version Python (3.9+)
python -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)"
if errorlevel 1 (
    echo [ERREUR] Python 3.9+ requis
    pause
    exit /b 1
)

echo [OK] Version Python compatible
echo.

REM 3. Verifier tkinter
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] tkinter non disponible
    echo tkinter est normalement inclus avec Python Windows
    echo Reinstallez Python en cochant "tcl/tk and IDLE"
    pause
) else (
    echo [OK] tkinter disponible
)

echo.

REM 4. Installer dependances (si requirements.txt existe)
if exist requirements.txt (
    echo [INFO] Installation des dependances...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [AVERTISSEMENT] Certaines dependances ont echoue
        echo Continuez quand meme, tkinter est inclus avec Python
    ) else (
        echo [OK] Dependances installees
    )
) else (
    echo [INFO] Pas de requirements.txt - stdlib uniquement
)

echo.

REM 5. Creer dossiers necessaires
if not exist "data" mkdir data
if not exist "shared_files" mkdir shared_files
if not exist "downloads" mkdir downloads
echo [OK] Dossiers crees (data, shared_files, downloads)

echo.
echo ============================================
echo    Installation terminee !
echo ============================================
echo.
echo Pour lancer l'application:
echo   - Double-cliquez sur run.bat
echo   - Ou tapez: python main.py
echo.
pause
