# -*- coding: utf-8 -*-
from git import Repo
from src.schedule import Schedule
import time


class Progress(object):
    def __init__(self, target_date):
        self.target_date = target_date
        self.repo = Repo('.')

    def add(self, file_path):
        self.repo.index.add([file_path])

    def commit(self, commit_message, date):
        self.repo.index.commit(commit_message, author_date=date, commit_date=date)

    def push(self):
        self.repo.remotes.origin.push()

    def update(self, file_path, commit_message, date=None):
        self.add(file_path)
        self.commit(commit_message, date)
        self.push()


def test():
    p = Progress(target_date='2022-01-04 05:20:00')
    p.update('E:\LV\projects\RL\project\RL_Snooker\play.py', '增加玩一局游戏的脚本')


def main():
    progress = Progress(target_date='2022-08-04 05:20:00')
    schedule = Schedule(target_date='2022-08-04 05:20:00')
    try:
        while True:
            cur_date = schedule.get_cur_date()
            res = schedule.write_message(cur_date)
            if res is not None:
                modified_file, message, date = res
                progress.update(modified_file, message, date)
                print(date, message)

            time.sleep(520)
    except KeyboardInterrupt:
        print('program has finished, but love will continue')


if __name__ == '__main__':
    main()
