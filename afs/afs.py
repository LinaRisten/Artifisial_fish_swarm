import os
import sys
import functools
import itertools
import operator
import typing

import numpy as np

DIMENSION = 2
NUM_ITERATIONS = 200


def loss_sphere(x: np.array):
    return np.sum(x ** 2)


def loss_step(x: np.array):
    return np.sum(np.abs(x + 0.5) ** 0.5)


def loss_rastrigin(x: np.array):
    return DIMENSION * 10 + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x))


def loss_rosenbrock(x: np.array):
    odd = x[::2]
    even = x[1::2]
    return np.sum(100 * (even ** 2 - odd) ** 2 + (even - 1) ** 2)


class AFSAOptimizer:

    @staticmethod
    def random_from_ball(n_dim: int, radius: float):

        direction = np.random.normal(0, 1, size=(n_dim,))
        direction /= np.linalg.norm(direction)

        random_radius = np.random.rand() ** (1 / n_dim)
        return direction * random_radius * radius

    def __init__(self,
                 loss_function: typing.Callable[[np.array], float],
                 vision_radius: float,
                 step: float,
                 delta: float,

                 try_number: int):
        self._Loss = loss_function
        self._V = vision_radius
        self._S = step
        self._D = delta
        self._T = try_number
        self._X = []
        self._L = []
        self._minima_loss = None
        self._minima_coordinates = None

    def add_unit(self, x: np.array) -> None:
        # Функция добавляет к стае еще одну рыбку, координаты которой
        # передаются в виде вектора x
        self._X.append(x)
        self._L.append(self._Loss(x))
        if self.minima_loss is None or self.minima_loss > self._L[-1]:
            self._minima_coordinates = self._X[-1].copy()
            self._minima_loss = self._L[-1]

    def _af_prey_one(self, x: np.array) -> np.array:
        # одна рыбка, находящаяся в координате x совершает стадию охоты
        y = self._Loss(x)
        for _ in range(self._T):
            x_new = x + AFSAOptimizer.random_from_ball(len(x), self._V) * self._S
            y_new = self._Loss(x_new)

            if y_new < y:
                return x + (x_new - x) / np.linalg.norm(x_new - x) * self._S

        return x + AFSAOptimizer.random_from_ball(len(x), self._V)

    def af_prey(self):
        # Каждая из рыбок стаи совершает охоту
        for index in range(len(self._X)):
            self._X[index] = self._af_prey_one(self._X[index])
            self._L[index] = self._Loss(self._X[index])

    def af_swarm(self):
        # Каждая рыбка рыбка хочет пойти к центру стаи
        x_center = functools.reduce(operator.add, self._X) / len(self._X)
        x_future_coords = []
        for x_index, x in enumerate(self._X):
            num_neighbors = 0
            for other_index, other_unit in enumerate(self._X):
                if other_index != x_index and np.linalg.norm(x - other_unit) <= self._V:
                    num_neighbors += 1

            if num_neighbors / len(self._X) < self._D:
                x_future_coords.append(x + (x_center - x) / np.linalg.norm(x_center - x) * self._S)
            else:
                x_future_coords.append(self._af_prey_one(x))

        self._X = x_future_coords
        self._L = list(map(self._Loss, self._X))

    def af_follow(self):
        # Каждая рыбка находит в своем радиусе звения самого удачливого соседа
        # и пытается сделать шаг в его сторону
        x_future_coords = []
        for x_index, x in enumerate(self._X):

            best_neighbor_index = None
            best_neighbor_loss = None
            num_neighbors = 0
            for other_index, other_unit in enumerate(self._X):
                if other_index != x_index and np.linalg.norm(x - other_unit) <= self._V:
                    num_neighbors += 1
                    if best_neighbor_loss is None or best_neighbor_loss > self._L[other_index]:
                        best_neighbor_loss = self._L[other_index]
                        best_neighbor_index = other_index

            if best_neighbor_index is not None and self._L[x_index] > best_neighbor_loss:
                x_future_coords.append(
                    x + (self._X[best_neighbor_index] - x) / np.linalg.norm(self._X[best_neighbor_index] - x) * self._S
                )
            else:
                x_future_coords.append(self._af_prey_one(x))

        self._X = x_future_coords
        self._L = list(map(self._Loss, self._X))

    def af_move(self):
        # Каждая рыбка просто идет куда-то в поле своего зрения
        for index in range(len(self._X)):
            self._X[index] += AFSAOptimizer.random_from_ball(len(self._X[index]), self._V)
            self._L[index] = self._Loss(self._X[index])

    def af_leap(self):
        pass

    def do_step(self):
        # Все рыбки последовательно проходят через все стадии алгоритма
        self.af_prey()
        self.update_minima_info()

        self.af_swarm()
        self.update_minima_info()

        self.af_follow()
        self.update_minima_info()

        self.af_move()
        self.update_minima_info()

        self.af_leap()
        self.update_minima_info()

    def update_minima_info(self):
        # Проверяем, не находится ли какая-то рыбка в положении, более выгодном
        # чем любое из ранее посещенных и если это так, то устанавливаем
        # наилучшее найденное положение в положение этой рыбки
        for index in range(len(self._X)):
            if self._minima_loss is None or self._minima_loss > self._L[index]:
                self._minima_loss = self._L[index]
                self._minima_coordinates = self._X[index].copy()

    def get_coords(self) -> np.array:
        # Просто возвращает текущее положения всех рыбок, было нужно для
        # построения анимашек
        return np.array(self._X)

    def get_losses(self) -> np.array:
        # Возвращает успешность каждой рыбки на данный момент, тоже нужно было
        # для построения графиков (правой части)
        return np.array(self._L)

    @property
    def minima_loss(self) -> typing.Optional[float]:
        # Возвращает значение в наилучшей найденной точке
        return self._minima_loss

    @property
    def minima_coordinates(self) -> typing.Optional[np.array]:
        # Возвращает координаты самой лучшей найденой точки
        return self._minima_coordinates


