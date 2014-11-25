import sys
import math
import time

# read file to dictionary
# flag = 0: <key, value> = <line, index>
# flag = 1: <key, value> = <index, line>
def file2dic(data_file, flag):
    data = open(data_file, 'r')
    data_dic = {}
    index = 1
    for line in data:
        line = line.replace("\n", "")
        line = line.replace('\r', '')
        if flag == 0:
            data_dic[line] = index
        if flag == 1:
            data_dic[index] = line
        index = index + 1
    return data_dic


def file2dic_user(user_file):
    user_dic = {}
    data = open(user_file, 'r')
    for line in data:
        temps = line.replace("\n", "").split(' ')
        uid = temps[0]
        name = ' '.join(temps[1:])
        user_dic[uid] = name
    return user_dic

def similarity( vectorA, vectorB ):
    if len( vectorA ) != len( vectorB ):
        return 0
    if sum( vectorA ) < 0.1 or sum( vectorB ) < 0.1:
        return 0

    #cosin
    v_sum = 0
    for i in range( len( vectorA ) ):
        v_sum = v_sum + vectorA[i] * vectorB[i]
    return v_sum * 1.0 / math.sqrt( sum(vectorA) * sum(vectorB) )

    #Pearson

    #adjusted cosin

    #jaddar index

def user_distance( profile_A, vector_A, profile_B, vector_B ):
    lamda = 0.5
    p_sim = 0
    if profile_A == profile_B:
        p_sim = 1
    v_sim = similarity( vector_A, vector_B )
    return lamda * p_sim + (1 - lamda) * v_sim

def preprocess( data_file ):
    print "function preprocess"
    start = time.time()
    data = open( data_file, 'r' )
    data_dic = {}
    user_profile_dic = {}
    item_profile_dic = {}
    user_list = []
    item_list = []
    for line in data:
        temps = line.replace("\n", "").replace('"', '').split("\t")
        date = temps[0]
        client_num = temps[1]
        location = temps[2]
        industry = temps[5]
        item_code = temps[10]
        category = temps[9]
        segment = temps[14]
        price = temps[15]
        user_code = location + "-" + client_num

        if item_code.find("UN") != -1:
            item_code = category + "-" + item_code.replace(' ', '')

        if user_list.count( user_code ) == 0:
            user_list.append( user_code )
        if item_list.count( item_code ) == 0:
            item_list.append( item_code )

        item_id = item_list.index( item_code )
        if data_dic.has_key( user_code ):
            data_dic[ user_code ].append([item_id, date ])
        else:
            data_dic[ user_code ] = [ [item_id, date ] ]
        user_id = user_list.index( user_code )
        if user_profile_dic.has_key( user_id ) == False:
            user_profile_dic[ user_id ] = industry
        if item_profile_dic.has_key( item_id ) == False:
            item_profile_dic[ item_id ] = category
    data.close()
    end = time.time()
    print str( end - start ) + ' seconds'
    return [data_dic, user_list, item_list, user_profile_dic, item_profile_dic]


# get the data dic about the transaction history
def preprocessV0( data_file, user_dic, item_dic ):
    print "function preprocess"
    data = open(data_file, 'r')
    data_dic = {}
    offering_time_dic = {}
    for line in data:
        temps = line.replace("\n", "").replace('"', '').split("\t")
        if len(temps) >= 17:
            date = temps[13]
            client_num = temps[9]
            client_name = temps[10]
            location = temps[3]
            pillar = temps[16].replace('\r', '')
            client_num = location + "-" + client_num
            stage = "08"
            if len(temps) >= 19:
                stage = temps[17]
            if stage >= "09":
                continue

            offering = -1

            if pillar == "LDMG" or pillar == "PORE" or pillar == "WRAP" or pillar == "LDEM" or pillar == "LCON":
                offering = 159

            if offering == -1 and item_dic.has_key(pillar):
                offering = item_dic[pillar]

            if offering != -1:
                if data_dic.has_key(client_num):
                    data_dic[client_num].append([offering, date])
                else:
                    data_dic[client_num] = [ [offering, date] ]
    data.close()
    return data_dic

def save_evaluation( pr_dic, item_name ):
    data = open( item_name + '.eval', 'a' )
    pr_list = sorted( pr_dic.items(), key = lambda d : d[0] )
    for item in pr_list:
        data.write( str(item[0]) + '\t' + str(item[1][0]) + '\t' + str(item[1][1]) + '\n' )
    data.close()

def save_ranking( rank_dic, item_name ):
    data = open( item_name + '.rank', 'a' )
    for item in rank_dic:
        data.write( str(item[0]) + '\t' + str(item[1]) + '\n' )
    data.close()


def mapping(user_file, mapping_file):
    map_dic = {}
    data = open(mapping_file, 'r')
    for line in data:
        temps = line.replace('\n', '').split('\t')
        uid = temps[0]
        name = temps[1]
        if map_dic.has_key(uid) is False:
            map_dic[uid] = name
        else:
            map_dic[uid] = map_dic[uid] + ";" + name

    data = open(user_file, 'r')
    for line in data:
        line = line.replace('\n', '')
        if map_dic.has_key(line):
            print line + '\t' + map_dic[line]
        else:
            print line + '\t '


def load_log_file( log_file ):
    rank_dic = {}
    data = open( log_file, 'r' )
    index = 1
    key = 0
    for line in data:
        if index > 8950:
            break
        #if index % 6021 == 1:
        if index % 895 == 1:
            key = int( line )
            rank_dic[ key ] = []
        else:
            temps = line.replace('\n', '').split('\t')
            rank_dic[ key ].append( temps[0] )
        index += 1
    data.close()
    return rank_dic


if __name__ == "__main__":
    # example, your code here
    mapping(sys.argv[1], sys.argv[2])
