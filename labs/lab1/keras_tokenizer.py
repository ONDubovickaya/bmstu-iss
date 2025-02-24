import time
import re

import numpy as np
import matplotlib.pyplot as plt

from functions import read_text, print_text_stats, vectorize_sequence

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tensorflow.keras.preprocessing.text import Tokenizer


# объем словаря токенайзера
MAX_WORDS_COUNT = 20000

# как кол-во слов в "окне" (отрезок текста)
# размер каждой подвыборки внутри словаря
WINDOW_SIZE = 1000

# как шаг окна разбиения текста на векторы
# смещение для получения новой отличающейся подвыборки
WINDOW_STEP = 100


# контекстный менеджер для измерения времени операций
# операция обертывается менеджером с помощью оператора with
class timex:
    def __enter__(self):
        # фиксация времени старта процесса
        self.t = time.time()
        return self

    def __exit__(self, type, value, traceback):
        # вывод времени работы
        print('\033[91mВремя обработки: {:.2f} с\033[0m'.format(time.time() - self.t))


authors_names = []
train_text = []
test_text = []

count_train = 0
count_test = 0

for i in os.listdir('./writers'):
    authors_names.append(re.findall(r'((?<=[(])[А-я].+(?=[)]))', i)[0])

writers_list = sorted(list(set(authors_names)))
writers_count = len(writers_list)

for writer in writers_list:
    for filename in os.listdir('./writers'):
        if writer in filename:
            if 'Обучающая' in filename:
                print(f'В обучающую выборку добавлен {writer}[{count_train}]')
                train_text.append(read_text(f'./writers/{filename}'))
                count_train += 1

            else:
                print(f'В тестовую выборку добавлен {writer}[{count_test}]')
                test_text.append(read_text(f'./writers/{filename}'))
                count_test += 1

    print('-' * 100)

print('-' * 100)
with timex():
    print("Построение частотного словаря по обучающим текстам..")
    tokenizer = Tokenizer(num_words=MAX_WORDS_COUNT,
                          filters='!"#$%&()*+,-–—./…:;<=>?@[\]^_`{|}~«»\t\n\xa0\ufeff',
                          lower=True,
                          split=' ',
                          oov_token='неизвестное_слово',
                          char_level=False)

    # построение частотного словаря по обучающим текстам
    tokenizer.fit_on_texts(train_text)
    items = list(tokenizer.word_index.items())

print('-' * 100)
# вывод первых 120 слов (наиболее встречающиеся)
print(items[:120])
# вывод слов с 10001 по 10120 (по индексам списка с 10000 по 10119)
print(items[10000:10120])

# вывод реального кол-ва слов в словаре
# причём только 1-ые num_words используются при построении послед-ности индексов слов и векторов bag of words
print(f"Размер частотного словаря: {len(items)}")
print('-' * 100)

# ПОСТРОЕНИЕ ГРАФИКА ДЛЯ КОРПУСА ОБУЧАЮЩЕГО ТЕКСТА
species = ('TEXT')
sex_counts = {
    'MAX_WORDS_COUNT': np.array([20_000]),
    'TOTAL': np.array([133_070])
}
width = 0.6

fig, ax = plt.subplots(figsize=(2, 6))
bottom = np.zeros(3)

colors = {
    'MAX_WORDS_COUNT': '#ff9933',
    'TOTAL': '#0099cc'
}

for sex, sex_counts in sex_counts.items():
    p = ax.bar(species, sex_counts, width, label=sex, bottom=bottom, color=colors.get(sex, 'gray'))
    bottom += sex_counts
    ax.bar_label(p, label_type='center', color='black')

ax.set_title('Корпус обучающего текста')
plt.savefig('./diagrams/train_text_corpus.png', bbox_inches='tight')

"""
try:
    print('Интересующее слово имеет индекс:', tokenizer.word_index[input('Введите слово: ')])
except:
    print('Интересующего вас слова нет в словаре')
"""

with timex():
    print("Построение последовательности индексов слов по обучающим текстам..")
    sequence_train = tokenizer.texts_to_sequences(train_text)
    print("Построение последовательности индексов слов по тестовым текстам..")
    sequence_test = tokenizer.texts_to_sequences(test_text)

print('-' * 100)
print(dict(zip(train_text[1].replace('\ufeff', '').split()[:10], sequence_train[1][:10])))
print('-' * 100)
print('-' * 100)

print_text_stats('обучающим', train_text, sequence_train, writers_list)
print_text_stats('тестовым', test_text, sequence_test, writers_list)

print('-' * 100)
# ФОРМИРОВАНИЕ ОБУЧАЮЩЕЙ И ТЕСТОВОЙ ВЫБОРОК
with timex():
    print("Формирование обучающей выборки..")
    x_train, y_train = vectorize_sequence(sequence_train, WINDOW_SIZE, WINDOW_STEP)

    print("Формирование тестовой выборки..")
    x_test, y_test = vectorize_sequence(sequence_test, WINDOW_SIZE, WINDOW_STEP)

    print("\nФормы сформированных данных:")
    print(f"x_train: {x_train.shape}\ny_train: {y_train.shape}\n")
    print(f"x_test: {x_test.shape}\ny_test: {y_test.shape}")

print('-' * 100)
print(y_train[0])
print(len(x_train[0]), end='\n\n')
print(x_train[0][:100])
print(x_train.shape)

print('-' * 100)
with timex():
    print("Формирование обучающей выборки в формате Bag Of Words..")
    x_train_01 = tokenizer.sequences_to_matrix(x_train.tolist())
    print("Формирование тестовой выборки в формате Bag Of Words..")
    x_test_01 = tokenizer.sequences_to_matrix(x_test.tolist())

    print(f"\nФорма обучающей выборки в виде разреженной матрицы Bag of Words: {x_train_01.shape}")
    print(f"Фрагмент отрезка обучающего текста в виде Bag of Words:\n{x_train_01[0][0:100]}")

print('-' * 100)