# if __name__ == "__main__":
#     DIMENSION = 10
#     losses = [loss_sphere, loss_step, loss_rastrigin, loss_rosenbrock]
#
#     for loss in losses:
#         print(loss.__name__)
#         loss_function = loss
#
#         opt = AFSAOptimizer(loss_function, 0.5, 0.2, 0.5, 5)
#
#         for _ in range(15):
#             opt.add_unit(np.random.uniform(-10, 10, (DIMENSION,)))
#
#         for _ in range(NUM_ITERATIONS):
#             opt.do_step()
#
#         print('minimal loss = {:.06g}'.format(opt.minima_loss))
#
#         for _ in range(2000 - NUM_ITERATIONS):
#             opt.do_step()
#
#         print('minimal loss = {:.06g}'.format(opt.minima_loss))
#
#         print('-' * 40)

def run(function='loss_sphere', param_1=0.5, param_2=0.2, param_3=0.5, param_4=5):
    losses = {'loss_sphere': loss_sphere, 'loss_step': loss_step, 'loss_rastrigin': loss_rastrigin,
              'loss_rosenbrock': loss_rosenbrock}
    function = losses[function]
    result = dict()
    print(function.__name__)

    opt = AFSAOptimizer(function, param_1, param_2, param_3, param_4)

    for _ in range(15):
        opt.add_unit(np.random.uniform(-10, 10, (DIMENSION,)))

    for _ in range(NUM_ITERATIONS):
        opt.do_step()

    result['minima_loss_1'] = opt.minima_loss

    for _ in range(2000 - NUM_ITERATIONS):
        opt.do_step()

    result['minima_loss_2'] = opt.minima_loss
    return result


if __name__ == '__main__':
    DIMENSION = 10
    losses = ['loss_sphere', 'loss_step', 'loss_rastrigin', 'loss_rosenbrock']

    for loss in losses:
        result = run(loss)
        # print(f'minima_loss_1: {result["minima_loss_1"]}\nminima_loss_2: {result["minima_loss_2"]}\n', end='-'*40)
        print('minima_loss_1: {minima_loss_1}\nminima_loss_2: {minima_loss_2}\n'.format(minima_loss_1=result["minima_loss_1"],
            minima_loss_2=result["minima_loss_2"]), end='-'*40)
