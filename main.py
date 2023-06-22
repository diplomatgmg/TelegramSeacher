import sys
from dotenv import load_dotenv
from managment.services import validate_number_with_message
from managment.settings import DEBUG, INDENT


def main():
    message = (
        f"\nЧто Вы хотите сделать? "
        f"{INDENT}1. Создать/удалить категорию"
        f"{INDENT}2. Добавить/удалить каналы"
        f"{INDENT}3. Искать по ключевому слову"
    )

    action = validate_number_with_message(message, 1, 3)

    if action == 1:
        from managment.create_delete_category import choice_category
        return choice_category()

    elif action == 2:
        from managment.add_remove_channels import choice_channels
        return choice_channels()

    elif action == 3:
        from managment.searcher import preparing_search
        preparing_search()


if __name__ == "__main__":
    load_dotenv()

    if DEBUG:
        print("\nВключен режим отладки")

    try:
        main()
        input('\nПоиск новостей окончен. Для выхода нажмите Enter\n')
    except:
        input('\nПроизошла ошибка при работе программы. Обратитесь к программисту\n')
    finally:
        sys.exit()
