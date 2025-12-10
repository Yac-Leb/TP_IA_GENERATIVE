@echo off
REM Script d'installation automatique Vibeyf-AI pour Windows
echo ========================================
echo   INSTALLATION VIBEYF-AI
echo ========================================
echo.

REM Vérifier Python
echo [1/5] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    echo Telechargez Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Créer l'environnement virtuel
echo [2/5] Creation de l'environnement virtuel...
if exist venv (
    echo Environnement virtuel deja existant
) else (
    python -m venv venv
    echo Environnement virtuel cree
)
echo.

REM Activer l'environnement virtuel
echo [3/5] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)
echo Environnement virtuel active
echo.

REM Installer les dépendances
echo [4/5] Installation des dependances...
echo Cela peut prendre plusieurs minutes...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERREUR: Echec de l'installation des dependances
    pause
    exit /b 1
)
echo Dependances installees avec succes
echo.

REM Créer le fichier .env
echo [5/5] Configuration de l'environnement...
if exist .env (
    echo Fichier .env deja existant
) else (
    copy .env.example .env
    echo Fichier .env cree a partir de .env.example
    echo.
    echo IMPORTANT: Editez .env et ajoutez votre cle API Gemini
    echo Pour obtenir une cle gratuite: https://makersuite.google.com/app/apikey
)
echo.

echo ========================================
echo   INSTALLATION TERMINEE
echo ========================================
echo.
echo Prochaines etapes:
echo   1. Editez .env et ajoutez votre cle API Gemini (optionnel)
echo   2. Activez l'environnement virtuel: venv\Scripts\activate
echo   3. Lancez l'exemple: python main.py
echo.
echo Guide de demarrage: GUIDE_DEMARRAGE.md
echo.
pause
