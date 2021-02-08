import unittest
from unittest import mock
from modules.gress_lib import Gress


class Test_gress_lib(unittest.TestCase):

    def test_gress_lib_obj(self):
        obj = Gress('test', 'tests/testf')
        self.assertEqual(obj.mode, 'grep')
        self.assertEqual(len(obj.files), 1000)
        self.assertEqual(len(obj.grep_arr), 107)

    def test_handle_l(self):
        with mock.patch('modules.gress_lib.Gress.display_lines'):
            obj = Gress('test', 'tests/testf')
            obj.handle_l()
            self.assertEqual(obj.mode, 'file')

    def test_handle_h(self):
        with mock.patch('modules.gress_lib.Gress.display_lines'):
            obj = Gress('test', 'tests/testf')
            obj.handle_h()
            self.assertEqual(obj.mode, 'grep')

    def test_decrement_command(self):
        with mock.patch('modules.gress_lib.Gress.display_lines'):
            obj = Gress('test', 'tests/testf')
            obj.decrement_command('k')
            self.assertEqual(obj.grep_highlight_index, 0)
            self.assertEqual(obj.grep_index, 0)
            obj.grep_highlight_index = 10
            obj.decrement_command('k')
            self.assertEqual(obj.grep_highlight_index, 9)
            self.assertEqual(obj.grep_index, 0)

if __name__ == "__main__":
    unittest.main()
