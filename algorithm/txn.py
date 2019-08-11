import array
import numpy as np
from datetime import datetime

class T(object):

    @property
    def ts(self):
        return self.__ts

    @ts.setter
    def ts(self, value):
        self.__ts = value
        
    def __init__(self, ts):
        self.__ts = ts.timestamp()

class Txn(T):

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value           

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        self.__amount = value

    @property
    def final(self):
        return self.__final

    @final.setter
    def final(self, value):
        self.__final = value

    def __init__(self, name, type, price, amount, ts):
        super(Txn, self).__init__(ts)
        self.__name = name
        self.__type = type
        self.__price = price
        self.__amount = amount
        self.__final = round(-1.0, 2)

    def __eq__(self, other):
        return self.ts == other.ts

    def __lt__(self, other):
        return self.ts < other.ts

    def __gt__(self, other):
        return self.ts > other.ts

    def __str__(self):
        return "{} {} {:,} Shs {} @ ${:,}.......${:,} Value ${:,}".format(\
        datetime.utcfromtimestamp(self.ts).strftime('%Y-%m-%d %H:%M:%S'),
        ("Pur" if self.__type == 0 else "Sold"), round(self.__amount, 3), self.__name, \
        round(self.__price, 2), round((self.__price * self.__amount), 2), \
        round((self.__final * self.__amount), 2))