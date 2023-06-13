import os
import re


def clear_screen():
    os.system("cls")


def get_choice_input(message: str, min_num: int, max_num: int):
    while True:
        print(message)
        choice_input = input()

        if choice_input.isnumeric():
            choice_input_num = int(choice_input)

            if not (min_num <= choice_input_num <= max_num):
                clear_screen()
                print(f"Проверьте корректность введенного значения!")
                continue
            else:
                return choice_input_num
        else:
            clear_screen()
            print("Вы должны ввести число!")


def is_valid_filename(filename):
    pattern = r"^[а-яА-Яa-zA-Z0-9\s!#$%&\'()\-\@^_`{}~.]+$"

    # Проверка соответствия имени файла паттерну
    if re.match(pattern, filename):
        # Проверка длины имени файла
        if len(filename) <= 255:
            # Проверка наличия символов, отличных от пробела и точки
            if not (filename.strip() == "." or filename.strip() == ""):
                return filename
            else:
                print("\nИмя файла не может состоять только из пробелов или точек.")
        else:
            print("\nДлина имени файла превышает 255 символов.")
    else:
        print("\nИмя файла содержит недопустимые символы.")

    return False
