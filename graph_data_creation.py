"""
read output of hashtagOS.py; import into CSV files for Tulip graphing library
"""

hashtag_file = open("/Users/anniepreston/Desktop/hashtag_os_test_output.txt", 'r')
node_file = open("/Users/anniepreston/Desktop/hashtag_os_nodes.txt", 'w')
edge_file = open("/Users/anniepreston/Desktop/hashtag_os_edges.txt", 'w')

"""
skip header stuff
"""

for x in range(0, 8):
    hashtag_file.readline()

"""
iterate over lines:
"""

node_id_counter = 0;
string_list = []

#soon: don't hard code for each column; iterate
"""
column 1
"""

for line in hashtag_file:
    test_string = line.split()[0].partition("(")[0]
    n_matches = 0
    for string in string_list:
        if test_string == string:
            n_matches += 1
    if n_matches == 0:
        string_list.append(test_string)
        node_file.write(str(node_id_counter) + " " + test_string + "\n")
        node_id_counter += 1

"""
column 2
"""
#rewind...
hashtag_file.seek(0)

for x in range(0, 8):
    hashtag_file.readline()

for line in hashtag_file:
    test_string = line.split()[1].partition("(")[0]
    n_matches = 0
    for string in string_list:
        if test_string == string:
            n_matches += 1
    if n_matches == 0:
        string_list.append(test_string)
        node_file.write(str(node_id_counter) + " " + test_string + "\n")
        node_id_counter += 1
        
"""
column 3
"""
#rewind...
hashtag_file.seek(0)

for x in range(0, 8):
    hashtag_file.readline()

for line in hashtag_file:
    test_string = line.split()[2].partition("(")[0]
    n_matches = 0
    for string in string_list:
        if test_string == string:
            n_matches += 1
    if n_matches == 0:
        string_list.append(test_string)
        node_file.write(str(node_id_counter) + " " + test_string + "\n")
        node_id_counter += 1
node_file.close()

"""
now, create the edges file:
"""
node_file = open("/Users/anniepreston/Desktop/hashtag_os_nodes.txt", 'r')

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
    