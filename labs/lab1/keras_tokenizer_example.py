import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tensorflow.keras.preprocessing.text import Tokenizer
# import pickle


sample_text = ['один два две двум двум двум три четыре пять два '
               'Три три четыре четыре четыре пять пять пять пять шесть семь восемь']

print(f"Sample text contains {len(sample_text[0].split())} words")

# разбиение текста и построение частотного словаря
# num_words -- объем словаря
# filters -- убираемые из текста ненужные символы
# lower -- приведение слов к нижнему регистру
# split -- разделитель слов
# char_level -- указание разделять по словам, а не по единичным символам
# oov_token -- токен для слов, которые не вошли в словарь
tokenizer = Tokenizer(num_words=5,
                      filters='!"#$%&()*+,-–—./…:;<=>?@[\]^_`{|}~«»\t\n\xa0\ufeff',
                      lower=True,
                      split=' ',
                      oov_token='неизвестное_слово',
                      char_level=False)

# построение частотного словаря по тексту
tokenizer.fit_on_texts(sample_text)

# сохранение объекта-токенизатора в файл
# with open('tokenizer.pickle', 'wb') as f:
    # pickle.dump(tokenizer, f)

# вывод словаря токенизатора с индексами слов
print(tokenizer.word_index)

# вывод представления словаря в виде списка пар (слово, индекс)
print(list(tokenizer.word_index.items()))

sample_text = ['один трем два три четыре пять два два '
               'Три три четыре четыре четыре пять пять пять пять шесть семь восемь']

# представление исходного текста в виде последовательности индексов слов
sample_seq = tokenizer.texts_to_sequences(sample_text)
print(sample_seq)
print(len(sample_seq[0]))

x_train = [sample_seq[0][i:i + 3] for i in range(0, len(sample_seq[0]), 3)]
print(x_train)

# Представление списка подпоследовательностей в виде разреженной матрицы:
# каждая подпоследовательность представляется как вектор bag of words
print(tokenizer.sequences_to_matrix(x_train))
