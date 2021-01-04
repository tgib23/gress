from curses import wrapper
import curses
import time


class Gress:
    def __init__(self, target_word, file_name):
        curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
#        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

        self.grep_arr = []
        self.files = []
        self.rows, self.cols = 0, 0
        self.mode = 'grep'
        self.grep_index = 0
        self.file_index = 0
        self.grep_highlight_index = 0
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
            self.LIMIT_LENGTH = len(self.grep_arr)
        if self.rows < len(self.files):
            self.FILE_LIMIT_LENGTH = self.rows
        else:
            self.FILE_LIMIT_LENGTH = len(self.files)
        stdscr.clear()  # 画面のクリア
        self.initial_display(stdscr)
        self.cursor_move(stdscr)

    def cursor_move(self, stdscr):

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
            elif key == 'd':
                self.handle_d(stdscr)
            elif key == 'b':
                print('rows',
                      self.rows,
                      'cols',
                      self.cols,
                      'LIMIT_LENGTH',
                      self.LIMIT_LENGTH,
                      'FILE_LIMIT_LENGTH',
                      self.FILE_LIMIT_LENGTH,
                      'len(self.grep_arr)',
                      len(self.grep_arr))
            elif key == 'q':
                break
            else:
                j = 0
                for i in range(
                        self.grep_index,
                        self.grep_index +
                        self.LIMIT_LENGTH):
                    stdscr.addstr(
                        j,
                        0,
                        self.grep_arr[i]['key'] +
                        ' ' +
                        self.grep_arr[i]['line'])
                    stdscr.refresh()
                    j += 1
                continue

    def handle_l(self, stdscr):
        self.mode = 'file'
        self.file_index = int(self.grep_arr[self.grep_index]['key'])
        if self.file_index + self.FILE_LIMIT_LENGTH > len(self.files):
            self.file_index = len(self.files) - self.FILE_LIMIT_LENGTH
        self.display_lines(stdscr, self.file_index)

    def handle_h(self, stdscr):
        self.mode = 'grep'
        if self.grep_index + self.LIMIT_LENGTH > len(self.grep_arr):
            self.grep_index -= 1
        self.display_lines(stdscr, self.grep_index)

    def handle_k(self, stdscr):
        if self.mode == 'grep':
            self.decrement_highlight_index()
            self.decrement_grep_index()
            self.display_lines(stdscr, self.grep_index)
        else:
            self.file_index -= 1
            if self.file_index < 0:
                self.file_index += 1
            self.display_lines(stdscr, self.file_index)

    def handle_j(self, stdscr):
        if self.mode == 'grep':
            self.increment_highlight_index(stdscr)
            self.increment_grep_index()
            self.display_lines(stdscr, self.grep_index)
        else:
            self.file_index += 1
            if self.file_index + self.FILE_LIMIT_LENGTH > len(self.files):
                self.file_index -= 1
            self.display_lines(stdscr, self.file_index)

    def handle_d(self, stdscr):
        if self.mode == 'grep':
            self.increment_highlight_index(stdscr)
            self.increment_grep_index()
            self.display_lines(stdscr, self.grep_index)
        else:
            self.file_index += 1
            if self.file_index + self.FILE_LIMIT_LENGTH > len(self.files):
                self.file_index -= 1
            self.display_lines(stdscr, self.file_index)


    def initial_display(self, stdscr):
        self.grep_index = 0
        self.display_lines(stdscr, self.grep_index)

    def increment_highlight_index(self, stdscr):
        if self.grep_highlight_index < len(self.grep_arr) - 1:
            self.grep_highlight_index += 1
#        else:
##            stdscr.bkgdset(curses.color_pair(2))
#            stdscr.bkgd(curses.COLOR_RED)
##            stdscr.bkgd(curses.COLOR_WHITE)
#            stdscr.refresh()
#            time.sleep(1)
##            curses.use_default_colors()
#            stdscr.bkgd(curses.COLOR_WHITE)
#            stdscr.refresh()

    def increment_grep_index(self):
       if self.rows < len(self.grep_arr):
           if self.grep_index + self.LIMIT_LENGTH/2 < self.grep_highlight_index:
               self.grep_index += 1
               if self.grep_index + self.LIMIT_LENGTH > len(self.grep_arr):
                   self.grep_index -= 1

    def decrement_highlight_index(self):
        if self.grep_highlight_index > 0:
            self.grep_highlight_index -= 1

    def decrement_grep_index(self):
        if self.grep_index + self.LIMIT_LENGTH/2 > self.grep_highlight_index:
            self.grep_index -= 1
            if self.grep_index < 0:
                self.grep_index += 1

    def display_lines(self, stdscr, index):
        stdscr.clear()
        display_line = 0
        if self.mode == 'grep':
            for i in range(index, index + self.LIMIT_LENGTH):
                if i == self.grep_highlight_index:
                    stdscr.addstr(
                        display_line,
                        0,
                        self.grep_arr[i]['key'] +
                        ' ' +
                        self.grep_arr[i]['line'],
                        curses.color_pair(3)
                    )
                else:
                    stdscr.addstr(
                        display_line,
                        0,
                        self.grep_arr[i]['key'] +
                        ' ' +
                        self.grep_arr[i]['line'])
                stdscr.refresh()
                display_line += 1
        else:
            for i in range(index, index + self.FILE_LIMIT_LENGTH):
                stdscr.addstr(display_line, 0, str(i) + ' ' + self.files[i], curses.color_pair(3))
                stdscr.refresh()
                display_line += 1
