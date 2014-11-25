import math
import sys
import time

# find the TOP-3 highest similarity users for each item , and overall
def refer_user(matrix, sim_mat, user_list, ten_offering):
    # TOP-3 highest similarity users
    print "Overall\t"
    for i in range( len(user_list) ):
        uid = user_list[i]
        u_sim = sim_mat[i]
        u_sim_dic = {}
        for u in range( len(u_sim) ):
            u_sim_dic[u] = u_sim[u]
        u_sim = sorted(u_sim_dic.items(), key = lambda d: -d[1])[:3]
        u_refer = []
        for u in u_sim:
            u_refer.append( str(user_list[u[0]]) )
        print "%s\t%s"%(str(uid), ','.join(u_refer))

    # TOP-3 highest similarity users for each item
    for item_index in ten_offering:
        print str(item_index) + '\t'
        for i in range( len(user_list) ):
            uid = user_list[i]
            u_sim = sim_mat[i]
            u_sim_dic = {}
            for u in range( len(u_sim) ):
                if matrix[u][ item_index - 1 ] > 0:
                    u_sim_dic[u] = u_sim[u]
            u_sim = sorted(u_sim_dic.items(), key = lambda d: -d[1])[:3]
            u_refer = []
            for u in u_sim:
                u_refer.append( str(user_list[u[0]]) )
            print "%s\t%s"%(str(uid), ','.join(u_refer))


# compute the user_item matrix
# integrate the bought times
# split dataset into train/test
# train: before 2014
# test: 2014
def purchase_matrix(data_dic, user_list, item_list):
    print "function purchase_matrix"
    rows = len(user_list)
    cols = len(item_list)
    train = []
    test = []
    for i in range(rows):
        u_train = [0] * cols
        u_test = [0] * cols
        uid = user_list[i]
        if data_dic.has_key(uid):
            for t in data_dic[uid]:
                if t[1].find("2014") == -1:
                    u_train[ t[0] ] = 1
                else:
                    #u_train[ t[0] ] = 1
                    u_test[ t[0] ] = 1
        train.append( u_train )
        test.append( u_test )
    return [train, test]


def user_similarity(matrix, item_index):
    print "function user_similarity"
    start = time.time()
    rows = len(matrix)
    cols = len(matrix[0])
    mat = []
    for i in range(rows):
        u_sim = [0] * rows
        if sum( matrix[i] ) < 0.1:
            mat.append(u_sim)
            continue
        for j in range(i + 1, rows):
            user_a = matrix[i]
            user_b = matrix[j]
            if sum( user_a ) < 0.1 and sum( user_b ) < 0.1:
                continue
            sim = 0
            for k in range(cols):
				#if item_index != (k + 1):
				#	sim = sim + user_a[k] * user_b[k]
				sim = sim + user_a[k] * user_b[k]
            if sim > 0:
				sim = sim * 1.0 / ( math.sqrt( sum(user_a) )  * math.sqrt( sum(user_b) ) )
            u_sim[j] = sim
        for j in range(0, i):
            u_sim[j] = mat[j][i]
        mat.append(u_sim)
    end = time.time()
    print str( end - start ) + ' seconds'
    return mat

def related_users(user_sim, K):
    print "function related_users"
    start = time.time()
    related = {}
    rows = len(user_sim)
    for i in range( rows ):
        u_sim = {}
        for x in range(len(user_sim[i])):
            u_sim[x] = user_sim[i][x]
        u_sim = sorted(u_sim.items(), key = lambda d: -d[1])[:K]
        related[i] = u_sim
    end = time.time()
    print str( end - start ) + ' seconds'
    return related



def predict_user_based(matrix, related_users):
    print "function predict_user_based"
    start = time.time()
    rows = len(matrix)
    cols = len(matrix[0])

    # user item matrix, probability
    user_item_mat = []
    for i in range(rows):
        u_item = [0] * cols
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

            # based on user-similarity
            u_sim = related_users[i]
            sum_u_sim = 0
            for sim in u_sim:
                u_item[j] = u_item[j] + sim[1] * matrix[ sim[0] ][j]
                sum_u_sim = sum_u_sim + sim[1]
            if sum_u_sim > 0:
                u_item[j] = u_item[j] * 1.0 / sum_u_sim
        user_item_mat.append(u_item)
    #for each item, we get a user ranking list
    end = time.time()
    print str( end - start ) + ' seconds'
    return user_item_mat


def ranking_users( user_item_mat, item_index ):
    print "hello"
    # TODO



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
