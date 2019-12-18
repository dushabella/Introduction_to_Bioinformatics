import numpy as np
from typing import Tuple
"""**P**"""

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

def edit_distance(s: str, t: str) -> Tuple[int, np.ndarray]:
    m = len(s) + 1
    n = len(t) + 1
    dynamic_table = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            if i == 0:
                dynamic_table[i][j] = j
            elif j == 0:
                dynamic_table[i][j] = i
            elif s[i - 1] == t[j - 1]:
                dynamic_table[i][j] = dynamic_table[i - 1][j - 1]
            else:
                dynamic_table[i][j] = 1 + min(dynamic_table[i - 1][j - 1],
                                              dynamic_table[i][j - 1],
                                              dynamic_table[i - 1][j])
    return int(dynamic_table[m-1][n-1]), dynamic_table

def edit_distance2(a: str, b: str) ->int:
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

def make_best_align_strings(s: str, t: str, dynamic_table: np.ndarray, indel: str = "-") -> Tuple[str, str]:
    s_out = ""
    t_out = ""
    m = len(s)
    n = len(t)

    while m > 0 and n > 0:
        options = {
            "diag": dynamic_table[m - 1][n - 1],
            "up": dynamic_table[m - 1][n],
            "left": dynamic_table[m][n - 1]
        }
        move = min(options, key=options.get)

        if move == "diag":
            s_out += s[m - 1]
            t_out += t[n - 1]
            m -= 1
            n -= 1
        elif move == "up":
            s_out += s[m - 1]
            t_out += indel
            m -= 1
        elif move == "left":
            s_out += indel
            t_out += t[n - 1]
            n -= 1

    return s_out[::-1], t_out[::-1]

def hamming_distance(s, t):
    counter = 0
    for i in range(len(s)):
        if s[i] != t[i]:
            counter += 1
    return counter

distance, d_t = edit_distance(strings[0], strings[1])
print(distance)
new_s, new_t = make_best_align_strings(strings[0], strings[1], d_t)
print(new_s)
print(new_t)