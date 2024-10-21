#!usr/bin/env python3


import sys 

current_word = None
current_count = 0

for line in sys.stdin:

    word, count = line.split("\t", 1)

    count = int(count)

    if word ==  current_word:

        current_count += count 
    else:

        print("{}\t{}".format(current_word, current_count))

        current_word = word
        current_count = count

    if word ==  current_word:
        
        print("{}\t{}".format(current_word, current_count))








