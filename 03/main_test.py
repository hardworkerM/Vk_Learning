import unittest
from main import CustomList


class MainTest(unittest.TestCase):

    def test_add(self):
        cl_l1 = CustomList([1, 1])
        cl_l2 = CustomList([2, 2, 2])
        l_l1 = [3, 3]
        self.assertEqual(list(cl_l1 + cl_l2), [3, 3, 2])
        self.assertEqual(list(cl_l1 + l_l1), [4, 4])
        self.assertEqual(list(l_l1 + cl_l1), [4, 4])
        self.assertEqual(list(l_l1 + cl_l2), [5, 5, 2])

    def test_sub(self):
        cl_l1 = CustomList([1, 1])
        cl_l2 = CustomList([2, 2, 2])
        l_l1 = [3, 3]
        self.assertEqual(list(cl_l1 - cl_l2), [-1, -1, -2])
        self.assertEqual(list(cl_l1 - l_l1), [-2, -2])
        self.assertEqual(list(l_l1 - cl_l1), [2, 2])
        self.assertEqual(list(l_l1 - cl_l2), [1, 1, -2])

    def test_str(self):
        cl_l = CustomList([1, 1, 1, 1])
        self.assertEqual(str(cl_l), '1, 1, 1, 1: 4')

    def test_eq(self):
        cl_l1 = CustomList([1, 2, 1])
        cl_l2 = CustomList([2, 2])
        self.assertTrue(cl_l1 == cl_l2)
        cl_l2 = CustomList([1, 1, 1])
        self.assertTrue(cl_l1 != cl_l2)

    def test_less(self):
        cl_l1 = CustomList([1, 2, 1])
        cl_l2 = CustomList([5])
        self.assertTrue(cl_l1 < cl_l2)
        cl_l2 = CustomList([1, 3])
        self.assertTrue(cl_l1 <= cl_l2)

    def test_greater(self):
        cl_l1 = CustomList([1, 2, 1])
        cl_l2 = CustomList([3])
        self.assertTrue(cl_l1 > cl_l2)
        cl_l2 = CustomList([4])
        self.assertTrue(cl_l1 >= cl_l2)


if __name__ == '__main__':
    unittest.main()
