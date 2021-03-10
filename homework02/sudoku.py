import pathlib
import random
import typing as tp
from typing import List

T = tp.TypeVar("T")


def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in "123456789."]
    grid = group(digits, 9)
    return grid


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    Lists = []
    while values:
        Lists.append(values[:n])
        del values[:n]
    return Lists


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    Cols = []
    for i in range(len(grid)):
        Cols.append(grid[i][pos[1]])
    return Cols


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    start = (0, 3, 6)
    for row in grid[start[pos[0] // 3] : start[pos[0] // 3] + 3]:
        block.extend(row[start[pos[1] // 3] : start[pos[1] // 3] + 3])
    return block


def get_diagonal(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List:
    """Возвращает все значения диагоналей, в который попадает позиция pos

>>> grid = [["0", "2", "3", "4", "5", "6", "7", "8", "1"], \
                ["1", "0", "3", "4", "5", "6", "7", "1", "9"], \
                ["1", "2", "0", "4", "5", "6", "1", "8", "9"], \
                ["1", "2", "3", "0", "5", "1", "7", "8", "9"], \
                ["1", "2", "3", "4", "0", "6", "7", "8", "9"], \
                ["1", "2", "3", "1", "5", "0", "7", "8", "9"], \
                ["1", "2", "1", "4", "5", "6", "0", "8", "9"], \
                ["1", "1", "3", "4", "5", "6", "7", "0", "9"], \
                ["1", "2", "3", "4", "5", "6", "7", "8", "0"]]
    >>> get_diagonal(grid, (0, 0))
    ['0', '0', '0', '0', '0', '0', '0', '0', '0']
    >>> get_diagonal(grid, (1, 1))
    ['0', '0', '0', '0', '0', '0', '0', '0', '0']
    >>> get_diagonal(grid, (3, 3))
    ['0', '0', '0', '0', '0', '0', '0', '0', '0']
    >>> get_diagonal(grid, (8, 8))
    ['0', '0', '0', '0', '0', '0', '0', '0', '0']
    >>> get_diagonal(grid, (7, 7))
    ['0', '0', '0', '0', '0', '0', '0', '0', '0']
    >>> get_diagonal(grid, (8, 0))
    ['1', '1', '1', '1', '0', '1', '1', '1', '1']
    >>> get_diagonal(grid, (2, 6))
    ['1', '1', '1', '1', '0', '1', '1', '1', '1']
    >>> get_diagonal(grid, (6, 2))
    ['1', '1', '1', '1', '0', '1', '1', '1', '1'] 
    """
    diagonal_left = []  # вот такая диагональ - \
    diagonal_right = []  # вот такая диагональ - /

    # работаем с ЛЕВОЙ диагональю
    # запишем в список все значения диагонали от позиции pos и влево
    top = pos[0]
    left = pos[1]
    while top != 0 and left != 0:
        diagonal_left.append(grid[top - 1][left - 1])
        top -= 1
        left -= 1

    # получим результат "снизу вверх", преобразуем в "сверху вниз"
    diagonal_left.reverse()

    # дополним список значениями диагонали от позиции pos и вправо
    bottom = pos[0]
    right = pos[1]
    while bottom != 9 and right != 9:
        diagonal_left.append(grid[bottom][right])
        bottom += 1
        right += 1

    # работаем с ПРАВОЙ диагональю
    # запишем в список все значения диагонали от позиции pos и вправо
    top = pos[0]
    right = pos[1]
    while top != 0 and right != 9:
        diagonal_right.append(grid[top - 1][right + 1])
        top -= 1
        right += 1

    # получим результат "снизу вверх", преобразуем в "сверху вниз"
    diagonal_right.reverse()

    # запишем в список все значения диагонали от позиции pos и влево
    bottom = pos[0]  # row
    left = pos[1]  # col
    while bottom != 9 and left != -1:
        diagonal_right.append(grid[bottom][left])
        bottom += 1
        left -= 1

    # если попали на цент. клетку, то вернем две диагонали
    # если в правой диагонали оказалось больше значений, то мы должны вернуть ее
    # во всех остальных случаях возвращаем левую
    if pos[0] == pos[1] == 4:
        return (diagonal_left, diagonal_right)  # type: ignore
    elif len(diagonal_right) > len(diagonal_left):
        return diagonal_right
    else:
        return diagonal_left


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    _set = set()
    for i in range(1, 10):
        _set.add(str(i))
    _set -= set(get_row(grid, pos))
    _set -= set(get_col(grid, pos))
    _set -= set(get_block(grid, pos))
    return _set


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    row, col = pos
    for i in find_possible_values(grid, pos):
        grid[row][col] = i
        answer = solve(grid)
        if answer:
            return answer
    grid[row][col] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    sol = solution
    for row in range(len(sol)):
        res = set(get_row(sol, (row, 0)))
        if res != set("123456789"):
            return False
    for col in range(len(sol)):
        res = set(get_col(sol, (0, col)))
        if res != set("123456789"):
            return False
    for row in range(0, (len(sol) - 1), 3):
        for col in range(0, (len(sol) - 1), 3):
            res = set(get_block(sol, (row, col)))
            if res != set("123456789"):
                return False
    return True


def generate_sudoku(N: int) -> tp.Optional[tp.List[tp.List[str]]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = solve([["."] * 9 for _ in range(9)])
    N = 81 - min(81, N)
    while N:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid is not None:
            if grid[row][col] != ".":
                grid[row][col] = "."
                N -= 1
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
