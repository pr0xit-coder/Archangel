@echo off
chcp 65001 > nul

python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python не установлен.
    echo Скачайте Python с https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe
    pause
    exit /b
)

echo Удаление старого модуля whois...
pip uninstall -y whois
echo Удаление модуля python-whois...
pip uninstall -y python-whois

echo Установка необходимых модулей...
pip install pandas requests beautifulsoup4 tqdm chardet dnspython pystyle python-whois fake-useragent instaloader vininfo g4f

echo Установка завершена.

echo Запуск скрипта в новом окне с заданными размерами...

start "" /max cmd /c "mode con: cols=300 lines=300 && python main.py"

pause
