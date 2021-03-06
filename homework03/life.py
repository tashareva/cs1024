import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1
        # Минимальная сумма элементов, находящихся на поле
        self.minisum = float("inf")

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        if randomize:
            matrix = [[random.randint(0, 1) for y in range(self.cols)] for x in range(self.rows)]
            return matrix
        if not randomize:
            matrix = [[0 for y in range(self.cols)] for x in range(self.rows)]
        return matrix

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighb = []
        row, col = cell
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if (i, j) != cell:
                    neighb.append(self.curr_generation[i][j])
        return neighb

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        copy_grid = self.create_grid(False)
        for i in range(self.rows):
            for j in range(self.cols):
                if (self.curr_generation[i][j] == 0) and sum(self.get_neighbours((i, j))) == 3:
                    copy_grid[i][j] = 1
                elif (self.curr_generation[i][j] == 1) and (
                    1 < sum(self.get_neighbours((i, j))) < 4
                ):
                    copy_grid[i][j] = 1
        return copy_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    def elements_sum(self) -> int:
        """
        Сумма элементов текущего поколения
        Returns
        ----------
        out: int
        """

        el_sum = 0
        for i in range(self.rows):
            for j in range(self.cols):
                el_sum += self.curr_generation[i][j]
        return el_sum

    def checking(self) -> bool:
        """
        Проверка на зацикливание игры.
        ----------
        out: bool
        """

        el_sum = self.elements_sum
        if el_sum < self.minisum:  # type: ignore
            self.proizv = self.rows * self.cols
            self.minisum = el_sum  # type: ignore
            return False
        else:
            self.proizv -= 1
            if self.proizv == 0:
                return True
            else:
                return False

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations == self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        doc = open(filename, "r")
        doc_grid = [[int(col) for col in row.strip()] for row in doc]
        doc.close()
        game = GameOfLife((len(doc_grid), len(doc_grid[0])))
        game.curr_generation = doc_grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        doc = open(filename, "w")
        for row in self.curr_generation:
            for col in row:
                doc.write(str(col))
            doc.write("\n")
        doc.close()
