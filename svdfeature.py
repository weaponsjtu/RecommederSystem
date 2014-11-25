import sys

def file2list( data_file ):
    result = []
    data = open( data_file, 'r' )
    for line in data:
        line = line.replace('\n', '')
        result.append( line )
    data.close()
    return result

def main( argv ):
    if len( argv ) < 4:
        print "Usage: %s data_file user_file item_file" %( argv[0] )
        exit(1)

    user_list = file2list( argv[2] )
    item_list = file2list( argv[3] )

    data = open( data_file, 'r' )
    for line in data:
        temps = line.replace( '\n', '' ).split( '\t' )
        year = temps[0]
        user_num = temps[1]
        city = temps[2]
        industry = temps[5]
        group = temps[9]
        item_code = temps[10]
        segment = temps[14]
        price = temps[15]
        if item_code == "UN":
            item_code = group + "-UN"
        user_code = city + "-" + user_num



