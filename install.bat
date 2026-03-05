@echo off
setlocal EnableDelayedExpansion
set "ERROR_FOUND=0"
set "PYTHON_CMD=python"

echo ============================================
echo    INSTALLATEUR AUTOMATIQUE
echo    P2P File Sharing
echo ============================================
echo.
echo Cet installateur va automatiquement:
echo  - Detecter/installer Python
echo  - Configurer l'environnement
echo  - Installer les dependances
echo.
echo Vous devrez juste repondre Oui (O) ou Non (N)
echo.
pause

REM ============================================
REM ETAPE 1: DETECTION ET INSTALLATION PYTHON
REM ============================================
echo.
echo [1/5] Detection de Python...
echo.

REM Essayer differentes commandes Python
python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :python_found
)

py --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    goto :python_found
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python3"
    goto :python_found
)

REM Python non trouve - Proposer installation
echo [!] Python n'est pas detecte sur ce PC
echo.
echo Voulez-vous telecharger et installer Python automatiquement ?
echo.
choice /C ON /N /M "[O] Oui, telecharger Python    [N] Non, annuler: "
if errorlevel 2 (
    echo.
    echo Installation annulee par l'utilisateur.
    set "ERROR_FOUND=1"
    goto :end
)

echo.
echo Telechargement de Python en cours...
echo Ouverture de la page de telechargement officielle...
echo.
echo INSTRUCTIONS IMPORTANTES:
echo 1. Telechargez Python 3.9 ou superieur
echo 2. Lancez l'installateur telecharge
echo 3. COCHEZ "Add Python to PATH" (TRES IMPORTANT!)
echo 4. Cliquez sur "Install Now"
echo 5. Revenez ici une fois l'installation terminee
echo.
start https://www.python.org/downloads/
echo.
echo Appuyez sur une touche une fois Python installe...
pause >nul

REM Verifier a nouveau apres installation
python --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    echo.
    echo [OK] Python detecte avec succes!
    goto :python_found
)

py --version >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py"
    echo.
    echo [OK] Python detecte avec succes!
    goto :python_found
)

echo.
echo [INFO] Python n'est pas encore detecte dans ce terminal.
echo.
echo C'est NORMAL : apres l'installation de Python,
echo le terminal doit etre redemarre pour recharger le PATH.
echo.
echo Voulez-vous relancer automatiquement ce script
echo dans un nouveau terminal ?
echo.
choice /C ON /N /M "[O] Oui, relancer    [N] Non, je ferai manuellement: "
if errorlevel 2 (
    echo.
    echo Tres bien ! Fermez ce terminal et relancez install.bat
    echo.
    set "ERROR_FOUND=1"
    goto :end
)

echo.
echo Relancement du script dans un nouveau terminal...
echo Fermez ce terminal apres avoir vu le nouveau s'ouvrir.
echo.
timeout /t 2 >nul
start "" "%~f0"
exit

:python_found
echo [OK] Python detecte: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM ============================================
REM ETAPE 2: VERIFICATION VERSION PYTHON
REM ============================================
echo [2/5] Verification de la version Python...
%PYTHON_CMD% -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] Python 3.9+ recommande
    echo Version actuelle:
    %PYTHON_CMD% --version
    echo.
    echo Voulez-vous continuer quand meme?
    choice /C ON /N /M "[O] Oui, continuer    [N] Non, annuler: "
    if errorlevel 2 (
        set "ERROR_FOUND=1"
        goto :end
    )
) else (
    echo [OK] Version compatible (3.9+)
)
echo.

REM ============================================
REM ETAPE 3: VERIFICATION TKINTER
REM ============================================
echo [3/5] Verification de tkinter (interface graphique)...
%PYTHON_CMD% -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo [AVERTISSEMENT] tkinter non disponible
    echo.
    echo tkinter est necessaire pour l'interface graphique.
    echo Il est normalement inclus avec Python sur Windows.
    echo.
    echo Solution: Reinstallez Python et cochez "tcl/tk and IDLE"
    echo.
    echo Voulez-vous continuer sans interface graphique?
    choice /C ON /N /M "[O] Oui, continuer    [N] Non, annuler: "
    if errorlevel 2 (
        set "ERROR_FOUND=1"
        goto :end
    )
) else (
    echo [OK] tkinter disponible
)

echo.

REM ============================================
REM ETAPE 4: INSTALLATION DEPENDANCES
REM ============================================
echo [4/5] Installation des dependances Python...
if exist requirements.txt (
    echo.
    echo Les dependances vont etre installees automatiquement.
    echo Cela peut prendre quelques minutes...
    echo.
    choice /C ON /N /M "Continuer? [O] Oui    [N] Non: "
    if errorlevel 2 (
        echo Installation des dependances ignoree
        goto :create_folders
    )
    
    echo.
    echo Mise a jour de pip...
    %PYTHON_CMD% -m pip install --upgrade pip --quiet
    
    echo Installation des packages...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [AVERTISSEMENT] Certaines dependances ont echoue
        echo L'application peut quand meme fonctionner avec tkinter
        echo.
    ) else (
        echo [OK] Toutes les dependances sont installees
    )
) else (
    echo [INFO] Pas de requirements.txt trouve
    echo L'application utilisera uniquement les modules standards
)

echo.

REM ============================================
REM ETAPE 5: CREATION DOSSIERS
REM ============================================
:create_folders
echo [5/5] Creation des dossiers necessaires...
if not exist "data" mkdir data
if not exist "shared_files" mkdir shared_files
if not exist "downloads" mkdir downloads
echo [OK] Dossiers crees:
echo     - data/         (base de donnees)
echo     - shared_files/ (fichiers partages)
echo     - downloads/    (telechargements)

echo.

:end
if "!ERROR_FOUND!"=="1" (
    echo.
    echo ============================================
    echo    Installation ECHOUEE - Erreurs detectees
    echo ============================================
    echo.
    echo Veuillez corriger les erreurs ci-dessus
    echo et relancer l'installation.
    echo.
) else (
    echo ============================================
    echo    Installation REUSSIE !
    echo ============================================
    echo.
    echo L'application est prete a etre utilisee!
    echo.
    echo Pour lancer l'application:
    echo   - Double-cliquez sur run.bat
    echo   - Ou executez: %PYTHON_CMD% main.py
    echo.
    echo Voulez-vous lancer l'application maintenant?
    choice /C ON /N /M "[O] Oui, lancer    [N] Non, quitter: "
    if not errorlevel 2 (
        echo.
        echo Lancement de l'application...
        start run.bat
    )
)

echo.
echo Appuyez sur une touche pour fermer...
pause >nul
