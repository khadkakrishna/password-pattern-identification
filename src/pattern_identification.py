from itertools import combinations
from tinydb import TinyDB, Query
import enchant
import logging

db = TinyDB('db.json')
table = db.table('user')
query = Query()

security_ans = []
old_pswds = []
personal_info = []

"""
main function that gives the message why the password is rejected
"""
def find(username, password):
    messages = []
    password_all_possible = [x.lower() for x in util_find_all_possible_substrings(password)]

    if security_ans_exist(username, password) == True:
        messages.append("Security answer(s) exists in new password") 

    if personal_info_exist(username, password) == True:
        messages.append("New Password contains user's personal information") 

    if old_password_pattern_exist(username, password) == True:
        messages.append("New Password pattern found from old password(s)") 

    if word_find_nlp(password_all_possible) == True:
        messages.append("NLP model found some predictable/common word or pattern in new password")

    logging.info("Messages from NLP model:", messages)
    return messages

def security_ans_exist(username, password):
    print(password)
    pswd_list = util_split_password(password)
    print(pswd_list)
    security_ans = [x.lower() for x in get_security_ans(username)]
    for x in security_ans:
        for y in pswd_list:
            if (x in y) or (y in x):
                return True
    return False
        
def personal_info_exist(username, password):
    personal_info = [x.lower() for x in check_for_personal_info(username)]
    for x in personal_info :
        for y in util_split_password(password):
            if (x in y) or (y in x):
                return True
    return False


def old_password_pattern_exist(username, password):
    old_password_info = [x.lower() for x in check_for_old_pass(username)]
    for x in old_password_info:
        for y in util_split_password(password):
            if (x in y) or (y in x):
                return True
    return False

def word_find_nlp(l):
    d = enchant.DictWithPWL("en_US", "wordlist.txt")
    print(l)
    for s in l:
        if d.check(s) == True:
            return True
    return False


"""
These functions fetches the values from the database
"""
def check_for_personal_info(username):
    data = table.search(query.username == username)[0]['personal_details']
    l=[]
    l.append(data['first_name'])
    l.append(data['last_name'])
    l.append(data['phone_number'])
    l.append(data['nationality'])
    l.append(data['employeeID'])
    l.append(data['personalemail'])
    l.append(data['companyemail'])
    l.append("".join(data['DOB'].split('/')) )
    l= l + data['address'].split() + data['company'].split()
    return l

def get_security_ans(username):
    l =[]
    data = table.search(query.username == username)[0]['security_questions']
    l.append(data['answer1'])
    l.append(data['answer2'])
    return l

def check_for_old_pass(username):
    old_pswds = table.search(query.username == username)[0]['old_passwords']
    l = [j for i in old_pswds for j in util_split_password(i) ]
    print("old passwords comb", l)
    return l


"""
util_split_password(string)
returns: list of splitted alphabets and numbers
"""
def util_split_password(string):
    alpha = ""
    num = ""
    special = ""
    for i in range(len(string)):
        if (string[i].isdigit()):
            num = num+ string[i]
        elif((string[i] >= 'A' and string[i] <= 'Z') or
             (string[i] >= 'a' and string[i] <= 'z')):
            alpha += string[i]
        else:
            special += string[i]
    return [alpha, num]

"""
util_find_all_possible_substrings(string):
returns: all possible substrings for string and numbers as well of size greater than 3
"""
def util_find_all_possible_substrings(string):
    alpha = ""
    num = ""
    special = ""
    for i in range(len(string)):
        if (string[i].isdigit()):
            num = num+ string[i]
        elif((string[i] >= 'A' and string[i] <= 'Z') or
             (string[i] >= 'a' and string[i] <= 'z')):
            alpha += string[i]
        else:
            special += string[i]
    alpha_list = util_possible_substring(alpha)
    num_list = util_possible_substring(num)

    if alpha not in alpha_list:
        alpha_list.append(alpha)
    if num not in num_list:
        num_list.append(num)
    return alpha_list + num_list

"""
util_possible_substring(string):
returns: all possible substrings for given string
"""
def util_possible_substring(test_str):
    res = [test_str[x:y] for x, y in combinations(range(len(test_str) + 1), r = 2)]
    return [ i for i in res if len(i) >3]

def util_convert_special_characters(password):
    """
    ToDo: Add code to convert special characters e.g. @ to 'a'
    """
    return password


