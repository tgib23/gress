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
        self.target_appendix = []
        self.grep_size_short = False
        self.file_size_short = False
        f = open(file_name)
        for i, line in enumerate(f.readlines()):
            self.files.append(line.rstrip())
            if target_word in line:
                record = dict()
                record['key'] = str(i+1)
                record['line'] = line.rstrip()
                self.grep_arr.append(record)
                self.target_appendix.append(i)
        self.GREP_DISPLAY_RANGE, self.FILE_DISPLAY_RANGE = 0, 0
        self.METAINFO_LINE_NUM = 1

    def run(self):
        wrapper(self.main)

    def main(self, stdscr):
        self.rows, self.cols = stdscr.getmaxyx()
        self.stdscr = stdscr
        if self.rows < len(self.grep_arr) - self.METAINFO_LINE_NUM:
            self.GREP_DISPLAY_RANGE = self.rows - self.METAINFO_LINE_NUM
        else:
            self.GREP_DISPLAY_RANGE = len(self.grep_arr)
            self.grep_size_short= True
        if self.rows < len(self.files) - self.METAINFO_LINE_NUM:
            self.FILE_DISPLAY_RANGE = self.rows - self.METAINFO_LINE_NUM
        else:
            self.FILE_DISPLAY_RANGE = len(self.files)
            self.file_size_short= True
        self.stdscr.clear()  # 画面のクリア
        self.initial_display()
        self.cursor_move()

    def cursor_move(self):

        while True:
            key = self.stdscr.getkey()
            self.stdscr.addch(key)  # 結果的に、1行1番目。↑の次の座標に追加される
            if key == 'l':
                self.handle_l()
            elif key == 'h':
                self.handle_h()
            elif key in ['k', '']:
                self.decrement_command('k')
            elif key in ['j', '']:
                self.increment_command('j')
            elif key in ['d', '']:
                self.increment_command('d')
            elif key in ['u', '']:
                self.decrement_command('u')
            elif key in ['f', '']:
                self.increment_command('f')
            elif key in ['b', '']:
                self.decrement_command('b')
            elif key == 'G':
                self.increment_command('G')
            elif key == 'g':
                self.decrement_command('g')
            elif key == 'x':
                print('rows',
                      self.rows,
                      'cols',
                      self.cols,
                      'GREP_DISPLAY_RANGE',
                      self.GREP_DISPLAY_RANGE,
                      'FILE_DISPLAY_RANGE',
                      self.FILE_DISPLAY_RANGE,
                      'len(self.grep_arr)',
                      len(self.grep_arr),
                      'grep_index',
                      self.grep_index,
                      'grep_highlight_index',
                      self.grep_highlight_index
                      )
            elif key == 'q':
                break
            else:
                j = 0
                for i in range(
                        self.grep_index,
                        self.grep_index +
                        self.GREP_DISPLAY_RANGE):
                    self.stdscr.addstr(
                        j,
                        0,
                        self.grep_arr[i]['key'] +
                        ' ' +
                        self.grep_arr[i]['line'])
                    self.stdscr.refresh()
                    j += 1
                continue

    def handle_l(self):
        self.mode = 'file'
        self.file_index = int(self.grep_arr[self.grep_index]['key'])
        if self.file_index + self.FILE_DISPLAY_RANGE > len(self.files):
            self.file_index = len(self.files) - self.FILE_DISPLAY_RANGE
        self.display_lines()

    def handle_h(self):
        self.mode = 'grep'
        if self.grep_index + self.GREP_DISPLAY_RANGE > len(self.grep_arr):
            self.grep_index = len(self.grep_arr) - self.GREP_DISPLAY_RANGE - 1
        self.display_lines()

    def increment_command(self, command):
        if self.mode == 'grep':
            self.increment_highlight_index(command)
            self.increment_grep_index(command)
            self.display_lines()
        else:
            self.increment_file_index(command)
            self.display_lines()

    def decrement_command(self, command):
        if self.mode == 'grep':
            self.decrement_highlight_index(command)
            self.decrement_grep_index(command)
            self.display_lines()
        else:
            self.decrement_file_index(command)
            self.display_lines()

    def initial_display(self):
        self.grep_index = 0
        self.display_lines()

    def increment_highlight_index(self, command):
        if command == 'j':
            if self.grep_highlight_index < len(self.grep_arr) - 1:
                self.grep_highlight_index += 1

        if command in ['d', 'f']:
            increment_line_num = 0
            if command == 'd':
                increment_line_num = self.rows // 2
            if command == 'f':
                increment_line_num = self.rows

            if self.grep_highlight_index < len(self.grep_arr) - self.rows:
                if self.grep_highlight_index + increment_line_num < len(self.grep_arr) - self.rows:
                    self.grep_highlight_index += increment_line_num
                else:
                    self.grep_highlight_index = len(self.grep_arr) - self.rows + 1

        if command == 'G':
            # works only if the size of grep_arr is longer than window size
            if len(self.grep_arr) - self.rows > 0:
                self.grep_highlight_index = len(self.grep_arr) - self.rows + 1

    def increment_grep_index(self, command):
        if command in ['j', 'd', 'f']:
            increment_line_num = 0
            if command == 'j':
                increment_line_num = 1
            if command == 'd':
                increment_line_num = self.rows // 2
            if command == 'f':
                increment_line_num = self.rows

            # in case the highlight is above the half line of the display,
            # just increment the highlight index, not the display
            if command == 'j':
                if self.grep_index + self.GREP_DISPLAY_RANGE // 2 >= self.grep_highlight_index:
                    return
            if self.grep_index < len(self.grep_arr) - self.GREP_DISPLAY_RANGE:
                self.grep_index += increment_line_num
                if self.grep_index > len(self.grep_arr) - self.GREP_DISPLAY_RANGE:
                    self.grep_index = len(self.grep_arr) - self.GREP_DISPLAY_RANGE

        if command == 'G':
            if self.grep_size_short is False:
                self.grep_index = len(self.grep_arr) - self.rows + 1

    def increment_file_index(self, command):
        if command in ['j', 'd', 'f']:
            increment_line_num = 0
            if command == 'j':
                increment_line_num = 1
            if command == 'd':
                increment_line_num = self.rows // 2
            if command == 'f':
                increment_line_num = self.rows

            if self.file_index < len(self.files) - self.rows + 1:
                if self.file_index + increment_line_num < len(self.files) - self.rows + 1:
                    self.file_index += increment_line_num
                else:
                    self.file_index = len(self.files) - self.rows + 1

        if command == 'G':
            if self.file_size_short is False:
                self.file_index = len(self.files) - self.rows + 1

    def decrement_highlight_index(self, command):
        if command in ['k', 'u', 'b']:
            decrement_line_num = 0
            if command == 'k':
                decrement_line_num = 1
            if command == 'u':
                decrement_line_num = self.rows // 2
            if command == 'b':
                decrement_line_num = self.rows
            self.grep_highlight_index -= decrement_line_num
            if self.grep_highlight_index < 0:
                self.grep_highlight_index = 0

        if command == 'g':
            self.grep_highlight_index = 0

    def decrement_grep_index(self, command):
        if command in ['k', 'u', 'b']:
            decrement_line_num = 0
            if command == 'k':
                decrement_line_num = 1
            if command == 'u':
                decrement_line_num = self.rows // 2
            if command == 'b':
                decrement_line_num = self.rows

            # in case the highlight is below the half line of the display,
            # just decrement the highlight index, not the display
            if command == 'k':
                if self.grep_index + self.GREP_DISPLAY_RANGE // 2 <= self.grep_highlight_index:
                    return

            self.grep_index -= decrement_line_num
            if self.grep_index < 0:
                self.grep_index = 0

        if command == 'g':
            self.grep_index = 0

    def decrement_file_index(self, command):
        if command in ['k', 'u', 'b']:
            decrement_line_num = 0
            if command == 'k':
                decrement_line_num = 1
            if command == 'u':
                decrement_line_num = self.rows // 2
            if command == 'b':
                decrement_line_num = self.rows

            if self.file_index > decrement_line_num:
                self.file_index -= decrement_line_num
            else:
                self.file_index = 0

        if command == 'g':
            self.file_index = 0

    def display_lines(self):
        self.stdscr.clear()
        display_line = 0
        if self.mode == 'grep':
            for i in range(self.grep_index, self.grep_index + self.GREP_DISPLAY_RANGE):
                if i == self.grep_highlight_index:
                    self.stdscr.addstr(
                        display_line,
                        0,
                        self.grep_arr[i]['key'] +
                        ' ' +
                        self.grep_arr[i]['line'],
                        curses.color_pair(3)
                    )
                else:
                    self.stdscr.addstr(
                        display_line,
                        0,
                        self.grep_arr[i]['key'] +
                        ' ' +
                        self.grep_arr[i]['line'])
                display_line += 1
            self.stdscr.addstr(
                display_line,
                0,
                '[%s mode] %d / %d' % (self.mode, self.grep_highlight_index, len(self.grep_arr))
            )
        else:
            for i in range(self.file_index, self.file_index + self.FILE_DISPLAY_RANGE):
                if i in self.target_appendix:
                    self.stdscr.addstr(display_line, 0, str(i+1) + ' ' + self.files[i], curses.color_pair(3))
                else:
                    self.stdscr.addstr(display_line, 0, str(i+1) + ' ' + self.files[i], curses.COLOR_WHITE)
                self.stdscr.refresh()
                display_line += 1
            self.stdscr.addstr(
                display_line,
                0,
                '[%s mode] %d / %d' % (self.mode, self.file_index, len(self.files))
            )
        self.stdscr.refresh()
