from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from managment.create_delete_category import choice_category
from managment.send_tg import send_telegram
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
from managment.settings import INDENT, CATEGORY_DIRECTORY_NAME, TELEGRAM_DOMAIN, DEBUG

KEYWORDS = list()


def get_keywords(old_keywords=None, category_path=None):
    global KEYWORDS

    if old_keywords:
        keywords = input(
            f"\nПрошлые ключевые слова: {old_keywords}.\n"
            f"\nВведите ключевые слова или нажмите 'Enter', чтобы оставить прошлые.\n"
        )

        if keywords == "":
            return preparing_search(KEYWORDS, skip_category=True)
        else:
            KEYWORDS = combine_words(keywords)
            return preparing_search(
                KEYWORDS, skip_category=True, category_path=category_path
            )

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


def preparing_search(
        old_keywords: list = None, skip_category=False, category_path=None
):
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

    channels_dict = read_channels_from_csv(category_path)

    if not channels_dict:
        print(f'\nВ категории "{selected_category_for_print}" '
              f'нет ни одного канала! Добавьте или выберите другую категорию!')
        return preparing_search(old_keywords, skip_category, category_path)



    if not old_keywords and not KEYWORDS:
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
        return get_keywords(KEYWORDS, category_path)

    print_hours_message(time_interval)

    return searcher(channels_dict, time_interval)


def searcher(channels_dict: dict, time_interval: int):
    global KEYWORDS

    datetime_interval = datetime.now() - timedelta(hours=time_interval)

    for channel_href, channel_name in channels_dict.items():
        bad_time = False  # Если все посты в ленте подходят по времени
        channel_page_next = None
        incorrect_channel = False

        while not bad_time and not incorrect_channel:
            channel_page = SESSION.get(channel_page_next or channel_href)
            channel_soup = BeautifulSoup(channel_page.content, "html.parser")

            # Парсим посты снизу в верх
            messages_blocks = reversed(
                channel_soup.find_all(
                    "div",
                    class_="tgme_widget_message text_not_supported_wrap js-widget_message",
                )
            )

            for message_block in messages_blocks:
                message_time_and_href = message_block.find(
                    "a", class_="tgme_widget_message_date"
                )

                message_str_time = message_time_and_href.find("time")["datetime"]
                message_href = message_time_and_href["href"]

                message_time = convert_time(message_str_time)

                if message_time < datetime_interval:
                    bad_time = True  # Пост в ленте идет раньше временного интервала, дальше смысла искать нет
                    break

                message_raw = message_block.find(
                    "div", class_="tgme_widget_message_text js-message_text"
                )

                if not message_raw:
                    continue

                message = message_raw.text.strip()

                if any(keyword in message.lower().split() for keyword in KEYWORDS):
                    to_send = f"{channel_name}\n({message_href})\n\n" f"{message}"

                    if not DEBUG:
                        print(f'Новость подходит! [{channel_name}]')
                        send_telegram(to_send)
                    else:
                        print("=" * 80)
                        print(to_send)

            if not bad_time:
                channel_page_next_raw = channel_soup.find(
                    "a", class_="tme_messages_more"
                )  # /s/....?before=...

                if not channel_page_next_raw:
                    print(f"Не удалось найти посты на канале [{channel_name}]")
                    incorrect_channel = True
                    continue

                channel_page_next = TELEGRAM_DOMAIN + channel_page_next_raw["href"]
