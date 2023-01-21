import re
import sys
import model
import pickle

def obtain_data(file_read):
    r = open(file_read)
    all_lines = r.readlines()
    choice = model.CompareWords()
    lines = []
    for iter in all_lines:
        iter = iter.strip()
        iter = iter.lower()
        iter = re.sub(r'[^a-z ]', '', iter)
        lines.append(iter)
    data_list = []
    for iter in lines:
        list_of_lines = choice.callAll(iter)
        data_list.append(list_of_lines)
    return data_list

def main():
    arg1 = sys.argv[1]
    read_file = open(arg1, 'rb')
    root = pickle.load(read_file)
    f = 0
    if isinstance(root, list):
        print("Ada Boost")
    else:
        f = 1
        print("Decision Tree")
    if f == 1:
        data_list = obtain_data(sys.argv[2])
        for iter in data_list:
            if check_if_correct(iter, root) == 'en':
                print("en")
            else:
                print("nl")
    else:
        data_list = obtain_data(sys.argv[2])
        for iter in data_list:
            if check_if_correct(iter, root) == 'en':
                print("nl")
            else:
                print("en")


def check_if_correct(sentence, root) -> list:
    if isinstance(root, list):
        dutch = 0
        english = 0
        for iter in range(len(root)):
            if root[iter][0].checker(sentence):
                dutch = dutch + root[iter][1]
            else:
                english = english + root[iter][1]
        if dutch > english:
            return 'nl'
        else:
            return 'en'
    else:
        if root.subtrue == None and root.subfalse == None and root.column_number == None:
            optimal_value = 0
            best_class = None
            for label in root.map_number:
                if root.map_number[label] > optimal_value:
                    optimal_value = root.map_number[label]
                    best_class = label
            return best_class
        if root.column_number.checkEqual(sentence):
            return check_if_correct(sentence, root.subfalse)
        else:
            return check_if_correct(sentence, root.subtrue)


if __name__ == "__main__":
    main()

