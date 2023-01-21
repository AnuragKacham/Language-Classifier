"""
@author: Anurag Kacham
AK4579
Lab_3
"""

import math
import random

class CompareWords: 
    def callAll(self,line):
        row = []
        row.append(self.if_ij_exists(line))
        row.append(self.if_de_het_exists(line))
        row.append(self.if_dutch_words_exists(line))
        row.append(self.if_length(line))
        row.append(self.if_bigram_exists(line))
        row.append(self.if_en_exists(line))
        row.append(self.if_str_exists(line))
        row.append(self.if_dutch_number_exists(line))
        row.append(self.if_english_number_exists(line))
        row.append(self.if_jij_u_exists(line))
        row.append(self.if_dutch_unique_alphabets(line))
        return row
    
    def if_bigram_exists(self,line):
        common_bigrams = ['th', 'he', 'in', 'en', 'nt', 're', 'er', 'an', 'ti', 'es', 'on', 'at',\
             'se', 'nd', 'or', 'ar', 'al', 'te', 'co', 'de', 'to', 'ra', 'et', 'ed', 'it', 'sa', 'em', 'ro']
        for iter in line.split():
            for bigram in common_bigrams:
                if bigram in iter:
                    return True
                else:
                    return False

    def if_de_het_exists(self,line):
        kw = ['de', 'het']
        for iter in line.split():
            if iter not in kw:
                return True
        return False

    def if_jij_u_exists(self,line):
        for iter in line.split():
            if iter == "jij" or iter == "u":
                return True
            return False

    def if_dutch_number_exists(self,line):
        numb = ['een', 'twee', 'drie', 'vier', 'vijf', 'zes', 'zeven', 'acht', 'negen', 'tien']
        for iter in line.split():
            if iter in numb:
                return True
        return False
    
    def if_ij_exists(self,line):
        total = 0
        for iter in line.split():
            if 'ij' in iter:
                total += 1
                if total >= 2:
                    return True
        return False
    
    def if_str_exists(self,line):
        en_common_substrings = ['ity','men','ess','mic','the','unt','and','sth','oss','re','ing','tio',\
            'ion','ive','tis','lly','for','nde','ist','has','nce','edt','ual','oft','tha','tage','tive']
        for iter in line.split():
            for i in en_common_substrings:
                if i in iter:
                    return True
        return False

    def if_dutch_words_exists(self,line):
        bool = False
        nl_common = []
        lines = line.split()
        f = open('dutch_words.txt')
        while True:
            line = f.readline().strip().replace('\n', '')
            if not line:
                break
            nl_common.append(line)
        f.flush()
        f.close()
        for iter in lines:
            if iter in nl_common:
                bool = True
        return bool

    def if_dutch_unique_alphabets(self,line):
        alphabets = ['á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ë', 'ï', 'ö', 'ü']
        for iter in line.split():
            if iter in alphabets:
                return True
        return False

    def if_length(self,line):
        total = 0
        k = len(line)
        average_length = 0.0
        for iter in line.split():
            total += len(iter)
        if k > 0:
            average_length = total / k
            if average_length >= 4.5:
                return True
        return False

    def if_english_number_exists(self,line):
        numb = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        for word in line.split():
            if word in numb:
                return True
        return False

    def if_en_exists(self,line):
        for word in line.split():
            if word == "en" or word == "een":
                return True
        return False


class ModelTree:
    
    __slots__ = ['column_number', 'map_number', 'subtrue', 'subfalse']

    def __init__(self, fullques, level, subtrue, subfalse):
        self.column_number = fullques
        self.subtrue = subtrue
        self.subfalse = subfalse
        self.map_number = nl_or_en_count(level)


class OptimalChoice:
    __slots__ = ['index', 'count']

    def __init__(self, index, count):
        self.index = index
        self.count = count

    def checkEqual(self, lines):
        val = lines[self.index]
        return val == self.count


