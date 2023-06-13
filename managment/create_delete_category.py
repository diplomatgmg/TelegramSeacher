import os

from managment.services import get_choice_input, is_valid_filename


def choice_category():
    if 'category' not in os.listdir():
        os.mkdir('category')

    message = """\nЧто Вы хотите сделать?
        1. Создать категорию
        2. Удалить категорию
        0. В главное меню"""

    action = get_choice_input(message, 0, 2)

    if action == 0:
        from main import main

        return main()

    if action == 1:
        return create_category()

    if action == 2:
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
            with open(f"categories/{file_name}.txt", "w"):
                print(f'\nКатегория "{file_name}" успешно создана.')
            return choice_category()


def delete_category():
    directory_files = os.listdir('categories')

    if not directory_files:
        print('У вас нет категорий для удаления!')
        return choice_category()

    categories_files = {index: file_name for index, file_name in enumerate(directory_files, start=1)}

    message = """\nВыберите категорию для удаления
        0. Назад"""

    for index, file_name in categories_files.items():
        message += (f'''
        {index}. {file_name}''')

    action = get_choice_input(message, 0, len(categories_files))

    if action == 0:
        return choice_category()

    selected_file: str = categories_files[action]
    selected_file_for_print = selected_file.replace('.txt', '')

    print(f'''\nВы выбрали категорию "{selected_file_for_print}". Удаляем?
        1. Да
        0. Нет''')

    action = input()

    if action != '1':
        return delete_category()
    else:
         pass

