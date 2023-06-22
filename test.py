




class Text:
    def __init__(self, text: str):
        self.text = self.validate_str(text)
        self.filtered_text = self.get_only_words()

    @staticmethod
    def validate_str(text):
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return text

    def get_only_words(self):
        return ''.join(filter(lambda x: x.isalpha() or x.isspace(), self.text.lower()))

    def get_max_length(self):
        return max(self.filtered_text.split(), key=len)

    def get_most_frequent_word(self):
        words = dict()

        for word in self.filtered_text.split():
            if len(word) >= 3:
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
        return sorted(words.items(), key=lambda x: -x[1])[0]

    def get_count_special_symbols(self):
        symbols = list(filter(lambda x: not x.isspace() and not x.isalpha() and not x.isnumeric(), self.text))
        return len(symbols)

    def get_palindromes(self):
        palindromes = []

        for word in self.filtered_text.split():
            filter_word = ''.join(filter(lambda x: x.isalpha(), word))
            if len(filter_word) >= 3 and filter_word == filter_word[::-1]:
                palindromes.append(filter_word)

        return palindromes


book_words = 'Замысел эпопеи мамам формировался парарап задолго до начала работы над тем текстом, который известен под названием задолго «Война и мир». В наброске предисловия к «Войне и миру» Толстой писал, что в 1856 году начал писать эпопеи повесть, «герой которой должен эпопеи был быть декабрист, возвращающийся с семейством в Россию. Невольно от настоящего я перешёл к 1825 году… Но и в 1825 году герой мой был уже возмужалым, семейным человеком. Чтобы понять его, мне нужно было перенестись к его молодости, и молодость его совпала с … эпохой 1812 года… Ежели причина нашего торжества была не случайна, но лежала в сущности характера русского народа и войска, то характер этот должен был выразиться ещё ярче в эпоху неудач и поражений…» Так Лев Николаевич постепенно пришёл к необходимости начать повествование с 1805 года.'

obj = Text(book_words)

print(obj.get_only_words())
print(obj.get_max_length())
print(obj.get_most_frequent_word())
print(obj.get_count_special_symbols())
print(obj.get_palindromes())



