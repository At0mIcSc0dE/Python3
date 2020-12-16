import sqlite3 as sql
import multiprocessing
import concurrent.futures
import random
from MyDecorators import *
import itertools
from tkinter import *
import time
import threading
from functools import lru_cache


# def insert(string: str):
#     lstbox.insert(0, string)
#
#
# def returnAfter():
#     lstbox.insert(0, 'message')
#
#
# def threadings():
#     for _ in range(100):
#         t = threading.Thread(target=returnAfter).start()
#         threads.append(t)
#
#
# root = Tk()
# root.geometry('1200x600')
# root.resizable(False, False)
#
# lstbox = Listbox(root, height=25, width=35)
# lstbox.pack()
#
# _start = time.perf_counter()
#
# threads = []
# # btn = Button(root, text='click', command=threadings)
# threadings()
# # btn.pack()
#
# print(time.perf_counter()-_start)
# root.mainloop()







# def insertintoDtb(names):
#         cursor.execute('INSERT INTO OneTimeExpenseTable (Expense, Price, MoreInfo, Day, Month, Year) VALUES (?, ?, ?, ?, ?, ?)', (names, 1, 'info', 1, 1, 2019))
#         conn.commit()
#
# names = ['naem' for _ in range(100000)]
# conn = sql.connect('C:/tmp/ExpenseTracker/Expenses.db')
# cursor = conn.cursor()
# for _ in range(100000):
#     insertintoDtb(names[_])


@lru_cache(maxsize=100000)
def getNthFib(n):
    if n == 0:
        return 0
    elif n <= 2:
        return 1
    elif n > 2:
        return getNthFib(n-1) + getNthFib(n-2)



for n in range(1, 10001):
    print(str(getNthFib(n)) + '\n')













