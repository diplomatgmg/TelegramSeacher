from pathlib import Path

from managment.create_delete_category import create_category
from managment.services import (
    get_category_files,
    get_choice_input,
    get_filename_from_extension,
    get_action_for_channels,
    csv_channel_manager,
)

from managment.settings import CATEGORY_DIRECTORY_NAME


def choice_channels():
    category_files = get_category_files()

    if not category_files:
        print("\nУ вас должна быть хотя бы одна категория! Создайте!")
        return create_category()

    message = """\nЧто Вы хотите сделать?
        1. Добавить каналы
        2. Удалить каналы
        0. В главное меню"""

    action = get_choice_input(message, 0, 2)

    if action == 0:
        from main import main

        return main()

    elif action == 1:
        return manage_channels(method="write")

    elif action == 2:
        return manage_channels(method="remove")


def manage_channels(method: str):
    category_files = get_category_files()

    action = get_action_for_channels(
        "\nВыберите категорию для "
        + ("добавления" if method == "write" else "удаления")
        + " каналов",
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

    action = csv_channel_manager(method, category_path)

    if action == 0:
        return choice_channels()
