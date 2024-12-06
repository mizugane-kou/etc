@echo off
REM 仮想環境をアクティベート
call "C:\your\path\venv\Scripts\activate.bat"

REM 入力フォルダを取得
python img2psd.py "%1"

REM 仮想環境をディアクティベート
deactivate
