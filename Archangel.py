import time
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import chardet  
import os
import dns.resolver
import whois
import re
from pystyle import Colors, Center, Box, Anime, Write, System
from pystyle import Colors, Colorate
from fake_useragent import UserAgent
import instaloader
from instaloader import Instaloader
from vininfo import Vin
import xml.etree.ElementTree as ET
import asyncio
import itertools
from g4f.client import Client

logo = """                                 
                  ▓██████████████████░                        
              ▒████▓              ▒██████████████▓░           
            ░████           ▒███████▓            ▓█████       
      ██████████      ████████░                      ████▒    
  █████     ████     ███          ▓████████████       ▓████   
░████       ████     ███   ░███████          ▓███████▓ ████   
████        ████     █████▓        ▒█████           ██████    
▓███░       ████     ███              ███░████▓▒        ████  
  ████        ▓█████░███              ███     ████        ███▓
    ▒█████           █████▓        ▒█████     ████        ████
    ███░▓████████          ▓██████░   ███     ████       ████▒
    ████       ████████████▓          ███     ████     █████  
     ████                       ████████      ██████████░     
       ██████            ▓███████▒           ████▓            
           ▒███████████████▓              ▓█████              
                        ░███████████████████░

"""

banner = f"""
           ▄████████    ▄████████  ▄████████    ▄█    █▄       ▄████████ ███▄▄▄▄      ▄██████▄     ▄████████  ▄█       
          ███    ███   ███    ███ ███    ███   ███    ███     ███    ███ ███▀▀▀██▄   ███    ███   ███    ███ ███       
          ███    ███   ███    ███ ███    █▀    ███    ███     ███    ███ ███   ███   ███    █▀    ███    █▀  ███       
          ███    ███  ▄███▄▄▄▄██▀ ███         ▄███▄▄▄▄███▄▄   ███    ███ ███   ███  ▄███         ▄███▄▄▄     ███       
        ▀███████████ ▀▀███▀▀▀▀▀   ███        ▀▀███▀▀▀▀███▀  ▀███████████ ███   ███ ▀▀███ ████▄  ▀▀███▀▀▀     ███       
          ███    ███ ▀███████████ ███    █▄    ███    ███     ███    ███ ███   ███   ███    ███   ███    █▄  ███       
          ███    ███   ███    ███ ███    ███   ███    ███     ███    ███ ███   ███   ███    ███   ███    ███ ███▌    ▄ 
          ███    █▀    ███    ███ ████████▀    ███    █▀      ███    █▀   ▀█   █▀    ████████▀    ██████████ █████▄▄██ 
                       ███    ███                                                                            ▀         



                                {Colorate.Color(Colors.cyan, 'Telegram of developer:') + Colorate.Color(Colors.white, '   https://t.me/pr0xit')}


                                                {Colorate.Color(Colors.cyan, '[1]') + Colorate.Vertical(Colors.white, 'Поиск по базам')}                 {Colorate.Color(Colors.cyan, '[2]') + Colorate.Vertical(Colors.white, 'Поиск по номеру')}

                               {Colorate.Color(Colors.cyan, '[3]') + Colorate.Vertical(Colors.white, 'Поиск по почте')}                 {Colorate.Color(Colors.cyan, '[4]') + Colorate.Vertical(Colors.white, 'Поиск по айпи')}

                               {Colorate.Color(Colors.cyan, '[5]') + Colorate.Vertical(Colors.white, 'Поиск по PayPal')}                {Colorate.Color(Colors.cyan, '[6]') + Colorate.Vertical(Colors.white, 'Поиск по Instagram')} 

                               {Colorate.Color(Colors.cyan, '[7]') + Colorate.Vertical(Colors.white, 'Поиск по VIN')}                   {Colorate.Color(Colors.cyan, '[8]') + Colorate.Vertical(Colors.white, 'Поиск по MAC')}


                                              {Colorate.Color(Colors.cyan, '[9]') + Colorate.Vertical(Colors.white, 'Поиск с помощью ИИ')}

                                                    {Colorate.Color(Colors.cyan, '[10]') + Colorate.Vertical(Colors.white, 'Выход')}


               """

us = UserAgent()
x = Instaloader()
client = Client()



def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))  
        return result['encoding']



