"""Tests for Python file with C-extension"""
import unittest
from random import randint
import cutils
from main import py_mul_matrix


class MainTest(unittest.TestCase):
    """Equal and load tests"""

    def test_equal_results(self):
        """Tests if any size of matrix is processed"""
        arr1 = [
                [1, 1],
                [2, 2]
        ]
        arr2 = [
                [1, 1],
                [2, 2]
        ]
        self.assertEqual(py_mul_matrix(arr1, arr2),
                         cutils.mult_matrix(arr1, arr2))
        arr1 = [
                [1, 1],
                [2, 2],
                [3, 3]
        ]
        arr2 = [
                [1, 1],
                [2, 2]
        ]
        self.assertEqual(py_mul_matrix(arr1, arr2),
                         cutils.mult_matrix(arr1, arr2))

        arr1 = [
                [1, 1],
                [2, 2]
        ]
        arr2 = [
                [1, 1, 1],
                [2, 2, 2]
        ]
        self.assertEqual(py_mul_matrix(arr1, arr2),
                         cutils.mult_matrix(arr1, arr2))
        arr1 = [
                [1, 1, 1],
                [2, 2, 2]
        ]
        arr2 = [
                [1, 1],
                [2, 2]
        ]
        self.assertEqual(py_mul_matrix(arr1, arr2), None)
        with self.assertRaises(SystemError):
            cutils.mult_matrix(arr1, arr2)
        arr1 = [
                [1, 1],
                [2, 2]
        ]
        arr2 = [
                [1, 1],
                [2, 2],
                [3, 3]
        ]
        self.assertEqual(py_mul_matrix(arr1, arr2), None)
        with self.assertRaises(SystemError):
            cutils.mult_matrix(arr1, arr2)

    def test_load(self):
        """Tests with a big matrix"""
        row1 = 30
        col1 = 33
        row2 = col1
        col2 = 50
        arr1 = [
            [randint(99999, 999999) for i in range(col1)]
            for j in range(row1)
        ]
        arr2 = [
            [randint(99999, 999999) for i in range(col2)]
            for j in range(row2)
        ]
        self.assertEqual(py_mul_matrix(arr1, arr2),
                         cutils.mult_matrix(arr1, arr2))


if __name__ == '__main__':
    unittest.main()
