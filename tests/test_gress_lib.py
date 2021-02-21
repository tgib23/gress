import unittest
from unittest import mock
from unittest.mock import MagicMock
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
            obj_grep_k = Gress('test', 'tests/testf')
            obj_grep_k.decrement_command('k')
            self.assertEqual(obj_grep_k.grep_highlight_index, 0)
            self.assertEqual(obj_grep_k.grep_index, 0)
            obj_grep_k.grep_highlight_index = 10
            obj_grep_k.decrement_command('k')
            self.assertEqual(obj_grep_k.grep_highlight_index, 9)
            self.assertEqual(obj_grep_k.grep_index, 0)

            obj_file_k = Gress('test', 'tests/testf')
            obj_file_k.mode = 'file'
            obj_file_k.file_index = 200
            obj_file_k.decrement_command('k')
            self.assertEqual(obj_file_k.file_index, 199)

    def test_increment_command(self):
        with mock.patch('modules.gress_lib.Gress.display_lines'):
            obj_grep_j = Gress('test', 'tests/testf')
            obj_grep_j.increment_command('j')
            self.assertEqual(obj_grep_j.grep_highlight_index, 1)
            self.assertEqual(obj_grep_j.grep_index, 1)

            obj_file_j = Gress('test', 'tests/testf')
            obj_file_j.mode = 'file'
            obj_file_j.file_index = 20
            obj_file_j.increment_command('j')
            self.assertEqual(obj_file_j.file_index, 21)

    def test_increment_d_command(self):
        # size of grep-arr is several times larger than rows
        obj_grep_ = Gress('test', 'tests/testf')
        obj_grep_.rows = 30
        obj_grep_.GREP_DISPLAY_RANGE = 29
        obj_grep_.grep_highlight_index = 0
        obj_grep_.display_lines = MagicMock(return_value='ok')

        obj_grep_.increment_command('d')
        obj_grep_.display_lines.assert_called_once()
        self.assertEqual(obj_grep_.grep_highlight_index, 15)
        self.assertEqual(obj_grep_.grep_index, 15)

        # size of grep_arr is not very different against rows
        obj_grep_2 = Gress('test', 'tests/testf')
        obj_grep_2.rows = 100
        obj_grep_2.GREP_DISPLAY_RANGE = 99
        obj_grep_2.grep_highlight_index = 0
        obj_grep_2.display_lines = MagicMock(return_value='ok')

        obj_grep_2.increment_command('d')
        obj_grep_2.display_lines.assert_called_once()
        self.assertEqual(obj_grep_2.grep_highlight_index, 8)
        self.assertEqual(obj_grep_2.grep_index, 8)


if __name__ == "__main__":
    unittest.main()
