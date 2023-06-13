from managment.services import get_choice_input


def main():
    message = """\nЧто Вы хотите сделать? 
        1. Создать/удалить категорию
        2. Добавить канал(ы)
        3. Искать по ключевому слову"""

    action = get_choice_input(message, 1, 3)

    if action == 1:
        from managment.create_delete_category import choice_category

        return choice_category()

    if action == 2:
        pass
    if action == 3:
        pass


if __name__ == "__main__":
    main()
