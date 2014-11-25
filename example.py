import sys

from user_based import *
from tools import file2dic, file2dic_user, preprocess


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python " + sys.argv[0] + " data_file target_offering_file"
        exit(1)

    #ten_offering_Korea = [53, 159, 5, 92, 156, 81, 117, 135, 134, 132]


    [data_dic, user_list, item_list] = preprocess(sys.argv[1])
    [train_mat, test_mat] = purchase_matrix(data_dic, user_list, item_list)

    target_offering = []
    data = open( sys.argv[2], 'r' )
    for line in data:
        line = line.replace('\n', '')
        if item_list.count( line ) > 0:
            target_offering.append( item_list.index(line) + 1 )

    print "Users: " + str( len(user_list) )
    print "Items: " + str( len(item_list) )

    sim_mat = user_similarity(train_mat, 0)
    related_user = related_users( sim_mat, 10 )
    user_item_mat = predict_user_based(train_mat, related_user)

    all_rank = {}
    ndcg = {}
    #for i in [ item_list.index( "PAST" ) + 1 ]:
    for i in target_offering:
        print str(i) + '\t'

        [precision, recall, PR] = evaluate( test_mat, user_item_mat, i )
        for item in PR.items():
            print str( item[1][0] ) + "\t" + str( item[1][1] )

        rank_dic = {}
        for k in range(len(user_list)):
            rank_dic[ user_list[k] ] = user_item_mat[k][i - 1]

        all_rank[i] = rank_dic
        rank_list = sorted(rank_dic.items(), key = lambda d: -d[1])
        for item in rank_list:
            print item[0] + '\t' + str( item[1] )
