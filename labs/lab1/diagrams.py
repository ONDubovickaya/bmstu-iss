import re
import os
import matplotlib.pyplot as plt

from functions import read_text


# 1) ВВОДНАЯ ЧАСТЬ
# 1.1) ВОЗВРАЩАЕМ ТЕКСТ ФАЙЛА
# text_1 = read_text('./writers/(Булгаков) Обучающая_5 вместе.txt')
# print(text_1[:500])

# 1.2) ПОЛУЧАЕМ ИМЯ АВТОРА ИЗ ИМЕНИ ФАЙЛА
# name_text_1 = './writers/(Булгаков) Обучающая_5 вместе.txt'
# print(re.findall(r'((?<=[(])\w.+(?=[)]))', name_text_1))

# 1.3) ПОЛУЧАЕМ МАССИВ ИМЁН АВТОРОВ
list_authors_names = []

for i in os.listdir('./writers'):
    list_authors_names.append(re.findall(r'((?<=[(])[А-я].+(?=[)]))', i)[0])

writers = sorted(list(set(list_authors_names)))
writers_count = len(writers)

# 1.4) ПОЛУЧАЕМ МАССИВЫ ТЕКСТОВ ДЛЯ ОБУЧАЮЩЕЙ И ТЕСТОВОЙ ВЫБОРОК
train_text = []
test_text = []

count_train = 0
count_test = 0

for name in writers:
    for filename in os.listdir('./writers'):
        if name in filename:
            if 'Обучающая' in filename:
                print(f'В обучающую выборку добавлен {name}[{count_train}]')
                train_text.append(read_text(f'./writers/{filename}'))
                count_train += 1

            else:
                print(f'В тестовую выборку добавлен {name}[{count_test}]')
                test_text.append(read_text(f'./writers/{filename}'))
                count_test += 1

    print('-' * 100)

"""
for item in range(writers_count):
    print(f'Класс: {writers[item]}[{item}]')
    print(f'  train: {train_text[item][:200]}')
    print(f'  test : {test_text[item][:200]}')
    print()
"""

# 1.5) ГРАФИКИ РАСПРЕДЕЛЕНИЯ ТЕКСТОВ ПО ПИСАТЕЛЯМ
plt.style.use('ggplot')
plt.figure(figsize=(15, 5))

color_list_bar = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
color_list_pie = [0.6, 0.68, 0.72, 0.85, 0.95, 1.]

colors_bar = plt.cm.viridis(color_list_bar)
colors_pie = plt.cm.viridis(color_list_pie)

text_lengths = list(map(len, train_text))

# СТОЛБЧАТАЯ ДИАГРАММА
plt.subplot(1, 2, 1)
plt.bar(writers, text_lengths, color=colors_bar)

for i, count in enumerate(text_lengths):
    plt.text(i, count - 200000, str(count), ha='center', color='white', fontweight='bold')

plt.xticks(rotation=45, ha='right', color=colors_bar[1])
plt.xlabel('Писатели', color='m')
plt.ylabel('Длина текста', color='b')
plt.title('Длина текста для каждого писателя', color=colors_bar[0])

# КРУГОВАЯ ДИАГРАММА
plt.subplot(1, 2, 2)
plt.pie(text_lengths, labels=writers, colors=colors_pie, autopct='%1.1f%%', startangle=90, counterclock=False)
plt.title('Рапределение текстов по писателям', color=colors_bar[0])

# регулируем расположение графиков и выводим их
plt.tight_layout()
# plt.show()
plt.savefig('./diagrams/texts_distribution.png', bbox_inches='tight')
