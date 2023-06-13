import os

import main
from managment.services import (
    get_choice_input,
    is_valid_filename,
    get_category_files,
    get_filename_from_extension,
    get_action_for_channels,
)
from managment.settings import CATEGORY_DIRECTORY_NAME, INDENT


def choice_category():
    message = (
        f"\nЧто Вы хотите сделать?"
        f"{INDENT}1. Создать категорию"
        f"{INDENT}2. Удалить категорию"
        f"{INDENT}0. В главное меню"
    )

    action = get_choice_input(message, 0, 2)

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

    if action != "1":
        return delete_category()
    else:
        os.remove(f"{CATEGORY_DIRECTORY_NAME}/{selected_category_with_extension}")
        print(f'Категория "{selected_category_for_print}" удалена!')
        return choice_category()
