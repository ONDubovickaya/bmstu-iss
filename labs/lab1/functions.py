import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tensorflow.keras import utils


# ф-ция для считывания текста файла
def read_text(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        text = text.replace('\n', ' ')
    return text


# ф-ция для вывода статистики по загруженным текстам
def print_text_stats(title, texts, sequences, class_labels):
    chars = 0
    words = 0

    print(f'Статистика по {title} текстам:')

    for writer_name in range(len(class_labels)):
        print(f'{class_labels[writer_name]:<15} '
              f'{len(texts[writer_name]):9} символов, '
              f'{len(sequences[writer_name]):8} слов')

        chars += len(texts[writer_name])
        words += len(sequences[writer_name])

    print('----')
    print(f'{"В сумме":<15} {chars:9} символов, {words:8} слов\n')


# ф-ция для прохождения послед-ности окнами с заданным шагом
def split_sequence(sequence, window_size, window_hop):
    return [sequence[i:i + window_size] for i in range(0, len(sequence) - window_size + 1, window_hop)]


# ф-ция для формирования выборок из послед-ностей индексов
# формирует выборку отрезков и соответствующих им меток классов в виде OHE
# OHE -- one hot encoding
def vectorize_sequence(sequence_list, window_size, window_hop):
    class_count = len(sequence_list)
    x, y = [], []

    for item in range(class_count):
        vectors = split_sequence(sequence_list[item], window_size, window_hop)
        x += vectors
        y += [utils.to_categorical(item, class_count)] * len(vectors)

    return np.array(x), np.array(y)


# ф-ция компиляции и обучения модели нейронной сети
def compile_train_model(schema_file, model, x_train, y_train, x_value, y_value, optimizer='adam',
                        epochs=50, batch_size=128, figsize=(20, 5)):

    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_value, y_value))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle('График процесса обучения модели')

    ax1.plot(history.history['accuracy'], label='Доля верных ответов на обучающем наборе')
    ax1.plot(history.history['val_accuracy'], label='Доля верных ответов на тестовом наборе')

    ax1.xaxis.get_major_locator().set_params(integer=True)

    ax1.set_xlabel('Эпоха обучения')
    ax1.set_ylabel('Доля верных ответов')
    ax1.legend()

    ax2.plot(history.history['loss'], label='Ошибка на обучающем наборе')
    ax2.plot(history.history['val_loss'], label='Ошибка на тестовом наборе')

    ax2.xaxis.get_major_locator().set_params(integer=True)

    ax2.set_xlabel('Эпоха обучения')
    ax2.set_ylabel('Ошибка')
    ax2.legend()

    plt.savefig(f'./diagrams/{schema_file}_ctm.png', bbox_inches='tight')


# ф-ция вывода р-тов оценки модели на заданных данных
def eval_model(schema_file, model, x, y_true, class_labels=[],
               cm_round=3, title='', figsize=(10, 10)):

    plt.style.use('default')

    y_predicted = model.predict(x)

    cm = confusion_matrix(np.argmax(y_true, axis=1),
                          np.argmax(y_predicted, axis=1),
                          normalize='true')

    cm = np.around(cm, cm_round)

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(f'Нейросеть {title}: нормализованная матрица ошибок', fontsize=18)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_labels)
    disp.plot(ax=ax)

    plt.gca().images[-1].colorbar.remove()
    plt.xlabel('Предсказанные классы', fontsize=16)
    plt.ylabel('Верные классы', fontsize=16)

    fig.autofmt_xdate(rotation=45)
    plt.savefig(f'./diagrams/{schema_file}_em.png', bbox_inches='tight')

    print('-'*100)
    print(f'Нейросеть: {title}')

    for class_name in range(len(class_labels)):
        class_predicted = np.argmax(cm[class_name])
        message = 'ВЕРНО :-)' if class_predicted == class_name else 'НЕВЕРНО :-('
        print('Класс: {:<20} {:3.0f}% сеть отнесла к классу {:<20} - {}'.format(class_labels[class_name],
                                                                                100. * cm[class_name, class_predicted],
                                                                                class_labels[class_predicted],
                                                                                message))

    print('\nСредняя точность распознавания: {:3.0f}%'.format(100. * cm.diagonal().mean()))


# совместная функция обучения и оценки модели нейронной сети
def compile_train_eval_model(schema_file, model, x_train, y_train, x_test, y_test,
                             class_labels, title, optimizer='adam', epochs=50,
                             batch_size=128, graph_size=(20, 5), cm_size=(10, 10)):
    compile_train_model(schema_file, model, x_train, y_train, x_test, y_test,
                        optimizer=optimizer, epochs=epochs, batch_size=batch_size, figsize=graph_size)

    eval_model(schema_file, model, x_test, y_test,
               class_labels=class_labels,
               title=title, figsize=cm_size)
