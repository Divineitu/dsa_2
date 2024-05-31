import glob
import os
import sys


class SparseMatrix:
    def __init__(self, rows=0, cols=0):
        self.rows_count = rows
        self.cols_count = cols
        self.values = {}

    @staticmethod
    def create_from_file(file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                rows = int(lines[0].strip().split('=')[1])
                cols = int(lines[1].strip().split('=')[1])
                matrix = SparseMatrix(rows, cols)
                for line in lines[2:]:
                    line = line.strip()
                    if not line:
                        continue
                    if line[0] != '(' or line[-1] != ')':
                        raise ValueError("Incorrect format in input file")
                    row, col, value = map(int, line[1:-1].split(','))
                    matrix.set_value(row, col, value)
                return matrix
        except Exception as e:
            raise ValueError(f"Error while processing file {file_path}: {e}")

    def set_value(self, row, col, value):
        if value != 0:
            self.values[(row, col)] = value
        elif (row, col) in self.values:
            del self.values[(row, col)]

    def get_value(self, row, col):
        return self.values.get((row, col), 0)

    def addition(self, other):
        if self.rows_count != other.rows_count or self.cols_count != other.cols_count:
            raise ValueError("Matrix dimensions must match for addition operation")
        result = SparseMatrix(self.rows_count, self.cols_count)
        for (row, col), value in self.values.items():
            result.set_value(row, col, value + other.get_value(row, col))
        for (row, col), value in other.values.items():
            if (row, col) not in self.values:
                result.set_value(row, col, value)
        return result

    def subtraction(self, other):
        if self.rows_count != other.rows_count or self.cols_count != other.cols_count:
            raise ValueError("Matrix dimensions must match for subtraction operation")
        result = SparseMatrix(self.rows_count, self.cols_count)
        for (row, col), value in self.values.items():
            result.set_value(row, col, value - other.get_value(row, col))
        for (row, col), value in other.values.items():
            if (row, col) not in self.values:
                result.set_value(row, col, -value)
        return result

    def multiplication(self, other):
        if self.cols_count != other.rows_count:
            raise ValueError(f"Matrix dimensions must match for multiplication: {self.cols_count} (cols) != {other.rows_count} (rows)")
        result = SparseMatrix(self.rows_count, other.cols_count)
        for (row, col), value in self.values.items():
            for k in range(other.cols_count):
                if (col, k) in other.values:
                    result.set_value(row, k, result.get_value(row, k) + value * other.get_value(col, k))
        return result

    def write_to_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(f"rows={self.rows_count}\n")
            f.write(f"cols={self.cols_count}\n")
            for (row, col), value in sorted(self.values.items()):
                f.write(f"({row}, {col}, {value})\n")


def execute_operations():
    if len(sys.argv) != 2:
        print("Usage: python sparse_matrix.py <operation>")
        print("Available operations: add, subtract, multiply")
        return

    operation = sys.argv[1]

    input_pattern = r'C:\Users\USER\PycharmProjects\SparseMatrix\dsa\sparse_matrix\sample_inputs\easy_sample_*.txt'
    input_files = glob.glob(input_pattern)

    print(f"Input files found: {input_files}")

    if len(input_files) < 2:
        print("Error: Not enough input files found.")
        return

    matrices = [SparseMatrix.create_from_file(file) for file in input_files]

    for i, matrix in enumerate(matrices, start=1):
        print(f"Matrix {i} dimensions: {matrix.rows_count}x{matrix.cols_count}")
        print(f"Matrix {i} values: {matrix.values}")

    if operation == 'add':
        result = matrices[0].addition(matrices[1])
    elif operation == 'subtract':
        result = matrices[0].subtraction(matrices[1])
    elif operation == 'multiply':
        result = matrices[0].multiplication(matrices[1])
    else:
        print("Invalid operation")
        return

    output_file = rf'C:\Users\HP\Desktop\Matrix\Sparse-Matrix\sample_results\sample_results_{operation}.txt'
    result.write_to_file(output_file)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    execute_operations()
