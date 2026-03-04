@echo off
echo ============================================
echo    Desinstallation P2P File Sharing
echo ============================================
echo.
echo ATTENTION: Cette operation va supprimer:
echo   - Le dossier 'data' (base de donnees et logs)
echo   - Le dossier 'shared_files' (fichiers partages)
echo   - Le dossier 'downloads' (fichiers telecharges)
echo.
echo Les fichiers source du programme seront conserves.
echo.

pause

if exist "data" (
    rmdir /S /Q data
    echo [OK] Dossier 'data' supprime
)

if exist "shared_files" (
    rmdir /S /Q shared_files
    echo [OK] Dossier 'shared_files' supprime
)

if exist "downloads" (
    rmdir /S /Q downloads
    echo [OK] Dossier 'downloads' supprime
)

echo.
echo ============================================
echo    Desinstallation terminee !
echo ============================================
echo.
echo Pour reinstaller, lancez: install.bat
echo.
pause
