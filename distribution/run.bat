@echo off

REM Verifier que installation a ete faite
if not exist "data" (
    echo [ERREUR] Dossier 'data' absent
    echo Lancez install.bat d'abord !
    pause
    exit /b 1
)

REM Lancer avec pythonw (pas de console) si disponible
where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start pythonw main.py
) else (
    REM Fallback sur python normal
    start python main.py
)

REM Note: start detache le processus
