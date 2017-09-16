from typing import *
from copy import deepcopy


class Cell:

    row: int = 0
    column: int = 0
    value: float = 0.0

    def __init__(self, row: int, column: int, value: float) -> None:
        self.row = row
        self.column = column
        self.value = value

    def __str__(self) -> str:
        return "{}".format(self.value)


class Solver:

    debug: bool = False

    matrix: List[Cell]
    original_matrix: List[Cell]

    min_len: float = 0

    def __init__(self, fname: str)->None:
        input_values: List[Cell] = []
        with open(fname) as f:
            for i, line in enumerate(f):
                for j, elem in enumerate(line.strip().split()):
                    if elem == '-':
                        input_values.append(Cell(i, j, float('inf')))
                        continue
                    input_values.append(Cell(i, j, float(elem)))

        self.matrix = input_values
        self.original_matrix = deepcopy(input_values)

    def __str__(self) -> str:
        result = ""
        row = 0
        for elem in self.matrix:
            if row < elem.row:
                result += "\n"
            result += "{} ".format(elem)
            row = elem.row
        return result

    def get_column(self, index: int) -> List[Cell]:
        result: List[Cell] = []
        for item in self.matrix:
            if item.column == index:
                result.append(item)
        return result

    def get_row(self, index: int) -> List[Cell]:
        result: List[Cell] = []
        for item in self.matrix:
            if item.row == index:
                result.append(item)
        return result

    def get_min_from_row(self, index: int) -> Cell:
        return min(self.get_row(index), key=lambda x: x.value)

    def get_min_from_column(self, index: int) -> Cell:
        return min(self.get_column(index), key=lambda x: x.value)

    def get_min_for_zero(self, i: int, j: int) -> float:
        row: List[Cell] = []
        col: List[Cell] = []
        for ii, elem in enumerate(self.get_row(i)):
            if ii != i:
                row.append(elem)
        for jj, elem in enumerate(self.get_column(j)):
            if jj != i:
                col.append(elem)
        return min(row, key=lambda x: x.value).value + min(col, key=lambda x: x.value).value

    def get_original_value(self, i: int, j: int) -> Cell:
        t: Cell
        for cell in self.original_matrix:
            if cell.row == i and cell.column == j:
                t = cell
                break
        return cell

    def minus_number_from_row(self, index: int, number: float) -> None:
        if self.debug and number != 0.0:
            print("Вычитаю из колонки {}, значение {}".format(index, number))
        for elem in self.matrix:
            if elem.row == index:
                elem.value -= number

    def minus_number_from_column(self, index: int, number: float) -> None:
        if self.debug and number != 0.0:
            print("Вычитаю из строки {}, значение {}".format(index, number))
        for elem in self.matrix:
            if elem.column == index:
                elem.value -= number

    def remove_row(self, index: int) -> None:
        if self.debug:
            print("Удаляю строку {}".format(index))
        new_matrix: List[Cell] = []
        for elem in self.matrix:
            if elem.row != index:
                new_matrix.append(elem)
        self.matrix = new_matrix

    def remove_column(self, index: int) -> None:
        if self.debug:
            print("Удаляю колонку {}".format(index))
        new_matrix: List[Cell] = []
        for elem in self.matrix:
            if elem.column != index:
                new_matrix.append(elem)
        self.matrix = new_matrix

    def max_way(self) -> Cell:
        ways: List[Cell] = []
        for elem in self.matrix:
            if elem.value == 0.0:
                leng = self.get_min_for_zero(elem.row, elem.column)
                ways.append(elem)
        return max(ways, key=lambda x: x.value)

    def found_min(self) -> None:
        min_rows: Dict[int, float] = {}
        min_cols: Dict[int, float] = {}

        for elem in self.matrix:
            if elem.row in min_rows:
                continue
            t = self.get_min_from_row(elem.row)
            min_rows[elem.row] = t.value
            self.minus_number_from_row(t.row, t.value)

        for elem in self.matrix:
            if elem.column in min_cols:
                continue
            t = self.get_min_from_column(elem.column)
            min_cols[elem.column] = t.value
            self.minus_number_from_column(t.column, t.value)
        if self.debug:
            print("Минимальные значения для строк {}".format(min_rows))
            print("Минимальные значения для столбцов {}".format(min_cols))
            print()
        self.min_len += sum(min_rows.values()) + sum(min_cols.values())

    def solve(self) -> float:
        way: Dict[Tuple[int, int], float] = {}
        while len(self.matrix) >= 1:
            self.found_min()
            temp = self.max_way()
            if self.debug:
                print(self)
            self.remove_row(temp.row)
            self.remove_column(temp.column)
            way[(temp.row, temp.column)] = self.get_original_value(
                temp.row, temp.column).value
            # self.matrix[j][i] = float('inf')
            if self.debug:
                print(self)
                print("Текущий путь")
                print(way)
                print("Длинна пути:")
                print(sum(way.values()))
        return sum(way.values())


def main():
    s = Solver('input.txt')
    print('Оригинальная матрица')
    print(s)

    s.debug = True

    way = s.solve()
    print()
    print("Получившийся путь:")
    print(way)
    print('Минимальный путь:')
    print(s.min_len)
    print()


if __name__ == '__main__':
    main()
