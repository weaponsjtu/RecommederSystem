import sys
import math
import time

class MatrixModel():
    def __init__(self, data_dic, matrix = None, user_list = None, item_list = None, train_conf, test_conf):
        self.data_dic = data_dic
        self.train_conf = train_conf
        self.test_conf = test_conf

	# compute the user_item matrix
    # integrate the bought times
    # split dataset into train/test
    # train_conf/test_conf: [start, end], eg: [2012.1, 2012.6]
    def split_data(self):
        print "function purchase_matrix"
        rows = len(self.user_list)
        cols = len(self.item_list)
        train = []
        test = []
        for i in range(rows):
            u_train = [0] * cols
            u_test = [0] * cols
            uid = self.user_list[i]
            if self.data_dic.has_key(uid):
                for t in self.data_dic[uid]:
                    date = t[1]
                    if date.find("2014") == -1:
                        u_train[ t[0] ] = 1
                    else:
                        #u_train[ t[0] ] = 1
                        u_test[ t[0] ] = 1
            train.append( u_train )
            test.append( u_test )
        self.train = train
        self.test = test

    def is_train_sample(self, date):
        pass

    def is_test_sample(self, date):
        pass



    def sort_by_row(row_index):
        pass

    def sort_by_col(col_index):
        pass

class User():
    def __init__(self):
        pass

class Item():
    def __init__(self):
        pass
