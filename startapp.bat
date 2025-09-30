@echo off
REM -----------------------------------------
REM 1️⃣ Tạo shortcut ra Desktop (chỉ tạo 1 lần)
REM -----------------------------------------

SET SHORTCUT_NAME=CRM.lnk
SET TARGET_PATH=%~dp0startapp.bat
SET ICON_PATH=%~dp0\static\common\favicon.ico
SET DESKTOP=%USERPROFILE%\Desktop

IF NOT EXIST "%DESKTOP%\%SHORTCUT_NAME%" (
    powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\%SHORTCUT_NAME%'); $s.TargetPath='%TARGET_PATH%'; $s.IconLocation='%ICON_PATH%'; $s.Save()"
    echo Shortcut created on Desktop.
)

REM -----------------------------------------
REM 2️⃣ Chạy Flask App
REM -----------------------------------------

REM cd đến thư mục chứa app
cd /d %~dp0

REM activate virtual environment nếu cần
call .env\Scripts\activate.bat

REM chạy Flask app
python main.py

pause
