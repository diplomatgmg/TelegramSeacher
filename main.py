from managment.services import get_choice_input
from managment.settings import DEBUG


def main():
    message = """\nЧто Вы хотите сделать? 
        1. Создать/удалить категорию
        2. Добавить/удалить каналы
        3. Искать по ключевому слову"""

    action = get_choice_input(message, 1, 3)

    if action == 1:
        from managment.create_delete_category import choice_category

        return choice_category()

    elif action == 2:
        from managment.add_delete_channels import choice_channels

        return choice_channels()
    elif action == 3:
        pass


if __name__ == "__main__":
    if DEBUG:
        print("Включен режим отладки")

    main()
