import os

import main
from managment.services import (
    get_choice_input,
    is_valid_filename,
    get_category_files,
    get_filename_from_extension,
)
from managment.settings import CATEGORY_DIRECTORY_NAME


def choice_category():
    message = """\nЧто Вы хотите сделать?
        1. Создать категорию
        2. Удалить категорию
        0. В главное меню"""

    action = get_choice_input(message, 0, 2)

    if action == 0:
        from main import main

        return main()

    elif action == 1:
        return create_category()

    elif action == 2:
        return delete_category()


def create_category():
    message = """\nУкажите название категории
        0. Назад"""

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
        print("У вас нет категорий для удаления!")
        return choice_category()

    message = """\nВыберите категорию для удаления
        0. Назад"""

    for index, file_name_with_extension in category_files.items():
        file_name = get_filename_from_extension(file_name_with_extension)
        message += f"""
        {index}. {file_name}"""

    action = get_choice_input(message, 0, len(category_files))

    if action == 0:
        return choice_category()

    selected_category_with_extension = category_files[action]
    selected_category_for_print = get_filename_from_extension(
        selected_category_with_extension
    )

    print(
        f"""\nВы выбрали категорию "{selected_category_for_print}". Удаляем?
        1. Да
        0. Нет"""
    )

    action = input()

    if action != "1":
        return delete_category()
    else:
        os.remove(f"{CATEGORY_DIRECTORY_NAME}/{selected_category_with_extension}")
        print(f'Категория "{selected_category_for_print}" удалена!')
        return choice_category()
