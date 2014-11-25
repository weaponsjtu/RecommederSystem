import math
import sys

from user_based import eval_ndcg, refer_user, purchase_matrix
from tools import file2dic, file2dic_user, preprocess


def item_similarity(matrix):
    print "function item_similarity"
    rows = len(matrix)
    cols = len(matrix[0])
    mat = []
    for i in range(cols):
        i_sim = [0] * cols
        for j in range(i + 1, cols):
            user_a = []
            user_b = []
            sim = 0
            for k in range(rows):
                user_a.append(matrix[k][i])
                user_b.append(matrix[k][j])
                sim = sim + matrix[k][i] * matrix[k][j]
            if sim > 0:
                sim = sim * 1.0 / ( math.sqrt( sum(user_a) )  * math.sqrt( sum(user_b) ) )
            i_sim[j] = sim
        for j in range(0, i):
            i_sim[j] = mat[j][i]
        mat.append(i_sim)
    return mat


def related_items( item_sim, K ):
    related = {}
    rows = len( item_sim )
    for i in range( rows ):
        i_sim = {}
        for x in range(len(item_sim[j])):
            i_sim[x] = item_sim[j][x]
        i_sim = sorted(i_sim.items(), key = lambda d: -d[1])[:K]
        related[i] = i_sim
    return related


def predict_item_based( matrix, related_items ):
    print "function predict_item_based"
    rows = len(matrix)
    cols = len(matrix[0])

    # user item matrix, probability
    user_item_mat = []
    for i in range(rows):
        i_item = [0] * cols
        for j in range(cols):
            # based on rules
            #flag = 0
            #if offering_dic is not None and rules_dic is not None and rules_dic.has_key( item_dic[j + 1] ):
            #    rules = rules_dic[ item_dic[j + 1] ]
            #    for rule in rules:
            #        if offering_dic.has_key(rule) and matrix[i][ offering_dic[rule] - 1 ] == 1 and matrix[i][j] == 0:
            #            u_item[j] = 1.0
            #            flag = 1
            #            break

            #if flag == 1:
            #    continue

            i_sim = related_items[i]
            sum_i_sim = 0
            for sim in i_sim:
                i_item[j] = i_item[j] + sim[1] * matrix[i][ sim[0] ]
                sum_i_sim += sim[1]
            if sum_i_sim > 0:
                i_item[j] = i_item[j] * 1.0 / sum_i_sim
        user_item_mat.append(i_item)
    #for each item, we get a user ranking list
    return user_item_mat
