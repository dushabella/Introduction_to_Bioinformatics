from Bio import pairwise2
from Bio.pairwise2 import format_alignment

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
print(strings)

def edit_distance(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between two strings *a* and *b*."""
    """ https://dzone.com/articles/the-levenshtein-algorithm-1 """
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    if not a:
        return len(b)
    previous_row = range(len(b) + 1)
    for i, column1 in enumerate(a):
        current_row = [i + 1]
        for j, column2 in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (column1 != column2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

levensthein_dist = edit_distance(strings[0], strings[1])
print(levensthein_dist)

alignments = pairwise2.align.globalxx(strings[0], strings[1])
print(format_alignment(*alignments[0]))
""" more about alignments: https://developer.ibm.com/articles/j-seqalign/"""
