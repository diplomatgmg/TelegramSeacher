from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from managment.create_delete_category import choice_category
from managment.services import (
    validate_number_with_message,
    combine_words,
    get_category_files,
    get_action_for_channels,
    get_filename_from_extension,
    read_channels_from_csv,
    SESSION,
    convert_time,
)
from managment.settings import INDENT, CATEGORY_DIRECTORY_NAME

KEYWORDS = None


def get_keywords(old_keywords=None):
    global KEYWORDS

    if old_keywords is not None:
        keywords = input(
            f"\nПрошлые ключевые слова: {old_keywords}.\n"
            f"\nВведите ключевые слова или нажмите 'Enter', чтобы оставить прошлые.\n"
        )

        if keywords == "":
            return preparing_search(KEYWORDS, skip_category=True)
        else:
            KEYWORDS = combine_words(keywords)
            return preparing_search(KEYWORDS, skip_category=True)

    action_or_keywords = input(
        "\nВведите через пробел ключевые слова для поиска.\n"
        f'Для поиска двух слов используйте "+". '
        f'Например: "ядерное+оружие"'
        f"{INDENT}0. Выбрать другую категорию\n"
    )

    if action_or_keywords == "0":
        return preparing_search()
    else:
        keywords = action_or_keywords

    KEYWORDS = combine_words(keywords)
    return KEYWORDS


def print_hours_message(hours: int) -> None:
    if hours == 1:
        print(f"\nВыполняется поиск новостей за последний {'час'}")
    elif hours % 10 == 1 and hours % 100 != 11:
        print(f"\nВыполняется поиск новостей за последний {hours} час")
    elif hours % 10 in (2, 3, 4) and hours % 100 not in (12, 13, 14):
        print(f"\nВыполняется поиск новостей за последние {hours} часа")
    else:
        print(f"\nВыполняется поиск новостей за последние {hours} часов")


def preparing_search(old_keywords: list = None, skip_category=False):
    global KEYWORDS

    if not skip_category:
        category_files = get_category_files()

        if not category_files:
            print("\nУ вас нет категорий для поиска!")
            return choice_category()

        action = get_action_for_channels(
            "\nВыберите категорию для поиска каналов", category_files
        )

        if action == 0:
            from main import main

            return main()

        selected_category_with_extension = category_files[action]
        selected_category_for_print = get_filename_from_extension(
            selected_category_with_extension
        )
        category_path = f"{CATEGORY_DIRECTORY_NAME}/{selected_category_with_extension}"

        print(f'\nВы выбрали категорию "{selected_category_for_print}"')

    if old_keywords is None and KEYWORDS is None:
        KEYWORDS = get_keywords()

    print(f"\nКлючевые слова: {str(KEYWORDS)}")

    min_num = 0
    max_num = 96

    message = (
        f"\nЗа какое время искать? (в часах). "
        f"От {min_num} до {max_num}. "
        f"{INDENT}0. Ввести заново ключевые слова"
    )

    time_interval = validate_number_with_message(message, min_num, max_num)

    if time_interval == 0:
        return get_keywords(KEYWORDS)

    print_hours_message(time_interval)

    return searcher(category_path, time_interval)


def searcher(category_path: str, time_interval: int):
    datetime_interval = datetime.now() - timedelta(hours=time_interval)
    channels_dict = read_channels_from_csv(category_path)

    for channel_href, channel_name in channels_dict.items():
        channel_page = SESSION.get(channel_href)
        channel_soup = BeautifulSoup(channel_page.content, "html.parser")

        messages_block_channel = reversed(
            channel_soup.find_all(
                "div",
                class_="tgme_widget_message text_not_supported_wrap js-widget_message",
            )
        )

        for message_block in messages_block_channel:
            message_time_and_href = message_block.find(
                "a", class_="tgme_widget_message_date"
            )

            message_str_time = message_time_and_href.find("time")["datetime"]
            message_href = message_time_and_href["href"]

            message_time = convert_time(message_str_time)
            print(message_time, message_href)

            if message_time < datetime_interval:
                break
            else:
                pass

            # TODO
