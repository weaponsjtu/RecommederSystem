import math
import time

class UserBased():
    def __init__(self, matrix, user_list, item_list, sim_mat = None, related_users = None, user_item_mat = None):
        # train matirx
        self.matrix = matrix
		self.user_list = user_list
		self.item_list = item_list

    # find the TOP-3 highest similarity users for each item , and overall
    def refer_user(self, ten_offering):
        # TOP-3 highest similarity users
        print "Overall\t"
        for i in range( len(self.user_list) ):
            uid = self.user_list[i]
            u_sim = self.sim_mat[i]
            u_sim_dic = {}
            for u in range( len(u_sim) ):
                u_sim_dic[u] = u_sim[u]
            u_sim = sorted(u_sim_dic.items(), key = lambda d: -d[1])[:3]
            u_refer = []
            for u in u_sim:
                u_refer.append( str(self.user_list[u[0]]) )
            print "%s\t%s"%(str(uid), ','.join(u_refer))

        # TOP-3 highest similarity users for each item
        for item_index in ten_offering:
            print str(item_index) + '\t'
            for i in range( len(user_list) ):
                uid = self.user_list[i]
                u_sim = self.sim_mat[i]
                u_sim_dic = {}
                for u in range( len(u_sim) ):
                    if self.matrix[u][ item_index - 1 ] > 0:
                        u_sim_dic[u] = u_sim[u]
                u_sim = sorted(u_sim_dic.items(), key = lambda d: -d[1])[:3]
                u_refer = []
                for u in u_sim:
                    u_refer.append( str(self.user_list[u[0]]) )
                print "%s\t%s"%(str(uid), ','.join(u_refer))

    def user_similarity(self):
        print "function user_similarity"
        start = time.time()
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        mat = []
        for i in range(rows):
            u_sim = [0] * rows
            if sum( self.matrix[i] ) < 0.1:
                mat.append(u_sim)
                continue
            for j in range(i + 1, rows):
                user_a = self.matrix[i]
                user_b = self.matrix[j]
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
        self.sim_mat = mat

    def related_users(self, K):
        print "function related_users"
        start = time.time()
        related = {}
        rows = len(user_sim)
        for i in range( rows ):
            u_sim = {}
            for x in range(len(self.sim_mat[i])):
                u_sim[x] = self.sim_mat[i][x]
            u_sim = sorted(u_sim.items(), key = lambda d: -d[1])[:K]
            related[i] = u_sim
        end = time.time()
        print str( end - start ) + ' seconds'
        self.related_users = related


    def predict_user_based():
        print "function predict_user_based"
        start = time.time()
        rows = len(self.matrix)
        cols = len(self.matrix[0])

        # user item matrix, probability
        user_item_mat = []
        for i in range(rows):
            u_item = [0] * cols
            for j in range(cols):
                # based on user-similarity
                u_sim = self.related_users[i]
                sum_u_sim = 0
                for sim in u_sim:
                    u_item[j] = u_item[j] + sim[1] * self.matrix[ sim[0] ][j]
                    sum_u_sim = sum_u_sim + sim[1]
                if sum_u_sim > 0:
                    u_item[j] = u_item[j] * 1.0 / sum_u_sim
            user_item_mat.append(u_item)
        #for each item, we get a user ranking list
        end = time.time()
        print str( end - start ) + ' seconds'
        self.user_item_mat = user_item_mat


    def ranking_users( user_item_mat, item_index ):
        print "hello"
        # TODO


class ItemBased():
    def __init__(self, matrix, user_list, item_list, item_sim = None, related_items = None, user_item_mat = None):
        self.matrix = matrix
        self.user_list = user_list
        self.item_list = item_list

    def item_similarity(self):
        print "function item_similarity"
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        mat = []
        for i in range(cols):
            i_sim = [0] * cols
            for j in range(i + 1, cols):
                user_a = []
                user_b = []
                sim = 0
                for k in range(rows):
                    user_a.append(self.matrix[k][i])
                    user_b.append(self.matrix[k][j])
                    sim = sim + self.matrix[k][i] * self.matrix[k][j]
                if sim > 0:
                    sim = sim * 1.0 / ( math.sqrt( sum(user_a) )  * math.sqrt( sum(user_b) ) )
                i_sim[j] = sim
            for j in range(0, i):
                i_sim[j] = mat[j][i]
            mat.append(i_sim)
        self.sim_mat = mat


    def related_items(self, K):
        related = {}
        rows = len( self.item_sim )
        for i in range( rows ):
            i_sim = {}
            for x in range(len(self.item_sim[j])):
                i_sim[x] = self.item_sim[j][x]
            i_sim = sorted(i_sim.items(), key = lambda d: -d[1])[:K]
            related[i] = i_sim
        self.related_items = related

    def predict_item_based(self):
        print "function predict_item_based"
        rows = len(self.matrix)
        cols = len(self.matrix[0])

        # user item matrix, probability
        user_item_mat = []
        for i in range(rows):
            i_item = [0] * cols
            for j in range(cols):
                i_sim = self.related_items[i]
                sum_i_sim = 0
                for sim in i_sim:
                    i_item[j] = i_item[j] + sim[1] * self.matrix[i][ sim[0] ]
                    sum_i_sim += sim[1]
                if sum_i_sim > 0:
                    i_item[j] = i_item[j] * 1.0 / sum_i_sim
            user_item_mat.append(i_item)
        #for each item, we get a user ranking list
        self.user_item_mat = user_item_mat
