from managment.create_delete_category import create_category
from managment.services import (
    get_category_files,
    get_choice_input,
    write_channel_to_csv,
    get_filename_from_extension,
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
        return add_channels()

    elif action == 2:
        return remove_channels()


def add_channels():
    category_files = get_category_files()

    message = """\nВыберите категорию для добавления
            0. Назад"""

    for index, file_name_with_extension in category_files.items():
        file_name = get_filename_from_extension(file_name_with_extension)
        message += f"""
            {index}. {file_name}"""

    action = get_choice_input(message, 0, len(category_files))

    if action == 0:
        return choice_channels()

    selected_category_with_extension = category_files[action]
    selected_category_for_print = get_filename_from_extension(
        selected_category_with_extension
    )

    print(f'\nВы выбрали категорию "{selected_category_for_print}"')

    print(
        "\nНачните вводить телеграм-каналы. "
        "После каждого ввода жмите Enter. "
        'Для выхода введите "0"'
        '\nФормат ввода - "https://t.me/идентификатор_канала" или "@идентификатор_канала"\n'
    )

    while True:
        link_channel_or_action = input()

        if link_channel_or_action == "0":
            return choice_channels()

        elif link_channel_or_action.startswith("https://t.me/"):
            link_channel = link_channel_or_action

        elif link_channel_or_action.startswith("@"):
            link_channel = "https://t.me/" + link_channel_or_action[1:]

        else:
            print("Убедитесь в корректности ссылки/идентификатора канала!")
            continue

        selected_category_path = (
            f"{CATEGORY_DIRECTORY_NAME}/{selected_category_with_extension}"
        )

        write_channel_to_csv(selected_category_path, link_channel)
        print('\nПродолжайте добавлять каналы или введите "0" для выхода.\n')


def remove_channels():
    pass
