

![Иллюстрация к проекту](https://github.com/pr0xit-coder/Archangel/blob/main/Archangel-photo.png)

# Archangel OSINT

⚠️ DISCLAIMER ⚠️

***Автор не несет отвественности за ваши действия. Отвественность за всё что вы делаете лежит только на вас.***

📌Archangle OSINT это простая программа с открытым исходным кодом для поиска общедоступной информации для проведения интернет разведок.

# ⚙️ Функции

+ Поиск по номеру
+ Поиск по почте
+ Поиск по IP
+ Поиск по базам
+ Поиск по PayPal
+ Поиск по Instagram
+ Поиск по VIN
+ Поиск по MAC
+ Поиск с помощью ИИ (AI)

## 📁 Папка datab 

**Папка datab** служит для хранения баз данных и поиска по ним. Просто добавьте свои базы в эту папку.

## ✅ Установка

### 🖥️ Установка на Windows

1. Скачайте и установите Python с [Python.org](https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe), если он еще не установлен.
2. Запустите файл `install_win.bat` двойным щелчком.
3. Следуйте инструкциям на экране.
4. Для последующих запусков используйте `start_win.bat`

### 💻 Установка на Linux

1. Убедитесь, что у вас установлен Python. Вы можете проверить это, выполнив команду:

```
python3 --version
```
Если Python не установлен, вы можете установить его с помощью следующей команды (для Ubuntu/Debian):
```
sudo apt update
sudo apt install python3 python3-pip
```

2. Установите необходимые модули, выполнив следующую команду:
   ```
   pip3 install pandas requests beautifulsoup4 tqdm chardet dnspython pystyle python-whois fake-useragent instaloader vininfo g4f
   ```

3. Запусите файл Archangel
   ```
   python3 Archangel.py
   ```

### 📱 Установка на Termux

1. Установите Termux на ваше устройство Android с сайта FDOID [FDROID Termux 0.118.0]https://f-droid.org/repo/com.termux_118.apk
2. Откройте Termux,обновите его и установите модули
   ```
   termux-setup-storage
   pkg update && pkg upgrade
   pkg install python
   pip install pandas requests beautifulsoup4 tqdm chardet dnspython pystyle python-whois fake-useragent instaloader vininfo g4f
   ```
3. Запусите файл Archangel
   ```
   python3 Archangel.py
   ```
## 🪼 Наше Telegram сообщество [pr0xit](https://t.me/+ZLIXp4YJn-0xY2Ey)
