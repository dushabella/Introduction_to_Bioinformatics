from difflib import SequenceMatcher

# read file to appropriate format
with open('input.txt', 'r') as file:
    lines = file.readlines()
strings = []
temp = []
for line in lines:
    if line.startswith('>'):
        temp = ''.join(temp)
        strings.append(temp)
        temp = []
        continue
    else:
        temp.append(line[:-1])
temp = ''.join(temp)
strings.append(temp)
strings.remove('')

def lcs1(str1: str, str2: str) -> str:
    """ difflib package solution """
    """ lcs problem explenation: https://www.youtube.com/watch?v=HgUOWB0StNE"""
    seqMatch = SequenceMatcher(None, str1, str2)
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))
    res = str1[match.a: match.a + match.size]
    return(res)

def lcs2(str1, str2):
    """ longest common substring problem (LCS) """
    """ a simple, easy to understand but inefficient solution """
    """ the complexity of this algorithm is O(N^2) """
    res = ""
    len1, len2 = len(str1), len(str2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and str1[i + j] == str2[j]):
                match += str2[j]
            else:
                if (len(match) > len(res)): res = match
                match = ""
    return(res)

# here starts the exact solution

def lcs(find, data):
    if len(data) < 1 and len(find) < 1:
        return False
    for i in range(len(data)):
        if find not in data[i]:
            return False
    return True

def lcs_of_few_strings(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and lcs(data[0][i:i+j], data):
                    substr = data[0][i:i+j]
    return substr

print(lcs_of_few_strings(strings))