def start_tree(rows):
    total_true = []
    total_false = []
    choice, gain_total = calculate_information_gain(rows)
    if gain_total == 0:
        return ModelTree(None, rows, None, None)
    if choice is not None:
        for iter in rows:
            if choice.checkEqual(iter):
                total_true.append(iter)
            else:
                total_false.append(iter)
    if len(total_true) == 0 or len(total_false) == 0:
        return ModelTree(None, rows, None, None)
    false_branch = start_tree(total_true)
    true_branch = start_tree(total_false)
    return ModelTree(choice, rows, true_branch, false_branch)

def build_tree(lat):
    return start_tree(lat)

def calculate_information_gain(rows):
    if len(rows) == 0:
        return None, 0
    gain_total = 0
    value_total = None
    total_entropy = find_entropy_iter(rows)
    for indices in range(10):
        column_truth = []
        for iter in rows:
            if(iter[indices] not in column_truth or len(column_truth) == 0):
                column_truth.append(iter[indices])
            else:
                if len(column_truth) == 2:
                    break
                if(iter[indices] == True and column_truth[0] == False):
                    column_truth.append(True)
                    break
                elif(iter[indices] == False and column_truth[0] == True):
                    column_truth.append(False)
                    break

        for iter in column_truth:
            correct = []
            wrong = []
            correct_choice = OptimalChoice(indices, iter)
            for i in range(len(rows)):
                if correct_choice.checkEqual(rows[i]):
                    correct.append(rows[i])
                else:
                    wrong.append(rows[i])
            if len(correct) == 0 or len(wrong) == 0:
                continue
            gain_now = total_entropy - (len(correct) / len(rows)) * find_entropy_iter(correct) - (len(wrong) / len(rows)) * find_entropy_iter(wrong)
            if gain_now > gain_total:
                gain_total = gain_now
                value_total = correct_choice
    return value_total, gain_total
    

def find_entropy_iter(rows):
    count = nl_or_en_count(rows)
    total_entropy = 0.0
    for iter in count:
        if len(count) == 1:
            return 0
        prob = count[iter] / len(rows)
        total_entropy += -prob * math.log(prob, 2)
    return total_entropy



def nl_or_en_count(rows):
    total = {}
    for iter in rows:
        if iter[-1] not in total:
            total[iter[-1]] = 1
        else:
            total[iter[-1]] += 1
    return total

class Adaboost:

    __slots__ = ['column_number']

    def __init__(self, column_number):
        self.column_number = column_number

    def importance(self, rows):
        return calculate_information_gain(rows)[1]

    def checker(self, row):
        return self.column_number.checkEqual(row)


def learn(rows, values):
    total = 0
    weight = []
    latest = []
    if len(rows) == 0:
        return latest, total
    for iter in values:
        if iter != 0:
            total += iter
        weight += [total]
    if total == 0:
        return latest, total
    for iter in range(len(rows)):
        choose = random.uniform(0, 1)
        for loop_inc in range(len(weight)):
            if choose < weight[loop_inc]:
                latest.append(rows[loop_inc])
                break
    choice = calculate_information_gain(latest)
    return latest, Adaboost(choice[0])

def ada_boost(rows):
    length_rows = len(rows)
    results = [rows[index][-1] != 'en' for index in range(length_rows)]
    weights = [1 / length_rows for _ in range(length_rows)]
    height = [None for _ in range(len(rows[0]) - 1)]
    indices = [0 for _ in range(len(rows[0]) - 1)]
    if length_rows == 0:
        return height
    for iter in range(len(rows[0]) - 1):
        height[iter] = start_tree(rows)
        current = []
        current, height[iter] = learn(rows, weights)
        total_error = 0
        total_weight = []
        for loop_inc in range(length_rows):
            if current[loop_inc][iter] != results[loop_inc]:
                total_error += weights[loop_inc]
        for loop_inc in range(length_rows):
            if not current[loop_inc][iter] != results[loop_inc]:
                weights[loop_inc] = weights[loop_inc] * (total_error / (1 - total_error))
        for i in range(len(weights)):
            total_weight.append(weights[i] / sum(weights))
        weights = total_weight
        if total_error == 1:
            indices[iter] = 0
        elif total_error == 0:
            indices[iter] = float('inf')
        else:
            indices[iter] = math.log((1 - total_error) / total_error)
    return [(height[index], indices[index]) for index in range(len(rows[0]) - 1)]
