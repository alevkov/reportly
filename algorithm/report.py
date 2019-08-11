from algorithm.txn import Txn
from datetime import datetime
from datetime import timedelta
from io import StringIO

import heapq
import collections
import pandas as pd

class Report(object):

    def __init__(self, csv, boy):
        super(Report, self).__init__()
        
        self.__initialize(csv, boy)


    def __initialize(self, csv, boy):
        self.__txin = []
        self.__txout = []
        self.__aqmap = {}
        self.__stock = pd.read_csv(StringIO(csv))
        self.__stock.set_index('name', inplace=True)

        date = self.__str_to_date(boy)

        for row in self.__stock.itertuples(index=True):
            name = row[0]
            price = row[1]
            amount = row[2]
            self.__aqmap[name] = collections.deque([])
            self.__aqmap[name].append(Txn(name, 0, price, amount, date))


    def __while_no_error(self, run, error):
        while True:
            try:
                run()
            except error as e:
                break


    def __run(self):
        txn = heapq.heappop(self.__txin)
        n = txn.amount

        if txn.type is 0:
            self.__aqmap[txn.name].append(txn)
        else:
            while n > 0:
                if len(self.__aqmap[txn.name]) is 0:
                    raise Exception('Underflow. Sold more than owned.')

                if n <= self.__aqmap[txn.name][-1].amount: # txn amount is less than topmost amount
                    sold = txn

                    # this represents the value of the part of acquired stocks that is now being sold
                    aqn = Txn(sold.name, 0, \
                        self.__aqmap[sold.name][-1].price, sold.amount, \
                        datetime.fromtimestamp(self.__aqmap[sold.name][-1].ts));
                    aqn.final = sold.price
                    sold.final = self.__aqmap[sold.name][-1].price

                    # number sold subtracted from acquisitions
                    self.__aqmap[sold.name][-1].amount = self.__aqmap[sold.name][-1].amount - n

                    # if the sell cancelled the acquisition, simply remove it
                    if self.__aqmap[sold.name][-1].amount == 0:
                        self.__aqmap[sold.name].pop()

                    heapq.heappush(self.__txout, aqn)
                    heapq.heappush(self.__txout, sold)

                    break;
                else: # txn amount exceeds top of FIFO
                    aqn = self.__aqmap[txn.name].pop() # The acquisition being sold

                    # Gennerating new sold for each acquisition 
                    sold = Txn(txn.name, 1, txn.price, aqn.amount, datetime.fromtimestamp(txn.ts))
                    sold.final = aqn.price

                    # set selling price to original acquisitionn
                    aqn.final = txn.price

                    heapq.heappush(self.__txout, aqn)
                    heapq.heappush(self.__txout, sold)

                    n = n - aqn.amount


    def __str_to_date(self, s):
        return datetime.strptime(s, '%b %d %Y')


    def run(self, txns):
        for t in txns:
            heapq.heappush(self.__txin, Txn(t['name'], t['type'], t['price'], \
            t['amount'], self.__str_to_date(t['ts'])))

        self.__while_no_error(self.__run, IndexError);

        return [row[0] for row in self.__stock.itertuples(index=True) if len(self.__aqmap[row[0]]) > 0]


    def reval(self, reval):
        for row in self.__stock.itertuples(index=True):
            name = row[0]
            
            if len(self.__aqmap[name]) is 0:
                continue
            for aqn in self.__aqmap[name]:
                aqn.final = reval[name]
                heapq.heappush(self.__txout, aqn)

        return [str(heapq.heappop(self.__txout)) for i in range(len(self.__txout))]
