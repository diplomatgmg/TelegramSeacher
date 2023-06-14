import os

import requests
from http import HTTPStatus
import main
from managment.services import (
    validate_number_with_message,
    is_valid_filename,
    get_category_files,
    get_filename_from_extension,
    get_action_for_channels,
)
from managment.settings import CATEGORY_DIRECTORY_NAME, INDENT, SITE_AUTO_ADD


def choice_category():
    message = (
        f"\nЧто Вы хотите сделать?"
        f"{INDENT}1. Создать категорию"
        f"{INDENT}2. Удалить категорию"
        f"{INDENT}0. В главное меню"
    )

    action = validate_number_with_message(message, 0, 2)

    if action == 0:
        from main import main

        return main()

    elif action == 1:
        return create_category()

    elif action == 2:
        return delete_category()


def create_category():
    message = f"\nУкажите название категории" f"{INDENT}0. Назад"

    while True:
        print(message)
        action_or_filename = input()

        if action_or_filename == "0":
            return choice_category()

        file_name = is_valid_filename(action_or_filename)

        if file_name:
            with open(
                f"{CATEGORY_DIRECTORY_NAME}/{file_name}.csv", "w", encoding="utf-8"
            ):
                print(f'\nКатегория "{file_name}" успешно создана.')
            return main.main()


def delete_category():
    category_files = get_category_files()

    if not category_files:
        print("\nУ вас нет категорий для удаления!")
        return choice_category()

    action = get_action_for_channels(
        "\nВыберите категорию для удаления каналов", category_files
    )

    if action == 0:
        return choice_category()

    selected_category_with_extension = category_files[action]
    selected_category_for_print = get_filename_from_extension(
        selected_category_with_extension
    )

    print(
        f'\nВы выбрали категорию "{selected_category_for_print}". Удаляем?'
        f"{INDENT}1. Да"
        f"{INDENT}0. Нет"
    )

    action = input()

    if action == "1":
        os.remove(f"{CATEGORY_DIRECTORY_NAME}/{selected_category_with_extension}")
        print(f'\nКатегория "{selected_category_for_print}" удалена!')
        return choice_category()
    else:
        print(f'\nОтмена удаления категории "{selected_category_for_print}"')
        return delete_category()




def connect_to_site(url: str):
    if url.startswith(SITE_AUTO_ADD) and url != SITE_AUTO_ADD:
        page = requests.get(url)
        if page.status_code == HTTPStatus.OK:
            return page
        elif page.status_code == HTTPStatus.NOT_FOUND:
            print("\nСтраница не найдена! Проверьте корректность введённой ссылки!")

    print("\nПроверьте корректность введённой ссылки!")
