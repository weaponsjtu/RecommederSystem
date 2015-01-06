import math
import sys
import time

class UserBased():
    def __init__(self, matrix, user_list, item_list):
        self.matrix = matrix
		self.user_list = user_list
		self.item_list = item_list

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


class ItemBased():
    def __init__(self, matrix, user_list, item_list):
        self.matrix = matrix
        self.user_list = user_list
        self.item_list = item_list

    def item_similarity():
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


    def predict_item_based( related_items ):
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
