"""
@author: Anurag Kacham
AK4579
Lab_3
"""

import re
import sys
import pickle
import model as mod


def main():
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
    r = open(arg1)
    file_read = r.readlines()
    rows = []
    for iter in file_read:
        split_line1, split_line2 = iter.split("|")
        split_line3 = split_line2.strip()
        remove_all = [re.sub(r'[^\w\s]', '', split_line3).lower(), split_line1]
        rows.append(remove_all)
    choice = mod.CompareWords()
    content = []
    for iter in rows:
        row = []
        i = 0
        row = choice.callAll(iter[0])
        row += [iter[1]]
        content.append(row)
    if(arg3 == "ada"):
        adaroot = mod.ada_boost(content)
        pickle.dump(adaroot, open(arg2, 'wb'))
        print("Ada Boost")
    elif(arg3 == "dt"):
        rootnode = mod.start_tree(content)
        pickle.dump(rootnode, open(arg2, 'wb'))
        print("Decision Tree")
    else:
        print("Please enter dt or ada")


if __name__ == '__main__':
    main()