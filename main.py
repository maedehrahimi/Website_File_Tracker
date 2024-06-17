# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
#
# import requests
# from bs4 import BeautifulSoup
# import sqlite3
# import time
# from urllib.parse import urljoin
# import schedule
#
# conn = sqlite3.connect('website_data.db')
# c = conn.cursor()
# c.execute('''
#     CREATE TABLE IF NOT EXISTS website_data (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         url TEXT,
#         filename TEXT,
#         status_code INTEGER,
#         load_time REAL
#     )
# ''')
# conn.commit()
#
#
# def get_files_and_status(url):
#     try:
#         start_time = time.time()
#         response = requests.get(url)
#         load_time = round(time.time() - start_time, 3)
#         status_code = response.status_code
#
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             files = []
#
#             for tag in soup.find_all(['link', 'script', 'img', 'video', 'audio', 'source'], src=True):
#                 src = tag.get('src')
#                 if src:
#                     files.append(urljoin(url, src))
#
#             for tag in soup.find_all('link', href=True):
#                 href = tag.get('href')
#                 if href and 'stylesheet' in tag.get('rel', []):
#                     files.append(urljoin(url, href))
#
#             return files, status_code, load_time
#         else:
#             return [], status_code, load_time
#     except Exception as e:
#         print(f"Error loading {url}: {e}")
#         return [], None, None
#
#
# def store_data(url, files, status_code, load_time):
#     try:
#         c.execute("SELECT filename FROM website_data WHERE url=?", (url,))
#         existing_files = c.fetchall()
#         existing_files = [item[0] for item in existing_files]
#         new_files = set(files)
#         old_files = set(existing_files)
#         added_files = new_files - old_files
#         removed_files = old_files - new_files
#
#         for file in added_files:
#             c.execute("INSERT INTO website_data (url, filename, status_code, load_time) VALUES (?, ?, ?, ?)",
#                       (url, file, status_code, load_time))
#
#         for file in removed_files:
#             c.execute("DELETE FROM website_data WHERE url=? AND filename=?", (url, file))
#
#         conn.commit()
#
#         if added_files:
#             print(f"Added files for {url}:")
#             for file in added_files:
#                 print(file)
#
#         if removed_files:
#             print(f"Removed files from {url}:")
#             for file in removed_files:
#                 print(file)
#
#     except Exception as e:
#         print(f"Error storing data for {url}: {e}")
#
#
# urls = [
#     'https://maktabkhooneh.org/',
#     'https://cloudguard.ir/'
# ]
#
# for url in urls:
#     files, status_code, load_time = get_files_and_status(url)
#     store_data(url, files, status_code, load_time)
#
# conn.close()
#
#
import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from urllib.parse import urljoin

# اتصال به پایگاه داده
conn = sqlite3.connect('website_data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS website_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        filename TEXT,
        status_code INTEGER,
        load_time REAL
    )
''')
conn.commit()

def get_files_and_status(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        load_time = round(time.time() - start_time, 3)
        status_code = response.status_code

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            files = []

            for tag in soup.find_all(['link', 'script', 'img', 'video', 'audio', 'source'], src=True):
                src = tag.get('src')
                if src:
                    files.append(urljoin(url, src))

            for tag in soup.find_all('link', href=True):
                href = tag.get('href')
                if href and 'stylesheet' in tag.get('rel', []):
                    files.append(urljoin(url, href))

            return files, status_code, load_time
        else:
            return [], status_code, load_time
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return [], None, None

def store_data(url, files, status_code, load_time):
    try:
        c.execute("SELECT filename FROM website_data WHERE url=?", (url,))
        existing_files = c.fetchall()
        existing_files = [item[0] for item in existing_files]
        new_files = set(files)
        old_files = set(existing_files)
        added_files = new_files - old_files
        removed_files = old_files - new_files

        for file in added_files:
            c.execute("INSERT INTO website_data (url, filename, status_code, load_time) VALUES (?, ?, ?, ?)",
                      (url, file, status_code, load_time))

        for file in removed_files:
            c.execute("DELETE FROM website_data WHERE url=? AND filename=?", (url, file))

        conn.commit()

        if added_files:
            print(f"Added files for {url}:")
            for file in added_files:
                print(file)

        if removed_files:
            print(f"Removed files from {url}:")
            for file in removed_files:
                print(file)

    except Exception as e:
        print(f"Error storing data for {url}: {e}")

def get_url():
    response = input(" do you want enter a url? (y/n):").strip().lower()
    if response == "y":
        url = input(" please enter your url: ").strip()
        return [url]
    else:
        return [
            'https://example.com',
            'https://example2.com'
        ]

urls = get_url()

for url in urls:
    files, status_code, load_time = get_files_and_status(url)
    store_data(url, files, status_code, load_time)

conn.close()
