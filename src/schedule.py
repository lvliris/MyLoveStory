# -*- coding: utf-8 -*-
import numpy as np
import datetime
import time
import os


class Schedule(object):
    def __init__(self, target_date):
        self.target_date = target_date
        self.date_format = '%Y-%m-%d %H:%M:%S'
        self.target_timeArray = time.strptime(target_date, self.date_format)
        cur_dir = os.path.dirname(__file__)
        self.source_txt_path = os.path.join(cur_dir, 'source.txt')
        self.target_txt_path = os.path.join(cur_dir, 'target.txt')
        self.write_message_num = 0
        self.write_message_set = set()
        self.message = []
        self.message_dict = {}
        self.words = [
            1, 1, 1, 1, 1, 1, 1,
            0, 0, 0, 0, 0, 1, 0,
            0, 0, 0, 0, 1, 0, 0,
            0, 0, 0, 1, 0, 0, 0,
            0, 0, 0, 0, 1, 0, 0,
            0, 0, 0, 0, 0, 1, 0,
            1, 1, 1, 1, 1, 1, 1,
            0, 0, 0, 0, 0, 0, 0,
            1, 1, 0, 0, 0, 0, 0,
            0, 1, 1, 1, 0, 0, 0,
            0, 0, 1, 0, 1, 1, 0,
            0, 0, 1, 0, 0, 1, 1,
            0, 0, 1, 0, 1, 1, 0,
            0, 1, 1, 1, 0, 0, 0,
            1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1,
            0, 0, 1, 0, 0, 0, 1,
            0, 0, 1, 1, 0, 0, 1,
            0, 1, 0, 0, 1, 0, 1,
            1, 0, 0, 0, 0, 1, 0,
            0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1,
            0, 0, 1, 0, 0, 0, 1,
            0, 0, 1, 1, 0, 0, 1,
            0, 1, 0, 0, 1, 0, 1,
            1, 0, 0, 0, 0, 1, 0,
            0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 1,
            0, 0, 0, 0, 0, 1, 0,
            0, 0, 0, 0, 1, 0, 0,
            1, 1, 1, 1, 0, 0, 0,
            0, 0, 0, 0, 1, 0, 0,
            0, 0, 0, 0, 0, 1, 0,
            0, 0, 0, 0, 0, 0, 1,
            0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1,
            0, 0, 0, 0, 0, 1, 0,
            0, 0, 0, 0, 1, 0, 0,
            0, 0, 0, 1, 0, 0, 0,
            0, 0, 0, 0, 1, 0, 0,
            0, 0, 0, 0, 0, 1, 0,
            1, 1, 1, 1, 1, 1, 1,
            0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1,
            1, 0, 0, 1, 0, 0, 1,
            1, 0, 0, 1, 0, 0, 1,
            1, 0, 0, 1, 0, 0, 1,
            1, 0, 0, 1, 0, 0, 1,
            1, 0, 0, 1, 0, 0, 1,
        ]

        self.init_message()

    def check_active(self, date_str):
        offset = self.get_offset(date_str)
        index = offset // 7 * 7 + 6 - offset % 7
        if 0 <= index < self.total():
            if self.words[index] == 1:
                return True
            else:
                return False
        else:
            return False

    def get_next_active_date(self, date_str):
        timestamp = time.mktime(time.strptime(date_str, self.date_format))
        for i in range(1, self.total()):
            new_timestamp = self.get_start_date()[0] + 24 * 3600 * i
            if new_timestamp <= timestamp:
                continue
            new_date_str = time.strftime(self.date_format, time.localtime(new_timestamp))
            if self.check_active(new_date_str):
                return new_date_str
        return None

    def get_message(self, date_str):
        message_left = len(self.message) - self.write_message_num
        offset = self.get_offset(date_str)
        active_left = sum(self.words[offset:])
        if message_left >= active_left:
            return self.message[message_left - 1]
        else:
            return None

    def write_message(self, cur_date_str):
        for date, message in sorted(self.message_dict.items()):
            if date < cur_date_str and date not in self.write_message_set:
                with open(self.target_txt_path, 'a', encoding='UTF-8') as fout:
                    fout.write('{}: {}'.format(date, message))
                self.write_message_num += 1
                self.write_message_set.add(date)
                return os.path.realpath(self.target_txt_path), message, date
        else:
            return None

    def init_message(self):
        with open(self.source_txt_path, 'r', encoding='UTF-8') as f:
            for line in f:
                if line.startswith('#'):
                    line = line[1:].strip()
                self.message.append(line)
        assert len(self.message) > self.active_num(), 'no enough source text: {} message vs {} active'.format(len(self.message), self.active_num())

        start_timestamp, start_date = self.get_start_date()
        i = 0
        while i <= len(self.message) - self.active_num():
            first_timeArray = time.localtime(start_timestamp + 300*i)
            first_date = time.strftime(self.date_format, first_timeArray)
            self.message_dict[first_date] = self.message[-i-1]
            i += 1

        next_date = self.get_next_active_date(start_date)
        while next_date and next_date < self.target_date:
            self.message_dict[next_date] = self.message[-i-1]
            next_date = self.get_next_active_date(next_date)
            i += 1

        for data, message in sorted(self.message_dict.items()):
            print(data, message)

        if os.path.exists(self.target_txt_path):
            with open(self.target_txt_path, 'r', encoding='UTF-8') as f:
                for line in f:
                    if line == '':
                        continue
                    self.write_message_num += 1
                    self.write_message_set.add(line.rsplit(':', 1)[0])

    def active_num(self):
        return sum(self.words)

    def total(self):
        return len(self.words)

    def show_words(self):
        words_array = np.array(self.words, dtype='uint8').reshape(-1, 7).transpose()[::-1, :]
        for row in words_array:
            for col in row:
                if col == 1:
                    print('\u2764', end='')
                else:
                    print('\u2003', end='')
            print('')

    def get_start_date(self):
        target_timestamp = time.mktime(self.target_timeArray)
        start_timestamp = target_timestamp - (self.total() + (self.target_timeArray.tm_wday + 1) % 7) * 24 * 3600
        start_timeArray = time.localtime(start_timestamp)
        start_date = time.strftime(self.date_format, start_timeArray)
        return start_timestamp, start_date

    def get_cur_date(self):
        timestamp = time.time()
        timeArray = time.localtime(timestamp)
        date_str = time.strftime(self.date_format, timeArray)
        return date_str

    def get_date(self, date_str):
        dateArray = time.strptime(date_str, self.date_format)
        date = datetime.datetime(dateArray.tm_year, dateArray.tm_mon, dateArray.tm_mday, dateArray.tm_hour, dateArray.tm_min)
        return date

    def get_offset(self, date_str):
        date = self.get_date(date_str)
        start_timestamp, start_date_str = self.get_start_date()
        start_date = self.get_date(start_date_str)
        offset = (date - start_date).days
        return offset


def test(s):
    print(s.active_num(), s.total())
    start_timestamp, start_date = s.get_start_date()
    print(start_date)
    active_map = np.zeros((7, 53))
    row, col = 0, 0
    for i in range(365):
        cur_timestamp = start_timestamp + i * 24 * 3600 + np.random.randint(10) * 3600
        cur_timeArray = time.localtime(cur_timestamp)
        row = (cur_timeArray.tm_wday + 1) % 7
        if row == 0:
            col += 1
        cur_date = time.strftime('%Y-%m-%d %H:%M:%S', cur_timeArray)
        if s.check_active(cur_date):
            print('curr date', cur_date)
            next_date = s.get_next_active_date(cur_date)
            if next_date is not None:
                print('next date', next_date)
            message = s.get_message(cur_date)
            while message is not None:
                modified_file = s.write_message(cur_date, message)
                print('modified file:', modified_file)
                message = s.get_message(cur_date)
            active_map[row, col] = 1

    for row in active_map:
        for col in row:
            if col == 1:
                print('\u2764', end='')
            else:
                print('  ', end='')
        print('')


if __name__ == '__main__':
    s = Schedule(target_date='2022-08-04 05:20:00')
    s.show_words()
    print(s.get_start_date())
