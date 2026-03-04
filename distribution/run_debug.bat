@echo off
echo ============================================
echo    P2P File Sharing - Mode Debug
echo ============================================
echo.

REM Verifier que installation a ete faite
if not exist "data" (
    echo [ERREUR] Dossier 'data' absent
    echo Lancez install.bat d'abord !
    pause
    exit /b 1
)

echo Lancement P2P File Sharing...
echo (La fenetre de console reste ouverte pour voir les logs)
echo.

python main.py

echo.
echo L'application s'est fermee.
pause
