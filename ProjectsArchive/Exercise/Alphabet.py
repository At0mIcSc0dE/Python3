import string

def getLower():
    return string.ascii_lowercase


def getUpper():
    return string.ascii_uppercase


def getUpperDic():
    dic = {char : itr for itr, char in enumerate(getUpper())}
    return dic

def getLowerDic():
    dic = {char : itr for itr, char in enumerate(getLower())}
    return dic
