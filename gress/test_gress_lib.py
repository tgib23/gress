import unittest
from unittest import mock
import gress_lib

class Test_gress_lib(unittest.TestCase):

    def test_gress_lib_obj(self):
        obj = gress_lib.Gress('test', 'test/testf')
        self.assertEqual(obj.mode, 'grep')
        self.assertEqual(len(obj.files), 1000)
        self.assertEqual(len(obj.grep_arr), 107)

    def test_handle_l(self):
        with mock.patch('gress_lib.Gress.display_lines'):
            obj = gress_lib.Gress('test', 'test/testf')
            obj.handle_l('test')
            self.assertEqual(obj.mode, 'file')


if __name__ == "__main__":
    unittest.main()
