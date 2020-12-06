import sys
import curses
from curses import wrapper
from time import sleep


class Gress:
    def __init__(self, target_word, file_name):
        self.grep_arr = []
        self.files = []
        self.rows, self.cols = 0, 0
        self.mode = 'grep'
        self.grep_index = 0
        self.file_index = 0
        f = open(file_name)
        for i, line in enumerate(f.readlines()):
            self.files.append(line.rstrip())
            if target_word in line:
                record = dict()
                record['key'] = str(i)
                record['line'] = line.rstrip()
                self.grep_arr.append(record)
        self.LIMIT_LENGTH, self.FILE_LIMIT_LENGTH = 0, 0

    def run(self):
        wrapper(self.main)

    def main(self, stdscr):
        self.rows, self.cols = stdscr.getmaxyx()
        if self.rows < len(self.grep_arr):
            self.LIMIT_LENGTH = self.rows
        else:
            self.LIMIT_LENGTH = len(self.grep_arr) - 1
        if self.rows < len(self.files):
            self.FILE_LIMIT_LENGTH = self.rows
        else:
            self.FILE_LIMIT_LENGTH = len(self.grep_arr) - 1
        stdscr.clear()  # 画面のクリア
        self.cursor_move(stdscr)

    def cursor_move(self, stdscr):
        stdscr.clear()  # 画面のクリア

        while True:
            key = stdscr.getkey()
            stdscr.addch(key)  # 結果的に、1行1番目。↑の次の座標に追加される
            if key == 'l':
                self.handle_l(stdscr)
            elif key == 'h':
                self.handle_h(stdscr)
            elif key == 'k':
                self.handle_k(stdscr)
            elif key == 'j':
                self.handle_j(stdscr)
            elif key == 'q':
                break
            else:
                j = 0
                for i in range(self.grep_index, self.grep_index + self.LIMIT_LENGTH):
                    stdscr.addstr(j, 0, self.grep_arr[i]['key'] + ' ' + self.grep_arr[i]['line'])
                    stdscr.refresh()
                    j += 1
                continue

    def handle_l(self, stdscr):
        self.mode = 'file'
        self.file_index = int(self.grep_arr[self.grep_index]['key'])
        if self.file_index + self.FILE_LIMIT_LENGTH > len(self.files):
            self.file_index -= 1
        self.display_lines(stdscr, self.file_index)

    def handle_h(self, stdscr):
        self.mode = 'grep'
        if self.grep_index + self.LIMIT_LENGTH > len(self.grep_arr):
            self.grep_index -= 1
        self.display_lines(stdscr, self.grep_index)

    def handle_k(self, stdscr):
        if self.mode == 'grep':
            self.grep_index -= 1
            if self.grep_index < 0:
                self.grep_index += 1
            self.display_lines(stdscr, self.grep_index)
        else:
            self.file_index -= 1
            if self.file_index < 0:
                self.file_index += 1
            self.display_lines(stdscr, self.file_index)

    def handle_j(self, stdscr):
        if self.mode == 'grep':
            self.grep_index += 1
            if self.grep_index + self.LIMIT_LENGTH > len(self.grep_arr):
                self.grep_index -= 1
            self.display_lines(stdscr, self.grep_index)
        else:
            self.file_index += 1
            if self.file_index+self.LIMIT_LENGTH > len(self.files):
                self.file_index -= 1
            self.display_lines(stdscr, self.file_index)

    def display_lines(self, stdscr, index):
        stdscr.clear()
        display_line = 0
        if self.mode == 'grep':
            for i in range(index, index+self.LIMIT_LENGTH):
                stdscr.addstr(display_line, 0, self.grep_arr[i]['key'] + ' ' + self.grep_arr[i]['line'])
                stdscr.refresh()
                display_line += 1
        else:
            for i in range(index, index+self.FILE_LIMIT_LENGTH):
                stdscr.addstr(display_line, 0, str(i) + ' ' + self.files[i])
                stdscr.refresh()
                display_line += 1
