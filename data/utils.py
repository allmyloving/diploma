from data import constants
import os


def count_symbols(lang):
    total_len = 0
    text_lang_folder = os.path.join(constants.WIKIPEDIA_TEXT_FOLDER, lang)
    for file in os.listdir(text_lang_folder):
        total_len += len(open(os.path.join(text_lang_folder, file), encoding='utf-8').read())
    return total_len


print(count_symbols('ru'))
print(count_symbols('uk'))
print(count_symbols('sr'))
