import sys
import math
import time


class Evaluation():
    def __init__(self, result_data, test_data):
        self.result_data = result_data
        self.test_data = test_data

    def eval_f1():
        pass

    def eval_roc():
        pass

    def eval_ndcg():
        pass

    def percent( scores, labels, K, N ):
        p = 0
        for score in scores[:K]:
            if labels[ score[0] ] == 1:
                p += 1
        print "%d\t%d\t%d" %( p, K, N )
        return p * 1.0 / N

    # evaluate by PR curve
    def evaluate( scores, labels ):
        sum_labels = 0
        rows = len( scores )
        for item in labels.items():
            sum_labels = sum_labels + item[1]
        scores = sorted(scores.items(), key = lambda d: -d[1])
        precision = {}
        recall = {}
        PR = {}
        k = 100
        while k < rows:
            precision[k] = percent( scores, labels, k, k )
            recall[k] = percent( scores, labels, k, sum_labels )
            PR[k] = [ precision[k], recall[k] ]
            k += 100
        return [precision, recall, PR]


    # evaluate by PR curve
    def evaluateV0( test_mat, user_item_mat, item_index ):
        rows = len( user_item_mat )
        scores = {}
        labels = {}
        sum_labels = 0
        for i in range( rows ):
            scores[i] = user_item_mat[i][ item_index - 1 ]
            labels[i] = test_mat[i][ item_index - 1 ]
            sum_labels = sum_labels + labels[i]
        scores = sorted(scores.items(), key = lambda d: -d[1])
        precision = {}
        recall = {}
        PR = {}
        k = 100
        while k < rows:
            precision[k] = percent( scores, labels, k, k )
            recall[k] = percent( scores, labels, k, sum_labels )
            PR[k] = [ precision[k], recall[k] ]
            k += 100
        return [precision, recall, PR]


    # evaluate by NDCG metric
    def eval_ndcg(test_matrix, item_index, rank_dic, user_list):
        ndcg = 0
        rank_list = sorted(rank_dic.items(), key = lambda d: -d[1])

        dcg = 0
        idcg = 0
        index = 1
        for i in range(1,  len(rank_list) ):
            uid = rank_list[i][0]
            #score = rank_list[i][1]
            score = 1
            u_index = user_list.index( uid )
            if test_matrix[ u_index ][ item_index - 1 ] > 0:
                if index == 1:
                    dcg = score
                    idcg = score
                else:
                    dcg = dcg + score * 1.0 / math.log(i, 2)
                    idcg = idcg + score * 1.0 / math.log(index, 2)
                index = index + 1
        if idcg > 0:
            ndcg = dcg / idcg
        return ndcg
