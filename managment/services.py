import csv
import os
import re

import requests
from bs4 import BeautifulSoup

from managment.settings import CATEGORY_DIRECTORY_NAME, INDENT


def clear_screen() -> None:
    os.system("cls")


def validate_number_with_message(message: str, min_num: int, max_num: int) -> int:
    while True:
        print(message)
        choice_input = input()

        if choice_input.isnumeric():
            choice_input_num = int(choice_input)
            if not (min_num <= choice_input_num <= max_num):
                print(f"\nПроверьте корректность введенного значения!")
                continue
            else:
                return choice_input_num
        else:
            print("\nВы должны ввести число!")


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


def get_action_for_channels(message: str, category_files: dict = None) -> int:
    category_files = category_files or get_category_files()

    for index, file_name_with_extension in category_files.items():
        file_name = get_filename_from_extension(file_name_with_extension)
        message += f"{INDENT}{index}. {file_name}"

    message += f"{INDENT}0. В главное меню"

    action = validate_number_with_message(message, 0, len(category_files))
    return action


def check_channel_link(channel_link) -> str | bool:
    tg_url = "https://t.me/s/"

    while True:
        if channel_link.startswith("@"):
            channel_link = tg_url + channel_link[1:]
            break
        elif channel_link.startswith(tg_url):
            break
        elif channel_link.startswith(tg_url[:2]):
            channel_link = tg_url + channel_link.split("/")[-1]
        else:
            print(
                '\nУбедитесь в корректности ссылки/идентификатора канала! Повторите ввод. Для выхода введите "0"'
            )
            return False

    return channel_link


def csv_channel_manager(method: str, category_path: str) -> int:
    print(
        "\nНачните вводить телеграм-каналы. "
        "После каждого ввода жмите Enter. "
        '\nФормат ввода - "https://t.me/идентификатор_канала" или "@идентификатор_канала"'
        f"{INDENT}0. Выбрать другую категорию для "
        f"{'ручного добавления' if method == 'write' else 'удаления'} каналов"
    )

    while True:
        link_channel_or_action = input()

        if link_channel_or_action == "0":
            return 0

        link_channel = check_channel_link(link_channel_or_action)

        if not link_channel:
            continue

        if method == "write":
            write_channel_to_csv(category_path, link_channel)
        elif method == "remove":
            remove_channel_from_csv(category_path, link_channel)

        print('\nПродолжайте вводить каналы или введите "0" для выхода.\n')


def write_channel_to_csv(
    category_path: str, channel_link: str, channel_name=None, permanent=False
) -> None:
    if not permanent:
        channel_page = requests.get(channel_link)
        channel_content = BeautifulSoup(channel_page.content, "html.parser")
        channel_name = channel_content.find(
            "div", class_="tgme_channel_info_header_title"
        ).text.strip()
    else:
        channel_link = check_channel_link(channel_link)

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


def remove_channel_from_csv(file_path: str, link_to_remove: str) -> None:
    to_remove = False
    lines = []
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            channel_link, channel_name = row
            if channel_link == link_to_remove:
                to_remove = True
                print(f'\nКанал "{channel_name}" успешно удалён!')
            else:
                lines.append(row)

    if to_remove:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(lines)
    else:
        print("\nДанного телеграм-канала нет в списке!")


def get_filename_from_extension(filename: str) -> str:
    return filename.replace(".csv", "")


def combine_words(words: str) -> list:
    result = []

    for word in words.split():
        word = " ".join(word.split("+"))
        result.append(word)

    return result
