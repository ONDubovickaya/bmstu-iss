import numpy as np

from functions import split_sequence


arr = np.arange(100)

example = []

# при таком разбиении с шагом 10 и общем кол-ве эл-тов 100 подмассивы не всегда будут длины 20
# (последний подмассив будет длины 10)
print("1) Срезы по 20 эл-тов с шагом 10:")
for i in range(0, len(arr), 10):
    print(arr[i:i + 20])
    example.append(arr[i:i + 20])

# example = np.array(example)
# print(f"\nNumpy-массив:\n{example}")

example = []

for i in range(0, len(arr)-20+1, 10):
  example.append(arr[i:i + 20])

example = np.array(example)

print(f"\n2) Срезы по 20 эл-тов с шагом 10\n(пока кол-во оставшихся эл-тов больше или равно 20):\n{example}")
print(f"\nФорма numpy-массива (кол-во срезов, кол-во эл-тов в срезе):\n{example.shape}\n")

print("3) Использование ф-ции split_sequence:")
vec = split_sequence(arr, window_size=20, window_hop=10)
print(f"> Массив подмассивов:\n{np.array(vec)}")
print(f"> Numpy-массив:\n{vec}")

print("\n4) Удвоение существующего массива:")
x1 = []

vec = split_sequence(arr, window_size=20, window_hop=10)
x1 += vec

vec = split_sequence(arr, window_size=20, window_hop=10)
x1 += vec
x2 = np.array(x1)
print(f"> Полученный удвоенный массив:\n{x2}")
print(f"> Форма удвоенного массива: {x2.shape}")