import sys
import math
import time

class PreProcessing():
    def __init__(self, data_file):
        self.data_file = data_file

    def preprocess():
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
