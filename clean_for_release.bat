@echo off
REM Script pour preparer l'archive de distribution
REM Nettoie tous les fichiers temporaires et de developpement

echo ============================================
echo    Preparation Archive Distribution
echo ============================================
echo.

REM 1. Nettoyer les donnees utilisateur
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

REM 2. Nettoyer __pycache__
echo.
echo Nettoyage des fichiers Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
echo [OK] Fichiers __pycache__ et .pyc supprimes

REM 3. Nettoyer fichiers de test
del /q .coverage 2>nul
if exist ".pytest_cache" rmdir /S /Q .pytest_cache 2>nul
echo [OK] Fichiers de test nettoyes

REM 4. Nettoyer fichiers Git (optionnel)
REM Si vous voulez exclure .git de l'archive, decommentez:
REM if exist ".git" rmdir /S /Q .git
REM echo [OK] Dossier .git supprime

echo.
echo ============================================
echo    Nettoyage termine !
echo ============================================
echo.
echo Fichiers prets pour archivage.
echo.
echo Pour creer l'archive ZIP:
echo   1. Selectionnez tous les fichiers
echo   2. Clic droit ^> Envoyer vers ^> Dossier compresse
echo   3. Nommez: p2p_file_sharing_v1.0.zip
echo.
pause
