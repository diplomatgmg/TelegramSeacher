from pathlib import Path

import requests
from bs4 import BeautifulSoup

from managment.create_delete_category import create_category, connect_to_site
from managment.services import (
    get_category_files,
    get_choice_input,
    get_filename_from_extension,
    get_action_for_channels,
    csv_channel_manager,
    write_channel_to_csv,
)
from managment.settings import CATEGORY_DIRECTORY_NAME, SITE_AUTO_ADD, INDENT


def choice_channels():
    category_files = get_category_files()

    if not category_files:
        print("\nУ вас должна быть хотя бы одна категория! Создайте!")
        return create_category()

    message = """\nЧто Вы хотите сделать?
        1. Добавить каналы вручную
        2. Добавить каналы автоматически
        3. Удалить каналы
        0. В главное меню"""

    action = get_choice_input(message, 0, 3)

    if action == 0:
        from main import main

        return main()

    elif action == 1:
        return manage_channels(method="write")

    elif action == 2:
        return manage_channels("write", automatic=True)

    elif action == 3:
        return manage_channels(method="remove")


def manage_channels(method: str, automatic=False):
    category_files = get_category_files()

    action = get_action_for_channels(
        f"\nВыберите категорию для {'' if automatic else ('добавления' if method == 'write' else 'удаления')} каналов",
        category_files,
    )

    if action == 0:
        return choice_channels()

    category_file_name_with_extension = category_files[action]

    selected_category_for_print = get_filename_from_extension(
        category_file_name_with_extension
    )

    print(f'\nВы выбрали категорию "{selected_category_for_print}"')

    category_path = Path(CATEGORY_DIRECTORY_NAME) / category_file_name_with_extension

    if not automatic:
        action = csv_channel_manager(method, category_path)
        if action == 0:
            return choice_channels()
    else:
        while True:
            category_href = input(
                '\nПерейдите на сайт "https://all-catalog.ru/", '
                "выберите нужную категорию и вставьте ее сюда."
                f"{INDENT}0. Назад\n"
            )

            if category_href == "0":
                return choice_channels()

            category_page = connect_to_site(category_href)

            if category_page:
                break

        category_content = BeautifulSoup(category_page.content, "html.parser")

        category_raw_name = category_content.find("h1", {"id": "h1_title"}).text.strip()
        category_name = category_raw_name.split("«")[1].split("»")[0]

        div_pages = category_content.find("div", {"style": "margin-bottom: 10px"})

        if not div_pages:
            pages = [category_href.split('/')[-1]]
        else:
            pages = div_pages.find_all("a")

        channels_hrefs = set()

        for page in pages:
            page: str | BeautifulSoup
            if type(page) != str:
                page_href = page.get("href")
            else:
                page_href = page

            if page_href:
                category_href = SITE_AUTO_ADD + "/tg_category/" + page_href
                category_page = connect_to_site(category_href)
                category_content = BeautifulSoup(category_page.content, "html.parser")

            channels = category_content.find_all(
                "div", class_="card-content card_catalog white grey-text text-darken-1"
            )

            for channel in channels:
                channel_href = SITE_AUTO_ADD + channel.find("a")["href"][2:]
                channels_hrefs.add(channel_href)

        message = (
            f'\nВ категории "{category_name}" около {len(channels_hrefs)} каналов, сколько добавлять?'
            f"{INDENT}1. Все"
            f"{INDENT}0. Назад"
        )

        action = get_choice_input(message, 0, len(channels_hrefs))

        if action == 0:
            return choice_channels()

        count_add = len(channels_hrefs) if action == 1 else action

        channels_hrefs = list(channels_hrefs)

        for channel_index in range(count_add):
            channel_href = channels_hrefs[channel_index]

            channel_page = requests.get(channel_href)
            channel_soup = BeautifulSoup(channel_page.content, "html.parser")

            channel_name = channel_soup.find("h1", class_="product_title").text.strip()
            channel_tg_href = channel_soup.find("a", id="img_btn")["href"]

            write_channel_to_csv(
                category_path, channel_tg_href, channel_name, permanent=True
            )

    return choice_channels()
