"""
read output of hashtagOS.py; import into CSV files for Tulip graphing library
"""
import sys, getopt

"""
define command line inputs:
"""

def main(argv):
    inputfile = ''
    nodefile = ''
    edgefile = ''
    try: 
        opts, args = getopt.getopt(argv, "hi:n:e:", ["ifile=", "nfile=", "efile="])
    except getopt.GetOptError:
        print 'graph_data_creation.py -i <inputfile> -n <nodefile> -e <edgefile>'
        sys.exit(2)
    for opt, arg in opts: 
        if opt == 'h':
            print 'graph_data_creation.py -i <inputfile> -n <nodefile> -e <edgefile>'
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-n", "--nfile"):
            nodefile = arg
        elif opt in ("-e", "--nfile"):
            edgefile = arg

    hashtag_file = open(inputfile, 'r')
    node_file = open(nodefile, 'w')
    edge_file = open(edgefile, 'w')
    node_file.write("node_id tag count\n")
    
    for x in range(0, 8):
        hashtag_file.readline()
    node_id_counter = 0;
    string_list = []

    for line in hashtag_file:
        test_string = line.split()[0].partition("(")[0]
        test_count = line.split()[0].partition("(")[2].partition(")")[0]
        n_matches = 0
        for string in string_list:
            if test_string == string:
                n_matches += 1
        if n_matches == 0:
            string_list.append(test_string)
            node_file.write(str(node_id_counter) + " " + test_string + " " + test_count + "\n")
            node_id_counter += 1
#rewind...
    hashtag_file.seek(0)

    for x in range(0, 8):
        hashtag_file.readline()

    for line in hashtag_file:
        test_string = line.split()[1].partition("(")[0]
        test_count = line.split()[1].partition("(")[2].partition(")")[0]

        n_matches = 0
        for string in string_list:
            if test_string == string:
                n_matches += 1
        if n_matches == 0:
            string_list.append(test_string)
            node_file.write(str(node_id_counter) + " " + test_string + " " + test_count + "\n")
            node_id_counter += 1

#rewind...
    hashtag_file.seek(0)

    for x in range(0, 8):
        hashtag_file.readline()

    for line in hashtag_file:
        test_string = line.split()[2].partition("(")[0]
        test_count = line.split()[2].partition("(")[2].partition(")")[0]

        n_matches = 0
        for string in string_list:
            if test_string == string:
                n_matches += 1
        if n_matches == 0:
            string_list.append(test_string)
            node_file.write(str(node_id_counter) + " " + test_string +  " " + test_count + "\n")
            node_id_counter += 1
    node_file.close()

    node_file = open(nodefile, 'r')

    target_string_list = []
#columns 1, 2:
    hashtag_file.seek(0)
    for x in range(0, 8):
        hashtag_file.readline()

    for line in hashtag_file:
        n_matches = 0
        source_string = line.split()[0].partition("(")[0]
        target_string = line.split()[1].partition("(")[0]
        #skip if already done this target string:
        for string in target_string_list:
            if target_string == string:
                n_matches += 1
        if n_matches == 0:
            target_string_list.append(target_string)
            for node_entry in node_file:
                guess_id = node_entry.split()[0]
                guess_string = node_entry.split()[1]
                if source_string == guess_string:
                    source_id = guess_id
                if target_string == guess_string:
                    target_id = guess_id
            edge_file.write(str(source_id) + " " + str(target_id) + "\n")
            node_file.seek(0)
        
#...same for columns 2, 3:
    node_file.seek(0)
    hashtag_file.seek(0)
    target_string_list = []
    for x in range(0, 8):
        hashtag_file.readline()

    for line in hashtag_file:
        n_matches = 0
        source_string = line.split()[1].partition("(")[0]
        target_string = line.split()[2].partition("(")[0]
        #skip if already done this target string:
        for string in target_string_list:
            if target_string == string:
                n_matches += 1
        if n_matches == 0:
            target_string_list.append(target_string)
            for node_entry in node_file:
                guess_id = node_entry.split()[0]
                guess_string = node_entry.split()[1]
                if source_string == guess_string:
                    source_id = guess_id
                if target_string == guess_string:
                    target_id = guess_id
            edge_file.write(str(source_id) + " " + str(target_id) + "\n")
            node_file.seek(0)


    hashtag_file.close()
    edge_file.close()
    
if __name__ == "__main__":
   main(sys.argv[1:])