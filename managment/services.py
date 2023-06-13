import csv
import os
import re

import requests
from bs4 import BeautifulSoup

from managment.settings import CATEGORY_DIRECTORY_NAME


def clear_screen() -> None:
    os.system("cls")


def get_choice_input(message: str, min_num: int, max_num: int) -> int:
    while True:
        print(message)
        choice_input = input()

        if choice_input.isnumeric():
            choice_input_num = int(choice_input)
            if not (min_num <= choice_input_num <= max_num):
                clear_screen()
                print(f"Проверьте корректность введенного значения!")
                continue
            else:
                return choice_input_num
        else:
            clear_screen()
            print("Вы должны ввести число!")


def is_valid_filename(filename: str) -> str | bool:
    pattern = r"^[а-яА-Яa-zA-Z0-9\s!#$%&\'()\-\@^_`{}~.]+$"

    if re.match(pattern, filename):
        if len(filename) <= 255:
            if not (filename.strip() == "." or filename.strip() == ""):
                return filename
            else:
                print("\nИмя файла не может состоять только из пробелов или точек.")
        else:
            print("\nДлина имени файла превышает 255 символов.")
    else:
        print("\nИмя файла содержит недопустимые символы.")

    return False


def get_category_files() -> dict:
    if CATEGORY_DIRECTORY_NAME not in os.listdir():
        os.mkdir(CATEGORY_DIRECTORY_NAME)
        return {}

    directory_files = os.listdir(CATEGORY_DIRECTORY_NAME)
    category_files = {
        index: file_name for index, file_name in enumerate(directory_files, start=1)
    }

    return category_files


def write_channel_to_csv(category_path: str, channel_link: str) -> None:
    channel_page = requests.get(channel_link)
    channel_content = BeautifulSoup(channel_page.content, "html.parser")
    channel_name = channel_content.find("div", class_="tgme_page_title").text.strip()

    channels_dict = read_channels_from_csv(category_path)
    if channel_link in channels_dict.keys():
        print(f"\nКанал {channels_dict[channel_link]} уже добавлен!")
        return

    with open(category_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([channel_link, channel_name])

    print(f'\nКанал "{channel_name}" успешно добавлен!')


def read_channels_from_csv(category_path: str) -> dict:
    with open(category_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        channels_dict = {link: name for link, name in reader}
        return channels_dict


def get_filename_from_extension(filename: str) -> str:
    return filename.replace(".csv", "")
