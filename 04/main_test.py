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

        self.assertEqual(CustomMeta.__new__(CustomMeta, 'TestClass', (), {}), Test)
        inst = TestClass
        self.assertEqual()
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