def search_in_txt(file_path, search_term):
    search_term = search_term.lower()  
    found_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            header = file.readline().strip()
            for line in file:
                if search_term in line.lower():  
                    found_data.append(f"Headers: {header}\nData: {line.strip()}")
    except UnicodeDecodeError:
        encoding = detect_encoding(file_path)
        if encoding:
            with open(file_path, 'r', encoding=encoding) as file:
                header = file.readline().strip()
                for line in file:
                    if search_term in line.lower():
                        found_data.append(f"Headers: {header}\nData: {line.strip()}")
    return found_data



def search_in_csv(file_path, search_term):
    search_term = search_term.lower()  
    found_data = []
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip')

        
        df_lower = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

        for index, row in df_lower.iterrows():
            if any(search_term in str(value) for value in row.values):
                found_data.append(
                    f"Headers: {', '.join(df.columns)}\nData: {', '.join([str(value) for value in df.iloc[index].values])}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return found_data



def search_in_xlsx(file_path, search_term):
    search_term = search_term.lower()
    found_data = []
    try:
        df = pd.read_excel(file_path)
        df_lower = df.applymap(lambda s: s.lower() if isinstance(s, str) else s)
        for index, row in df_lower.iterrows():
            if any(search_term in str(value) for value in row.values):
                found_data.append(
                    f"Headers: {', '.join(df.columns)}\nData: {', '.join([str(value) for value in df.iloc[index].values])}")
    except Exception:
        pass
    return found_data



def search_in_sql(db_path, search_term):
    found_data = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = "SELECT * FROM data"  
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        for row in rows:
            if search_term in str(row):
                found_data.append(f"Headers: {', '.join(columns)}\nData: {', '.join([str(value) for value in row])}")
    except Exception:
        pass
    return found_data



def search_in_files(search_term, folder='datab'):
    found_results = []
    if not os.path.exists(folder):
        return found_results

    files = os.listdir(folder)
    for file in files:
        file_path = os.path.join(folder, file)
        if file.endswith(".txt"):
            found_results.extend(search_in_txt(file_path, search_term))
        elif file.endswith(".csv"):
            found_results.extend(search_in_csv(file_path, search_term))
        elif file.endswith(".xlsx"):
            found_results.extend(search_in_xlsx(file_path, search_term))
        elif file.endswith(".db") or file.endswith(".sqlite3"):
            found_results.extend(search_in_sql(file_path, search_term))

    return found_results


def clean_text(label, text):
    cleaned_text = re.sub(f"^{label}:\\s*", "", text, flags=re.IGNORECASE).strip()

    if label == "Оператор" and "Оператор связи" in cleaned_text:
        cleaned_text = cleaned_text.replace("Оператор связи:", "").strip()
    elif label == "Город" and "Регион/Город" in cleaned_text:
        cleaned_text = cleaned_text.replace("Регион/Город:", "").strip()
    elif label == "Варианты" and "Варианты написания" in cleaned_text:
        cleaned_text = cleaned_text.replace("Варианты написания:", "").strip()

    return cleaned_text


def get_info_from_sambgo(phone_number):
    url = f"http://sambgo.ru/who-calls/{phone_number}"
    try:

        
        response = requests.get(url)

        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')

            
            selectors = {
                "Страна": "body > div.wrap.tc-0b64931eccfc-wrap > div > div.tc-0b64931e5f0b-container > div > div.col-lg-8.column_center.tc-0b64931e2cc1-column_center > ul > li:nth-child(1)",
                "Оператор": "body > div.wrap.tc-0b64931eccfc-wrap > div > div.tc-0b64931e5f0b-container > div > div.col-lg-8.column_center.tc-0b64931e2cc1-column_center > ul > li:nth-child(3)",
                "Город": "body > div.wrap.tc-0b64931eccfc-wrap > div > div.tc-0b64931e5f0b-container > div > div.col-lg-8.column_center.tc-0b64931e2cc1-column_center > ul > li:nth-child(4)",
                "Варианты": "body > div.wrap.tc-0b64931eccfc-wrap > div > div.tc-0b64931e5f0b-container > div > div.col-lg-8.column_center.tc-0b64931e2cc1-column_center > ul > li:nth-child(5)",
                "Рейтинг": "body > div.wrap.tc-0b64931eccfc-wrap > div > div.tc-0b64931e5f0b-container > div > div.col-lg-8.column_center.tc-0b64931e2cc1-column_center > div:nth-child(9) > div > div:nth-child(3) > div",
                "Отзывы": "body > div.wrap.tc-0b64931eccfc-wrap > div > div.tc-0b64931e5f0b-container > div > div.col-lg-8.column_center.tc-0b64931e2cc1-column_center > div:nth-child(9) > div > div.card.last-votes.my-3.tc-0b64931e9859-last_votes > div > table > tbody > tr > td:nth-child(1) > p > span"
            }

            
            extracted_info = {}

            
            for label, selector in selectors.items():
                info_section = soup.select_one(selector)
                if info_section:
                    
                    text = info_section.get_text(strip=True)
                    
                    cleaned_text = clean_text(label, text)
                    extracted_info[label] = cleaned_text
                else:
                    extracted_info[label] = "Информация не найдена."

            return extracted_info
        else:
            return f"Ошибка: {response.status_code}"

    except AttributeError:
        print((Colorate.Horizontal(Colors.red, "Ошибка, введите номер правильно.")))
        input("Ентер для продолжения")


def generate_google_dork(phone_number):
    dorks = [
        f'"{phone_number}"',
        f'intext:"{phone_number}"',
        f'intitle:"{phone_number}"',
        f'site:facebook.com "{phone_number}"',
        f'site:linkedin.com "{phone_number}"',
        f'site:twitter.com "{phone_number}"',
        f'site:vk.com "{phone_number}"',
        f'site:ok.ru "{phone_number}"',
        f'site:avito.ru "{phone_number}"',
        f'site:whatsapp.com "{phone_number}"',
        f'inurl:"contact" "{phone_number}"',
        f'inurl:"phone" "{phone_number}"',
    ]
    return dorks


def formatted_phone_info(phone_number_str):
    
    with tqdm(total=1, desc="Получение информации о номере телефона", unit=" шаг") as pbar:
        info = get_info_from_sambgo(phone_number_str)
        time.sleep(0.5)  
        pbar.update(1)

    
    with tqdm(total=1, desc="Генерация Google Dorks", unit=" шаг") as pbar:
        dorks = generate_google_dork(phone_number_str)
        time.sleep(0.5)  
        pbar.update(1)

    
    with tqdm(total=1, desc="Поиск в базах данных", unit=" шаг") as pbar:
        base_results = search_in_files(phone_number_str)
        time.sleep(0.5)  
        pbar.update(1)

    
    print("\n" + Colorate.Horizontal(Colors.blue_to_white, "[+]Информация о номере телефона:"))
    print(f"┌Страна: {info.get('Страна', 'Неизвестно')}")
    print(f"┃Оператор: {info.get('Оператор', 'Неизвестно')}")
    print(f"┃Регион/Город: {info.get('Город', 'Неизвестно')}")
    print(f"┃Варианты написания: {info.get('Варианты', 'Неизвестно')}")
    print(f"┃Рейтинг: {info.get('Рейтинг', 'Неизвестно')}")
    print(f"┖Отзывы: {info.get('Отзывы', 'Неизвестно')}")
    print(" |")

    print(Colorate.Horizontal(Colors.blue_to_white, "[+]Google dorks:"))
    
    for i, dork in enumerate(dorks):

        if i == len(dorks) - 1:

            print(f"└{dork}")
        else:
            print(f"├{dork}")
    print(" |")

    print(Colorate.Horizontal(Colors.blue_to_white, "[+]Базы данных:"))
    
    if base_results:
        for i, result in enumerate(base_results):
            if i == len(base_results) - 1:
                print(f"└{result}")
            else:
                print(f"├{result}")
    else:
        print(Colorate.Horizontal(Colors.red_to_white, "└Информации в базах не найдено"))
    print("\n\n")
    input(Colorate.Horizontal(Colors.green_to_white, "Нажмите Enter что-бы вернутся в меню"))
    main_menu()



def validate_email_format(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None



def check_email_domain(email):
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        return False



def get_whois_info(email):
    domain = email.split('@')[1]
    try:
        whois_info = whois.whois(domain)
        if 'google' in domain:
            company = "Google"
        elif 'yahoo' in domain:
            company = "Yahoo"
        elif 'microsoft' in domain:
            company = "Microsoft"
        else:
            company = whois_info.org if whois_info.org else "Unknown"
        return {
            'domain': domain,
            'registrar': whois_info.registrar,
            'company': company,
            'country': whois_info.country,
            'creation_date': whois_info.creation_date,
            'expiration_date': whois_info.expiration_date,
        }
    except Exception as e:
        return f"Ошибка WHOIS-запроса: {e}"



def formatted_email_info(email):
    with tqdm(total=1, desc="Проверка формата email", unit=" шаг") as pbar:
        if not validate_email_format(email):
            print("Неправильный формат email")
            return
        pbar.update(1)

    with tqdm(total=1, desc="Проверка MX записей домена", unit=" шаг") as pbar:
        if not check_email_domain(email):
            print("Домен электронной почты не существует или не имеет MX-записей")
            return
        pbar.update(1)

    with tqdm(total=1, desc="Получение WHOIS информации", unit=" шаг") as pbar:
        whois_info = get_whois_info(email)
        time.sleep(0.5)  
        pbar.update(1)

    
    with tqdm(total=1, desc="Поиск в базах данных", unit=" шаг") as pbar:
        base_results = search_in_files(email)  
        time.sleep(0.5)  
        pbar.update(1)

    
    print("\n" + Colorate.Horizontal(Colors.blue_to_white, "[+]Информация о электронной почте:"))
    print(f"┌Почта: {email}")
    print(f"┃Домен: {whois_info.get('domain', 'Неизвестно')}")
    print(f"┃Регистратор: {whois_info.get('registrar', 'Неизвестно')}")
    print(f"┃Компания: {whois_info.get('company', 'Неизвестно')}")
    print(f"┖Страна: {whois_info.get('country', 'Неизвестно')}")
    print(" |")

    print(Colorate.Horizontal(Colors.blue_to_white, "[+]Базы данных:"))
    
    if base_results:
        for i, result in enumerate(base_results):
            if i == len(base_results) - 1:
                print(f"└{result}")
            else:
                print(f"├{result}")
    else:
        print(Colorate.Horizontal(Colors.red_to_white, "└Информации в базах не найдено"))
    print("\n\n")
    input(Colorate.Horizontal(Colors.green_to_white, "Нажмите Enter что-бы вернутся в меню"))
    main_menu()



def get_ip_info(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,country,city,isp,lat,lon")
        data = response.json()

        if data["status"] == "success":
            return {
                "country": data.get("country", "Неизвестно"),
                "city": data.get("city", "Неизвестно"),
                "isp": data.get("isp", "Неизвестно"),
                "latitude": data.get("lat", "Неизвестно"),
                "longitude": data.get("lon", "Неизвестно")
            }
        else:
            return {"error": "Не удалось получить данные об IP"}
    except Exception as e:
        return {"error": f"Ошибка при запросе: {e}"}



def formatted_ip_info(ip_address):
    
    with tqdm(total=1, desc="Получение информации о IP", unit=" шаг") as pbar:
        ip_info = get_ip_info(ip_address)
        time.sleep(0.5)  
        pbar.update(1)

    
    with tqdm(total=1, desc="Поиск в базах данных", unit=" шаг") as pbar:
        base_results = search_in_files(ip_address)  
        time.sleep(0.5)  
        pbar.update(1)

    
    print("\n" + Colorate.Horizontal(Colors.blue_to_white, "[+]Информация об IP-адресе:"))
    if "error" in ip_info:
        print(f"└Ошибка: {ip_info['error']}")
    else:
        print(f"┌Страна: {ip_info.get('country', 'Неизвестно')}")
        print(f"┃Город: {ip_info.get('city', 'Неизвестно')}")
        print(f"┃Провайдер: {ip_info.get('isp', 'Неизвестно')}")
        print(f"┃Широта: {ip_info.get('latitude', 'Неизвестно')}")
        print(f"┖Долгота: {ip_info.get('longitude', 'Неизвестно')}")
    print(" |")

    print(Colorate.Horizontal(Colors.blue_to_white, "[+]Базы данных:"))
    
    if base_results:
        for i, result in enumerate(base_results):
            if i == len(base_results) - 1:
                print(f"└{result}")
            else:
                print(f"├{result}")
    else:
        print(Colorate.Horizontal(Colors.red_to_white, "└Информации в базах не найдено"))


def venmo_osint_info(username):
    print("\nПолучение информации о профиле Venmo...")

    try:
        
        r = requests.get(f"https://venmo.com/u/{username}", headers={"User-Agent": us.random})

        
        if r.status_code != 200:
            print(f"Ошибка: не удалось получить данные о пользователе {username}.")
            return

        
        soup = BeautifulSoup(r.text, "html.parser")
        transactions = soup.find_all("div", attrs={"class": "single-payment content-wrap"})

        print(f"Пользователь {username} имеет {len(transactions)} публичных транзакций.\n")

        venmo_data = []  

        
        for i, transaction in enumerate(transactions):
            send, recv = transaction.find_all("a")
            send, recv = send.getText(), recv.getText()
            message = transaction.find_all("div", attrs={"class": "paymentpage-text m_five_t"})[0].getText()
            date = transaction.find_all("div", attrs={"class": "date"})[0].getText()

            
            export_message = f"{send} заплатил {recv} {date} за {message}"
            venmo_data.append(export_message)
            print(f"├ {export_message}")

        if not venmo_data:
            print("└ Транзакции не найдены.")

    except requests.exceptions.ConnectionError:
        print("Ошибка, не удалось подключиться к Venmo. Проверьте интернет-соединение.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    input(Colorate.Horizontal(Colors.green_to_white, "Нажмите Enter что-бы вернуться в меню"))
    main_menu()


def show_startup_screen():
    System.Clear()  

    
    logo_lines = logo.splitlines()[:100]  
    banner_lines = banner.splitlines()

    
    max_lines = max(len(logo_lines), len(banner_lines))

    
    logo_width = max(len(line) for line in logo_lines)
    banner_width = max(len(line) for line in banner_lines)

    
    combined_output = []
    for i in range(max_lines):
        

        banner_part = banner_lines[i] if i < len(banner_lines) else ' ' * banner_width
        logo_part = logo_lines[i] if i < len(logo_lines) else ' ' * logo_width

        
        space_between = max(0, banner_width - len(logo_part) - 300)  

        
        colored_logo = Colorate.Horizontal(Colors.green_to_white, logo_part)

        
        colored_banner = Colorate.Color(Colors.light_green, banner_part)

        
        combined_output.append(f"{' ' * space_between}{colored_logo}{colored_banner}")

    
    for line in combined_output:
        print(line)


def insta(uname):
    try:
        with tqdm(total=1, desc="Получение информации о профиле", unit=" шаг") as pbar:
            f = instaloader.Profile.from_username(x.context, uname)
            time.sleep(0.5)
            pbar.update(1)

        print("\n" + Colorate.Horizontal(Colors.blue_to_white, "[+] Информация о пользователе инстаграм"))
        print(f"{Colorate.Color(Colors.cyan, '┌Имя пользователя:')} {Colorate.Color(Colors.white, f.username)}")
        print(
            f"{Colorate.Color(Colors.cyan, '┃ID:')} {Colorate.Color(Colors.white, str(f.userid))}")  
        print(f"{Colorate.Color(Colors.cyan, '┃Полное имя:')} {Colorate.Color(Colors.white, f.full_name)}")
        print(
            f"{Colorate.Color(Colors.cyan, '┃Биография:')} {Colorate.Color(Colors.white, f.biography or 'Не указано')}")
        print(
            f"{Colorate.Color(Colors.cyan, '┃Имя категории бизнеса:')} {Colorate.Color(Colors.white, f.business_category_name or 'Не указано')}")
        print(
            f"{Colorate.Color(Colors.cyan, '┃Внешний URL:')} {Colorate.Color(Colors.white, f.external_url or 'Не указано')}")
        print(
            f"{Colorate.Color(Colors.cyan, '┃Подписчики:')} {Colorate.Color(Colors.white, str(f.followed_by_viewer))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Подписки:')} {Colorate.Color(Colors.white, str(f.followees))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Число подписчиков:')} {Colorate.Color(Colors.white, str(f.followers))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Подписан на пользователя:')} {Colorate.Color(Colors.green if f.follows_viewer else Colors.red, str(f.follows_viewer))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Заблокированные пользователи:')} "
            f"{Colorate.Color(Colors.green if f.blocked_by_viewer else Colors.red, 'Да' if f.blocked_by_viewer else 'Нет')}"
        )

        print(
            f"{Colorate.Color(Colors.cyan, '┃Ранее заблокированные пользователи:')} "
            f"{Colorate.Color(Colors.green if f.has_blocked_viewer else Colors.red, 'Да' if f.has_blocked_viewer else 'Нет')}"
        )

        print(
            f"{Colorate.Color(Colors.cyan, '┃Есть выделенные моменты:')} {Colorate.Color(Colors.green if f.has_highlight_reels else Colors.red, str(f.has_highlight_reels))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Есть публичные истории:')} {Colorate.Color(Colors.green if f.has_public_story else Colors.red, str(f.has_public_story))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Отправлены запросы пользователям:')} {Colorate.Color(Colors.green if f.has_requested_viewer else Colors.red, str(f.has_requested_viewer))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Запросы от пользователей:')} {Colorate.Color(Colors.white, str(f.requested_by_viewer))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Есть истории, которые можно просмотреть:')} {Colorate.Color(Colors.green if f.has_viewable_story else Colors.red, str(f.has_viewable_story))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃IGTV:')} {Colorate.Color(Colors.white, str(f.igtvcount))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Бизнес-аккаунт:')} {Colorate.Color(Colors.green if f.is_business_account else Colors.red, str(f.is_business_account))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Личный аккаунт:')} {Colorate.Color(Colors.green if f.is_private else Colors.red, str(f.is_private))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┃Подтвержденный аккаунт:')} {Colorate.Color(Colors.green if f.is_verified else Colors.red, str(f.is_verified))}")  
        print(
            f"{Colorate.Color(Colors.cyan, '┖Посты:')} {Colorate.Color(Colors.white, str(f.mediacount))}")  
        print(f"{Colorate.Color(Colors.cyan, 'URL профиля:')} {Colorate.Color(Colors.white, f.profile_pic_url)}")
    except Exception:
        print("Произошла ошибка, возможно слишком много запросов.")
    input(Colorate.Horizontal(Colors.green_to_white, "\nНажмите Enter что-бы вернутся в меню"))
    main_menu()


def decode_vin(vin_number):
    try:
        with tqdm(total=1, desc="Получение информации о VIN", unit=" шаг") as pbar:
            vin = Vin(vin_number)
            pbar.update(1)

        print("\n" + Colorate.Horizontal(Colors.blue_to_white, "[+] Информация о транспортном средстве"))
        print(f"{Colorate.Color(Colors.cyan, '┎VIN:')} {Colorate.Color(Colors.white, vin_number)}")
        print(f"{Colorate.Color(Colors.cyan, '┃Страна:')} {Colorate.Color(Colors.white, vin.country or 'Не указано')}")
        print(
            f"{Colorate.Color(Colors.cyan, '┃Производитель:')} {Colorate.Color(Colors.white, vin.manufacturer or 'Не указано')}")
        print(f"{Colorate.Color(Colors.cyan, '┃Регион:')} {Colorate.Color(Colors.white, vin.region or 'Не указано')}")
        print(
            f"{Colorate.Color(Colors.cyan, '┃Год выпуска:')} {Colorate.Color(Colors.white, ', '.join(str(year) for year in vin.years) if vin.years else 'Не указано')}")

        details = vin.details
        if details is None or not details:
            print("┃Детали: Пусто")
        else:
            print(f"┃Детали: {details}")

        if vin.verify_checksum():
            print(Colorate.Color(Colors.green, "┖Контрольная сумма действительна"))
        else:
            print(Colorate.Color(Colors.red, "┖Контрольная сумма недействительна"))

    except Exception as e:
        print(Colorate.Color(Colors.red, "Произошла ошибка: " + str(e)))

    input(Colorate.Horizontal(Colors.green_to_white, "\nНажмите Enter что-бы вернуться в меню"))
    main_menu()


def get_mac_info(mac_address):
    try:
        with tqdm(total=1, desc="Получение информации о MAC", unit=" шаг") as pbar:
            response = requests.get(f"https://www.macvendorlookup.com/api/v2/{mac_address}/xml")
            pbar.update(1)

        if response.status_code != 200:
            print(Colorate.Color(Colors.red, "Произошла ошибка: Невозможно получить данные"))
            return

        root = ET.fromstring(response.content)

        company = root.find('company').text if root.find('company') is not None else "Не указано"
        addressL1 = root.find('addressL1').text if root.find('addressL1') is not None else "Не указано"
        addressL2 = root.find('addressL2').text if root.find('addressL2') is not None else ""
        addressL3 = root.find('addressL3').text if root.find('addressL3') is not None else ""
        country = root.find('country').text if root.find('country') is not None else "Не указано"
        mac_type = root.find('type').text if root.find('type') is not None else "Не указано"

        print("\n" + Colorate.Horizontal(Colors.blue_to_white, "[+] Информация о MAC-адресе"))
        print(f"{Colorate.Color(Colors.cyan, '┌MAC:')} {Colorate.Color(Colors.white, mac_address)}")
        print(f"{Colorate.Color(Colors.cyan, '┃Компания:')} {Colorate.Color(Colors.white, company)}")

        addresses = ', '.join(filter(None, [addressL1, addressL2, addressL3]))
        print(
            f"{Colorate.Color(Colors.cyan, '┃Адрес:')} {Colorate.Color(Colors.white, addresses if addresses else 'Не указано')}")

        print(f"{Colorate.Color(Colors.cyan, '┃Страна:')} {Colorate.Color(Colors.white, country)}")
        print(f"{Colorate.Color(Colors.cyan, '┖Тип:')} {Colorate.Color(Colors.white, mac_type)}")

    except Exception as e:
        print(Colorate.Color(Colors.red, "Произошла ошибка: " + str(e)))

    input(Colorate.Horizontal(Colors.green_to_white, "\nНажмите Enter что-бы вернуться в меню"))
    main_menu()


def classify_input_with_g4f(input_data):
    prompt = f"Определи, что это: номер телефона,никнейм Instagram, email, IP-адрес, MAC-адрес или VIN. Ответь одним словом из телефон,почта,ip,instagram никнейм,mac,vin,имя Venmo: '{input_data}'"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    classification = response.choices[0].message.content.strip().lower()
    return classification


async def spinning_animation():
    spinner = itertools.cycle(['⬖', '⬘', '⬗', '⬙'])
    while True:
        current_spinner = next(spinner)
        print(f"\r{current_spinner} Определяю...", end="", flush=True)
        await asyncio.sleep(0.2)


async def classify_and_search(input_data):
    spinner_task = asyncio.create_task(spinning_animation())

    classification = classify_input_with_g4f(input_data)

    spinner_task.cancel()
    print("\rКлассификация завершена.              ")

    if "телефон" in classification:
        print(f"Обнаружен номер телефона: {input_data}")
        formatted_phone_info(input_data)
    elif "почта" in classification:
        print(f"Обнаружен email: {input_data}")
        formatted_email_info(input_data)
    elif "ip" in classification:
        print(f"Обнаружен IP-адрес: {input_data}")
        formatted_ip_info(input_data)
    elif "имя" in classification:
        print(f"Обнаружено имя пользователя: {input_data}")
        venmo_osint_info(input_data)
    elif "mac" in classification:
        print(f"Обнаружен MAC-адрес: {input_data}")
        get_mac_info(input_data)
    elif "vin" in classification:
        print(f"Обнаружен VIN-номер: {input_data}")
        decode_vin(input_data)
    elif "instagram" in classification or "ник" in classification:
        print(f"Обнаружено имя пользователя Instagram: {input_data}")
        insta(input_data)
    else:
        print("Не удалось классифицировать ввод. Попробуйте снова.")


async def gpt_input():
    print("\nВведите запрос для анализа (например, номер телефона, email, IP, MAC-адрес, VIN или имя):")
    user_input = input("Введите ваш запрос -> ")

    await classify_and_search(user_input)


def gpt_main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(gpt_input())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


def main_menu():
    show_startup_screen()
    while True:
        print("\n\n\n")
        choice = input("Введите ваш выбор -> ")

        if choice == '1':
            search_term = input("Enter the search term: ")
            search_in_files(search_term, folder='datab')  
        elif choice == '2':
            phone_number = input("Введите номер телефона: ")
            formatted_phone_info(phone_number)  
        elif choice == '3':
            email = input("Введите email: ")
            formatted_email_info(email)  
        elif choice == '4':
            ip_address = input("Введите IP-адрес: ")
            formatted_ip_info(ip_address)  
        elif choice == '5':
            username = input("Введите имя пользователя Venmo: ")
            venmo_osint_info(username)  
        elif choice == '6':
            uname = input("Введите имя пользователя: ")
            insta(uname)
        elif choice == '7':
            vin_number = input("Введите VIN машины: ")
            decode_vin(vin_number)
        elif choice == '8':
            mac_address = input("Введите MAC адресс: ")
            get_mac_info(mac_address)
        elif choice == '9':
            gpt_main()
        elif choice == '10':
            print("Exiting the program.")
            exit(0)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main_menu()
