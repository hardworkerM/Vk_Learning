import unittest
from main import CustomMeta, Integer, String, PositiveInteger


class MainTest(unittest.TestCase):

    def test_meta_class(self):
        class TestClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=90):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return 'Test'

        inst = TestClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(TestClass.custom_x, 50)
        self.assertEqual(inst.custom_val, 90)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), 'Test')
        inst.dynamic = 'added later'
        self.assertEqual(inst.custom_dynamic, 'added later')
        with self.assertRaises(AttributeError):
            inst.dynamic
        with self.assertRaises(AttributeError):
            inst.x
        with self.assertRaises(AttributeError):
            inst.val
        with self.assertRaises(AttributeError):
            inst.line()
        with self.assertRaises(AttributeError):
            inst.non_exist
        with self.assertRaises(AttributeError):
            TestClass.x

    def test_integer(self):
        class TestType:
            num = Integer()

            def __init__(self, num):
                self.num = num
        with self.assertRaises(TypeError):
            TestType('1')
        with self.assertRaises(TypeError):
            TestType([1, 2])
        inst = TestType(1)
        del inst.num
        with self.assertRaises(AttributeError):
            inst.num

    def test_string(self):
        class TestType:
            line = String()

            def __init__(self, val):
                self.line = val
        with self.assertRaises(TypeError):
            TestType(1)
        with self.assertRaises(TypeError):
            TestType([1, 2])
        inst = TestType('test')
        del inst.line
        with self.assertRaises(AttributeError):
            inst.line

    def test_pos_integer(self):
        class TestType:
            neg_num = PositiveInteger()

            def __init__(self, neg_num):
                self.neg_num = neg_num
        with self.assertRaises(TypeError):
            TestType('1')
        with self.assertRaises(TypeError):
            TestType([1, 2])
        with self.assertRaises(TypeError):
            TestType(1)
        inst = TestType(-1)
        del inst.neg_num
        with self.assertRaises(AttributeError):
            inst.neg_num


if __name__ == '__main__':
    unittest.main()
